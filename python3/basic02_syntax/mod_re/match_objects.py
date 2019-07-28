#// https://docs.python.org/3.6/library/re.html#match-objects
import re

# 使用 re 或 str 相关的 方法时, 最好 同时 参考 api 文档, 因为某些方法的行为和
# 和该方法的名称的字面意思不完全相符(或者说 相同的调用
# 在不同的语言(如javascript)中却表现出了不同的行为)


# 注: python 中的 正则表达式 \d 和 [0-9] 并非总是等价, 这与编码有关系,
#     如果是仅匹配 0 到 9 之间的 数字, 最好使用 [0-9] 这种方式, 而不要使用
#     \d 这种方式

m = re.search(r'\d+', '٣٤٥۳')  # 不推荐使用 \d , 而最好使用 [0-9]
if m:  # 未匹配到时 m is None
  print(m.group(0))  # 输出: ٣٤٥۳,  所以如果没有指定 ASCII flag, \d 还会匹配 unicode 中 Nd 类别的其他字符.
                     # http://www.fileformat.info/info/unicode/category/Nd/list.htm
                     # https://docs.python.org/3.6/library/re.html
                     # https://docs.python.org/3.6/howto/regex.html

if m:
  m.group()


# 字符串的 字面量 表示方式见:
# https://docs.python.org/3.6/reference/lexical_analysis.html#literals


'''
prog = re.compile(pattern)
result = prog.match(string)

等价于:

result = re.match(pattern, string)
'''


re.fullmatch(r'[0-9]abc', '2abc')    # New in version 3.4

'''
>>> re.split(r'\W+', 'Words, words, words.')
['Words', 'words', 'words', '']
>>> re.split(r'(\W+)', 'Words, words, words.')
['Words', ', ', 'words', ', ', 'words', '.', '']
>>> re.split(r'\W+', 'Words, words, words.', 1)
['Words', 'words, words.']
>>> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
['0', '3', '9']


>>> re.findall(r'[0-9]{1,3}', '192.168.175.10')
['192', '168', '175', '10']

>>> re.sub(r'\.', r'_', '192.168.175.10')
'192_168_175_10'

>>> re.sub(r'\.', r'_\g<0>', '192.168.175.10')
'192_.168_.175_.10'

>>> re.sub(r'\.', r'_\g<0>', '192.168.175.10', count=2)
'192_.168_.175.10'

>>> re.subn(r'\.', r'_\g<0>', '192.168.175.10')
('192_.168_.175_.10', 3)


>>> print(re.escape('python.exe'))
python\.exe

>>> legal_chars = string.ascii_lowercase + string.digits + "!#$%&'*+-.^_`|~:"
>>> print('[%s]+' % re.escape(legal_chars))
[abcdefghijklmnopqrstuvwxyz0123456789\!\#\$\%\&\'\*\+\-\.\^_\`\|\~\:]+

>>> operators = ['+', '-', '*', '/', '**']
>>> print('|'.join(map(re.escape, sorted(operators, reverse=True))))
\/|\-|\+|\*\*|\*
'''


















