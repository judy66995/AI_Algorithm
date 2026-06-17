# 🧠 AI 多态性：稀疏 MoE Transformer

> 一个**入门友好**的深度学习项目，用 Transformer + 混合专家（MoE）技术实现"多态性"语言模型。

---

## 🤔 这是什么？（说人话版）

### 一句话概括

> 同一个模型，面对不同类型的输入文字，会自动激活**不同的"专家"**来处理——就像一个人遇到数学题用左脑、写诗用右脑一样。

### 举个例子

```
输入: "The derivative of the function is..."  → 激活 专家#0（擅长数学）
输入: "Python is a high-level programming..." → 激活 专家#1（擅长编程）
输入: "The history of ancient Rome..."        → 激活 专家#2（擅长人文）
```

**所有专家都在同一个模型里**，但每次只激活一小部分。这就是"多态性"——一个模型，多种形态。

### 核心技术

| 技术 | 通俗解释 |
|------|---------|
| **Transformer** | 当前最主流的 AI 模型架构，ChatGPT 就是用这个 |
| **MoE（混合专家）** | 把一个大模型拆成多个"小专家"，每次只叫醒少数几个，省算力 |
| **稀疏激活** | 不是所有人都干活，只有被选中的专家才计算 |

---

## 🚀 快速开始（3 步跑起来）

### 第 1 步：安装依赖

```bash
# 确保你用的是 conda torch_cuda 环境（这个才有 GPU 支持）
pip install torch datasets
```

> 💡 **提示**：如果你用默认 `python` 命令跑，脚本会自动检测并切换到 GPU 环境，不用手动激活 conda。

### 第 2 步：运行训练

```bash
# 最小配置（推荐！快速验证，不伤电脑）
python main.py --small

# 默认配置（轻量级，适合本地 GPU）
python main.py

# 查看所有可选参数
python main.py --help
```

### 第 3 步：观察结果

训练完成后会自动输出：

- ✅ **训练损失曲线**——看模型有没有在学习
- ✅ **验证困惑度**——数字越小越好
- ✅ **文本生成示例**——模型自己"写"的文字
- ✅ **专家路由分析**——看不同 token 被分配到了哪个专家

---

## 📊 三种运行模式

| 命令 | 参数量 | GPU 显存 | 训练时长 | 适合场景 |
|------|--------|----------|----------|----------|
| `python main.py --small` | **0.4M** | ~0.03 GB | 10 秒 | 🔥 快速验证、避免过热 |
| `python main.py` | **~5M** | ~0.5 GB | 几分钟 | 📝 默认实验 |
| `python main.py --full-moe` | **~8M** | ~1 GB | 十几分钟 | 🔬 深度实验 |

> ⚠️ **你的电脑如果跑太热**，就用 `--small` 模式。之前默认配置太大导致 WiFi/蓝牙掉线，就是因为 GPU 过热。现在已经改小了。

---

## 🧩 自定义参数

不想用默认配置？可以手动调参数：

```bash
# 加大模型
python main.py --d-model 512 --n-layers 6 --n-experts 8 --top-k 2

# 所有层都用 MoE（多态性最强）
python main.py --full-moe

# 不用混合精度（如果 AMP 出问题）
python main.py --no-amp

# 改训练步数
python main.py --max-steps 10000
```

### 常用参数速查

| 参数 | 含义 | 默认值 |
|------|------|--------|
| `--d-model` | 模型"宽度"（隐藏层维度） | 256 |
| `--n-layers` | Transformer 层数 | 4 |
| `--n-heads` | 注意力头数 | 4 |
| `--n-experts` | 专家数量 | 4 |
| `--top-k` | 每个 token 激活几个专家 | 1 |
| `--batch-size` | 一批训练多少样本 | 8 |
| `--max-steps` | 训练多少步 | 2000 |
| `--small` | 最小配置预设 | - |
| `--full-moe` | 所有层都用 MoE | - |

---

## 📁 项目文件结构

```
26_6_17/
├── main.py                 # 🚪 入口文件，从这里开始
├── generate_corpus.py      # 📝 生成训练用的文本数据
├── requirements.txt        # 📦 依赖列表
├── README.md               # 📖 本文件（项目说明）
├── CODE_GUIDE.md           # 📖 代码详解（深入理解用）
│
└── polymoe/                # 🧠 核心代码库
    ├── __init__.py          #   模块入口（懒加载）
    ├── config.py            #   ⚙️ 所有配置参数
    ├── tokenizer.py         #   🔤 分词器（文字→数字）
    ├── expert.py            #   👨‍🔬 单个专家（小 FFN）
    ├── router.py            #   🧭 路由器（决定 token 去哪）
    ├── moe_layer.py         #   🏗️ MoE 层（路由 + 多个专家）
    ├── transformer_block.py #   🧱 Transformer 块（注意力 + FFN）
    ├── model.py             #   🏛️ 完整 GPT 模型
    ├── data.py              #   📊 数据加载
    ├── trainer.py           #   🏋️ 训练器
    └── visualize.py         #   📈 可视化分析
```

---

## 🧪 交互式玩法

不用命令行也能玩，在 Python 里手动操作：

```python
from polymoe import MoEConfig, SimpleTokenizer, GPTMoE, Trainer, analyze_routing
from polymoe.data import TextDataset, load_wikitext

# 1. 创建配置
cfg = MoEConfig(d_model=128, n_layers=2, max_steps=100)

# 2. 加载数据 & 构建分词器
texts = load_wikitext()
tokenizer = SimpleTokenizer().fit(texts)

# 3. 创建模型
model = GPTMoE(cfg)

# 4. 训练几步
trainer = Trainer(model, cfg, tokenizer)
# ...

# 5. 看专家路由
analyze_routing(model, tokenizer, "The neural network learns patterns", cfg)
```

---

## ❓ 常见问题

### Q: 为什么我的 GPU 不工作？

A: 脚本会自动检测。如果显示 `✓ GPU 可用` 就对了。如果显示 `⚠ GPU 不可用`，检查是否安装了 CUDA 版 PyTorch。

### Q: 电脑太热怎么办？

A: 用 `python main.py --small`，0.4M 参数，显存占用不到 0.1GB，基本不发热。

### Q: 生成的文本质量很差？

A: 这是正常的！这是一个**教学项目**，不是 ChatGPT。小模型 + 少数据 + 少训练 = 生成质量有限。目的是展示 MoE 的多态性原理。

### Q: 怎么让模型更好？

A: 调大参数：`python main.py --d-model 512 --n-layers 8 --max-steps 50000`。但需要更多数据和更好的 GPU。

---

## 🔗 延伸阅读

- **Transformer 论文**: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- **MoE 论文**: [Switch Transformers](https://arxiv.org/abs/2101.03961)
- **GPT 论文**: [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)

---

> 📬 有问题？看看 [CODE_GUIDE.md](CODE_GUIDE.md) 了解代码细节。
