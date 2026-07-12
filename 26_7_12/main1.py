from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        # 定义上下左右四个边界
        top = 0
        bottom = len(matrix) - 1
        left = 0
        right = len(matrix[0]) - 1

        res = []
        total_num = len(matrix) * len(matrix[0])  # 矩阵总元素个数

        while len(res) < total_num:
            # 1. 从左到右遍历【上边界】一行
            if top <= bottom:
                for j in range(left, right + 1):
                    res.append(matrix[top][j])
                top += 1  # 上边界向下收缩一行

            # 2. 从上到下遍历【右边界】一列
            if left <= right:
                for i in range(top, bottom + 1):
                    res.append(matrix[i][right])
                right -= 1  # 右边界向左收缩一列

            # 3. 从右到左遍历【下边界】一行
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    res.append(matrix[bottom][j])
                bottom -= 1  # 下边界向上收缩一行

            # 4. 从下到上遍历【左边界】一列
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    res.append(matrix[i][left])
                left += 1  # 左边界向右收缩一列
        return res


if __name__ == "__main__":
    sol = Solution()
    # 题目示例1输入矩阵
    mat = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    print("原始矩阵：")
    for line in mat:
        print(line)
    
    result = sol.spiralOrder(mat)
    print("\n顺时针螺旋遍历结果：")
    print(result)