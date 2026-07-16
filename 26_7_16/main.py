# 链表节点定义
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        # 快慢指针：慢指针一次走1步，快指针一次走2步
        slow = head
        fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            # 快慢相遇，说明有环
            if slow == fast:
                return True
        # 快指针走到末尾空节点，无环
        return False


if __name__ == "__main__":
    # 构建链表 3 -> 2 -> 0 -> -4 ，-4.next = 2
    node3 = ListNode(3)
    node2 = ListNode(2)
    node0 = ListNode(0)
    node_neg4 = ListNode(-4)
    node3.next = node2
    node2.next = node0
    node0.next = node_neg4
    node_neg4.next = node2  # 尾节点指向node2，形成环

    sol = Solution()
    print("示例1链表是否有环：", sol.hasCycle(node3))  # 输出 True

    # 构建无环链表 1->2->3
    n1 = ListNode(1)
    n2 = ListNode(2)
    n3 = ListNode(3)
    n1.next = n2
    n2.next = n3
    print("无环链表是否有环：", sol.hasCycle(n1)) # 输出 False