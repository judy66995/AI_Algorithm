"""
GPTMoE —— 基于 GPT 架构的多态性 Transformer 语言模型。

架构：
  Token Embedding + Position Embedding
      ↓
  [Block 0: Dense FFN]     ← 密集层（全局基础能力）
      ↓
  [Block 1: MoE (8 experts)]← MoE 层（多态性 —— 不同 token 不同专家）
      ↓
  ...（交替排列）
      ↓
  Final LayerNorm → LM Head → logits
"""

from typing import Tuple, List

import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import MoEConfig
from .transformer_block import TransformerBlock


class GPTMoE(nn.Module):
    """GPT 风格的多态性 MoE 语言模型"""

    def __init__(self, config: MoEConfig):
        super().__init__()
        self.config = config

        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = nn.Embedding(config.max_seq_len, config.d_model)
        self.embed_dropout = nn.Dropout(config.dropout)

        self.blocks = nn.ModuleList([
            TransformerBlock(config, use_moe=(i in config.moe_layers))
            for i in range(config.n_layers)
        ])

        self.final_ln = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # 权重绑定：嵌入矩阵与输出投影共享参数
        self.lm_head.weight = self.token_embedding.weight

        self.apply(self._init_weights)
        self._print_model_info()

    def _init_weights(self, module):
        """GPT-2 风格的正态初始化"""
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                nn.init.zeros_(module.bias)

    def _print_model_info(self):
        total = sum(p.numel() for p in self.parameters()) / 1e6
        print(f"模型参数总数: {total:.2f}M")
        print(f"  - MoE 层编号: {self.config.moe_layers}")
        print(f"  - 专家数/层: {self.config.n_experts}, Top-K: {self.config.top_k}")

    def _causal_mask(self, sz: int, device: torch.device) -> torch.Tensor:
        """生成因果自注意力掩码"""
        return torch.triu(
            torch.ones(sz, sz, device=device) * float('-inf'), diagonal=1
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: (batch, seq_len) token ID 序列

        Returns:
            logits:          (B, S, vocab_size)
            total_lb_loss:   所有 MoE 层负载平衡损失之和
        """
        B, S = x.shape
        device = x.device

        positions = torch.arange(0, S, dtype=torch.long, device=device).unsqueeze(0)
        tok_emb = self.token_embedding(x)
        pos_emb = self.position_embedding(positions)
        hidden = self.embed_dropout(tok_emb + pos_emb)

        causal_mask = self._causal_mask(S, device)
        total_lb_loss = torch.tensor(0.0, device=device)

        for block in self.blocks:
            hidden, lb_loss = block(hidden, attn_mask=causal_mask)
            total_lb_loss = total_lb_loss + lb_loss

        logits = self.lm_head(self.final_ln(hidden))
        return logits, total_lb_loss

    @torch.no_grad()
    def generate(
        self,
        tokenizer,           # SimpleTokenizer（避免循环导入）
        prompt: str,
        max_new_tokens: int = 50,
        temperature: float = 0.8,
        top_p: float = 0.9,
    ) -> Tuple[str, List[List[float]]]:
        """
        自回归文本生成 + 专家路由追踪。

        Args:
            tokenizer: SimpleTokenizer 实例
            prompt:    输入文本
            max_new_tokens: 最多生成多少个新 token
            temperature:    采样温度（>1 更随机，<1 更确定）
            top_p:          nucleus sampling 阈值

        Returns:
            generated_text:  生成文本
            routing_traces:  每个生成步骤的 MoE 路由分布
        """
        self.eval()
        device = self.lm_head.weight.device

        # 清理训练后残留的 GPU 内存碎片
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        tokens = tokenizer.encode(prompt) or [
            tokenizer.word2idx[tokenizer.BOS_TOKEN]
        ]
        input_ids = torch.tensor([tokens], device=device, dtype=torch.long)
        routing_traces: List[List[float]] = []

        for _ in range(max_new_tokens):
            if input_ids.shape[1] > self.config.max_seq_len:
                input_ids = input_ids[:, -self.config.max_seq_len:]

            S = input_ids.shape[1]
            positions = torch.arange(0, S, dtype=torch.long, device=device).unsqueeze(0)
            tok_emb = self.token_embedding(input_ids)
            pos_emb = self.position_embedding(positions)
            hidden = self.embed_dropout(tok_emb + pos_emb)
            causal_mask = self._causal_mask(S, device)

            step_trace = []
            for block in self.blocks:
                hidden, _ = block(hidden, attn_mask=causal_mask)

                if block.use_moe and block.moe is not None:
                    ln_out = block.ln2(hidden[:, -1:])        # 最后 token 的 pre-MoE 表示
                    _, _, probs = block.moe.router(ln_out)   # (1, 1, E)
                    step_trace.append(probs.squeeze(0).squeeze(0).cpu().tolist())

            if step_trace:
                routing_traces.append(step_trace)

            # ── 只取最后位置的 logits 做采样 ──
            logits = self.lm_head(self.final_ln(hidden[:, -1:, :]))
            logits = logits.squeeze(0).squeeze(0) / max(temperature, 1e-10)

            # ── 安全的 top-p (nucleus) sampling ──
            next_token = self._safe_sample(logits, top_p)
            input_ids = torch.cat([input_ids, next_token], dim=1)

            if next_token.item() == tokenizer.word2idx.get(tokenizer.EOS_TOKEN, -1):
                break

        return tokenizer.decode(input_ids.squeeze(0).tolist()), routing_traces

    def _safe_sample(self, logits: torch.Tensor, top_p: float) -> torch.Tensor:
        """安全的 top-p 采样，防止全 -inf 导致 NaN / CUDA 崩溃。

        退化策略：
          1. 正常 top-p → multinomial 采样
          2. 如果 top-p 把所有 token 过滤掉了 → 退化为 argmax
          3. multinomial 万一还是失败 → 再次退化为 argmax
        """
        # Top-p (nucleus) filtering
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cum_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # 找到 top-p 的截断位置（至少保留 1 个 token）
        keep_mask = cum_probs <= top_p
        keep_mask[0] = True  # 始终保留概率最高的 token
        # 确保第一个超过阈值的 token 也被保留
        first_exceed = (cum_probs > top_p).nonzero(as_tuple=True)[0]
        if len(first_exceed) > 0 and first_exceed[0].item() > 0:
            keep_mask[first_exceed[0]] = True

        # 把不在 top-p 内的 logits 置为 -inf
        remove = ~keep_mask
        masked_logits = logits.clone()
        masked_logits[sorted_indices[remove]] = float('-inf')

        probs = F.softmax(masked_logits, dim=-1)

        # 安全检查：如果 probs 含 NaN（全 -inf 导致 0/0），退化为 argmax
        if torch.isnan(probs).any() or probs.sum() <= 0:
            return logits.argmax(dim=-1, keepdim=True)

        try:
            return torch.multinomial(probs.unsqueeze(0), num_samples=1)
        except RuntimeError:
            # CUDA 异常时的最终兜底
            return logits.argmax(dim=-1, keepdim=True)
