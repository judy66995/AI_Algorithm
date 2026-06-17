"""
单专家模块 —— MoE 中一个独立的小型 FFN。

每个 Expert 都是一个 Linear→GELU→Linear 结构。
不同专家会"术业有专攻"，训练过程中逐渐分化出不同的特化能力。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Expert(nn.Module):
    """
    单专家 FFN。

    结构：Linear(d→4d) → GELU → Dropout → Linear(4d→d)
    和标准 Transformer FFN 相同，只是中间维度更小（由 expert_d_ff 控制）。
    """

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

        self._init_weights()

    def _init_weights(self):
        """He 初始化 —— GELU 激活函数的最佳搭档"""
        nn.init.kaiming_normal_(self.w1.weight, nonlinearity="relu")
        nn.init.kaiming_normal_(self.w2.weight, nonlinearity="linear")
        nn.init.zeros_(self.w1.bias)
        nn.init.zeros_(self.w2.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, d_model)
        Returns:
            (batch, seq_len, d_model)
        """
        return self.w2(self.dropout(F.gelu(self.w1(x))))
