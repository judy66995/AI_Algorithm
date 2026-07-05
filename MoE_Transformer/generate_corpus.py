#!/usr/bin/env python3
"""
生成足够大的训练文本数据集 —— 不依赖外部网络。

通过模板组合生成涵盖数学、编程、科技、生物等多个领域的文本，
足够训练一个 15M 参数的 MoE Transformer。
"""

import random

random.seed(42)


def generate_corpus(min_tokens: int = 80000) -> list[str]:
    """
    生成多领域文本语料库（循环直到满足 min_tokens 词数）。

    每个领域有各自的词汇和句式，训练后不同领域的 token
    会被 Router 路由到不同的 Expert → 展示 AI 多态性。
    """
    texts = []

    # ════════════════════════════════════════════════════════
    # 词库与模板（7 个领域 × 足够多的模板 = 多样性）
    # ════════════════════════════════════════════════════════

    domain_fns = [
        _code_domain,
        _math_domain,
        _ai_domain,
        _science_domain,
        _history_domain,
        _narrative_domain,
        _quotes_domain,
    ]

    def _total_tokens():
        return sum(len(t.split()) for t in texts)

    # 循环生成直到满足词数
    iteration = 0
    while _total_tokens() < min_tokens:
        for fn in domain_fns:
            texts.extend(fn())
        iteration += 1
        if iteration > 200:  # 安全上限
            break

    random.shuffle(texts)
    return texts


def _sample(nouns, verbs, templates, count=50):
    """从词库+模板生成 count 条文本"""
    return [
        random.choice(templates).format(
            noun=random.choice(nouns),
            verb=random.choice(verbs),
        )
        for _ in range(count)
    ]


def _code_domain():
    nouns = [
        "function", "class", "variable", "return", "import", "module",
        "algorithm", "recursion", "loop", "iteration", "condition",
        "boolean", "integer", "string", "array", "dictionary",
        "compiler", "interpreter", "syntax", "debugging", "optimization",
    ]
    verbs = [
        "implements", "executes", "processes", "evaluates", "compiles",
        "validates", "optimizes", "transforms", "allocates", "generates",
    ]
    templates = [
        "The {noun} {verb} the input data and produces the expected output.",
        "In programming, a {noun} is essential for building reliable software.",
        "The {noun} can {verb} complex operations efficiently.",
        "Developers use {noun} to solve computational problems.",
        "A well-designed {noun} {verb} memory and improves performance.",
        "Understanding {noun} is fundamental to computer science.",
        "The {noun} pattern {verb} common programming tasks.",
        "Proper use of {noun} leads to cleaner and more maintainable code.",
        "The {noun} mechanism {verb} data structures effectively.",
        "Learning about {noun} helps programmers write better software.",
        "Modern programming languages include {noun} as a core feature.",
        "The concept of {noun} {verb} how we think about computation.",
        "Advanced {noun} techniques {verb} system reliability.",
        "Every programmer should understand how {noun} works in practice.",
        "The {noun} abstraction {verb} underlying complexity.",
    ]
    return _sample(nouns, verbs, templates, 300)


def _math_domain():
    nouns = [
        "theorem", "equation", "function", "derivative", "integral",
        "matrix", "vector", "polynomial", "probability", "geometry",
        "algebra", "calculus", "topology", "number theory", "set",
        "sequence", "series", "limit", "convergence", "divergence",
    ]
    verbs = [
        "defines", "converges", "diverges", "approximates", "solves",
        "characterizes", "generalizes", "simplifies", "proves", "derives",
    ]
    templates = [
        "In mathematics, the {noun} {verb} a fundamental relationship.",
        "The {noun} can be {verb} using standard techniques.",
        "Mathematicians study {noun} to understand abstract structures.",
        "The concept of {noun} {verb} many important results.",
        "A {noun} is defined as a mapping between sets.",
        "One can {verb} the {noun} using the standard approach.",
        "The {noun} theorem {verb} a deep connection in mathematics.",
        "Understanding {noun} requires familiarity with basic principles.",
        "The theory of {noun} {verb} numerous applications in science.",
        "Proofs involving {noun} often require careful reasoning.",
        "The {noun} plays a central role in modern mathematics.",
        "Using the {noun}, one can {verb} complex problems.",
        "The study of {noun} {verb} our understanding of space.",
        "Advanced courses in mathematics cover {noun} in detail.",
        "The {noun} formula {verb} a concise representation.",
    ]
    return _sample(nouns, verbs, templates, 300)


