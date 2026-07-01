from typing import List
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m = len(grid)#行
        n = len(grid[0])#列
        
        #创建一个空的高速双端队列，命名为 q，用来存放网格里腐烂橘子的坐标，保证 BFS 遍历高效不超时。
        #BFS：广度优先搜索 Breadth-First Search， 一层一层向外铺开，先走完当前距离所有节点，再走下一层；
        #对比 DFS（深度优先）：一条路走到黑，再回头走别的分支。
        q = deque()
        fresh = 0
        dirs = [(-1,0), (1,0), (0,-1), (0,1)]
        
        # 初始化：把所有腐烂橘子入队，统计新鲜橘子总数
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1
        time = 0
        
        # 多源BFS逐层扩散
        while q and fresh > 0:
            # 当前层所有腐烂橘子同步扩散
            layer_size = len(q)
            for _ in range(layer_size):
                x, y = q.popleft()
                for dx, dy in dirs:
                    nx = x + dx
                    ny = y + dy
                    # 边界合法且是新鲜橘子
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        fresh -= 1
                        q.append((nx, ny))
            time += 1
        # 还有新鲜橘子剩余返回-1，否则返回扩散时间
        return time if fresh == 0 else -1

if __name__ == "__main__":
    sol = Solution()
    g1 = [
        [2,1,1],
        [1,1,0],
        [0,1,1]
    ]
    print(sol.orangesRotting(g1)) # 4
    g2 = [[2,1,1],[0,1,1],[1,0,1]]
    print(sol.orangesRotting(g2)) # -1
    g3 = [[0,2]]
    print(sol.orangesRotting(g3)) # 0