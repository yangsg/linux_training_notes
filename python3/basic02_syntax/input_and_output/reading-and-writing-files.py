
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


with open("reading-and-writing-files.py", "r", encoding="utf-8") as f:
    read_data = f.read()
    print(read_data)





