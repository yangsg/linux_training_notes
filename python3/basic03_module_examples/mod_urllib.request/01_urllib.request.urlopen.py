from urllib.request import urlopen

#// https://docs.python.org/3.6/tutorial/stdlib.html#internet-access
#// https://docs.python.org/3.6/library/urllib.request.html#module-urllib.request

#// urllib.request 用于获取 URLS 上的数据


with urlopen('http://www.baidu.com') as response:
    for line in response:
        line = line.decode('utf-8')  # Decoding the binary data to text.
        print(line)