def _ai_domain():
    nouns = [
        "neural network", "transformer", "attention mechanism", "gradient",
        "loss function", "optimizer", "backpropagation", "activation",
        "layer", "embedding", "token", "training data", "inference",
        "regularization", "dropout", "batch normalization",
        "convolutional network", "recurrent network", "language model",
        "reinforcement learning", "supervised learning", "generator",
        "discriminator", "latent space", "encoder", "decoder",
    ]
    verbs = [
        "learns", "predicts", "classifies", "generates", "optimizes",
        "regularizes", "encodes", "decodes", "transforms", "approximates",
    ]
    templates = [
        "The {noun} {verb} patterns from large datasets.",
        "Training a {noun} requires careful hyperparameter tuning.",
        "The {noun} architecture {verb} input representations efficiently.",
        "Modern AI systems use {noun} for state-of-the-art performance.",
        "The {noun} {verb} features at multiple levels of abstraction.",
        "Researchers developed the {noun} to improve model accuracy.",
        "A well-trained {noun} {verb} complex distributions accurately.",
        "The {noun} paradigm {verb} how machines process information.",
        "Using {noun} reduces overfitting and improves generalization.",
        "The {noun} component {verb} raw data into useful representations.",
        "Advances in {noun} have revolutionized natural language processing.",
        "The {noun} framework {verb} multimodal data effectively.",
        "Implementing {noun} from scratch deepens understanding of AI.",
        "The performance of {noun} depends on the quality of training data.",
        "New research on {noun} {verb} the boundaries of machine learning.",
    ]
    return _sample(nouns, verbs, templates, 300)


def _science_domain():
    nouns = [
        "electron", "molecule", "atom", "protein", "enzyme", "cell",
        "organism", "ecosystem", "gravity", "energy", "radiation",
        "temperature", "pressure", "velocity", "acceleration",
        "wavelength", "frequency", "isotope", "catalyst", "membrane",
        "mitochondria", "chromosome", "mutation", "species", "habitat",
    ]
    verbs = [
        "catalyzes", "transfers", "absorbs", "emits", "regulates",
        "transforms", "synthesizes", "decomposes", "interacts", "evolves",
    ]
    templates = [
        "The {noun} {verb} energy through the system.",
        "Scientists discovered that the {noun} plays a crucial role in metabolism.",
        "The {noun} {verb} signals across the cellular membrane.",
        "Understanding {noun} is essential for modern biology.",
        "The {noun} structure determines its chemical properties.",
        "In physics, {noun} {verb} according to conservation laws.",
        "The {noun} pathway {verb} genetic information into proteins.",
        "Research on {noun} has led to breakthrough treatments.",
        "The {noun} mechanism {verb} homeostasis in living organisms.",
        "Experiments showed that {noun} {verb} under specific conditions.",
        "The discovery of {noun} changed our understanding of nature.",
        "The {noun} process {verb} raw materials into useful products.",
        "Measuring {noun} requires precise laboratory instruments.",
        "The theory of {noun} explains many natural phenomena.",
        "Advanced microscopy revealed the structure of {noun} in detail.",
    ]
    return _sample(nouns, verbs, templates, 300)


