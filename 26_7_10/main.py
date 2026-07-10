from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # 边界：空数组直接返回
        if not intervals:
            return []
        
        # 1. 按区间左端点从小到大排序
        # key=lambda x: x[0] 表示按每个区间的第一个元素（左端点）排序
        intervals.sort(key=lambda x: x[0])
        res = [intervals[0]]  # 结果列表先存入第一个区间

        # 从第二个区间开始遍历
        for current in intervals[1:]:
            last = res[-1]  # 取出结果里最后一个区间
            # 判断是否重叠：当前区间左端点 <= 上一个区间右端点
            if current[0] <= last[1]:
                # 重叠，合并：更新右端点为两者最大值
                res[-1] = [last[0], max(last[1], current[1])]
            else:
                # 不重叠，直接加入结果
                res.append(current)
        return res


if __name__ == "__main__":
    sol = Solution()
    # 测试样例1
    test1 = [[1,3],[2,6],[8,10],[15,18]]
    print("样例1输入:", test1)
    print("样例1输出:", sol.merge(test1))
    print("-" * 40)
    # 测试样例2
    test2 = [[1,4],[4,5]]
    print("样例2输入:", test2)
    print("样例2输出:", sol.merge(test2))
    print("-" * 40)
    # 测试样例3（乱序区间）
    test3 = [[4,7],[1,4]]
    print("样例3输入:", test3)
    print("样例3输出:", sol.merge(test3))
