"""
Transformer Block —— 支持密集 FFN 和 MoE 两种前馈模式。

结构 (Pre-Norm)：
  Input → LN → MultiHeadAttention ──(+)──→ LN → [Dense FFN | MoE] ──(+)──→ Output
"""

from typing import Optional, Tuple

import torch
import torch.nn as nn

from .config import MoEConfig
from .moe_layer import MoELayer


class TransformerBlock(nn.Module):
    """
    单层 Transformer，可切换密集 / MoE 前馈。

    use_moe=True  → FFN 替换为 MoELayer（多态性）
    use_moe=False → 标准密集 FFN（基线）
    """

    def __init__(self, config: MoEConfig, use_moe: bool = False):
        super().__init__()
        self.use_moe = use_moe

        self.attention = nn.MultiheadAttention(
            embed_dim=config.d_model,
            num_heads=config.n_heads,
            dropout=config.dropout,
            bias=False,
            batch_first=True,
        )

        if use_moe:
            self.moe = MoELayer(
                d_model=config.d_model,
                n_experts=config.n_experts,
                top_k=config.top_k,
                expert_d_ff=config.expert_d_ff,
                dropout=config.dropout,
                capacity_factor=config.expert_capacity_factor,
            )
            self.ffn = None
        else:
            self.ffn = nn.Sequential(
                nn.Linear(config.d_model, config.d_ff),
                nn.GELU(),
                nn.Dropout(config.dropout),
                nn.Linear(config.d_ff, config.d_model),
                nn.Dropout(config.dropout),
            )
            self.moe = None

        self.ln1 = nn.LayerNorm(config.d_model)
        self.ln2 = nn.LayerNorm(config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(
        self, x: torch.Tensor, attn_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x:         (batch, seq_len, d_model)
            attn_mask: 因果注意力掩码

        Returns:
            output:  (B, S, D)
            lb_loss: 负载平衡损失（密集层返回 0）
        """
        lb_loss = torch.tensor(0.0, device=x.device)

        # ── 自注意力子层 ──
        residual = x
        x = self.ln1(x)
        attn_out, _ = self.attention(x, x, x, attn_mask=attn_mask)
        x = residual + self.dropout(attn_out)

        # ── FFN / MoE 子层 ──
        residual = x
        x = self.ln2(x)

        if self.use_moe and self.moe is not None:
            ffn_out, lb_loss = self.moe(x)
        elif self.ffn is not None:
            ffn_out = self.ffn(x)
        else:
            ffn_out = x

        x = residual + self.dropout(ffn_out)
        return x, lb_loss
