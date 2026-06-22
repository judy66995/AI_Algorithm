# -*- coding: utf-8 -*-
"""
LeetCode 139 单词拆分
动态规划+哈希集合，适配NLP分词场景
"""
from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # 转为集合，单词查找O(1)
        word_set = set(wordDict)
        str_len = len(s)
        # dp[i]：字符串前i个字符能否被合法拆分
        dp = [False] * (str_len + 1)
        dp[0] = True  # 边界：空字符串天然可拆分，作为DP起点

        # i代表当前处理到前i个字符
        for i in range(1, str_len + 1):
            # j是分割点，把前i个字符切成 [0,j] 和 [j,i] 两段
            for j in range(i):  # j从0到i-1, range(i) 会生成一串数字：0, 1, 2, ..., i-1
                # 前j位能拆分 + j到i这段子串是字典单词
                if dp[j] and s[j:i] in word_set: # s[j:i] 是字符串s从索引j到i-1的子串
                    dp[i] = True
                    break  # 找到合法分割，无需继续遍历j
        # 前全部字符是否可拆分
        return dp[str_len]


if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats","dog","sand","and","cat"], False),
        ("a", [], False),
        ("aaaaa", ["aa", "aaa"], True)
    ]
    for s, dic, expect in test_cases:
        res = sol.wordBreak(s, dic)
        print(f"输入字符串：{s} | 输出：{res} | 预期：{expect} {'✅正确' if res == expect else '❌错误'}")