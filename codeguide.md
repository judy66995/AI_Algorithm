# K个一组翻转链表 — 逐行代码详解

> 源文件：[26_7_18/main1.py](26_7_18/main1.py)
>
> 题目来源：LeetCode 25. Reverse Nodes in k-Group
>
> 核心算法：链表分组翻转

---

## 第一部分：链表数据结构定义（第1-5行）

```python
# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 1 | `# 定义链表节点` | 注释，说明接下来定义链表节点类。 |
| 2 | `class ListNode:` | 定义一个名为 `ListNode` 的类，这是链表的基本组成单元。每个节点包含两个信息：值和指向下一个节点的指针。 |
| 3 | `def __init__(self, val=0, next=None):` | 构造函数（初始化方法）。`self` 指向实例本身；`val=0` 表示节点值默认为0；`next=None` 表示默认不指向任何下一个节点（即当前节点是最后一个节点时，`next` 就是 `None`）。 |
| 4 | `self.val = val` | 把传入的 `val` 赋值给实例的 `val` 属性，用于存储当前节点的数值。例如 `ListNode(5)` 会创建一个值为5的节点。`self.val` 的 `self` 前缀表示这个属性属于当前实例——每个链表节点都有自己独立的 `val`，互不干扰。 |
| 5 | `self.next = next` | 把传入的 `next` 赋值给实例的 `next` 属性。`self.next` 是一个指针/引用，指向这个节点的下一个 `ListNode` 对象。如果 `next=None`（默认值），表示当前节点后面没有节点了（链表末尾）。 |

**数据结构示意图：**

```
链表: 1 → 2 → 3 → None

节点1: val=1, next→节点2
节点2: val=2, next→节点3
节点3: val=3, next→None
```

---

## 第二部分：工具函数（第7-23行）

### 2.1 数组转链表 `arr_to_link`（第8-14行）

```python
# 工具函数：数组转链表
def arr_to_link(arr):
    dummy = ListNode()
    cur = dummy
    for num in arr:
        cur.next = ListNode(num)
        cur = cur.next
    return dummy.next
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 8 | `def arr_to_link(arr):` | 定义函数 `arr_to_link`，接收一个 Python 列表 `arr`（如 `[1,2,3,4,5]`），返回对应链表的头节点。方便测试时快速构造链表。 |
| 9 | `dummy = ListNode()` | 创建一个**虚拟头节点**（哨兵节点）。`ListNode()` 调用无参构造函数，所以 `dummy.val=0`，`dummy.next=None`。这个节点**不存储业务数据**，它的唯一作用是作为链表的"起点前的一个占位"，让后续的插入逻辑统一——无论链表是否为空，始终有一个 `dummy` 在头上，这样添加第一个真实节点时不需要特殊判断"链表是不是空的"。 |
| 10 | `cur = dummy` | `cur` 是**当前指针**，初始化指向 `dummy`。`cur` 始终指向**当前已构造好的最后一个节点**。每次追加新节点时，我们从 `cur` 的位置往后挂，然后 `cur` 后移。初始时已构造好的"最后一个节点"就是 `dummy` 本身。 |
| 11 | `for num in arr:` | 遍历输入数组的每一个元素。例如 `[1,2,3,4,5]` 会依次取出 `1, 2, 3, 4, 5`。 |
| 12 | `cur.next = ListNode(num)` | **创建新节点并挂到当前链表尾部**。`ListNode(num)` 用当前数组元素值创建一个新节点（`next` 默认 `None`）。然后将 `cur.next` 指向这个新节点，即把新节点接到 `cur`（当前最后一个节点）的后面。 |
| 13 | `cur = cur.next` | **指针后移**。`cur` 现在移动到刚刚创建的新节点上，这样下一轮循环又可以把新节点挂到它后面。`cur` 始终保持在"链表当前最后一个节点"的位置。 |
| 14 | `return dummy.next` | 返回链表的**真正头节点**。`dummy` 是虚拟节点（值为0的占位节点），`dummy.next` 才是第一个真实数据节点的引用。调用者拿到的是 `[1,2,3,4,5]` 对应链表的头节点，感知不到 `dummy` 的存在。 |

**执行过程模拟（输入 `[1,2,3]`）：**

```
初始: dummy(0) → None
          ↑
         cur

