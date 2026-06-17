"""
简易词级别分词器 —— 自包含，不依赖 huggingface tokenizers。

设计意图：
  - 零外部依赖，从训练文本直接构建词表
  - 词级别 tokenizer 使每个 token 可读，便于观察专家路由偏好
"""

from typing import List, Dict
from collections import Counter


class SimpleTokenizer:
    """基于词频的简易分词器"""

    PAD_TOKEN = "<PAD>"
    UNK_TOKEN = "<UNK>"
    BOS_TOKEN = "<BOS>"
    EOS_TOKEN = "<EOS>"

    def __init__(self, vocab_size: int = 8192):
        self.vocab_size = vocab_size
        self.word2idx: Dict[str, int] = {}
        self.idx2word: Dict[int, str] = {}

    def fit(self, texts: List[str]) -> "SimpleTokenizer":
        """从文本列表构建词表（按词频取 top-N）"""
        counter = Counter()
        for text in texts:
            counter.update(text.split())

        # 特殊 token 占前 4 个位置
        self.word2idx = {
            self.PAD_TOKEN: 0,
            self.UNK_TOKEN: 1,
            self.BOS_TOKEN: 2,
            self.EOS_TOKEN: 3,
        }

        for word, _ in counter.most_common(self.vocab_size - 4):
            if word not in self.word2idx:
                self.word2idx[word] = len(self.word2idx)

        self.idx2word = {v: k for k, v in self.word2idx.items()}
        return self

    def encode(self, text: str) -> List[int]:
        """将文本编码为 token ID 列表"""
        return [self.word2idx.get(t, 1) for t in text.split()]  # 1 = UNK

    def decode(self, ids: List[int]) -> str:
        """将 token ID 列表解码为文本"""
        return " ".join(self.idx2word.get(i, self.UNK_TOKEN) for i in ids)

    def __len__(self) -> int:
        return len(self.word2idx)
