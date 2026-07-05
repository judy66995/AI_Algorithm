"""
路由器模块 —— AI 多态性的"决策大脑"。

Router 是一个可学习的门控网络：观察每个 token，输出该 token 应分配给
哪些 Expert 处理的概率分布。不同 token 激活不同专家 → 多态性的根源。
"""

from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


class Router(nn.Module):
    """
    Top-K 动态路由门控。

    流程：
      1. Linear(d_model → n_experts) 产生原始分数
      2. Softmax → 概率分布
      3. Top-K 截断 → 只保留概率最高的 K 个专家
      4. 重新归一化 → 被选中专家的权重之和 = 1

    多态性体现：
      Token A → Router(A) = [0.7(专家3), 0.2(专家5), ...] → 走专家 3+5
      Token B → Router(B) = [0.6(专家1), 0.3(专家7), ...] → 走专家 1+7
      → 同一模型，不同 token 走完全不同的计算子图
    """

    def __init__(self, d_model: int, n_experts: int, top_k: int = 2):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, n_experts, bias=False)

        # 小方差初始化，让所有专家初始概率接近
        nn.init.normal_(self.gate.weight, std=0.02)

    def forward(
        self, x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            x: (batch, seq_len, d_model)

        Returns:
            dispatch_mask:  (B, S, E) 二值风格的掩码，标记每个 token 被分配到哪些专家
            combine_weights:(B, S, E) 激活专家的权重（经重新归一化，其余为 0）
            routing_probs:  (B, S, E) 原始 Softmax 概率（用于计算负载均衡损失）
        """
        logits = self.gate(x)                       # (B, S, E)
        routing_probs = F.softmax(logits, dim=-1)   # (B, S, E)

        # Top-K 选择
        topk_weights, topk_indices = torch.topk(
            routing_probs, self.top_k, dim=-1
        )  # (B, S, K), (B, S, K)

        # 重新归一化：选中的 K 个权重之和 = 1
        topk_weights = topk_weights / (
            topk_weights.sum(dim=-1, keepdim=True) + 1e-10
        )

        # 将 topk_weights 散布回 n_experts 维度
        dispatch_mask = torch.zeros_like(routing_probs)  # (B, S, E)
        dispatch_mask.scatter_(-1, topk_indices, topk_weights)

        return dispatch_mask, dispatch_mask.clone(), routing_probs