第1轮 (num=1):
  cur.next = ListNode(1)  →  dummy(0) → (1) → None
  cur = cur.next          →               ↑
                                          cur

第2轮 (num=2):
  cur.next = ListNode(2)  →  dummy(0) → (1) → (2) → None
  cur = cur.next          →                      ↑
                                                 cur

第3轮 (num=3):
  cur.next = ListNode(3)  →  dummy(0) → (1) → (2) → (3) → None
  cur = cur.next          →                             ↑
                                                        cur

return dummy.next  →  (1) → (2) → (3) → None   ✅
```

### 2.2 打印链表 `print_link`（第17-23行）

```python
# 工具函数：打印链表
def print_link(head):
    res = []
    cur = head
    while cur:
        res.append(str(cur.val))
        cur = cur.next
    print("->".join(res))
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 17 | `def print_link(head):` | 定义函数 `print_link`，接收链表头节点 `head`，将链表以 `值1->值2->值3` 的格式打印到控制台。 |
| 18 | `res = []` | 创建一个空列表 `res`，用于临时存储每个节点值的**字符串形式**。为什么用字符串？因为最后要用 `"->"` 做 join 拼接，而 `join` 要求列表元素都是字符串。 |
| 19 | `cur = head` | `cur` 是**遍历指针**，初始指向头节点。`cur` 在遍历过程中不断后移，用于访问链表中的每一个节点。 |
| 20 | `while cur:` | 循环条件：`cur` 不为 `None`。当 `cur` 走到链表末尾时，`cur.next` 是 `None`，下一轮 `cur` 变成 `None`，循环结束。这是一个**哨兵循环**——Python 中 `None` 是 falsy 的，所以 `while cur` 等价于 `while cur is not None`。 |
| 21 | `res.append(str(cur.val))` | 取出当前节点的值 `cur.val`，用 `str()` 转成字符串，追加到 `res` 列表中。例如节点值为 `1`，则 `res` 变为 `["1"]`。 |
| 22 | `cur = cur.next` | **指针后移**。将 `cur` 更新为当前节点的下一个节点。这是链表遍历的核心操作——通过 `.next` 引用沿着链表一步一步前进。如果 `cur.next` 是 `None`，说明到了末尾，下一轮循环条件为假，循环结束。 |
| 23 | `print("->".join(res))` | 用 `"->"` 将 `res` 中的所有字符串连接起来并打印。例如 `res = ["1","2","3","4","5"]`，则输出 `1->2->3->4->5`。 |

---

## 第三部分：核心算法 — Solution 类（第25-65行）

### 3.1 方法签名和初始化（第26-29行）

```python
class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        # 虚拟头节点，统一处理头部翻转边界
        dummy = ListNode(0, head)
        pre = dummy  # pre：每组翻转区间的前一个节点
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 25 | `class Solution:` | 定义 `Solution` 类。LeetCode 风格——算法逻辑封装在类的实例方法中。 |
| 26 | `def reverseKGroup(self, head: ListNode, k: int) -> ListNode:` | 定义核心方法 `reverseKGroup`。参数：`self` 指向实例；`head` 是链表的头节点（`ListNode` 类型）；`k` 是每组要翻转的节点个数（`int` 类型）。返回类型标注为 `ListNode`，即返回翻转后新链表的头节点。 |
| 28 | `dummy = ListNode(0, head)` | 创建虚拟头节点。`ListNode(0, head)` 的含义：创建一个值为0的节点，它的 `next` 直接指向原链表的 `head`。**为什么需要 dummy？** 因为翻转可能从链表头部就开始，头节点会变化。有了 `dummy`，无论头部怎么翻转，`dummy.next` 始终能正确定位到新链表的头，我们最后返回 `dummy.next` 即可。 |
| 29 | `pre = dummy` | `pre` 是**每组翻转区间的前驱节点**。初始化时，还没有处理任何组，所以 `pre` 指向 `dummy` 这个虚拟头节点。每翻完一组后，`pre` 会移动到**已翻转组的尾部**（也就是下一组的前驱）。 |

**初始化状态示意图（输入 `[1,2,3,4,5]`, k=2）：**

```
dummy(0) → (1) → (2) → (3) → (4) → (5) → None
   ↑
  pre
