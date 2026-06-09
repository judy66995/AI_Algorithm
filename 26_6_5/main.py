class Solution:
    def longestConsecutive(self, nums):
        num_set = set(nums) # 将列表转换为集合，去重 + O(1)查找
        max_len = 0 # 初始化最长连续序列的长度为0
        for n in num_set: 
            if n - 1 not in num_set: # 只有当n-1不在集合中时，才以n为起点开始寻找连续序列
                cur, length = n, 1 # 从当前数字开始，长度初始化为1
                while cur + 1 in num_set:
                    cur += 1
                    length += 1
                max_len = max(max_len, length) # 更新最长连续序列的长度
        return max_len

if __name__ == "__main__":
    sol = Solution()
    print("案例1：", sol.longestConsecutive([100,4,200,1,3,2]))
    print("案例2：", sol.longestConsecutive([0,3,7,2,5,8,4,6,0,1]))