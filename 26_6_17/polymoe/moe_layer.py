"""
MoE 层 —— 多态性的"执行引擎"。

MoELayer = 1 个 Router + N 个 Expert + 负载均衡损失计算。

每个 token 只经过 Top-K 个专家（稀疏激活），不同 token 激活不同专家组合
→ 这就是 AI 多态性在微观层面的具体表现。
"""

from typing import Tuple

import torch
import torch.nn as nn

from .expert import Expert
from .router import Router


class MoELayer(nn.Module):
    """
    混合专家层。

    前向传播（稀疏激活）：
      1. Router 为每个 token 选择 Top-K 专家
      2. 各专家处理所有 token，按路由权重掩码合并
      3. 计算负载平衡损失，防止专家"贫富分化"
    """

    def __init__(
        self,
        d_model: int,
        n_experts: int,
        top_k: int,
        expert_d_ff: int,
        dropout: float = 0.1,
        capacity_factor: float = 1.25,
    ):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor

        self.router = Router(d_model, n_experts, top_k)
        self.experts = nn.ModuleList([
            Expert(d_model, expert_d_ff, dropout) for _ in range(n_experts)
        ])

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: (batch, seq_len, d_model)

        Returns:
            output:            (B, S, D)  专家加权合并输出
            load_balance_loss: 标量  负载平衡损失（加入总损失后训练）
        """
        B, S, D = x.shape
        device = x.device

        dispatch_mask, _combine_weights, routing_probs = self.router(x)

        # ── 专家计算（循环版 —— N 较小时足够高效）──
        expert_outputs = torch.zeros(B, S, D, device=device, dtype=x.dtype)

        for k in range(self.n_experts):
            mask_k = dispatch_mask[:, :, k]  # (B, S)
            if mask_k.sum() == 0:
                continue  # 无 token 分配给此专家，节省计算

            expert_out = self.experts[k](x)            # (B, S, D)
            expert_outputs += expert_out * mask_k.unsqueeze(-1)

        # ── 负载平衡损失 (Switch Transformer, Fedus et al. 2021) ──
        # loss = N · Σ( f_i · P_i )
        #   f_i = 专家 i 实际处理 token 的比例
        #   P_i = 专家 i 的平均路由概率

        fraction_per_expert = dispatch_mask.sum(dim=(0, 1)) / (B * S * self.top_k)
        fraction_per_expert = fraction_per_expert / (fraction_per_expert.sum() + 1e-10)
        prob_per_expert = routing_probs.mean(dim=(0, 1))

        load_balance_loss = self.n_experts * (fraction_per_expert * prob_per_expert).sum()

        return expert_outputs, load_balance_loss