```

### 3.2 主循环 — 寻找分组边界（第31-41行）

```python
        while True:
            # 1. 找到当前组的末尾tail，判断是否还有k个节点
            tail = pre
            for _ in range(k):
                tail = tail.next
                # 不足k个节点，直接结束循环，剩余节点不翻转
                if not tail:
                    return dummy.next
            
            # 保存下一组的开头，翻转完当前组要接上
            next_group_head = tail.next
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 31 | `while True:` | 无限循环。会在两种情况下退出：(1) 剩余节点不足k个时，通过 `return dummy.next` 退出；(2) 正常处理完所有完整分组后，在下一轮判断不足k个时退出。**为什么用 `while True` 而不是 `while <条件>`？** 因为退出条件需要在循环体**中间**检查（走了k步后才知道够不够），用 `while True` + 内部 `return` 是最清晰的写法。 |
| 33 | `tail = pre` | `tail` 是一个**探路指针**，初始化为 `pre`。它要从 `pre` 开始，向前走k步，看看能不能走到第k个节点。如果能走到，说明还有完整的一组可以翻转；走不到（中间遇到 `None`），说明剩下的不足k个。 |
| 34 | `for _ in range(k):` | 执行k次循环。`_` 是一个约定俗成的变量名，表示"我不关心这个循环变量的具体值，我只关心循环次数"。这里就是要让 `tail` 前进恰好k步。 |
| 35 | `tail = tail.next` | 每次循环 `tail` 向后移动一步。`tail.next` 指向当前节点的下一个节点。 |
| 37 | `if not tail:` | **不足k个节点的检测**。如果 `tail` 在移动k步的过程中变成了 `None`（即 `not tail` 为 `True`），说明链表剩余节点不够k个。`not tail` 等价于 `tail is None`——Python 中 `None` 是 falsy 值，`not None` 为 `True`。 |
| 38 | `return dummy.next` | 不足k个节点时，**直接返回整个链表**（通过 `dummy.next`）。此时剩余节点保持原顺序，不做翻转。这是算法的终止条件，也是唯一返回出口。 |
| 41 | `next_group_head = tail.next` | 走到这里说明凑齐了k个节点，`tail` 指向当前组的**最后一个节点**。`tail.next` 就是**下一组的第一个节点**（可能是 `None`，表示没有下一组了）。保存这个引用是为了**翻转过程中不会丢失下一组的入口**——翻转时节点的 `next` 指针会被改写，如果不提前保存下一组的头，翻转完就找不到后续链表了。 |

**k=2时的一次分组边界查找过程：**

```
操作前:
dummy(0) → (1) → (2) → (3) → (4) → (5) → None
   ↑
  pre

tail = pre  →  tail在dummy

第1步 (k=1):  tail=tail.next → tail在(1)
第2步 (k=2):  tail=tail.next → tail在(2)

凑齐k=2个节点! ✅
next_group_head = tail.next = (3)  ← 保存下一组入口
```

### 3.3 翻转区间链表（第43-57行）— 核心中的核心

