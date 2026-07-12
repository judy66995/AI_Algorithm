from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        原地修改矩阵，不额外开辟完整行列数组，空间复杂度 O(1)
        """
        m = len(matrix)
        n = len(matrix[0])
        # 标记第一行、第一列本身是否存在0
        first_row_has_zero = False
        first_col_has_zero = False

        # 步骤1：检查第一行有没有0
        for j in range(n):
            if matrix[0][j] == 0:
                first_row_has_zero = True
                break
        # 步骤2：检查第一列有没有0
        for i in range(m):
            if matrix[i][0] == 0:
                first_col_has_zero = True
                break
        
        # 步骤3：遍历除去第一行第一列的所有元素，用第一行第一列做标记
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0  # 当前行首置0，标记这一行要清零
                    matrix[0][j] = 0  # 当前列首置0，标记这一列要清零
        
        # 步骤4：根据第一列标记，把对应行全部置0（跳过第一行）
        for i in range(1, m):
            if matrix[i][0] == 0:
                for j in range(n):
                    matrix[i][j] = 0
        # 步骤5：根据第一行标记，把对应列全部置0（跳过第一列）
        for j in range(1, n):
            if matrix[0][j] == 0:
                for i in range(m):
                    matrix[i][j] = 0
        
        # 步骤6：最后处理原本就有0的第一行、第一列
        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0
        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0


if __name__ == "__main__":
    sol = Solution()
    # 示例1输入
    mat = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    print("修改前矩阵：")
    for row in mat:
        print(row)
    
    sol.setZeroes(mat)
    print("\n修改后矩阵：")
    for row in mat:
        print(row)