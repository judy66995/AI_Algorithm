from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # 字典：key=排序后的标准字符串，value=异位词分组
        # 普通字典如果访问不存在的 key 会报错，defaultdict(list) 当 key 不存在时自动创建空列表，不用额外写判断逻辑。
        group_map = defaultdict(list)
        for s in strs:
            # 将字符串字母排序，生成统一分组标识key
            '''
            sorted() 是 Python 内置排序函数，
            接收可迭代对象（字符串、列表、元组都可以），返回全新排序后的列表。
            字符串 s 会被拆成单个字符，按字母 ASCII 从小到大排序。
             sorted()关键特性：
            1.不修改原字符串 s，只会生成新列表；
            2.所有字母异位词排序后得到完全相同的字符列表，这是分组的核心依据；
            3.返回值类型：list 列表。
            '''
            '''
            "".join( 排序后的列表 )语法拆解：
            左边的 ""：空字符串，代表连接符，意思是 “把列表里所有元素拼接，中间不加任何分隔符”；
            .join()：字符串自带方法，接收一个「元素全是字符串」的可迭代对象（列表 / 元组），把所有元素拼接成一整条新字符串；
            限制：join 的参数里每一项必须是字符串，刚好 sorted(s) 输出字符列表，满足条件。
            '''
            sort_key = "".join(sorted(s))
            # 原字符串加入对应分组
            group_map[sort_key].append(s)
        # 取出所有分组列表返回
        return list(group_map.values())


if __name__ == "__main__":
    sol = Solution()
    print(sol.groupAnagrams(["eat","tea","tan","ate","nat","bat"]))
    # 输出 [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print(sol.groupAnagrams([""])) # [['']]