```python
            # 2. 翻转 [pre.next ~ tail] 这一段k个节点
            cur = pre.next
            prev = next_group_head  # 翻转后的尾部要指向下一组
            
            # cur 是当前正在处理的节点，next_group_head 是下一组链表的起点
            # 只要cur还没走到下一组起点，说明本组还有节点没翻转，继续循环
            while cur != next_group_head: 
                # 临时保存cur原本的下一个节点，防止修改cur.next后丢失后续链表
                temp = cur.next
                # 反转指针：让当前节点指向前一个已经翻转完成的节点
                cur.next = prev
                # 更新prev，prev现在变成当前节点，作为下一个节点的前驱
                prev = cur
                # cur前进到之前缓存好的下一个待处理节点，继续翻转
                cur = temp
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 44 | `cur = pre.next` | `cur` 是**当前待翻转的节点**。初始化为 `pre.next`，即当前组的第一个节点（翻转前就是组头）。例如第一组 k=2 时，`pre` 在 dummy，`pre.next` 就是节点(1)。 |
| 45 | `prev = next_group_head` | `prev` 是**已经翻转完成部分的链表头**。初始化为 `next_group_head`（下一组的第一个节点）。**为什么初始值是下一组头？** 因为翻转后，原来这组的最后一个节点（现在是翻转后的第一个节点，也就是组头）的 `next` 需要指向下一组。让 `prev` 一开始就是 `next_group_head`，翻转过程中每一轮 `cur.next = prev` 自然就把组尾连到了下一组头。这是链表翻转的经典技巧——相当于把下一组的头当作"已翻转链表"的初始部分。 |
| 49 | `while cur != next_group_head:` | 循环条件：`cur` 还没走到 `next_group_head`。因为翻转范围是 `[pre.next, tail]` 这k个节点，而 `tail.next == next_group_head`，所以当 `cur` 走到 `next_group_head` 时，说明本组的k个节点已经全部处理完毕，循环结束。**如果 `next_group_head` 是 `None`，这个判断同样正确**——`cur` 会在处理完k个节点后变成 `None`。 |
| 51 | `temp = cur.next` | **关键：缓存下一个节点**。因为下一步（第53行）要修改 `cur.next` 的指向（从指向下一个改为指向前一个），如果不先保存原 `cur.next`，就会丢失对后续链表的引用。`temp`（temporary，"临时的"）保存了 `cur` 原来指向的下一个节点。 |
| 53 | `cur.next = prev` | **反转指针！** 把当前节点的 `next` 指针从原来指向"后面"改为指向"前面"（即 `prev`，已翻转部分）。例如：翻转前 `1→2→3`，处理节点1时 `cur.next = prev(=下一组头)` 变成 `1→下一组头`，下一轮处理节点2时 `cur.next = prev(=节点1)` 变成 `2→1→下一组头`。 |
| 55 | `prev = cur` | **更新已翻转链表的头**。`cur` 刚刚已经完成了指针反转，现在它成为"已翻转部分"的最新头部节点。把 `prev` 指向 `cur`，这样下一轮别的节点再翻转时，`cur.next = prev` 就能正确接到这个新的头。 |
| 57 | `cur = temp` | **cur 前进**。`cur` 跳到之前缓存的下一个节点（`temp`），继续处理下一个待翻转节点。**不能写 `cur = cur.next`！** 因为在第53行 `cur.next` 已经被改写了（指向了 `prev` 而不是原来的下一个），所以必须用缓存好的 `temp`。 |

**翻转过程完整模拟（第一组 `[1,2]`, k=2, 下一组头=3）：**

```
初始状态:
pre → dummy(0) → (1) → (2) → (3) → (4) → (5) → None
                             ↑
                      next_group_head

待翻转: pre.next=1 到 tail=2
cur = 1
prev = next_group_head = 3

═══════════════════════════════════════
第1轮循环 (cur=1, cur≠next_group_head=3):
═══════════════════════════════════════
  temp = cur.next = 2          ——缓存 (2)，防止丢失
  cur.next = prev = 3          ——(1) 的next改为指向 (3)
  prev = cur = 1               ——prev 更新为 (1)
  cur = temp = 2               ——cur 前进到 (2)

  当前状态:
  dummy(0) → (1) → (3) → (4) → (5) → None
             (2) → ?
  已翻转: prev=(1)
  待处理: cur=(2)

