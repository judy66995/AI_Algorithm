from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # key:前缀和，value:该前缀和出现次数
        prefix_count = {0: 1}
        pre_sum = 0
        res = 0
        for num in nums:
            pre_sum += num
            # 查找需要的前置前缀和
            target = pre_sum - k
            if target in prefix_count:
                res += prefix_count[target]
            # 更新当前前缀和计数
            prefix_count[pre_sum] = prefix_count.get(pre_sum, 0) + 1
        return res

# 测试用例
if __name__ == "__main__":
    sol = Solution()
    print(sol.subarraySum([1,1,1], 2))   # 输出 2
    print(sol.subarraySum([1,2,3], 3))   # 输出 2
    print(sol.subarraySum([1,-1,0], 0))  # 输出 3