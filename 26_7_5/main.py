class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        res = []
        nums.sort() # nums.sort() 是 Python 列表自带的原地排序方法：直接修改原列表 nums，把列表里的数字从小到大升序排列，函数本身没有返回值（返回 None）。
        n = len(nums)
        
        # 固定第一个数 i
        for i in range(n):
            # 第一个数重复，跳过去重
            if i > 0 and nums[i] == nums[i - 1]:
                continue # continue 会直接结束本次外层 for 循环，跳过后面的双指针查找逻辑，直接进入下一轮 i 的循环。
            left = i + 1
            right = n - 1
            target = -nums[i] # 计算目标值 target，目标值是当前固定的第一个数 nums[i] 的相反数，因为我们要找三个数的和为 0，所以剩下两个数的和必须等于 -nums[i]。
            
            while left < right:
                cur_sum = nums[left] + nums[right] # 计算当前 left 和 right 指针指向的两个数的和
                if cur_sum == target:
                    res.append([nums[i], nums[left], nums[right]])
                    # 跳过 left 重复值
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # 跳过 right 重复值
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    # 同时收缩双指针
                    left += 1
                    right -= 1
                elif cur_sum < target:
                    left += 1
                else:
                    right -= 1
        return res



if __name__ == "__main__":
    sol = Solution()
    # 示例1
    nums1 = [-1, 0, 1, 2, -1, -4]
    print(f"输入 {nums1}")
    print(f"输出 {sol.threeSum(nums1)}\n")
    
    # 示例2
    nums2 = [0, 1, 1]
    print(f"输入 {nums2}")
    print(f"输出 {sol.threeSum(nums2)}")