class Solution:
    def longestConsecutive(self, nums):
        num_set = set(nums)
        max_len = 0
        for n in num_set:
            if n - 1 not in num_set:
                cur, length = n, 1
                while cur + 1 in num_set:
                    cur += 1
                    length += 1
                max_len = max(max_len, length)
        return max_len

if __name__ == "__main__":
    sol = Solution()
    print("案例1：", sol.longestConsecutive([100,4,200,1,3,2]))
    print("案例2：", sol.longestConsecutive([0,3,7,2,5,8,4,6,0,1]))