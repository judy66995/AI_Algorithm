from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        # 第一步：原地交换，把数字放到对应下标位置
        for i in range(n):
            # 当前数字x满足：1<=x<=n 且 不在正确位置，就循环交换
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                x = nums[i]
                # 交换 nums[i] 和 nums[x-1]
                nums[i], nums[x - 1] = nums[x - 1], nums[i]

        # 第二步：遍历查找第一个不匹配的位置
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        # 1~n全部齐全，答案是n+1
        return n + 1


if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        [1, 2, 0],
        [3, 4, -1, 1],
        [7, 8, 9, 11, 12],
        [2, 1],
        [1]
    ]
    for case in test_cases:
        # 复制数组避免修改原测试数据
        temp = case.copy()
        res = sol.firstMissingPositive(temp)
        print(f"输入数组 {case} → 缺失最小正数：{res}")