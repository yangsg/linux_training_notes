```python
import time

def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        return_value = func(*args, **kwargs)
        end_time = time.time()
        print('function name: %s, waste time: %s' % (func.__name__, (end_time - start_time)))
        return return_value
    return wrapper

@log_time
def f():
    print(f.__name__)
    time.sleep(2)

if __name__ == '__main__':
    f()
```
