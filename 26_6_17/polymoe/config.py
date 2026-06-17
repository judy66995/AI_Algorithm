"""
配置数据类 —— 模型与训练的所有超参数集中管理。
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class MoEConfig:
    """MoE Transformer 的完整配置

    用法：
        # 大型实验配置
        cfg = MoEConfig(n_experts=16, top_k=4, moe_layers=(0,1,2,3,4,5))

        # 快速调试配置
        cfg = MoEConfig(d_model=128, n_layers=2, max_steps=100)
    """
    # ── 模型架构（轻量默认值，适合本地 CPU/低配 GPU）──
    vocab_size: int = 8192           # 词表大小（训练时根据数据自动更新）
    d_model: int = 256               # 隐藏层维度（模型的"宽度"）
    n_heads: int = 4                 # 注意力头数（必须能整除 d_model）
    n_layers: int = 4                # Transformer 层数
    d_ff: int = 1024                 # 密集 FFN 的中间层维度
    max_seq_len: int = 128           # 最大序列长度

    # ── MoE 配置（轻量默认值）──
    n_experts: int = 4               # 专家总数（多态性的"形态"数量）
    top_k: int = 1                   # 每个 token 激活的专家数
    expert_d_ff: int = 256           # 每个专家的中间层维度
    moe_layers: Tuple[int, ...] = (1, 3, 5)  # 哪些层使用 MoE（0-indexed）
    expert_capacity_factor: float = 1.25     # 专家容量因子（>1.0 留余量）
    load_balance_coef: float = 0.01  # 负载平衡损失的权重

    # ── 训练 ──
    batch_size: int = 8
    seq_len: int = 128
    learning_rate: float = 3e-4
    warmup_steps: int = 500
    max_steps: int = 2000
    grad_accum_steps: int = 2        # 梯度累积步数
    clip_grad: float = 1.0

    # ── 混合精度 & 正则化 ──
    use_amp: bool = True             # fp16 混合精度
    dropout: float = 0.1

    # ── 数据集 ──
    dataset_name: str = "wikitext"
    dataset_config: str = "wikitext-2-raw-v1"
