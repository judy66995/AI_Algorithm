"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AI 多态性：动态稀疏 MoE Transformer 语言模型                       ║
║           Polymorphic AI: Sparse Mixture-of-Experts Transformer            ║
╚══════════════════════════════════════════════════════════════════════════════╝

用法：
    python main.py                # 使用默认配置训练
    python main.py --small        # 快速调试（小模型 + 少步数）
    python main.py --full-moe     # 所有层都用 MoE
    python main.py --help         # 查看所有参数

交互式使用：
    from polymoe import GPTMoE, MoEConfig, Trainer, analyze_routing
    # ...（自定义训练流程）

模块结构：
    polymoe/
    ├── config.py            — MoEConfig 配置数据类
    ├── tokenizer.py         — SimpleTokenizer 词级别分词器
    ├── expert.py            — Expert 单专家 FFN
    ├── router.py            — Router Top-K 动态路由
    ├── moe_layer.py         — MoELayer 混合专家层
    ├── transformer_block.py — TransformerBlock（注意力 + FFN/MoE）
    ├── model.py             — GPTMoE 完整语言模型
    ├── data.py              — TextDataset + WikiText-2 加载
    ├── trainer.py           — Trainer（AMP + 梯度累积 + 学习率调度）
    ├── visualize.py         — analyze_routing 专家路由可视化
    └── __init__.py          — 统一导出接口
"""

import argparse
import os
import subprocess
import sys
import time

# ── GPU 自动切换：当前环境无 CUDA 时，自动切到 conda torch_cuda 环境 ──
def _ensure_gpu():
    """如果当前 Python 没有 CUDA PyTorch，自动切换到 conda torch_cuda 环境"""
    # 先尝试 import torch，看有没有 CUDA
    import torch as _torch
    if _torch.cuda.is_available():
        return  # 已经是 GPU 版，什么都不用做

    # 找 conda 的 torch_cuda 环境
    conda_home = os.environ.get("CONDA_EXE") or os.environ.get("MAMBA_EXE")
    if conda_home:
        # 已经在某个 conda 环境中，但它是 CPU 版，别死循环
        conda_env = os.environ.get("CONDA_DEFAULT_ENV", "")
        if conda_env == "torch_cuda":
            return  # 已经是 torch_cuda 但没 CUDA，不重试

    # 尝试几个常见的 conda 路径
    candidates = [
        r"C:\Users\JC\radioconda\envs\torch_cuda\python.exe",
        r"C:\Users\JC\miniconda3\envs\torch_cuda\python.exe",
        os.path.expanduser(r"~\radioconda\envs\torch_cuda\python.exe"),
    ]
    gpu_python = None
    for p in candidates:
        if os.path.isfile(p):
            gpu_python = p
            break

    if not gpu_python:
        # 没有找到 GPU 环境，继续用 CPU 跑
        return

    # 用 GPU 版 Python 重新执行当前脚本
    print(f"[auto-switch] 检测到 GPU 环境: {gpu_python}")
    print(f"[auto-switch] 正在切换到 CUDA PyTorch...\n")
    sys.stdout.flush()
    subprocess.run(
        [gpu_python] + sys.argv,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )
    sys.exit(0)

_ensure_gpu()

import torch

# 修复 Windows GBK 编码下 Unicode 打印问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from torch.utils.data import DataLoader

from polymoe import (
    MoEConfig,
    SimpleTokenizer,
    GPTMoE,
    TextDataset,
    load_wikitext,
    Trainer,
    analyze_routing,
)


# ═══════════════════════════════════════════════════════════════════════════
# CLI 参数
# ═══════════════════════════════════════════════════════════════════════════

def parse_args() -> MoEConfig:
    """解析命令行参数，返回 MoEConfig"""
    parser = argparse.ArgumentParser(
        description="AI 多态性：稀疏 MoE Transformer 训练",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                          # 默认配置
  python main.py --small                  # 快速调试
  python main.py --n-experts 16 --top-k 4 # 更大 MoE
  python main.py --full-moe               # 所有层都是 MoE
        """,
    )

    # 预设
    parser.add_argument("--small", action="store_true",
                        help="快速调试模式（小模型 + 200 步）")
    parser.add_argument("--full-moe", action="store_true",
                        help="所有 Transformer 层都使用 MoE")

    # 模型架构（轻量默认值，避免过热）
    parser.add_argument("--d-model", type=int, default=256)
    parser.add_argument("--n-heads", type=int, default=4)
    parser.add_argument("--n-layers", type=int, default=4)
    parser.add_argument("--d-ff", type=int, default=1024)
    parser.add_argument("--max-seq-len", type=int, default=128)

    # MoE（减少专家数以降低计算量）
    parser.add_argument("--n-experts", type=int, default=4)
    parser.add_argument("--top-k", type=int, default=1)
    parser.add_argument("--expert-d-ff", type=int, default=256)
    parser.add_argument("--load-balance-coef", type=float, default=0.01)

    # 训练（减小 batch 和步数）
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--max-steps", type=int, default=2000)
    parser.add_argument("--grad-accum", type=int, default=2)
    parser.add_argument("--no-amp", action="store_true",
                        help="禁用混合精度训练")

    args = parser.parse_args()

    # ── 应用预设 ──
    if args.small:
        config = MoEConfig(
            d_model=128, n_heads=2, n_layers=2, d_ff=256,
            max_seq_len=64, n_experts=2, top_k=1, expert_d_ff=128,
            moe_layers=(1,), batch_size=4, seq_len=64, max_steps=200,
        )
        return config

    moe_layers = tuple(range(args.n_layers)) if args.full_moe else (1, 3, 5)

    return MoEConfig(
        d_model=args.d_model,
        n_heads=args.n_heads,
        n_layers=args.n_layers,
        d_ff=args.d_ff,
        max_seq_len=args.max_seq_len,
        n_experts=args.n_experts,
        top_k=args.top_k,
        expert_d_ff=args.expert_d_ff,
        moe_layers=moe_layers,
        batch_size=args.batch_size,
        seq_len=args.max_seq_len,
        learning_rate=args.lr,
        max_steps=args.max_steps,
        grad_accum_steps=args.grad_accum,
        load_balance_coef=args.load_balance_coef,
        use_amp=not args.no_amp,
    )


