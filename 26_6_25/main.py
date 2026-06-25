from typing import List
import heapq
from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 1. 哈希统计频次
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1
        
        heap = []
        # 2. 遍历所有数字，维护大小为k的小顶堆
        for num, count in freq.items():
            heapq.heappush(heap, (count, num))
            # 堆超过k个元素，弹出最小频率的元素
            if len(heap) > k:
                heapq.heappop(heap)
        
        # 3. 提取堆内数字
        res = [item[1] for item in heap]
        return res


if __name__ == "__main__":
    sol = Solution()
    print(sol.topKFrequent([1,1,1,2,2,3], 2)) # [2,1] 顺序不影响结果
    print(sol.topKFrequent([1], 1)) # [1]
    print(sol.topKFrequent([4,1,-1,2,-1,2,3], 2)) # [-1,2]