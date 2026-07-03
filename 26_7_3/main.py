class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        双指针原地解法，O(n)时间 O(1)空间
        """
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1



if __name__ == "__main__":
    sol = Solution()

    # 测试用例1
    nums1 = [0, 1, 0, 3, 12]
    sol.moveZeroes(nums1)
    print(f"测试用例1输出: {nums1}  预期: [1, 3, 12, 0, 0]")

    # 测试用例2
    nums2 = [0]
    sol.moveZeroes(nums2)
    print(f"测试用例2输出: {nums2}  预期: [0]")

    # 测试用例3 全连续非零
    nums3 = [1, 2, 3, 4]
    sol.moveZeroes(nums3)
    print(f"测试用例3输出: {nums3}  预期: [1, 2, 3, 4]")

    # 测试用例4 全零
    nums4 = [0, 0, 0]
    sol.moveZeroes(nums4)
    print(f"测试用例4输出: {nums4}  预期: [0, 0, 0]")

    # 测试用例5 零在中间
    nums5 = [0, 0, 1, 0, 2, 0]
    sol.moveZeroes(nums5)
    print(f"测试用例5输出: {nums5}  预期: [1, 2, 0, 0, 0, 0]")