from typing import List

class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        # 哈希表：存每个字符最后出现的下标
        last_pos = {}
        for idx, char in enumerate(s):
            last_pos[char] = idx
        
        res = [] 
        left = 0   # 当前片段左边界
        right = 0  # 当前片段最远右边界
        for idx, char in enumerate(s):
            # 更新当前片段最远右边界
            right = max(right, last_pos[char])
            # 走到当前片段的最远边界，说明可以分割
            if idx == right:
                res.append(right - left + 1) 
                left = idx + 1
        return res


if __name__ == "__main__":
    sol = Solution()
    print(sol.partitionLabels("ababcbacadefegdehijhklij")) # [9,7,8]
    print(sol.partitionLabels("eccbbbbdec")) # [10]