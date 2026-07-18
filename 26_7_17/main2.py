# 定义单链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 链表工具函数：数组转链表、链表打印
def arr_to_link(arr):
    dummy = ListNode()
    cur = dummy
    for num in arr:
        cur.next = ListNode(num)
        cur = cur.next
    return dummy.next

def print_link(head):
    res = []
    cur = head
    while cur:
        res.append(str(cur.val))
        cur = cur.next
        # "分隔符".join(字符串列表)
        # 作用：把列表里所有元素用分隔符拼接成一整串字符串。
    print("->".join(res))

# 题目解法：快慢指针 + 虚拟头节点
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # 虚拟头节点，解决删除头节点的边界问题
        dummy = ListNode(0, head)
        fast = dummy
        slow = dummy

        # 快指针先走n步
        for _ in range(n):
            fast = fast.next
        
        # 快慢指针一起走，直到快指针到末尾
        while fast.next:
            fast = fast.next
            slow = slow.next
        
        # slow.next就是要删除的倒数第n个节点
        slow.next = slow.next.next
        return dummy.next

# 测试示例1
if __name__ == "__main__":
    sol = Solution()
    # 输入链表 [1,2,3,4,5]，n=2
    head = arr_to_link([1,2,3,4,5])
    print("原链表：")
    print_link(head)
    new_head = sol.removeNthFromEnd(head, 2)
    print("删除倒数第2个节点后：")
    print_link(new_head)
    