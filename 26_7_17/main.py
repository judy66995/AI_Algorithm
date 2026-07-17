# 定义单链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 链表合并解法
class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        # 哨兵虚拟头节点，简化边界判断
        dummy = ListNode()
        cur = dummy  # cur用来遍历、拼接新链表
        
        # 两个链表都没遍历完时循环比较
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next  # 当前指针后移
        
        # 剩下没遍历完的链表直接接在尾部
        cur.next = list1 if list1 else list2
        return dummy.next

# 辅助函数：数组转链表，方便测试
def arr_to_link(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    tmp = head
    for num in arr[1:]:
        tmp.next = ListNode(num)
        tmp = tmp.next
    return head

# 辅助函数：链表转数组，打印结果
def link_to_arr(head):
    res = []
    tmp = head
    while tmp:
        res.append(tmp.val)
        tmp = tmp.next
    return res

# 测试示例
if __name__ == "__main__":
    l1 = arr_to_link([1,2,4])
    l2 = arr_to_link([1,3,4])
    sol = Solution()
    merged = sol.mergeTwoLists(l1, l2)
    print(link_to_arr(merged))  # 输出 [1,1,2,3,4,4]