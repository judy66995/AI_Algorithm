# 📘 代码详解 —— 小白也能看懂的源码指南

> 本文档逐文件解释整个项目的代码逻辑。适合想深入理解但不知从何下手的初学者。

---

## 🗺️ 整体架构（一张图看懂）

```
输入文字 "The cat sat"
     │
     ▼
┌──────────────────┐
│  SimpleTokenizer │  ← 把文字变成数字 ID
│  "The cat sat"   │     [2, 5, 18, 37]
│       ↓          │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│   Token Embedding │  ← 每个数字 → 一个 128 维向量
│   + Position Emb  │     向量是模型能"理解"的格式
└──────────────────┘
     │
     ▼
┌──────────────────────────────────────────────┐
│           Transformer Blocks（循环 N 层）      │
│                                              │
│  Block 0 (密集层):                            │
│    Attention → FeedForward                   │
│                                              │
│  Block 1 (MoE 层):          ← 多态性在此！     │
│    Attention → Router → Expert#0              │
│                      → Expert#1  (只走一个)   │
│                      → Expert#2              │
│                      → Expert#3              │
│                                              │
│  Block 2 (密集层):                            │
│    Attention → FeedForward                   │
│  ...                                         │
└──────────────────────────────────────────────┘
     │
     ▼
┌──────────────────┐
│   LM Head        │  ← 把向量变回词表概率
│   (Linear)       │     预测下一个 token
└──────────────────┘
     │
     ▼
输出: 每个位置预测下一个 token 的概率
```

---

## 📂 逐文件讲解

---

### 1. [config.py](polymoe/config.py) —— ⚙️ 配置中心

**作用**：存放模型和训练的所有参数。

```python
@dataclass
class MoEConfig:
    d_model: int = 256        # 模型的"宽度"。越大 → 越聪明但也越慢
    n_layers: int = 4         # 层数。越大 → 理解能力越深
    n_experts: int = 4        # MoE 层有多少个专家
    top_k: int = 1            # 每个 token 激活几个专家（1 = 最省算力）
    batch_size: int = 8       # 一次喂给模型多少条数据
    max_steps: int = 2000     # 总共训练多少步
    # ... 还有更多参数
```

**小白理解**：这里就像遥控器上的按钮，所有"设置"都在这里改。

---

### 2. [tokenizer.py](polymoe/tokenizer.py) —— 🔤 分词器

**作用**：把人类文字变成模型能理解的数字。

```
"the cat sat"  →  ["the", "cat", "sat"]  →  [5, 12, 37]
```

**关键代码**：

```python
class SimpleTokenizer:
    def fit(self, texts):
        # 统计所有文本中每个词出现的次数
        counter = Counter()
        for text in texts:
            counter.update(text.split())
        # 取出现最频繁的前 N 个词作为词表
        for word, _ in counter.most_common(vocab_size - 4):
            self.word2idx[word] = len(self.word2idx)

    def encode(self, text):
        # "hello world" → [5, 23]
        return [self.word2idx.get(word, 1) for word in text.split()]

    def decode(self, ids):
        # [5, 23] → "hello world"
        return " ".join(self.idx2word[i] for i in ids)
```

**小白理解**：就像一个翻译官，把人类语言翻译成"AI 数字语言"。

---

### 3. [expert.py](polymoe/expert.py) —— 👨‍🔬 单个专家

**作用**：每个专家就是一个小型神经网络（FFN），负责处理分配给它的 token。

```python
class Expert(nn.Module):
    def __init__(self, d_model, d_ff, dropout):
        self.w1 = nn.Linear(d_model, d_ff)   # 放大：128 → 256
        self.w2 = nn.Linear(d_ff, d_model)   # 缩回：256 → 128

    def forward(self, x):
        # x → Linear → GELU → Dropout → Linear → 输出
        return self.w2(F.gelu(self.w1(x)))
```

**小白理解**：专家就像一个"迷你大脑"。结构很简单——放大、激活、缩回。不同专家会自己学会处理不同类型的文字。

---

### 4. [router.py](polymoe/router.py) —— 🧭 路由器（多态性的关键！）

**作用**：看一个 token，决定把它发给哪个专家处理。

```python
class Router(nn.Module):
    def forward(self, x):
        logits = self.gate(x)                # 给每个专家打分
        routing_probs = softmax(logits)       # 转成概率 [0.1, 0.7, 0.1, 0.1]
        topk_weights, topk_indices = topk(routing_probs, k=self.top_k)
        # 只保留概率最高的 top_k 个专家
        return dispatch_mask  # 标记：这个 token → 专家 #1
```

**多态性如何体现**：

```
Token "derivative" → Router 打分 → [0.8, 0.1, 0.05, 0.05] → 选专家 #0（数学专家）
Token "function"   → Router 打分 → [0.2, 0.6, 0.1, 0.1]  → 选专家 #1（编程专家）
Token "history"    → Router 打分 → [0.1, 0.1, 0.7, 0.1]  → 选专家 #2（人文专家）
```

