

# 正则表达式
# python中使用正则表达式时建议使用原始字符串(raw string)

# https://docs.python.org/3.6/howto/regex.html
# https://docs.python.org/3.6/library/re.html


# 普通字符(ordinary characters)  表示字符本身的子面值  r'abc'
# 特殊字符(special characters)  约定了其具有特殊含义, 所以如果需要将其视作类似普通字符那样表示字符本身来看待，需要对其进行转义.  r'^abc\n$'


'''
特殊字符 special characters

.  (Dot.) 在默认模式，匹配除newline 之外的任意字符，如果指定了  DOTALL 标志， 则其会匹配包括newline在内的任意字符

#  位置
^(Caret.) 匹配字符串的开始位置， 如果在 MULTILINE 模式下，还会匹配每个newline紧随其后的位置

$  匹配 string 的结尾 或 string结尾的 newline 之前的位置,


# 量词
*
+
?
*?, +?, ??   非贪婪 最小匹配 lazy
{m}
{m,n}
{m,n}?

\  转义

[]  字符集
|   或  To match a literal '|', use \|, or enclose it inside a character class, as in [|].
(...)  组  To match the literals '(' or ')', use \( or \), or enclose them inside a character class: [(], [)].


(?...) 扩展标记 extension notation, 没有其他意义，具体意义由 ? 后的字符确定
(?:...)  非捕获组
(?imsx-imsx:...)
(?P<name>...)  命名组
(?P=name)      对命名组的后向引用 或 反向引用
(?#...)        注释，会被直接 ignored 掉
(?=...)        先行断言
(?!...)        否定先行断言
(?<=...)        positive lookbehind assertion
(?<!...)        negative lookbehind assertion
(?(id/name)yes-pattern|no-pattern)


'''

'''
re 模块：核心函数和方法

                        表1-2 常见的正则表达式属性

    函数/方法                                              描 述
仅仅是re 模块函数
compile(pattern，flags = 0)           使用任何可选的标记来编译正则表达式的模式，然后返回一个正则表达式对象

re 模块函数和正则表达式对象的方法
match(pattern，string，flags=0)       尝试使用带有可选的标记的正则表达式的模式来匹配字符串。如果匹配成功，就返回匹配对象；如果失败，就返回None
search(pattern，string，flags=0)      使用可选标记搜索字符串中第一次出现的正则表达式模式。如果匹配成功，则返回匹 配对象；如果失败，则返回None
findall(pattern，string [, flags] )   查找字符串中所有（非重复）出现的正则表达式模式，并返回一个匹配列表
finditer(pattern，string [, flags] )  与findall()函数相同，但返回的不是一个列表，而是一个迭代器。对于每一次匹配，迭代器都返回一个匹配对象
split(pattern，string，max=0)         根据正则表达式的模式分隔符，split 函数将字符串分割为列表，然后返回成功匹配的列表，分隔最多操作max 次（默认分割所有匹配成功的位置）

re 模块函数和正则表达式对象方法
sub(pattern，repl，string，count=0)   使用repl 替换所有正则表达式的模式在字符串中出现的位置，除非定义count，否则就将替换所有出现的位置（另见subn()函数，该函数返回替换操作的数目）
purge()                               清除隐式编译的正则表达式模式

常用的匹配对象方法（查看文档以获取更多信息）
group(num=0)                          返回整个匹配对象，或者编号为num 的特定子组
groups(default=None)                  返回一个包含所有匹配子组的元组（如果没有成功匹配，则返回一个空元组）
groupdict(default=None)               返回一个包含所有匹配的命名子组的字典，所有的子组名称作为字典的键（如果没有成功匹配，则返回一个空字典）

常用的模块属性（用于大多数正则表达式函数的标记）
re.I、re.IGNORECASE                   不区分大小写的匹配
re.L、re.LOCALE                       根据所使用的本地语言环境通过\w、\W、\b、\B、\s、\S 实现匹配
re.M、re.MULTILINE                    ^和$分别匹配目标字符串中行的起始和结尾，而不是严格匹配整个字符串本身的起始和结尾
re.S、rer.DOTALL                      “.”（点号）通常匹配除了\n（换行符）之外的所有单个字符；该标记表示“.”（点号）能够匹配全部字符
re.X、re.VERBOSE                      通过反斜线转义，否则所有空格加上#（以及在该行中所有后续文字）都被忽略，除非在一个字符类中或者允许注释并且提高可读性



'''

