# ═══════════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "=" * 80)
    print("  AI 多态性：动态稀疏 MoE Transformer")
    print("  AI Polymorphism: Sparse Mixture-of-Experts Transformer")
    print("=" * 80)

    # ── 0. CUDA 检查 ──
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"\n✓ GPU 可用: {gpu_name} ({gpu_mem:.1f} GB)")
    else:
        print("\n⚠ GPU 不可用，将使用 CPU 训练")

    # ── 1. 配置 ──
    config = parse_args()
    dense_layers = [i for i in range(config.n_layers) if i not in config.moe_layers]

    print(f"\n模型配置:")
    print(f"  架构: {config.n_layers} 层, d_model={config.d_model}, "
          f"n_heads={config.n_heads}")
    print(f"  密集层: {dense_layers}")
    print(f"  MoE 层: {list(config.moe_layers)} "
          f"({config.n_experts} 专家, Top-{config.top_k})")
    print(f"  训练: {config.max_steps} steps, batch={config.batch_size}, "
          f"lr={config.learning_rate}")

    # ── 2. 数据 ──
    print(f"\n{'─' * 40}\n加载数据集...")
    texts = load_wikitext()

    # ── 3. 分词器 ──
    print(f"\n构建分词器...")
    tokenizer = SimpleTokenizer(vocab_size=config.vocab_size)
    tokenizer.fit(texts)
    config.vocab_size = len(tokenizer)
    print(f"词表大小: {config.vocab_size}")

    # ── 4. DataLoader（自动适配数据量）──
    print(f"\n创建数据集...")
    split = int(len(texts) * 0.9)
    train_ds = TextDataset(texts[:split], tokenizer, config.seq_len)
    val_ds = TextDataset(texts[split:], tokenizer, config.seq_len)

    # 数据不足时自动降级
    while train_ds.n_samples < config.batch_size and config.batch_size > 2:
        config.batch_size //= 2
        config.seq_len = max(32, config.seq_len // 2)
        print(f"数据不足，自动调整: batch_size={config.batch_size}, "
              f"seq_len={config.seq_len}")
        train_ds = TextDataset(texts[:split], tokenizer, config.seq_len)
        val_ds = TextDataset(texts[split:], tokenizer, config.seq_len)
    if config.max_steps > train_ds.n_samples * 5:
        config.max_steps = max(200, train_ds.n_samples * 5)
        print(f"数据量有限，目标步数调整为: {config.max_steps}")

    train_loader = DataLoader(
        train_ds, batch_size=config.batch_size,
        shuffle=True, drop_last=True, pin_memory=True,
    )
    val_loader = DataLoader(
        val_ds, batch_size=config.batch_size,
        shuffle=False, drop_last=True, pin_memory=True,
    )
    print(f"训练批次/epoch: {len(train_loader)}, 目标总步数: {config.max_steps}")

    # ── 5. 模型 ──
    print(f"\n{'─' * 40}\n创建模型...")
    model = GPTMoE(config)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"总参数: {total_params / 1e6:.2f}M")
    print(f"预估显存 (fp16): ~{total_params * 2 / 1024**3 + 0.5:.1f} GB")

    # ── 6. 训练 ──
    print(f"\n{'─' * 40}\n开始训练...")
    trainer = Trainer(model, config, tokenizer)
    start_time = time.time()

    for epoch in range(200):  # 由 max_steps 控制提前退出
        print(f"\n{'=' * 60}\nEpoch {epoch + 1}\n{'=' * 60}")
        metrics = trainer.train_epoch(train_loader)

        print(f"Epoch {epoch + 1} 完成 | "
              f"LM Loss: {metrics['lm_loss']:.4f} | "
              f"LB Loss: {metrics['lb_loss']:.4f}")

        if len(val_loader) > 0:
            ppl = trainer.evaluate(val_loader)
            print(f"验证困惑度: {ppl:.2f}")

        if trainer.step >= config.max_steps:
            print(f"\n✓ 已达最大步数 {config.max_steps}")
            break

    print(f"\n训练完成！总耗时: {(time.time() - start_time) / 60:.1f} 分钟")

    # ── 7. 生成示例 ──
    print(f"\n{'─' * 40}\n文本生成示例...")
    for prompt in [
        "The artificial intelligence",
        "In mathematics, the",
        "The history of",
        "Machine learning is",
    ]:
        print(f"\n{'·' * 40}")
        print(f"Prompt: {prompt}")
        generated, _ = model.generate(tokenizer, prompt, max_new_tokens=30)
        print(f"生成:   {generated}")

    # ── 8. 可视化 ──
    print(f"\n{'─' * 40}\n专家路由分析...")
    test_text = (
        "The transformer model uses attention mechanisms to process sequences. "
        "In mathematics, the function is defined as a mapping between sets. "
        "Python code uses classes and functions to structure programs. "
        "The history of artificial intelligence began in ancient times."
    )
    analyze_routing(model, tokenizer, test_text, config)

    # ── 9. 总结 ──
    print(f"\n{'=' * 80}")
    print("  实验总结")
    print(f"{'=' * 80}")
    final_lm = trainer.train_losses[-1] if trainer.train_losses else float("nan")
    peak_mem = (torch.cuda.max_memory_allocated() / 1024**3
                if torch.cuda.is_available() else 0)

    print(f"""
  ✓ 训练步数: {trainer.step}
  ✓ 最终 LM Loss: {final_lm:.4f}
  ✓ 模型参数: {total_params / 1e6:.2f}M
  ✓ 显存峰值: {peak_mem:.2f} GB
  ✓ MoE: {config.n_experts} 专家/层, Top-{config.top_k}
  ✓ MoE 层: {list(config.moe_layers)}

  多态性体现：
  - Router 为每个 token 动态选择 {config.top_k}/{config.n_experts} 个专家
  - 不同 token → 不同专家 → 不同计算路径 → 多态性
  - 负载平衡损失确保专家"公平竞争"
  - analyze_routing() 可直观看到不同领域 token 的专家偏好
    """)

    return model, trainer, tokenizer


if __name__ == "__main__":
    main()