═══════════════════════════════════════
第2轮循环 (cur=2, cur≠next_group_head=3):
═══════════════════════════════════════
  temp = cur.next = 3          ——缓存 (3)，防止丢失
  cur.next = prev = 1          ——(2) 的next改为指向 (1)
  prev = cur = 2               ——prev 更新为 (2)
  cur = temp = 3               ——cur 前进到 (3)

  当前状态:
  (2) → (1) → (3) → (4) → (5) → None
  已翻转: prev=(2)
  cur=(3) == next_group_head → 循环结束! ✅
```

### 3.4 重新接入原链表（第59-65行）

```python
            # 3. 把翻转后的组接回原链表
            new_group_head = prev  # 翻转后这一组的新头
            old_group_head = pre.next  # 翻转前这一组的头（现在变成尾）
            pre.next = new_group_head  # 前驱节点接上翻转后的新头

            # 4. pre移动到当前组翻转后的尾部，作为下一组的前驱
            pre = old_group_head
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 60 | `new_group_head = prev` | `prev` 在翻转循环结束后，指向的是翻转后的新组头（原组的最后一个节点）。例如上面翻完 `[1,2]` 后，`prev=(2)`，新组头就是节点(2)。这个变量让代码更有可读性，明确表达"这是翻转后的组头"。 |
| 61 | `old_group_head = pre.next` | `pre.next` 在翻转**前**指向的是原组的第一个节点（节点1）。翻转完成后，节点1还在原来的内存位置，但它的 `next` 已经被改成了指向下一组头。所以 `old_group_head = pre.next` 得到的就是**翻转后的组尾**（原组头）。这个变量名说明它在翻转前的身份：旧组头。 |
| 62 | `pre.next = new_group_head` | **把前驱节点和翻转后的新组头连上**。`pre` 是当前组的前一个节点，`pre.next = new_group_head` 就是把前驱的 `next` 指针指向翻转后的新组头，让当前组正确接入链表。**如果没有这行，`pre` 还指着旧组头，链表就断了！** |
| 65 | `pre = old_group_head` | **准备下一轮**。将 `pre` 移动到当前组的尾部（即 `old_group_head`，翻转后变成组尾），这样 `pre` 就成为下一组的前驱节点。下一轮循环时，`tail` 从新的 `pre` 出发，找下一组k个节点。 |

**接入过程示意图（承接上一步翻转结果）：**

```
翻转前:  dummy(0) → (1) → (2) → (3) → (4) → (5) → None
翻转后:  dummy(0) → (1)→(3)    (2) → (1) → (3) → (4) → (5) → None
                    ↑断开!    ↑新组头        ↑

修复:
  new_group_head = prev = (2)
  old_group_head = pre.next = (1)  —— 注意 pre.next 还是指向 (1)
  pre.next = new_group_head  →  dummy(0) → (2) → (1) → (3) → (4) → (5) → None
  pre = old_group_head = (1) —— pre 移到组尾

下一轮:
                  dummy(0) → (2) → (1) → (3) → (4) → (5) → None
                                               ↑
                                              pre (下一组前驱)
```

---

## 第四部分：测试代码（第68-97行）

```python
if __name__ == "__main__":
    sol = Solution()
    # 示例1：输入 [1,2,3,4,5], k=2
    print("=====测试用例1：[1,2,3,4,5], k=2=====")
    head1 = arr_to_link([1,2,3,4,5])
    print("原链表：")
    print_link(head1)
    res1 = sol.reverseKGroup(head1, 2)
    print("翻转后：")
    print_link(res1)
    print("-"*40)
    
    # ... (测试用例2、3类似)
```

