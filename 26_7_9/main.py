from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # 动态规划 / 卡登斯算法(Kadane)核心逻辑
        # current：以当前数字结尾的最大连续子数组和
        # max_total：全局所有子数组的最大和
        current = max_total = nums[0]
        
        # 列表切片通用格式：列表[start : end : step]
        # start：起始下标（包含），省略默认 0
        # end：结束下标（不包含），省略默认到列表末尾
        # step：步长，省略默认 1
        
        # nums[1:] 拆解
        # start=1：从下标为 1 的元素开始取
        # end 省略：一直取到列表最后一个元素
        # 等价含义：跳过第 0 个元素，取数组剩下所有元素

        # 从第二个元素开始遍历
        for num in nums[1:]:
            # 两种选择：要么把当前数接在前面子数组后面，要么单独以当前数作为新子数组起点
            current = max(num, current + num)
            # 更新全局最大值
            max_total = max(max_total, current)
        return max_total


if __name__ == "__main__":
    sol = Solution()
    test1 = [-2,1,-3,4,-1,2,1,-5,4]
    test2 = [1]
    test3 = [5,4,-1,7,8]
    print(f"测试1输出：{sol.maxSubArray(test1)}") # 预期6
    print(f"测试2输出：{sol.maxSubArray(test2)}") # 预期1
    print(f"测试3输出：{sol.maxSubArray(test3)}") # 预期23