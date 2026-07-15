# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        # 步骤1：快慢指针找到链表中点
        slow = head
        fast = head

        # 两个条件同时满足时，说明还没有到链表末尾：
        # fast 本身不是空节点；
        # fast 的下一个节点也存在。
        while fast and fast.next:
            slow = slow.next # 慢指针一次走一步
            fast = fast.next.next # 快指针一次走两步
        
        # 步骤2：反转后半段链表
        def reverse(node):
            prev = None
            cur = node
            while cur:
                temp = cur.next
                cur.next = prev
                prev = cur
                cur = temp
            return prev
        
        # 后半段头节点
        second_half = reverse(slow)
        # 保存后半段起点，用于最后恢复链表
        copy_second = second_half
        
        # 步骤3：前后两段逐一对比值
        result = True
        first = head
        while second_half and result: # 只需要遍历后半段即可
            if first.val != second_half.val:
                result = False
            first = first.next
            second_half = second_half.next
        
        # 可选：恢复链表原始结构
        reverse(copy_second)
        return result

# 工具函数：数组转链表
def list_to_link(arr):
    if not arr:
        return None
    dummy = ListNode()
    p = dummy
    for num in arr:
        p.next = ListNode(num)
        p = p.next
    return dummy.next

# 工具函数：链表转数组，方便打印
def link_to_list(head):
    res = []
    p = head
    while p:
        res.append(p.val)
        p = p.next
    return res


if __name__ == "__main__":
    sol = Solution()
    # 测试用例1：回文 [1,2,2,1]
    test1 = list_to_link([1,2,2,1])
    print(f"链表{link_to_list(test1)} 是否回文：{sol.isPalindrome(test1)}")
    
    # 测试用例2：非回文 [1,2]
    test2 = list_to_link([1,2])
    print(f"链表{link_to_list(test2)} 是否回文：{sol.isPalindrome(test2)}")
    
    # 测试用例3：奇数长度回文 [1,2,3,2,1]
    test3 = list_to_link([1,2,3,2,1])
    print(f"链表{link_to_list(test3)} 是否回文：{sol.isPalindrome(test3)}")