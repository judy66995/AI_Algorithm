from typing import List
import random

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def dist(p):
            return p[0]**2 + p[1]**2

        def quick_select(l, r, k):
            # 随机选基准，避免最坏情况
            pivot_idx = random.randint(l, r)
            points[pivot_idx], points[r] = points[r], points[pivot_idx]
            pivot_dist = dist(points[r])

            # 分区：左边<=pivot，右边>pivot
            i = l
            for j in range(l, r):
                if dist(points[j]) <= pivot_dist:
                    points[i], points[j] = points[j], points[i]
                    i += 1
            points[i], points[r] = points[r], points[i]

            # 递归分区
            if i + 1 == k:
                return points[:k] # 找到前k个
            elif i + 1 < k: # 继续在右边找
                return quick_select(i + 1, r, k)
            else: # 继续在左边找
                return quick_select(l, i - 1, k)

        return quick_select(0, len(points) - 1, k) 

if __name__ == "__main__":
    sol = Solution()
    print(sol.kClosest([[1,3],[-2,2]], 1)) # 输出：[[-2,2]]
    print(sol.kClosest([[3,3],[5,-1],[-2,4]], 2)) # 输出：[[3,3],[-2,4]]（顺序可换）