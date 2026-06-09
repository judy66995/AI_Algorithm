# -*- coding: utf-8 -*-
"""
LeetCode 3. 无重复字符的最长子串
滑动窗口 + 哈希表（最优解 O(n)）
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index = dict()   # 记录字符最后出现的位置
        max_len = 0           # 最长无重复子串长度
        left = 0               # 滑动窗口左边界

        for right, ch in enumerate(s):
            # right: 右边界索引（也是当前字符的位置）
            # ch: 当前字符
            
            # 如果 ch 在当前窗口内出现过，左边界跳到上次出现的下一位
            if ch in char_index and char_index[ch] >= left:
                left = char_index[ch] + 1
            
            # 更新当前字符最新位置
            # 用 ch 作为字典的键，记录它最后出现的位置
            char_index[ch] = right

            # 更新最大长度
            current_len = right - left + 1
            if current_len > max_len:
                max_len = current_len

        return max_len


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        "abcabcbb",   # 预期 3
        "bbbbb",      # 预期 1
        "pwwkew",      # 预期 3
        "",            # 预期 0
        "abba"         # 预期 2
    ]

    for case in test_cases:
        res = sol.lengthOfLongestSubstring(case)
        print(f"输入: {repr(case)}  => 最长长度: {res}")