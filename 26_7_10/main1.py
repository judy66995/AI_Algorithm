from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        # 关键优化：轮转 n 次等于没转，取模消除多余循环
        k = k % n
        
        # 定义局部反转函数：反转数组 [left, right] 闭区间
        def reverse(arr, left, right):
            while left < right:
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
                right -= 1

        # 三步反转核心逻辑
        # 1. 整体全部反转
        reverse(nums, 0, n - 1)
        # 2. 反转前 k 个元素
        reverse(nums, 0, k - 1)
        # 3. 反转后面剩下 n-k 个元素
        reverse(nums, k, n - 1)


if __name__ == "__main__":
    sol = Solution()

    # 测试样例1
    nums1 = [1,2,3,4,5,6,7]
    k1 = 3
    sol.rotate(nums1, k1)
    print(f"样例1结果：{nums1}")
    print("-" * 40)

    # 测试样例2
    nums2 = [-1,-100,3,99]
    k2 = 2
    sol.rotate(nums2, k2)
    print(f"样例2结果：{nums2}")
    print("-" * 40)

    # 测试k大于数组长度的边界用例
    nums3 = [1,2,3]
    k3 = 5
    sol.rotate(nums3, k3)
    print(f"k=5，数组[1,2,3]结果：{nums3}")