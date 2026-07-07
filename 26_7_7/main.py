from typing import List

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # 26个小写字母计数数组，a-z对应下标0-25
        p_count = [0] * 26 # 统计模式字符串p中每个字符的出现次数
        window_count = [0] * 26 # 统计当前窗口中每个字符的出现次数
        res = []
        len_p = len(p)
        len_s = len(s)

        # 1. 先统计目标字符串p的字母出现次数
        for char in p:
            p_count[ord(char) - ord('a')] += 1

        # 2. 初始化滑动窗口：先填满前 len_p 个字符
        for right in range(len_p):
            if right >= len_s:
                return res
            window_count[ord(s[right]) - ord('a')] += 1
        
        # 判断第一个窗口是否是异位词
        # 后面的 for right in range(len_p, len_s) 循环只处理滑动更新窗口，
        # 它的逻辑是：先删左边旧字符、再加右边新字符。
        # 但第一个窗口没有 “左边旧字符要删除” 的过程，
        # 没法进入这个循环里做判断，所以必须单独提前初始化、单独判断。
        if window_count == p_count:
            res.append(0)

        # 3. 滑动窗口向右移动，逐个更新窗口
        for right in range(len_p, len_s):
            # 左 = 右 - (窗口长度 - 1) = 右 - len_p + 1
            # 移出窗口最左侧的左边字符：left = right - len_p
            left_char = s[right - len_p]
            window_count[ord(left_char) - ord('a')] -= 1
            # 加入当前新的右边界字符
            curr_char = s[right]
            window_count[ord(curr_char) - ord('a')] += 1

            # 当前窗口字符计数和p完全一致，说明是异位词
            if window_count == p_count:
                res.append(right - len_p + 1)
        return res


if __name__ == "__main__":
    sol = Solution()
    test1 = ("cbaebabacd", "abc")
    test2 = ("abab", "ab")
    s1, p1 = test1
    s2, p2 = test2
    print(f"输入s={s1}, p={p1}，输出：{sol.findAnagrams(s1, p1)}")
    print(f"输入s={s2}, p={p2}，输出：{sol.findAnagrams(s2, p2)}")