def _history_domain():
    nouns = [
        "civilization", "empire", "revolution", "dynasty", "democracy",
        "philosophy", "religion", "economics", "trade", "agriculture",
        "industrialization", "renaissance", "enlightenment", "constitution",
        "treaty", "monarchy", "republic", "culture", "migration",
    ]
    verbs = [
        "transformed", "established", "influenced", "developed", "spread",
        "unified", "divided", "expanded", "declined", "revolutionized",
    ]
    templates = [
        "The {noun} {verb} society in profound ways.",
        "Historians study the {noun} to understand cultural change.",
        "The rise of {noun} {verb} the political landscape.",
        "During this period, {noun} {verb} across the continent.",
        "The concept of {noun} emerged from centuries of philosophical thought.",
        "The {noun} movement {verb} traditional social structures.",
        "Scholars debate the impact of {noun} on modern civilization.",
        "The development of {noun} {verb} economic relationships globally.",
        "Ancient texts describe how {noun} {verb} in early societies.",
        "The legacy of {noun} continues to shape contemporary discourse.",
        "The {noun} era {verb} unprecedented technological progress.",
        "Understanding {noun} provides insight into current global issues.",
        "The principles of {noun} {verb} governance and law.",
        "Cultural exchange through {noun} {verb} artistic expression.",
        "The history of {noun} illustrates the complexity of human progress.",
    ]
    return _sample(nouns, verbs, templates, 300)


def _narrative_domain():
    return [
        "The results demonstrate that the proposed method achieves significant improvements.",
        "Previous work has shown that this approach is effective in practice.",
        "Several experiments were conducted to validate the theoretical findings.",
        "The analysis reveals interesting patterns in the collected data.",
        "Future research should investigate the limitations of current approaches.",
        "Comparative studies indicate that the new model outperforms existing baselines.",
        "A comprehensive evaluation demonstrates the robustness of the proposed algorithm.",
        "The findings suggest potential applications in various domains of study.",
        "Further investigation is needed to fully understand these phenomena.",
        "The methodology can be extended to handle more complex scenarios.",
        "Empirical results confirm the theoretical predictions of the framework.",
        "These observations lead to new questions about the underlying mechanisms.",
        "The proposed solution addresses long-standing challenges in the field.",
        "Systematic analysis reveals the critical factors affecting performance.",
        "The framework provides a foundation for building more sophisticated models.",
        "This paper introduces a novel approach to solving the optimization problem.",
        "Extensive testing demonstrates consistent improvements across all metrics.",
        "The theoretical framework unifies several previously disparate observations.",
        "Practical applications of this research span multiple industries and disciplines.",
        "The results highlight the importance of careful experimental design.",
    ]


def _quotes_domain():
    return [
        "The only true wisdom is in knowing you know nothing.",
        "The unexamined life is not worth living.",
        "I think therefore I am.",
        "Knowledge is power.",
        "The greatest glory in living lies not in never falling but in rising every time we fall.",
        "The way to get started is to quit talking and begin doing.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "In the middle of difficulty lies opportunity.",
        "What we know is a drop what we do not know is an ocean.",
        "Simplicity is the ultimate sophistication.",
        "The important thing is not to stop questioning.",
        "Imagination is more important than knowledge.",
        "The best way to predict the future is to create it.",
        "Science is a way of thinking much more than it is a body of knowledge.",
        "The cosmos is within us we are made of star stuff.",
        "Mathematics is the language in which God has written the universe.",
        "The only source of knowledge is experience.",
        "Time is an illusion.",
        "Everything should be made as simple as possible but not simpler.",
        "The measure of intelligence is the ability to change.",
        "Not everything that counts can be counted and not everything that can be counted counts.",
        "Stay hungry stay foolish.",
        "The purpose of computing is insight not numbers.",
        "First solve the problem then write the code.",
        "Programs must be written for people to read and only incidentally for machines to execute.",
    ]


# ═══════════════════════════════════════════════════════════
# 验证
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    corpus = generate_corpus()
    total_words = sum(len(t.split()) for t in corpus)
    print(f"Generated {len(corpus)} texts, ~{total_words/1000:.0f}K tokens")
    # 打印几个样例
    for t in corpus[:3]:
        print(f"  [{len(t.split())}w] {t[:80]}...")
    for t in corpus[400:403]:
        print(f"  [{len(t.split())}w] {t[:80]}...")