**小白理解**：路由器就像快递分拣员——看到包裹上的标签，决定送去哪个仓库。

---

### 5. [moe_layer.py](polymoe/moe_layer.py) —— 🏗️ MoE 层

**作用**：把 Router 和多个 Expert 组装在一起，并加上"负载均衡"机制。

```python
class MoELayer(nn.Module):
    def forward(self, x):
        # 1. Router 决定分配方案
        dispatch_mask = self.router(x)

        # 2. 每个专家处理被分配给它的 token
        for k in range(n_experts):
            expert_outputs += self.experts[k](x) * mask_k

        # 3. 计算负载均衡损失（防止所有 token 都挤到一个专家）
        load_balance_loss = n_experts * Σ(f_i · P_i)

        return expert_outputs, load_balance_loss
```

**负载均衡是什么？** 如果不加约束，Router 可能把所有 token 都发给专家 #0，其他专家"失业"。负载均衡损失惩罚这种行为，确保专家们"公平竞争"。

**小白理解**：MoE 层就像一个团队经理——分派任务（Router）、让各员工干活（Expert）、确保没人太闲也没人太忙（负载均衡）。

---

### 6. [transformer_block.py](polymoe/transformer_block.py) —— 🧱 Transformer 块

**作用**：一个标准的 Transformer 层 = 自注意力 + 前馈网络（可以是密集的，也可以是 MoE）。

```python
class TransformerBlock(nn.Module):
    def forward(self, x):
        # 第 1 步：自注意力（每个 token 看所有其他 token）
        x = x + self.attention(self.ln1(x))

        # 第 2 步：前馈网络
        if self.use_moe:
            x = x + self.moe(self.ln2(x))    # MoE 路径（多态性！）
        else:
            x = x + self.ffn(self.ln2(x))    # 普通 FFN 路径

        return x
```

**为什么混合使用密集层和 MoE 层？**
- **密集层**（如第 0、2、4 层）：处理通用模式，所有 token 共享
- **MoE 层**（如第 1、3、5 层）：处理专业化模式，不同 token 走不同专家

**小白理解**：就像公司有"通用技能培训"（密集层）和"专业技能分组"（MoE 层）交替进行。

---

### 7. [model.py](polymoe/model.py) —— 🏛️ 完整 GPT 模型

**作用**：把所有组件组装成完整的语言模型。

```python
class GPTMoE(nn.Module):
    def __init__(self, config):
        self.token_embedding    = nn.Embedding(...)     # 词嵌入
        self.position_embedding = nn.Embedding(...)     # 位置嵌入
        self.blocks = [TransformerBlock(...), ...]      # N 个 Transformer 块
        self.final_ln = nn.LayerNorm(...)               # 最后的归一化
        self.lm_head = nn.Linear(...)                   # 输出层

    def forward(self, x):
        # word → embedding → transformer blocks → output
        hidden = token_emb + position_emb
        for block in self.blocks:
            hidden, lb_loss = block(hidden)
        logits = self.lm_head(final_ln(hidden))
        return logits
```

**generate 方法**：自回归生成——每次预测下一个 token，然后把它接到输入后面，继续预测下一个…… 直到生成足够多或遇到结束符。

```python
def generate(self, tokenizer, prompt, max_new_tokens=50):
    tokens = tokenizer.encode(prompt)
    for _ in range(max_new_tokens):
        logits = model(tokens)         # 前向传播
        next_token = sample(logits[-1]) # 采样下一个 token
        tokens.append(next_token)       # 接上去
    return tokenizer.decode(tokens)
```

**小白理解**：GPTMoE 就是最终产品——输入文字，输出文字。生成过程就像"一个字一个字地往下接龙"。

---

### 8. [trainer.py](polymoe/trainer.py) —— 🏋️ 训练器

**作用**：控制模型学习的过程。

```python
class Trainer:
    def train_step(self, x, y):
        # 1. 前向传播：模型预测
        logits, lb_loss = model(x)

        # 2. 计算损失：预测 vs 正确答案
        lm_loss = cross_entropy(logits, y)
        total_loss = lm_loss + 0.01 * lb_loss

        # 3. 反向传播：算梯度
        total_loss.backward()

        # 4. 更新参数：往损失减小的方向调
        optimizer.step()
```

**关键技巧**：

| 技巧 | 作用 | 通俗解释 |
|------|------|---------|
| **混合精度 (AMP)** | fp16 半精度计算 | 省一半显存，速度还快 |
| **梯度累积** | 多步才更新一次 | 小显存也能模拟大 batch |
| **Warmup + 余弦衰减** | 学习率先升后降 | 起步稳、中途快、收尾细 |
| **梯度裁剪** | 限制梯度最大值 | 防止"学崩了" |

**小白理解**：训练器就像健身教练——告诉模型"你预测错了，往这个方向调整"。

---

