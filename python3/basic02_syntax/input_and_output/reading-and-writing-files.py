#// https://docs.python.org/3.6/tutorial/inputoutput.html#reading-and-writing-files


#// https://docs.python.org/3.6/library/functions.html#open
#// https://docs.python.org/3.6/glossary.html#term-file-object

#// syntax: open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)  return file object


#//     Character   Meaning
#//     'r' open for reading (default)
#//     'w' open for writing, truncating the file first
#//     'x' open for exclusive creation, failing if the file already exists
#//     'a' open for writing, appending to the end of the file if it exists
#//     'b' binary mode
#//     't' text mode (default)
#//     '+' open a disk file for updating (reading and writing)
#//     'U' universal newlines mode (deprecated)

#//  'r+' opens the file for both reading and writing. The mode argument is optional; 'r' will be assumed if it’s omitted.
#//
#//  Normally, files are opened in text mode, that means, you read and write strings from and to the file,
#//  which are encoded in a specific encoding. If encoding is not specified, the default is platform dependent 
#// 'b' appended to the mode opens the file in binary mode: 

#// 在文本模式中，默认读取时行末尾被规范化为'\n', 写入时会还原会系统平台相关的行末尾字符(如 \n \r\n \r)
#// In text mode, the default when reading is to convert platform-specific line endings (\n on Unix, \r\n on Windows)
#// to just \n. When writing in text mode, the default is to convert occurrences of \n back to platform-specific line endings. 

#// 读取 JPEG or EXE 是应该使用 binary mode 形式

#// 使用 with 关键字 处理 file object 是一个好习惯， 好处是 代码简洁，file object始终能保证被关闭释放(即使发生异常)


def read_text_file_01():
    with open('reading-and-writing-files.py') as f:
        #// 利用pycharm 开发工具可以快速跳转到对应的api
        #// https://docs.python.org/3.6/library/allos.html#generic-operating-system-services
        #// https://docs.python.org/3.6/library/io.html
        #// dir(f)
        #// help(f.read)
        #// help(f.readline)
        #// help(f.readlines)

        #//syntax: read(size=-1, /)
        read_data = f.read()   #// https://docs.python.org/3.6/tutorial/inputoutput.html#methods-of-file-objects
        print(read_data)

#// read_text_file_01()

def read_text_file_02():
    with open("reading-and-writing-files.py", "r", encoding="utf-8") as f:
        read_data = f.read()

    print(read_data)

#// read_text_file_02()


def read_text_file_line_by_line_01():
    with open("reading-and-writing-files.py", "r", encoding="utf-8") as f:
        line = f.readline()  #//注：line变量的内容中包含着'\n', 详见 https://docs.python.org/3.6/tutorial/inputoutput.html#methods-of-file-objects
        while line:
            print(line, end='')
            line = f.readline()

#// read_text_file_line_by_line_01()


def read_text_file_line_by_line_02():
    with open("reading-and-writing-files.py", "r", encoding="utf-8") as f:
        for line in f:
            print(line, end='')

#// read_text_file_line_by_line_02()


def read_text_file_line_by_line_03():
    with open("reading-and-writing-files.py", "r", encoding="utf-8") as f:
        line_list = f.readlines()  #//语法： readlines(hint=-1, /) Return a list of lines from the stream.
        for line in line_list:
            print(line, end='')

#// read_text_file_line_by_line_03()

#// 真正的copy操作应该使用shutil.copy或shutil.copy2, 因为 shutil.copy 函数对可能地各种情况都做了考虑
#// 本例只是简单拷贝了shutil.copy的部分源码, 用于演示 shutil.copy 在拷贝 binary file时实际是怎么读取写入的
#// 可以利用pycharm 工具查看 shutil.copy 的源码来学习更多内容
def copy_binary_file(src, dst):
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            length = 16*1024; #// 设置缓冲区长度
            while 1:
                buf = fsrc.read(length)
                if not buf:
                    break
                fdst.write(buf)


#// copy_binary_file('reading-and-writing-files.py', '/tmp/reading-and-writing-files.py.copy')  #// 完成后可用 md5sum 校验一下

#// 其他demo   https://www.devdungeon.com/content/working-binary-data-python


#// file object 还有一些如 f.tell() 和 f.seek(offset, from_what) 之类的方法函数
#// https://docs.python.org/3.6/tutorial/inputoutput.html#methods-of-file-objects









