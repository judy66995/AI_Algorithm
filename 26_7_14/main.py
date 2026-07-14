from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # 处理空矩阵
        if not matrix or not matrix[0]: # 如果矩阵本身啥都没有，或者矩阵只有空行，直接判定找不到目标，返回 False，避免程序报错。
            return False
        
        m = len(matrix)       # 总行数
        n = len(matrix[0])    # 总列数
        
        # 起点：右上角 第一行最后一列
        row = 0
        col = n - 1
        
        # 循环：指针不越界就持续查找
        while row < m and col >= 0:
            cur = matrix[row][col]
            if cur == target:
                # 找到目标，直接返回True
                return True
            elif cur > target:
                # 当前数字太大，舍弃当前列，左移
                col -= 1
            else:
                # 当前数字太小，舍弃当前行，下移
                row += 1
        # 指针越界，全部搜完没找到
        return False

# 测试用例（直接运行看结果）
if __name__ == "__main__":
    sol = Solution()
    test_matrix = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 13, 20],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]
    # 测试1：存在数字5
    print(sol.searchMatrix(test_matrix, 5))   # 输出 True
    # 测试2：不存在数字200
    print(sol.searchMatrix(test_matrix, 200)) # 输出 False
    # 测试3：边界数字1
    print(sol.searchMatrix(test_matrix, 1))    # 输出 True
    # 测试4：边界数字30
    print(sol.searchMatrix(test_matrix, 30))   # 输出 True
    # 测试5：空矩阵
    print(sol.searchMatrix([], 1))             # 输出 False