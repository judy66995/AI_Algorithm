from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n  # 初始化结果数组，全部为1
        
        # 第一趟：左到右，计算前缀积存入res
        left_product = 1 # 初始化前缀积为1
        for i in range(n): # 遍历数组
            res[i] = left_product # 将当前的前缀积存入结果数组
            left_product *= nums[i] # 更新前缀积为当前元素的乘积
        
        # 第二趟：右到左，计算后缀积，直接乘进res
        right_product = 1 # 初始化后缀积为1
        # range(起始值, 终止值, 步长),规则：包含起始值，不包含终止值，循环到离终止值前一个数就停下。
        for i in range(n-1, -1, -1): # 从n-1到0，步长为-1  
            res[i] *= right_product # 将当前的后缀积乘进结果数组
            right_product *= nums[i] # 更新后缀积为当前元素的乘积
        return res


if __name__ == "__main__":
    sol = Solution()
    # 测试用例1
    nums1 = [1,2,3,4]
    print(f"输入 {nums1}，输出：{sol.productExceptSelf(nums1)}")
    # 测试用例2（含0）
    nums2 = [-1,1,0,-3,3]
    print(f"输入 {nums2}，输出：{sol.productExceptSelf(nums2)}")