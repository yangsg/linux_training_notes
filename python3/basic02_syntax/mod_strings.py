import string
import sys

def demo_poor_ipv4_check():
    ipv4_input = input("请输入一个ip: ").strip()

    print(ipv4_input)

    #// 检查0.0.0.0, 先排除掉最特殊的一个
    if ipv4_input == '0.0.0.0':
        print('valid ip')
        sys.exit()

    #// 按点'.'分片
    ip_parts = ipv4_input.split('.');
    if len(ip_parts) != 4:
        print('invalid ip')
        sys.exit()

    #// 判断每部分的是否合法
    for part in ip_parts:
        #// 如果长度不再1-3之间，则非法
        if len(part) < 1 or len(part) > 3:
            print('invalid ip')
            sys.exit()
        #// 如果以非'1'、'2'的字符开始，则非法
        if part[0] not in '12':
            print('invalid ip')
            sys.exit()

        #// 如果非数字，则非法
        if not part.isdigit():
            print('invalid ip')
            sys.exit()

        #// 如果越界，则非法
        num_part = int(part)
        if num_part < 0 or num_part > 255:
            print('invalid ip')
            sys.exit()

demo_poor_ipv4_check()



