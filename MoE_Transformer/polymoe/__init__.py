"""
polymoe — 基于稀疏 MoE (Mixture of Experts) 的 AI 多态性 Transformer

分层模块结构：
  config            — MoEConfig 配置数据类
  tokenizer         — SimpleTokenizer 词级别分词器
  expert            — Expert 单专家 FFN
  router            — Router 动态路由门控
  moe_layer         — MoELayer 混合专家层（路由 + 多专家 + 负载均衡）
  transformer_block — TransformerBlock（注意力 + FFN/MoE）
  model             — GPTMoE 完整 GPT 语言模型
  data              — TextDataset + 数据加载
  trainer           — Trainer 训练器（AMP + 梯度累积 + 学习率调度）
  visualize         — 专家路由可视化分析

用法:
    from polymoe import GPTMoE, MoEConfig, Trainer, analyze_routing
    from polymoe.data import load_wikitext, TextDataset
"""

import torch  # 必须在其他子模块之前导入，避免 CUDA segfault

# 轻量级模块可立即导入，重模块（含 torch CUDA）按需加载
from .config import MoEConfig
from .tokenizer import SimpleTokenizer
from .expert import Expert
from .router import Router
from .moe_layer import MoELayer
from .transformer_block import TransformerBlock

# 模型、训练、可视化 —— 按需导入（触发 CUDA 初始化）
__all__ = [
    "MoEConfig",
    "SimpleTokenizer",
    "Expert",
    "Router",
    "MoELayer",
    "TransformerBlock",
    "GPTMoE",
    "TextDataset",
    "load_wikitext",
    "Trainer",
    "analyze_routing",
]


def __getattr__(name):
    """懒加载重型模块，避免 CUDA 提前初始化导致 segfault"""
    _lazy = {
        "GPTMoE": ".model",
        "TextDataset": ".data",
        "load_wikitext": ".data",
        "Trainer": ".trainer",
        "analyze_routing": ".visualize",
    }
    if name in _lazy:
        import importlib
        mod = importlib.import_module(_lazy[name], __package__)
        attr = getattr(mod, name)
        globals()[name] = attr  # 缓存
        return attr
    raise AttributeError(f"module 'polymoe' has no attribute '{name}'")
