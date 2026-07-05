"""
训练器 —— 封装训练循环、评估与统计。

特性：
  - 混合精度训练 (AMP) —— fp16 节省 50% 显存
  - 梯度累积          —— 突破 GPU 显存限制模拟大 batch
  - Warmup + 余弦衰减 —— 稳定训练
  - 负载平衡损失       —— 防止 MoE 专家"赢家通吃"
"""

import math
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

from .config import MoEConfig
from .model import GPTMoE
from .tokenizer import SimpleTokenizer


class Trainer:
    """GPTMoE 训练器"""

    def __init__(
        self, model: GPTMoE, config: MoEConfig, tokenizer: SimpleTokenizer
    ):
        self.model = model
        self.config = config
        self.tokenizer = tokenizer
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model.to(self.device)

        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=0.01,
            betas=(0.9, 0.95),
        )

        self.scaler = torch.amp.GradScaler('cuda', enabled=config.use_amp)
        self.use_amp = config.use_amp and self.device.type == "cuda"

        self.step = 0
        self.best_loss = float("inf")

        self.train_losses: List[float] = []
        self.lb_losses: List[float] = []
        self.learning_rates: List[float] = []

        self._print_setup()

    def _print_setup(self):
        print(
            f"\n训练配置:\n"
            f"  设备: {self.device}\n"
            f"  混合精度: {self.use_amp}\n"
            f"  Batch size: {self.config.batch_size}\n"
            f"  梯度累积: {self.config.grad_accum_steps}\n"
            f"  有效 Batch: {self.config.batch_size * self.config.grad_accum_steps}\n"
            f"  学习率: {self.config.learning_rate}\n"
            f"  总步数: {self.config.max_steps}"
        )

    # ── 学习率调度 ────────────────────────────────────────────

    def get_lr(self) -> float:
        """Warmup → Cosine Decay"""
        if self.step < self.config.warmup_steps:
            return self.config.learning_rate * (self.step + 1) / self.config.warmup_steps

        progress = (self.step - self.config.warmup_steps) / max(
            1, self.config.max_steps - self.config.warmup_steps
        )
        return self.config.learning_rate * 0.5 * (1.0 + math.cos(math.pi * progress))

    # ── 单步训练 ──────────────────────────────────────────────

    def train_step(self, x: torch.Tensor, y: torch.Tensor) -> Tuple[float, float]:
        """一次前向 + 反向传播（支持梯度累积）"""
        self.model.train()
        x, y = x.to(self.device), y.to(self.device)

        with torch.amp.autocast('cuda', enabled=self.use_amp):
            logits, lb_loss = self.model(x)
            lm_loss = F.cross_entropy(
                logits.view(-1, self.config.vocab_size),
                y.view(-1),
                ignore_index=-100,
            )
            total_loss = lm_loss + self.config.load_balance_coef * lb_loss

        self.scaler.scale(
            total_loss / self.config.grad_accum_steps
        ).backward()

        return lm_loss.item(), lb_loss.item()

    # ── Epoch 训练 ────────────────────────────────────────────

    def train_epoch(self, dataloader: DataLoader) -> Dict[str, float]:
        """训练一个 epoch（或直到达到 max_steps）"""
        self.optimizer.zero_grad()
        epoch_lm_loss = 0.0
        epoch_lb_loss = 0.0
        n_batches = 0

        for batch_idx, (x, y) in enumerate(dataloader):
            lr = self.get_lr()
            for pg in self.optimizer.param_groups:
                pg["lr"] = lr

            lm_loss, lb_loss = self.train_step(x, y)
            epoch_lm_loss += lm_loss
            epoch_lb_loss += lb_loss
            n_batches += 1

            # 梯度累积触发点
            if (batch_idx + 1) % self.config.grad_accum_steps == 0:
                self.scaler.unscale_(self.optimizer)
                nn.utils.clip_grad_norm_(
                    self.model.parameters(), self.config.clip_grad
                )
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()

                self.step += 1
                self.train_losses.append(lm_loss)
                self.lb_losses.append(lb_loss)
                self.learning_rates.append(lr)

                if self.step % 200 == 0:
                    self._log_progress()

                if self.step >= self.config.max_steps:
                    break

        return {
            "lm_loss": epoch_lm_loss / max(n_batches, 1),
            "lb_loss": epoch_lb_loss / max(n_batches, 1),
        }

    def _log_progress(self):
        window = min(200, len(self.train_losses))
        avg_lm = sum(self.train_losses[-window:]) / window
        avg_lb = sum(self.lb_losses[-window:]) / window
        mem = (torch.cuda.memory_allocated() / 1024**3
               if torch.cuda.is_available() else 0)
        print(
            f"  Step {self.step:5d} | LM Loss: {avg_lm:.4f} | "
            f"LB Loss: {avg_lb:.4f} | LR: {self.learning_rates[-1]:.2e} | "
            f"GPU: {mem:.1f}GB",
            flush=True,
        )

    # ── 评估 ──────────────────────────────────────────────────

    @torch.no_grad()
    def evaluate(self, dataloader: DataLoader) -> float:
        """返回困惑度 (Perplexity)"""
        self.model.eval()
        total_loss = 0.0
        total_tokens = 0

        for x, y in dataloader:
            x, y = x.to(self.device), y.to(self.device)
            with torch.amp.autocast('cuda', enabled=self.use_amp):
                logits, _ = self.model(x)
                loss = F.cross_entropy(
                    logits.view(-1, self.config.vocab_size),
                    y.view(-1),
                    ignore_index=-100,
                    reduction="sum",
                )
            total_loss += loss.item()
            total_tokens += (y != -100).sum().item()

        return math.exp(total_loss / max(1, total_tokens))