### 9. [data.py](polymoe/data.py) —— 📊 数据模块

**作用**：加载训练数据，打包成模型能吃的格式。

```python
class TextDataset(Dataset):
    def __getitem__(self, idx):
        # 返回 (input, target)，target 是 input 向后移一位
        # 例如："the cat sat on" → "cat sat on the"
        return x, y  # 自回归任务
```

数据来源优先级：
1. 本地 `generate_corpus.py` 生成的合成语料（最稳定）
2. 内置的 45+ 条示例文本
3. 联网下载 WikiText-2（可选）

**小白理解**：DataLoader 就像食堂打饭窗口——把原始食材（文本）做成一份份套餐（batch），喂给模型。

---

### 10. [visualize.py](polymoe/visualize.py) —— 📈 可视化

**作用**：展示多态性的核心证据——不同 token 被路由到了哪个专家。

```python
def analyze_routing(model, tokenizer, text):
    # 对输入文本的每个 token，记录它在每一层 MoE 中被
    # 分配给了哪个专家，然后打印出来
```

**示例输出**：
```
Layer 1 (MoE) — 各 token 首选的专家:
  专家 0: 'transformer'(0.51) 'model'(0.52) 'derivative'(0.55)  ← 技术类 token
  专家 1: 'The'(0.50) 'history'(0.49) 'culture'(0.51)           ← 通用/人文类 token

各专家使用率统计:
  专家 0: ████████████████████████░░░░░░░░░░ 48.5%
  专家 1: ██████████████████████████░░░░░░░░ 51.5%
```

**小白理解**：这个函数让你"看到"多态性——不同 token 确实走了不同的专家。

---

### 11. [generate_corpus.py](generate_corpus.py) —— 📝 语料生成器

**作用**：用模板生成涵盖 7 个领域的训练文本，不依赖网络。

| 领域 | 示例内容 |
|------|---------|
| 编程 | function, algorithm, compiler... |
| 数学 | theorem, derivative, matrix... |
| AI | neural network, transformer, gradient... |
| 科学 | electron, molecule, gravity... |
| 历史 | civilization, empire, revolution... |
| 叙事 | 学术论文风格的标准句式 |
| 名言 | "I think therefore I am" 等经典句子 |

**小白理解**：因为模型需要"课本"来学习，这个文件就是自动印课本的印刷机。

---

### 12. [main.py](main.py) —— 🚪 入口文件

**作用**：整合所有模块，提供命令行接口。

**流程**：
```
1. 解析命令行参数  →  MoEConfig
2. 加载数据         →  texts
3. 构建分词器       →  tokenizer
4. 创建 DataLoader  →  train_loader, val_loader
5. 创建模型         →  GPTMoE
6. 训练             →  Trainer
7. 生成示例         →  model.generate()
8. 可视化路由       →  analyze_routing()
9. 打印总结         →  统计信息
```

**自动 GPU 切换**：如果当前 Python 没有 CUDA，会自动找到 conda 的 `torch_cuda` 环境并切换过去。

---

## 🔗 数据流全景图

```
main.py
  │
  ├─→ parse_args()          → MoEConfig（所有设置）
  ├─→ load_wikitext()       → texts（训练文本）
  ├─→ SimpleTokenizer.fit() → tokenizer（文字↔数字）
  ├─→ TextDataset()         → DataLoader（打包好的数据）
  │
  ├─→ GPTMoE(config)        → 模型
  │     ├─ Token Embedding
  │     ├─ Position Embedding
  │     ├─ TransformerBlock × N
  │     │     ├─ MultiHeadAttention
  │     │     └─ Dense FFN 或 MoELayer
  │     │           ├─ Router（决策）
  │     │           └─ Expert × 4（执行）
  │     └─ LM Head
  │
  ├─→ Trainer(model, config)
  │     └─ train_epoch() → 训练循环
  │           ├─ 前向传播
  │           ├─ 计算 loss（语言模型 loss + 负载均衡 loss）
  │           ├─ 反向传播
  │           └─ 更新参数
  │
  ├─→ model.generate()      → 文本生成
  └─→ analyze_routing()     → 可视化分析
```

---

## 💡 核心概念一句话总结

| 概念 | 一句话 |
|------|--------|
| **Embedding** | 把文字变成数学向量 |
| **Attention** | 让每个词"看到"句子里的其他词 |
| **FFN** | 对每个词做一次非线性变换 |
| **Router** | 决定每个词应该由哪个专家处理 |
| **Expert** | 一个专门的小网络，擅长处理某类词 |
| **MoE** | 多个专家 + 一个路由器 = 动态选择 |
| **多态性** | 不同输入走不同计算路径 |
| **负载均衡** | 防止某些专家过劳、某些专家闲置 |
| **Cross Entropy** | 衡量"预测"和"正确答案"的差距 |
| **Perplexity** | 模型"困惑"程度，越低越好 |

---

> 📬 回到 [README.md](README.md) 看项目概览和快速开始指南。
