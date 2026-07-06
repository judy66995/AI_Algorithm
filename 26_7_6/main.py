from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n <= 2:
            return 0
        
        #[0]是一个只包含数字0的列表；* n是列表乘法，表示把这个列表复制n份，拼接成一个新列表。
        left_max = [0] * n 
        right_max = [0] * n
        res = 0

        # 预处理左侧最大值
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i-1], height[i]) # 比较左侧最大值和当前高度，取较大者作为新的左侧最大值。
        
        # 预处理右侧最大值
        right_max[-1] = height[-1]
        for i in range(n-2, -1, -1): #range(start, stop, step)；start = n-2，stop = -1，step = -1
            right_max[i] = max(right_max[i+1], height[i]) # 比较右侧最大值和当前高度，取较大者作为新的右侧最大值。
        
        # 累加每一格雨水
        for i in range(n):
            res += min(left_max[i], right_max[i]) - height[i]
        return res


if __name__ == "__main__":
    sol = Solution()
    test1 = [0,1,0,2,1,0,1,3,2,1,2,1]
    test2 = [4,2,0,3,2,5]
    print(sol.trap(test1))  # 输出 6
    print(sol.trap(test2))  # 输出 9