| 行号 | 代码 | 作用详解 |
|------|------|----------|
| 68 | `if __name__ == "__main__":` | Python 惯用法。当这个 `.py` 文件被**直接运行**时（`python main1.py`），`__name__` 变量的值为 `"__main__"`，条件成立，执行测试代码。当这个文件被**作为模块导入**时（`import main1`），`__name__` 是模块名 `"main1"`，条件不成立，测试代码不会执行。这是一种良好的代码组织方式。 |
| 69 | `sol = Solution()` | 创建 `Solution` 类的实例对象 `sol`。`Solution` 类没有自定义 `__init__`，所以使用父类 `object` 的默认构造函数，不执行任何特殊初始化。 |
| 72 | `head1 = arr_to_link([1,2,3,4,5])` | 调用工具函数将数组 `[1,2,3,4,5]` 转换为链表，返回头节点赋值给 `head1`。 |
| 73-74 | `print("原链表：")` / `print_link(head1)` | 打印提示信息和原链表内容，输出 `1->2->3->4->5`。 |
| 75 | `res1 = sol.reverseKGroup(head1, 2)` | 调用核心算法，每2个节点一组翻转。返回翻转后的新链表头节点。 |
| 76-77 | `print("翻转后：")` / `print_link(res1)` | 打印翻转后的链表，预期输出 `2->1->4->3->5`。 |
| 78 | `print("-"*40)` | `"-"` 是一个字符串，`*40` 表示重复40次，输出 `----------------------------------------` 作为分隔线。 |

---

## 测试用例预期结果

| 测试用例 | 输入 | k | 翻转过程 | 预期输出 |
|----------|------|---|----------|----------|
| 1 | `[1,2,3,4,5]` | 2 | 第1组 `[1,2]→[2,1]`，第2组 `[3,4]→[4,3]`，剩 `[5]` 不变 | `2->1->4->3->5` |
| 2 | `[1,2,3,4,5]` | 3 | 第1组 `[1,2,3]→[3,2,1]`，剩 `[4,5]` 不变（不足3个） | `3->2->1->4->5` |
| 3 | `[1,2,3,4]` | 2 | 第1组 `[1,2]→[2,1]`，第2组 `[3,4]→[4,3]`，刚好整除 | `2->1->4->3` |

---

## 变量速查表

| 变量名 | 类型 | 作用 | 生命周期 |
|--------|------|------|----------|
| `dummy` | `ListNode` | 虚拟头节点，统一边界处理，`dummy.next` 始终指向结果链表头 | 整个 `reverseKGroup` 方法 |
| `pre` | `ListNode` | 当前待翻转组的前驱节点（即前一组的最后一个节点） | 整个 `reverseKGroup` 方法，每次翻完一组后更新 |
| `tail` | `ListNode` | 探路指针，从 `pre` 出发前进k步，检测是否凑齐k个节点 | 每次外层循环重新赋值 |
| `next_group_head` | `ListNode` | 下一组链表的头节点引用（用于翻转时临时保存接入点） | 每次外层循环重新赋值 |
| `cur` | `ListNode` | 当前正在翻转的节点 | 每次外层循环的翻转内层循环 |
| `prev` | `ListNode` | 已翻转部分的链表头 | 每次外层循环的翻转内层循环 |
| `temp` | `ListNode` | 临时缓存 `cur.next`，防止翻转时丢失后续链表 | 每次翻转内层循环迭代重新赋值 |
| `new_group_head` | `ListNode` | 翻转后的组头（便于理解代码语义） | 每次外层循环重新赋值 |
| `old_group_head` | `ListNode` | 翻转前的组头 / 翻转后的组尾（便于理解代码语义） | 每次外层循环重新赋值 |

---

## 算法复杂度

- **时间复杂度**：O(n)，其中 n 是链表节点总数。每个节点恰好被访问两次——一次是 `tail` 探路时经过，一次是翻转时处理。
- **空间复杂度**：O(1)，只使用了常数个额外指针变量（`dummy`, `pre`, `tail`, `cur`, `prev`, `temp` 等），没有使用额外的数据结构，是原地翻转。
