#// https://docs.python.org/3.6/tutorial/datastructures.html#using-lists-as-queues

#// 使用专有的 deque 比原始的 list 更高效

from collections import deque
queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")           # Terry arrives
queue.append("Graham")          # Graham arrives
queue.popleft()                 # The first to arrive now leaves
queue.popleft()                 # The second to arrive now leaves



