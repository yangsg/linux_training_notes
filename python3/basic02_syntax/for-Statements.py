#// https://docs.python.org/3.6/tutorial/controlflow.html#for-statements

#// Python’s for statement iterates over the items of any sequence (a list or a string), in the order that they appear in the sequence.
def measure_some_strings():
    words = ['cat', 'window', 'defenestrate']
    for w in words:
        print(w, len(w))

def demo_on_slice_copy():
    words = ['cat', 'window', 'defenestrate']

    #// words[:] 利用slice生成了words的一个副本
    for w in words[:]:  # Loop over a slice copy of the entire list.
        if len(w) > 6:
            words.insert(0, w)


#measure_some_strings()
#demo_on_slice_copy()



