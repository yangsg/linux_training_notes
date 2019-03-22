#// https://docs.python.org/3.6/tutorial/controlflow.html#default-argument-values

def nginx(option, action=''):
    print('nginx ', option, ' ', action)


nginx('-t')
nginx('-s', 'start')

nginx(option='-s', action='start')
nginx(action='start', option='-s')

nginx(*['-s', 'start'])
nginx(**{'option': '-s', 'action': 'start'})


#// 注：默认参数值在定义时被计算，且只被计算一次
#// 所以注意下面两者的差别
def f01(a, L=[]):
    L.append(a)
    return L

def f02(a, L=None):
    if L is None:
        L = []
        L.append(a)
        return L

