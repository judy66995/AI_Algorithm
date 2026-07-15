# 定义单链表节点
class ListNode:
    # 参数默认值：不传参时 val=0，next=None。
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 题目要求的反转链表类方法
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        # 双指针迭代法
        prev = None   # 前一个节点，初始为空（反转后链表末尾指向None）
        cur = head    # 当前遍历节点，从头节点开始
        while cur is not None:
            # 1. 先保存下一个节点，防止断链
            temp_next = cur.next
            # 2. 反转当前节点的指针，指向前一个节点
            cur.next = prev
            # 3. 两个指针同步向后移动一位
            prev = cur
            cur = temp_next
        # 循环结束时cur为空，prev就是反转后的头节点
        return prev

# 辅助函数：列表转链表（方便测试输入）
def list_to_link(arr):
    if not arr:
        return None
    dummy = ListNode() # 创建一个虚拟头节点，方便操作
    p = dummy
    for num in arr:
        # ListNode(num)：调用节点类的构造函数，新建一个链表节点对象，
        # 这个节点的 val = num，默认 next = None。
        p.next = ListNode(num)
        p = p.next
    return dummy.next

# 辅助函数：链表转列表（打印输出看结果）
def link_to_list(head):
    res = []
    p = head
    while p:
        res.append(p.val)
        p = p.next
    return res


if __name__ == "__main__":
    sol = Solution()
    # 测试用例1：输入 [1,2,3,4,5]
    input_arr = [1,2,3,4,5]
    head = list_to_link(input_arr)
    reverse_head = sol.reverseList(head)
    print("原链表：", input_arr)
    print("反转后链表：", link_to_list(reverse_head))