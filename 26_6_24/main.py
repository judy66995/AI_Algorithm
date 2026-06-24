from typing import List

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        # 二维DP表，(m+1)行 (n+1)列，初始全0
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1):
            c1 = text1[i-1]
            for j in range(1, n+1):
                c2 = text2[j-1]
                if c1 == c2:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]


if __name__ == "__main__":
    sol = Solution()
    print(sol.longestCommonSubsequence("abcde", "ace")) # 3
    print(sol.longestCommonSubsequence("abc", "abc")) # 3
    print(sol.longestCommonSubsequence("abc", "def")) # 0