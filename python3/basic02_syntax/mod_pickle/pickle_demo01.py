
#// 相比 json, pickle 是一种可序列换任意复杂的Python objects的协议，
#// 不过 pickle 是 python语言特有的协议，所以其无法用于和其他语言做数据交换，
#// pickle 默认也是非安全的：用非信任的source的 pickcle data来反序列化可以执行
#// 任意的代码(如果the data was crafted by a skilled attacker)

#// https://www.datacamp.com/community/tutorials/pickle-python-tutorial
#// https://www.cnblogs.com/zhangxinqi/p/8034380.html

import pickle

obj = { 'name': 'Bob', 'age': 25, 'languages': ['English', '中文字符']}

obj_in_bytes = pickle.dumps(obj)
print(type(obj_in_bytes))  #// <class 'bytes'>
print(obj_in_bytes)
#// 输出结果：b'\x80\x03}q\x00(X\x04\x00\x00\x00nameq\x01X\x03\x00\x00\x00Bobq\x02X\x03\x00\x00\x00ageq\x03K\x19X\t\x00\x00\x00languagesq\x04]q\x05(X\x07\x00\x00\x00Englishq\x06X\x0c\x00\x00\x00\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe7\xac\xa6q\x07eu.' 

obj_restored = pickle.loads(obj_in_bytes)
print(type(obj_restored))  #// <class 'dict'>
print(obj_restored)        #// {'name': 'Bob', 'age': 25, 'languages': ['English', '中文字符']}


def dump_object_to_pickle_file():
    with open('/tmp/pickle.dump','wb') as f:   #// 以 binary mode 打开文件
        pickle.dump(obj ,f)

print('---' * 20)
dump_object_to_pickle_file()


def load_object_from_pickle_file():
    with open('/tmp/pickle.dump','rb') as f:
        obj_from_file = pickle.load(f)
        return obj_from_file

obj_by_load = load_object_from_pickle_file()
print(type(obj_by_load)) #// <class 'dict'>
print(obj_by_load)       #// {'name': 'Bob', 'age': 25, 'languages': ['English', '中文字符']}













