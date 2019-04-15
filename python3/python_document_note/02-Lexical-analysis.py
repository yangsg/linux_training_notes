#// https://docs.python.org/3.6/reference/index.html

'''
逻辑行
物理行


# 注释

行结尾字符；
    \n    unix linux  (linefeed)
    \r\n  windows
    \r    mac         (return)

编码声明：

编码声明：
# -*- coding: UTF-8 -*-

UTF-8 byte-order mark (b'\xef\xbb\xbf')



显示的行连接(join), 作用将多个物理行连接合并为一个逻辑行
注：反斜线后不能有出换行符之外的任意字符，包括注释
if 1900 < year < 2100 and 1 <= month <= 12 \
   and 1 <= day <= 31 and 0 <= hour < 24 \
   and 0 <= minute < 60 and 0 <= second < 60:   # Looks like a valid date
        return 1


隐式的行连接(join)
  小圆括号'()', 方括号'[]', 大括号'{}' 中的表达式都支持 隐式的行连接

month_names = ['Januari', 'Februari', 'Maart',      # These are the
               'April',   'Mei',      'Juni',       # Dutch names
               'Juli',    'Augustus', 'September',  # for the months
               'Oktober', 'November', 'December']   # of the year


缩进:  注意不要tab 和 space 混用
       python的代码风格中喜欢使用4个空格来缩进



其他标志 token

标志符和关键字  Identifiers and keywords

标志符： 字母，下划线，数字(但不能以数字开头)

关键字
下面这些字符都是保留字或关键字：
    False      class      finally    is         return
    None       continue   for        lambda     try
    True       def        from       nonlocal   while
    and        del        global     not        with
    as         elif       if         or         yield
    assert     else       import     pass
    break      except     in         raise



Reserved classes of identifiers  保留的标志符类

_*     不会被 'from module import * ' 语句导入，即约定为非公共的API (non public api)
__*__  系统定义的名字 System-defined names, 被解释器 和 其实现(包括标准库)所定义
__*    类私有名字Class-private names. 会应用‘name mangling’机制


字面量 Literals
字面量是一些built-in 类型常量值的符号

字符串字面量：

'hello world'
"hello world"
"""\
hello
world"""

'''

"""
'''
hello
world
'''

前缀和字符串之间不能有空格(更多信息见官网)
r'[abc]'  #// raw strings 原始字符串(反斜线'\'会被当做字面值对待) (表示正则表达式的字符串中特别常用)

"""

# bytes 字面量 (语法上类似于字符串字面量)
#  bytes 字面量 只能包含 ASCII 字符，numeric value为128或128以上的byte都需要通过转义来表示
type(b'abc')  #// <class 'bytes'>

username = 'Bob'
f'{username}'   #// formatted string literal
fr'{username}'   #// formatted string literal

'''
 In triple-quoted literals, unescaped newlines and quotes are allowed (and are retained)

 这一特性在编写即包含单引号又包含双引号的字符串时很方便
'''

'''

转义序列
\newline  Backslash and newline ignored
\\        Backslash (\)
\'        Single quote (')
\"        Double quote (")
\a        ASCII Bell (BEL)
\b        ASCII Backspace (BS)
\f        ASCII Formfeed (FF)
\n        ASCII Linefeed (LF)
\r        ASCII Carriage Return (CR)
\t        ASCII Horizontal Tab (TAB)
\v        ASCII Vertical Tab (VT)
\ooo      Character with octal value ooo  (1,3)
\xhh      Character with hex value hh     (2,3)


只在字符串字面量中识别的转义序列：
\N{name}       Character named name in the Unicode database (4)
\uxxxx         Character with 16-bit hex value xxxx (5)
\Uxxxxxxxx     Character with 32-bit hex value xxxxxxxx (6)



字符串字面量拼接 String literal concatenation (注：该处理在编译时执行，而'+'操作符是在运行时执行)

多个毗邻的 string or bytes literals 会自动发生拼接, 这个特性可以减少转义斜线符'\'的使用, 而将长字符串分开写到多行.
re.compile("[A-Za-z_]"       # letter or underscore
           "[A-Za-z0-9_]*"   # letter, digit or underscore
          )


格式化字符串字面量 Formatted string literals

f'abc {(lambda x: x * 3)(username)}'  #// 格式化字符串字面量中还可使用lambda表达式(当然，lambda要用括号括起来)


数字字面量  Numeric literals
三中数字字面量: integers, floating point numbers, and imaginary numbers
注： 数字字面量不包括 sign(即 正负号 + -), 所以 -1 是 操作符 - 和 字面量 1 的运算


整数字面量示例：
7     2147483647                        0o177    0b100110111
3     79228162514264337593543950336     0o377    0xdeadbeef
      100_000_000_000                   0b_1110_0101

浮点数字面量示例：
3.14    10.    .001    1e100    3.14e-10    0e0    3.14_15_93


虚部字面量：
3.14j   10.j    10j     .001j   1e100j   3.14e-10j   3.14_15_93j



操作符 Operators
+       -       *       **      /       //      %      @
<<      >>      &       |       ^       ~
<       >       <=      >=      ==      !=


分隔符 Delimiters

(       )       [       ]       {       }
,       :       .       ;       @       =       ->
+=      -=      *=      /=      //=     %=      @=
&=      |=      ^=      >>=     <<=     **=



'''


















































