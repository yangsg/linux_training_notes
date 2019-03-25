#// https://docs.python.org/3.6/tutorial/datastructures.html#nested-list-comprehensions


matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

[[row[i] for row in matrix] for i in range(4)]

list(zip(*matrix))


