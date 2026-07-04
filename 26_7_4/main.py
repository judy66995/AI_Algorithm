from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            width = right - left
            h = min(height[left], height[right])
            current_area = width * h
            if current_area > max_area:
                max_area = current_area
            # 移动短板
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area


if __name__ == "__main__":
    sol = Solution()
    # 题目示例用例
    test1 = [1,8,6,2,5,4,8,3,7]
    print(f"输入数组: {test1}")
    print(f"最大盛水量: {sol.maxArea(test1)}")  # 预期输出49

    # 额外测试用例
    test2 = [1,1]
    print(f"\n输入数组: {test2}")
    print(f"最大盛水量: {sol.maxArea(test2)}")  # 预期输出1

    test3 = [4,3,2,1,4]
    print(f"\n输入数组: {test3}")
    print(f"最大盛水量: {sol.maxArea(test3)}")  # 预期输出16