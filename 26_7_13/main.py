from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        方法：先转置矩阵，再翻转每一行
        """
        n = len(matrix)
        # 1. 矩阵转置：只遍历上三角，避免重复交换
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # 2. 每一行左右翻转
        for row in matrix:
            row.reverse()


if __name__ == "__main__":
    # 测试用例1 题目示例
    mat1 = [[1,2,3],[4,5,6],[7,8,9]]
    sol = Solution()
    print("原始矩阵：", mat1)
    sol.rotate(mat1)
    print("旋转90度后：", mat1)
    print("-" * 40)

    # 测试用例2 2阶矩阵
    mat2 = [[1,2],[3,4]]
    print("原始矩阵：", mat2)
    sol.rotate(mat2)
    print("旋转90度后：", mat2)