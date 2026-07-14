from typing import Optional

# 链表节点定义
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # Optional来自 typing 模块，它的规则：Optional[X] = Union[X, None]
    # 也就是说，Optional[X]要么是 X 类型，要么是 None。
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        # 双指针p、q分别指向两条链表头
        p, q = headA, headB
        
        # 两个指针不相等就循环移动
        while p != q:
            # 变量 = 真值表达式 if 判断条件 else 假值表达式
            
            # p走到空就切换到B链表头，否则走下一个
            p = p.next if p else headB
            # q走到空就切换到A链表头，否则走下一个
            q = q.next if q else headA
        # 相遇：要么是交点，要么都是None（无交点）
        return p


if __name__ == "__main__":
    # 1. 构建公共相交尾部 c1->c2->c3
    c1 = ListNode(1)
    c2 = ListNode(2)
    c3 = ListNode(3)
    c1.next = c2
    c2.next = c3

    # 链表A：a1 -> a2 -> c1
    a1 = ListNode(10)
    a2 = ListNode(20)
    a1.next = a2
    a2.next = c1

    # 链表B：b1 -> b2 -> b3 -> c1
    b1 = ListNode(100)
    b2 = ListNode(200)
    b3 = ListNode(300)
    b1.next = b2
    b2.next = b3
    b3.next = c1

    sol = Solution()
    intersect_node = sol.getIntersectionNode(a1, b1)
    if intersect_node:
        print(f"相交节点的值为：{intersect_node.val}")  # 输出 1
    else:
        print("无相交节点")

    # 测试无交点案例
    n1 = ListNode(1)
    n2 = ListNode(2)
    res = sol.getIntersectionNode(n1, n2)
    print(f"无交点测试结果：{res}")  # 输出 None