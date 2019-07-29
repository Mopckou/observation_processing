a = [1, 2, 3, 4]
c = [1, 2]

def f(n):
    d = []
    for i in c:
        d.append(i)
    return d

b = []

b.extend(i for *i in [[1, 2, 3, 4], [1, 2]])

print(b)