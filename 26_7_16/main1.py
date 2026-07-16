# 定义链表节点
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        # 第一步：快慢指针判断是否有环，找到相遇点
        slow = head
        fast = head
        has_ring = False
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                has_ring = True
                break
        # 无环直接返回None
        if not has_ring:
            return None
        
        # 第二步：一个指针从头，一个从相遇点，同速前进，相遇点就是环入口
        ptr1 = head
        ptr2 = slow
        while ptr1 != ptr2:
            ptr1 = ptr1.next
            ptr2 = ptr2.next
        return ptr1


if __name__ == "__main__":
    # 构建题目示例1链表：3 -> 2 -> 0 -> -4，-4.next = 2，环入口是节点2
    n3 = ListNode(3)
    n2 = ListNode(2)
    n0 = ListNode(0)
    n_neg4 = ListNode(-4)
    n3.next = n2
    n2.next = n0
    n0.next = n_neg4
    n_neg4.next = n2

    sol = Solution()
    entry_node = sol.detectCycle(n3)
    print(f"示例1环入口节点值：{entry_node.val}")  # 输出 2

    # 测试无环链表 1->2->3
    n1 = ListNode(1)
    n2 = ListNode(2)
    n3 = ListNode(3)
    n1.next = n2
    n2.next = n3
    res = sol.detectCycle(n1)
    print(f"无环链表结果：{res}")  # 输出 None

    # 测试单节点自环 5->5
    n5 = ListNode(5)
    n5.next = n5
    entry = sol.detectCycle(n5)
    print(f"自环链表入口值：{entry.val}") # 输出5