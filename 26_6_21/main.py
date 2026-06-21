from typing import List # 输入列表和窗口大小，输出每个窗口的最大值列表
from collections import deque # 双端队列：存储下标，对应数值单调递减

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 双端队列：存储下标，对应数值单调递减
        q = deque() # 存储下标，队列头部对应当前窗口的最大值，队列尾部对应当前窗口的最小值
        res = [] # 结果列表：存储每个窗口的最大值
        for idx, val in enumerate(nums):
            # 1. 维护单调递减：队尾小于等于当前值全部弹出
            while q and nums[q[-1]] <= val: # 当前值大于等于队尾对应的数值，弹出队尾
                q.pop()# 弹出队尾下标，继续比较新的队尾下标对应的数值，直到队尾对应的数值大于当前值或者队列为空
            q.append(idx)# 将当前下标添加到队列尾部，当前值对应的数值大于等于之前的数值，保持单调递减

            # 2. 弹出滑出窗口的队首（窗口左边界：idx - k + 1）
            while q[0] <= idx - k:
                q.popleft()# 弹出队首下标，继续比较新的队首下标，直到队首下标在当前窗口范围内

            # 3. 窗口长度达到k，记录最大值
            if idx >= k - 1:
                res.append(nums[q[0]]) # 队首下标对应的数值是当前窗口的最大值，添加到结果列表中
        return res

if __name__ == "__main__":
    sol = Solution()
    print(sol.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3)) # [3,3,5,5,6,7]
    print(sol.maxSlidingWindow([1], 1)) # [1]