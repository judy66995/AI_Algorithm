"""
路由可视化 —— 展示 AI 多态性的核心证据。

对输入文本中的每个 token，显示它被路由器分配到了哪些专家。
不同领域的 token 会激活不同的专家组合 → 可视化多态性。
"""

import torch

from .config import MoEConfig
from .model import GPTMoE
from .tokenizer import SimpleTokenizer


def analyze_routing(
    model: GPTMoE,
    tokenizer: SimpleTokenizer,
    text: str,
    config: MoEConfig,
):
    """
    分析并打印输入文本中各 token 在 MoE 层的专家路由分布。

    Args:
        model:     训练好的 GPTMoE 模型（或初始化后的）
        tokenizer: SimpleTokenizer 实例
        text:      待分析的输入文本
        config:    MoEConfig（仅用于引用超参数显示）
    """
    print("\n" + "=" * 80)
    print("🔬 专家路由可视化 —— AI 多态性分析")
    print("=" * 80)

    model.eval()
    device = next(model.parameters()).device

    tokens = tokenizer.encode(text)
    if not tokens:
        print("（输入文本为空，无法分析）")
        return

    tokens = tokens[:config.max_seq_len]
    input_ids = torch.tensor([tokens], device=device)
    token_strings = [tokenizer.idx2word.get(t, tokenizer.UNK_TOKEN) for t in tokens]

    # ── 前向传播并收集每层 MoE 的路由概率 ──
    B, S = input_ids.shape
    positions = torch.arange(0, S, dtype=torch.long, device=device).unsqueeze(0)
    tok_emb = model.token_embedding(input_ids)
    pos_emb = model.position_embedding(positions)
    hidden = model.embed_dropout(tok_emb + pos_emb)
    causal_mask = model._causal_mask(S, device)

    layer_routings = []  # [(layer_idx, routing_probs: (1, S, E)), ...]

    for layer_idx, block in enumerate(model.blocks):
        hidden, _ = block(hidden, attn_mask=causal_mask)
        if block.use_moe and block.moe is not None:
            _, _, routing_probs = block.moe.router(hidden)
            layer_routings.append((layer_idx, routing_probs))

    if not layer_routings:
        print("（模型中没有 MoE 层，无法显示路由信息）")
        return

    print(f"\n输入 token 数: {len(token_strings)}")
    print(f"MoE 层: {[l for l, _ in layer_routings]}, "
          f"每层 {config.n_experts} 专家, Top-{config.top_k}")

    # ── 逐层展示 ──
    for layer_idx, routing_probs in layer_routings:
        probs = routing_probs.squeeze(0)       # (S, E)
        top_experts = probs.argmax(dim=-1)     # (S,)

        print(f"\n{'─' * 60}")
        print(f"Layer {layer_idx} (MoE) — 各 token 首选的专家:")
        print(f"{'─' * 60}")

        for expert_id in range(min(config.n_experts, 8)):
            assigned = [
                (i, token_strings[i], probs[i, expert_id].item())
                for i in range(len(token_strings))
                if top_experts[i] == expert_id
            ]
            if assigned:
                summary = " ".join(
                    f"'{t}'({p:.2f})" for _, t, p in assigned[:10]
                )
                extra = f" ...共 {len(assigned)} 个" if len(assigned) > 10 else ""
                print(f"  专家 {expert_id}: {summary}{extra}")

    # ── 总体统计 ──
    print(f"\n{'─' * 60}")
    print("各专家使用率统计（跨所有 MoE 层）:")
    print(f"{'─' * 60}")

    all_usage = torch.zeros(config.n_experts, device=device)
    for _, routing_probs in layer_routings:
        assignments = routing_probs.squeeze(0).argmax(dim=-1)
        for e in range(config.n_experts):
            all_usage[e] += (assignments == e).sum()

    total = all_usage.sum()
    if total > 0:
        for e in range(config.n_experts):
            pct = all_usage[e].item() / total.item() * 100
            bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
            print(f"  专家 {e}: {bar} {pct:.1f}%")
