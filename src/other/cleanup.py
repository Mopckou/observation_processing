import scipy
file = scipy.loadtxt("rez_example.txt", dtype=float)
x = file[:, 0]
y = file[:, 1]

f = open("rez_example_realx3.txt")

rf = f.read()
d = []

rfd = rf.split('\n')[:-1]

for i in range(0, len(rfd)-1):

    if rfd[i] == rfd[i + 1]:
        d.append(True)
    else:
        d.append(False)
d.append(False)
c = 0

for i in range(0, len(rfd)):
    #print(rfd[i], d[i])
    if d[i]:
        c += 1
print(c)
print(len(rfd), len(d))

for i in range(0, len(rfd) - 1):
    r1 = rfd[i].split(' ')
    r2 = rfd[i+1].split(' ')

    if r1[0] == r2[0]:
        d[i] = True

    print(len(rfd) - 1, i, rfd[i], rfd[i + 1])
c = 0
for i in range(0, len(d)):
    if d[i]:
        c += 1
print(c)

res = []
for i in range(len(rfd) - 1):
    if not d[i]:
        res.append(rfd[i])




e = open("rez_example_realx1.txt", 'w')
for i in range(len(rfd) - 1):
    v = rfd[i].split()[1]
    if not d[i]:
        if float(v) > 6.:
            spl = rfd[i-1].split()
            n = spl[0]
            v = spl[1]
            e.write('%s %s\n' % (n, v))
        else:
            spl = rfd[i].split()
            n = spl[0]
            v = spl[1]
            e.write('%s %s\n' % (n, v))
e.close()
# for i in res:
#     print(type(i))
#     e.write(i)
#     e.write('\n')
# e.close()