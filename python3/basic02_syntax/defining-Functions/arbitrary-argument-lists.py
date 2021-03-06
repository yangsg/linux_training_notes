#// https://docs.python.org/3.6/tutorial/controlflow.html#unpacking-argument-lists


#// demo01
def sep_str_join(separator, *args):
    str = separator.join(args)
    print(str)

sep_str_join('-', '1', '2', '3')
sep_str_join('-', *['1', '2', '3'])
sep_str_join('-', *('1', '2', '3'))

#//demo02
def concat(*args, sep='/'):
    print(sep.join(args))

concat('1', '2', '3', sep='/')
concat('1', '2', '3', sep='-')
concat(*('1', '2', '3'), sep='-')
concat(*['1', '2', '3'], sep='-')


