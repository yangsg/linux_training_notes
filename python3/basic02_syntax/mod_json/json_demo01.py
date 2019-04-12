#// https://docs.python.org/3.6/tutorial/inputoutput.html#saving-structured-data-with-json

import json

#// serializing 序列化
def dump_json_object_to_string():
    #// dumps : dump string
    jsonStr = json.dumps([1, 'simple', 'list', {'key01': '中文字符', 'key02': {'nested_key01': [1, 2, 3]}}]) #// 类似javascript中的 JSON.stringify()函数
    return jsonStr

#// print(dump_json_object_to_string());

#// deserializing  反序列化
def load_json_object_from_string():
    jsonStr = dump_json_object_to_string()
    #// loads: load string
    jsonObj = json.loads(jsonStr)   #// 类似javascript中的 JSON.parse()函数
    return jsonObj

#// print(load_json_object_from_string())

def dump_json_object_to_file():
    with open("/tmp/json.dump", "w") as f: #// open 默认就是以 text mode 打开文件
        obj = [1, 'simple', 'list', {'key01': '中文字符', 'key02': {'nested_key01': [1, 2, 3]}}];
        json.dump(obj, f)

#// dump_json_object_to_file()
#//       [root@python3lang ~]# cat /tmp/json.dump
#//       [1, "simple", "list", {"key01": "\u4e2d\u6587\u5b57\u7b26", "key02": {"nested_key01": [1, 2, 3]}}][root@python3lang ~]#


def load_json_object_from_file():
    with open("/tmp/json.dump", "r") as f:  #// 此处 f 也是以默认的 text mode 打开的
        jsonObj = json.load(f)
        return jsonObj

#// print(load_json_object_from_file())
#//      [root@python3lang mod_json]# python3 json_demo01.py
#//      [1, 'simple', 'list', {'key01': '中文字符', 'key02': {'nested_key01': [1, 2, 3]}}]


def pretty_dump_json_object_to_string():
    jsonStr = json.dumps([1, 'simple', 'list', {'key01': '中文字符', 'key02': {'nested_key01': [1, 2, 3]}}],
                indent=4)
    return jsonStr

#// print(pretty_dump_json_object_to_string())

def sort_dump_json_object_to_string(): #// 用 sort_keys=True 来对字典的 key 进行排序
    jsonStr = json.dumps([1, 'simple', 'list', {'key02': '中文字符', 'key01': {'nested_key01': [1, 2, 3, 8, 6]}}],
                indent=4, sort_keys=True)
    return jsonStr

#// print(sort_dump_json_object_to_string())



















