# 定义单链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 工具函数：数组转链表
def arr_to_link(arr):
    dummy = ListNode()
    cur = dummy
    for num in arr:
        cur.next = ListNode(num)
        cur = cur.next
    return dummy.next

# 工具函数：打印链表
def print_link(head):
    res = []
    cur = head
    while cur:
        res.append(str(cur.val))
        cur = cur.next
    print("->".join(res))

class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        # 虚拟头节点，统一处理交换头部节点的边界
        dummy = ListNode(0, head)
        pre = dummy  # pre：每一组交换节点的前一个节点

        # 循环条件：存在一对节点可以交换（当前后面至少2个节点）
        while pre.next and pre.next.next:
            # 取出要交换的两个节点
            a = pre.next        # 第一节点
            b = pre.next.next   # 第二节点

            # 三步交换两个节点
            a.next = b.next   # 1节点指向3，断开和2的连接
            b.next = a        # 2节点指向1，完成两两互换
            pre.next = b      # 上一组的尾节点指向新的头b

            # pre移动到下一组交换节点的前驱（也就是a）
            pre = a
        
        return dummy.next


if __name__ == "__main__":
    sol = Solution()
    # 示例1：[1,2,3,4]
    head1 = arr_to_link([1,2,3,4])
    print("原链表1：")
    print_link(head1)
    res1 = sol.swapPairs(head1)
    print("交换后链表1：")
    print_link(res1)
    print("-"*30)

    # 测试奇数长度 [1,2,3]
    head2 = arr_to_link([1,2,3])
    print("原链表2：")
    print_link(head2)
    res2 = sol.swapPairs(head2)
    print("交换后链表2：")
    print_link(res2)
    print("-"*30)

    # 测试单节点 [1]
    head3 = arr_to_link([1])
    print("原链表3：")
    print_link(head3)
    res3 = sol.swapPairs(head3)
    print("交换后链表3：")
    print_link(res3)