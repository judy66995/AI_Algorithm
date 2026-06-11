class TrieNode:
    """前缀树节点"""
    # __slots__ 的作用：强制限定这个类的实例，只能拥有你写在括号里的这些属性，不允许额外新增属性；同时砍掉默认的__dict__，节省内存、提速访问。Python 里每个普通对象默认会有一个 __dict__ 字典，用来动态存对象的属性,但是使用 __slots__ 后，实例就没有了 __dict__，只能通过定义的属性来存储数据，这样可以节省内存和提高访问速度。
    __slots__ = ("children", "is_end_of_word")  # TrieNode 这个类创建出来的对象，只允许有 children 和 is_end_of_word 两个属性，不能再动态加别的属性，并且优化内存占用。
    def __init__(self):
        self.children = [None] * 26 # 存储 26 个小写字母的子节点
        self.is_end_of_word = False


class Trie:
    def __init__(self): # 构造函数
        """初始化前缀树"""
        self.root = TrieNode() # 前缀树的根节点

    def insert(self, word: str) -> None: # 插入单词
        """向前缀树中插入单词"""
        node = self.root # 从根节点开始插入单词
        for char in word:
            index = ord(char) - ord('a') 
            if not node.children[index]: # 如果当前字符对应的子节点不存在，就创建一个新的 TrieNode 作为子节点
                node.children[index] = TrieNode() # 创建一个新的 TrieNode 作为子节点
            node = node.children[index] # 移动到子节点继续插入下一个字符
        node.is_end_of_word = True # 插入完成后，标记当前节点为一个完整单词的结尾

    def search(self, word: str) -> bool:
        """判断单词是否存在（必须是完整单词）"""
        node = self.root
        for char in word:
            index = ord(char) - ord('a')
            if not node.children[index]:
                return False
            node = node.children[index]
        return node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """判断是否存在以 prefix 为前缀的单词"""
        node = self.root
        for char in prefix:
            index = ord(char) - ord('a')
            if not node.children[index]:
                return False
            node = node.children[index]
        return True



if __name__ == "__main__":
    # 对应题目示例：
    # 输入: ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
    # 参数: [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
    # 输出: [null, null, true, false, true, null, true]

    obj = Trie()
    print("obj = Trie()")

    obj.insert("apple")
    print("insert(\"apple\")")

    print("search(\"apple\"):", obj.search("apple"))   # True
    print("search(\"app\"):", obj.search("app"))       # False
    print("startsWith(\"app\"):", obj.startsWith("app")) # True

    obj.insert("app")
    print("insert(\"app\")")

    print("search(\"app\"):", obj.search("app"))       # True