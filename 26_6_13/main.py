from typing import Dict

class ListNode:
    """双向链表节点"""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, ListNode] = {} # : Dict[int, ListNode] —— 类型注解（来自 typing），这一段只做类型标注，运行时不生效，用于 IDE 提示、静态检查。
        
        # 哨兵节点，简化边界处理
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 命中，移动到表头（标记为最近使用）
        node = self.cache[key] # 获取节点
        self._move_to_head(node) # 将节点移到表头（标记为最近使用）
        return node.value # 返回节点的值

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # 已存在：更新值 + 移到表头
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # 不存在：创建新节点
            new_node = ListNode(key, value)
            self.cache[key] = new_node # 将新节点加入缓存字典
            self._add_to_head(new_node)
            
            # 超过容量，删除表尾节点（最久未使用）
            if len(self.cache) > self.capacity:
                tail_node = self._remove_tail() # 移除表尾节点（最久未使用）
                del self.cache[tail_node.key] # 从缓存字典中删除对应的键

    def _remove_node(self, node: ListNode):
        """从链表中移除节点"""
        prev_node = node.prev # 获取前一个节点
        next_node = node.next # 获取下一个节点
        prev_node.next = next_node # 将前一个节点的 next 指向下一个节点
        next_node.prev = prev_node # 将下一个节点的 prev 指向前一个节点

    def _add_to_head(self, node: ListNode):
        """将节点添加到表头"""
        node.prev = self.head # 将节点的 prev 指向 head
        node.next = self.head.next # 将节点的 next 指向 head 的下一个节点
        self.head.next.prev = node # 将 head 的下一个节点的 prev 指向新节点
        self.head.next = node # 将 head 的 next 指向新节点

    def _move_to_head(self, node: ListNode): 
        """将节点移到表头（标记为最近使用）"""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> ListNode:
        """移除表尾节点（最久未使用）"""
        tail_node = self.tail.prev # 获取表尾节点（最久未使用的节点）
        self._remove_node(tail_node) # 从链表中移除表尾节点
        return tail_node # 返回被移除的表尾节点（最久未使用的节点）


if __name__ == "__main__":
    # 示例：
    # 输入：["LRUCache","put","put","get","put","get","put","get","get","get"]
    # 参数：[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
    # 输出：[null,null,null,1,null,-1,null,-1,3,4]

    obj = LRUCache(2)
    print("obj = LRUCache(2)")

    obj.put(1, 1)
    print("put(1, 1)")
    obj.put(2, 2)
    print("put(2, 2)")

    print("get(1):", obj.get(1))  # 返回 1
    print("put(3, 3)")
    obj.put(3, 3)  # 淘汰 key=2
    print("get(2):", obj.get(2))  # 返回 -1（被淘汰）
    print("put(4, 4)")
    obj.put(4, 4)  # 淘汰 key=1
    print("get(1):", obj.get(1))  # 返回 -1（被淘汰）
    print("get(3):", obj.get(3))  # 返回 3
    print("get(4):", obj.get(4))  # 返回 4