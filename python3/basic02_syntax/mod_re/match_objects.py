#// https://docs.python.org/3.6/library/re.html#match-objects
import re


# 注: python 中的 正则表达式 \d 和 [0-9] 并非总是等价, 这与编码有关系,
#     如果是仅匹配 0 到 9 之间的 数字, 最好使用 [0-9] 这种方式, 而不要使用
#     \d 这种方式

m = re.search(r'\d+', '٣٤٥۳')  # 不推荐使用 \d , 而最好使用 [0-9]
print(m.group(0))  # 输出: ٣٤٥۳,  所以如果没有指定 ASCII flag, \d 还会匹配 unicode 中 Nd 类别的其他字符.
                   # http://www.fileformat.info/info/unicode/category/Nd/list.htm
                   # https://docs.python.org/3.6/library/re.html
                   # https://docs.python.org/3.6/howto/regex.html

# 字符串的 字面量 表示方式见:
# https://docs.python.org/3.6/reference/lexical_analysis.html#literals



