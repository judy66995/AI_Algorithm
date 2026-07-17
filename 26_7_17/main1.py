# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        # 虚拟头节点，方便构建结果链表，不用单独处理第一个节点
        dummy = ListNode()
        cur = dummy  # 工作指针，用来不断追加新节点
        carry = 0    # 进位，初始无进位

        # 只要l1没走完 / l2没走完 / 还有进位，就继续循环
        while l1 or l2 or carry:
            # 取当前位数字，链表为空则取0
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # 本位总和 = 两个数字 + 上一轮进位
            total = val1 + val2 + carry
            # 当前节点数值：总和对10取余
            cur.val = total % 10
            # 更新进位：总和整除10
            # // 在 Python 里叫 整数除法（地板除 / 向下取整除）
            # 作用：两个数字相除，只保留商的整数部分，直接砍掉小数，不四舍五入。
            carry = total // 10

            # 两个链表指针后移
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

            # 如果还有下一位，新建节点，工作指针后移
            if l1 or l2 or carry:
                cur.next = ListNode()
                cur = cur.next
        
        return dummy

# 工具函数：把链表转为列表打印，方便看结果
def print_linked_list(head: ListNode):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    print(res)

# 测试示例1：l1 = [2,4,3]  数字342；l2 = [5,6,4] 数字465，和为807 → [7,0,8]
if __name__ == "__main__":
    # 构建链表 l1: 2 → 4 → 3
    l1 = ListNode(2)
    l1.next = ListNode(4)
    l1.next.next = ListNode(3)

    # 构建链表 l2:5 →6 →4
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)

    sol = Solution()
    result = sol.addTwoNumbers(l1, l2)
    print_linked_list(result)  # 输出 [7, 0, 8]