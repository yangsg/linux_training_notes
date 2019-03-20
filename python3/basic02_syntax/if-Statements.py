
#// https://docs.python.org/3.6/tutorial/controlflow.html#if-statements
def if_statements():
    x = int(input("Please enter an integer: "))
    if x < 0:
        x = 0
        print('Negative changed to zero')
    elif x == 0:
        print('Zero')
    elif x == 1:
        print('Single')
    else:
        print('More')

def if_check_user_type_on_centos7():
    print("This is Centos7")
    uid=int(input("Enter your uid: "))

    if uid == 0:
        print("user(uid=%s) is root" % uid)
    elif 0 < uid and uid < 1000:
        print("user(uid=%s) is system user" % uid)
    else:
        print("user(uid=%s) is common user" % uid)


if_check_user_type_on_centos7()
