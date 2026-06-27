from typing import List

class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m = len(grid) # 行数
        n = len(grid[0]) # 列数
        # 上下左右四个移动方向
        dirs = [(-1,0), (1,0), (0,-1), (0,1)]

        def dfs(i, j):
            '''
            dfs(当前陆地)
            1. 先判断：出格/是海 → 直接退出
            2. 没出格且是陆地 → 把自己改成海（标记处理完毕）
            3. 上下左右四个邻居挨个调用dfs
            邻居如果也是陆地，重复上面整套流程
            '''
            # 越界 或 当前是海洋，直接返回
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
                return
            # 把边界连通陆地淹成海洋，标记访问过
            grid[i][j] = 0 
            for dx, dy in dirs:
                dfs(i + dx, j + dy)

        # 第一步：遍历四条边界，把所有和边界相连的陆地全部淹没
        # 第一行、最后一行
        for j in range(n):# 遍历所有列
            dfs(0, j) # 第一行
            dfs(m - 1, j) # 最后一行
        # 第一列、最后一列（跳过首尾两行已遍历）
        for i in range(1, m - 1):
            dfs(i, 0) # 第一列
            dfs(i, n - 1) # 最后一列
        
        # 第二步：统计剩下所有陆地，就是飞地数量
        res = 0
        for i in range(m): # 遍历所有行
            for j in range(n): # 遍历所有列
                if grid[i][j] == 1:
                    res += 1
        return res


if __name__ == "__main__":
    sol = Solution()
    g1 = [
        [0,0,0,0],
        [1,0,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ]
    print(sol.numEnclaves(g1)) # 3