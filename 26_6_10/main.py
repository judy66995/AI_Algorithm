# -*- coding: utf-8 -*-
"""
LeetCode 395. 至少有 K 个重复字符的最长子串
题目：找出字符串中每个字符出现次数都 >= k 的最长子串的长度
"""

class Solution:
    # -------------------------- 解法1：分治递归 --------------------------
    def longestSubstring_divide_conquer(self, s: str, k: int) -> int:
        # 递归终止条件：字符串长度不足k，不可能满足要求
        if len(s) < k:
            return 0

        # 统计每个字符的出现次数
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1

        # 找到第一个出现次数 < k 的字符，用它分割字符串
        for c in freq:
            if freq[c] < k:
                # 对分割后的每个子串递归求解，取最大值
                return max(self.longestSubstring_divide_conquer(part, k) for part in s.split(c))

        # 所有字符都满足频次 >= k，直接返回当前长度
        return len(s)

    # -------------------------- 解法2：滑动窗口 --------------------------
    def longestSubstring_sliding_window(self, s: str, k: int) -> int:
        max_len = 0
        n = len(s)

        # 枚举窗口中最多包含的不同字符数量（1~26，因为只有小写字母）
        for max_unique in range(1, 27):
            freq = {}
            left = 0
            count_ge_k = 0   # 窗口中频次 >= k 的字符数
            unique_count = 0 # 窗口中不同字符的数量

            for right in range(n):
                # 右指针扩展窗口
                c = s[right]
                if freq.get(c, 0) == 0:
                    unique_count += 1
                freq[c] = freq.get(c, 0) + 1
                if freq[c] == k:
                    count_ge_k += 1

                # 窗口内不同字符数超过当前枚举值，左指针收缩
                while unique_count > max_unique:
                    left_c = s[left]
                    if freq[left_c] == k:
                        count_ge_k -= 1
                    freq[left_c] -= 1
                    if freq[left_c] == 0:
                        unique_count -= 1
                    left += 1

                # 窗口内所有字符频次都 >= k，更新最大长度
                if count_ge_k == unique_count:
                    max_len = max(max_len, right - left + 1)

        return max_len


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        # (s, k, expected)
        ("aaabb", 3, 3),
        ("ababbc", 2, 5),
        ("abcab", 2, 0),
        ("abacbbc", 2, 7),
        ("", 1, 0),
        ("a", 1, 1),
        ("ab", 2, 0),
        ("aaabbb", 3, 6),
    ]

    print("=== 分治递归解法测试 ===")
    for i, (s, k, expected) in enumerate(test_cases, 1):
        res = sol.longestSubstring_divide_conquer(s, k)
        print(f"测试用例{i}: s={s}, k={k}")
        print(f"  预期结果: {expected}, 实际结果: {res} {'✅' if res == expected else '❌'}")

    print("\n=== 滑动窗口解法测试 ===")
    for i, (s, k, expected) in enumerate(test_cases, 1):
        res = sol.longestSubstring_sliding_window(s, k)
        print(f"测试用例{i}: s={s}, k={k}")
        print(f"  预期结果: {expected}, 实际结果: {res} {'✅' if res == expected else '❌'}")