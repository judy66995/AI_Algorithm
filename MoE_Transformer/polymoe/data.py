"""
数据模块 —— TextDataset + WikiText-2 加载 + 内置示例文本后备。
"""

from typing import List, Tuple

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

from .tokenizer import SimpleTokenizer


class TextDataset(Dataset):
    """
    自回归语言建模数据集。

    每个样本 = (input_ids[:-1], input_ids[1:])
    → 模型学习用前 N-1 个 token 预测后 N-1 个 token。
    """

    def __init__(self, texts: List[str], tokenizer: SimpleTokenizer, seq_len: int):
        self.seq_len = seq_len

        all_tokens = []
        for text in texts:
            if not text.strip():
                continue
            tokens = tokenizer.encode(text)
            all_tokens.extend(tokens)
            all_tokens.append(tokenizer.word2idx[tokenizer.EOS_TOKEN])

        self.data = torch.tensor(all_tokens, dtype=torch.long)
        self.n_samples = max(0, (len(self.data) - 1) // seq_len)

        print(f"数据集: {len(self.data)} tokens, "
              f"{self.n_samples} 个样本 (seq_len={seq_len})")

    def __len__(self) -> int:
        return self.n_samples

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        start = idx * self.seq_len
        end = start + self.seq_len

        x = self.data[start:end]
        y = self.data[start + 1:end + 1]

        # 补齐最后一个样本
        if len(x) < self.seq_len:
            x = F.pad(x, (0, self.seq_len - len(x)), value=0)
        if len(y) < self.seq_len:
            y = F.pad(y, (0, self.seq_len - len(y)), value=-100)

        return x, y


def load_wikitext() -> List[str]:
    """
    加载训练语料。

    使用本地合成语料（涵盖编程、数学、AI、科学、历史等多个领域），
    便于观察不同领域的 token 被路由到不同专家。

    注意：不通过 datasets 库下载 WikiText-2，因为其 HTTP 请求
    （aiohttp）与 CUDA 上下文冲突会导致 segfault。
    """
    return _get_sample_texts()



def _get_sample_texts() -> List[str]:
    """
    内置多领域示例文本 + 程序化生成语料库。

    文本涵盖编程、数学、AI、科学、历史等多个领域，
    便于观察不同领域的 token 被路由到不同专家。
    """
    texts = _base_texts()

    # 尝试通过外部语料生成器扩充
    try:
        from generate_corpus import generate_corpus
        corpus = generate_corpus(min_tokens=500000)
        texts.extend(corpus)
        total_w = sum(len(t.split()) for t in texts)
        print(f"已生成合成语料，总计 ~{total_w/1000:.0f}K tokens ({len(texts)} 段)")
    except ImportError:
        print("（未找到语料生成器，仅使用内置文本）")

    return texts


def _base_texts() -> List[str]:
    """基础示例文本"""
    return [
        # ── 文学叙事 ──
        "The quick brown fox jumps over the lazy dog. This classic pangram contains every letter of the English alphabet at least once.",
        "It was a dark and stormy night. The rain fell in torrents, except at occasional intervals when it was checked by a violent gust of wind.",
        "In the beginning, God created the heavens and the earth. The earth was without form and void, and darkness was over the face of the deep.",
        "To be or not to be, that is the question. Whether it is nobler in the mind to suffer the slings and arrows of outrageous fortune.",
        "All happy families are alike. Each unhappy family is unhappy in its own way. Everything was in confusion in the Oblonsky household.",

        # ── 人工智能 / 科技 ──
        "Artificial intelligence is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.",
        "The transformer is a deep learning architecture introduced in 2017. It relies on a parallel multi-head attention mechanism.",
        "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.",
        "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability.",
        "A graphics processing unit (GPU) is a specialized electronic circuit designed to rapidly manipulate and alter memory.",

        # ── 数学 ──
        "In mathematics, the Pythagorean theorem is a fundamental relation in Euclidean geometry among the three sides of a right triangle.",
        "The derivative of a function of a real variable measures the sensitivity to change of the function value with respect to a change in its argument.",
        "A prime number is a natural number greater than 1 that is not a product of two smaller natural numbers.",

        # ── 计算机科学 ──
        "The history of computer science began long before the modern discipline of computer science. Developments in previous centuries alluded to the discipline.",
        "Machine learning algorithms build a model based on sample data, known as training data, in order to make predictions or decisions.",
        "Neural networks are computing systems inspired by the biological neural networks that constitute animal brains.",
        "Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with interactions between computers and human language.",
        "The Internet is the global system of interconnected computer networks that uses the Internet protocol suite to communicate between networks and devices.",

        # ── 自然科学 ──
        "Quantum computing is the exploitation of collective properties of quantum states, such as superposition and entanglement, to perform computation.",
        "The theory of relativity usually encompasses two interrelated theories by Albert Einstein: special relativity and general relativity.",
        "Climate change includes both global warming driven by human-induced emissions of greenhouse gases and the resulting large-scale shifts in weather patterns.",
        "DNA is a molecule composed of two polynucleotide chains that coil around each other to form a double helix carrying genetic instructions.",
        "The solar system is the gravitationally bound system of the Sun and the objects that orbit it. It formed 4.6 billion years ago.",
        "The periodic table, also known as the periodic table of elements, is a tabular display of the chemical elements.",
        "Evolution is change in the heritable characteristics of biological populations over successive generations.",
        "A black hole is a region of spacetime where gravity is so strong that nothing, including light, has enough energy to escape.",

        # ── 人文历史 ──
        "The Renaissance was a period in European history marking the transition from the Middle Ages to modernity.",
        "Economics is the social science that studies the production, distribution, and consumption of goods and services.",
        "Philosophy is the study of general and fundamental questions, such as those about existence, reason, knowledge, values, mind, and language.",
        "Democracy is a form of government in which the people have the authority to deliberate and decide legislation.",
        "The French Revolution was a period of radical political and societal change in France.",
        "The Great Wall of China is a series of fortifications that were built across the historical northern borders of ancient Chinese states.",
        "Chess is a board game for two players. It is sometimes called international chess or Western chess.",

        # ── 其他 ──
        "Music is the art of arranging sounds in time to produce a composition through the elements of melody, harmony, rhythm, and timbre.",
        "The human brain is the central organ of the human nervous system, and with the spinal cord makes up the central nervous system.",
        "Photography is the art, application, and practice of creating durable images by recording light.",
        "Robotics is an interdisciplinary branch of computer science and engineering.",
        "The scientific method is an empirical method for acquiring knowledge that has characterized the development of science since at least the 17th century.",
    ]
