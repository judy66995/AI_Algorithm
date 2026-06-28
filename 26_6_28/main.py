from collections import defaultdict # 导入默认字典，不存在的 key 自动初始值 0，方便统计字符次数。

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = defaultdict(int) 
        left = 0
        max_freq = 0
        res = 0
        
        for right in range(len(s)):
            char_r = s[right] # 右指针指向的字符
            count[char_r] += 1 # 统计右指针字符出现次数
            # 更新窗口内出现最多字符的频次
            max_freq = max(max_freq, count[char_r])
            
            # 窗口长度 - 最多字符数 = 需要替换的字符数量，超过k则收缩左边界
            window_len = right - left + 1
            if window_len - max_freq > k: # 如果需要替换的字符数量大于 k，则收缩左边界
                count[s[left]] -= 1
                left += 1
            
            # 更新合法窗口最大长度
            res = max(res, right - left + 1)
        return res

if __name__ == "__main__":
    sol = Solution()
    print(sol.characterReplacement("AABABBA", 1)) # 4
    print(sol.characterReplacement("ABAB", 2)) #4
    print(sol.characterReplacement("AAAA", 0)) #4