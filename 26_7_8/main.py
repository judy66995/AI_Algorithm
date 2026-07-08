from collections import defaultdict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # 1. 初始化need字典：统计t每个字符需要的数量
        need = defaultdict(int)
        for char in t:
            need[char] += 1
        need_size = len(need)  # t中有多少种不同字符

        window = defaultdict(int)  # 当前窗口内字符计数
        left = 0
        valid = 0  # 窗口内满足need数量的字符种类
        # float('inf') 是 Python 里的特殊浮点数，它有一个核心特性：
        # 任何数字 < 无穷大
        min_len = float('inf')  # 记录最小合法窗口长度
        start_idx = 0  # 最小窗口起始下标

        # 2. right指针扩张窗口
        for right in range(len(s)):
            cur_char = s[right]
            # 如果当前字符是t需要的，计入window
            if cur_char in need:
                window[cur_char] += 1
                # 当前字符数量刚好达标，有效种类+1
                if window[cur_char] == need[cur_char]:
                    valid += 1

            # 3. 窗口合法，开始收缩left，尝试找更短区间
            while valid == need_size:
                # 更新最小窗口
                window_len = right - left + 1
                if window_len < min_len:
                    min_len = window_len
                    start_idx = left
                # 收缩左边界
                left_char = s[left]
                if left_char in need:
                    # 如果这个字符刚好等于需要数量，移除后会不达标，有效种类-1
                    if window[left_char] == need[left_char]:
                        valid -= 1
                    window[left_char] -= 1
                left += 1
        
        # 如果没找到合法窗口，返回空串，否则截取最小子串
        if min_len == float('inf'):
            return ""
        return s[start_idx : start_idx + min_len]


if __name__ == "__main__":
    sol = Solution()
    # 示例1
    s1 = "ADOBECODEBANC"
    t1 = "ABC"
    print(f"示例1输出：{sol.minWindow(s1, t1)}")  # BANC

    # 示例2
    s2 = "a"
    t2 = "a"
    print(f"示例2输出：{sol.minWindow(s2, t2)}")  # a

    # 示例3
    s3 = "a"
    t3 = "aa"
    print(f"示例3输出：'{sol.minWindow(s3, t3)}'") # 空字符串