from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 哈希表存储 数值:下标
        hash_map = dict()
        for idx, num in enumerate(nums):
            # 需要配对的差值
            match_num = target - num
            if match_num in hash_map:
                # 找到配对，直接返回两个下标
                return [hash_map[match_num], idx]
            # 当前数字存入哈希表
            hash_map[num] = idx
        # 题目保证一定有解，此行不会走到
        return []


if __name__ == "__main__":
    sol = Solution()
    # 示例1
    print(sol.twoSum([2,7,11,15], 9))  # [0, 1]
    # 示例2
    print(sol.twoSum([3,2,4], 6))      # [1, 2]
    # 示例3（重复数字）
    print(sol.twoSum([3,3], 6))        # [0, 1]