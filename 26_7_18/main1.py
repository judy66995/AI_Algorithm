# 定义链表节点
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
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        # 虚拟头节点，统一处理头部翻转边界
        dummy = ListNode(0, head)
        pre = dummy  # pre：每组翻转区间的前一个节点

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

            # 2. 翻转 [pre.next ~ tail] 这一段k个节点
            cur = pre.next
            prev = next_group_head  # 翻转后的尾部要指向下一组
            
            # cur 是当前正在处理的节点，next\_group\_head是下一组链表的起点
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
            
            # 3. 把翻转后的组接回原链表
            new_group_head = prev  # 翻转后这一组的新头
            old_group_head = pre.next  # 翻转前这一组的头（现在变成尾）
            pre.next = new_group_head  # 前驱节点接上翻转后的新头

            # 4. pre移动到当前组翻转后的尾部，作为下一组的前驱
            pre = old_group_head


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

    # 测试用例2：k=3，[1,2,3,4,5]
    print("=====测试用例2：[1,2,3,4,5], k=3=====")
    head2 = arr_to_link([1,2,3,4,5])
    print("原链表：")
    print_link(head2)
    res2 = sol.reverseKGroup(head2, 3)
    print("翻转后：")
    print_link(res2)
    print("-"*40)

    # 测试用例3：刚好整除 [1,2,3,4], k=2
    print("=====测试用例3：[1,2,3,4], k=2=====")
    head3 = arr_to_link([1,2,3,4])
    print("原链表：")
    print_link(head3)
    res3 = sol.reverseKGroup(head3, 2)
    print("翻转后：")
    print_link(res3)
