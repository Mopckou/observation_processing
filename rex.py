# n = open('rez_example_realx1.txt')
# r = n.read()
# m = r.split('\n')[:-1]
#
# n2 = open('rez_new_example_realx1.txt', 'w')
# for i in range(len(m)):
#     n2.write('%s %s\n' % (i, m[i].split()[1]))
#
# n2.close()

n = open('file_obs92_c.txt')
r = n.read()
m = r.split('\n')[:-1]

n2 = open('file_obs92cm_cifra_version3.txt', 'w')
for i in range(len(m)):
    s = m[i].split()
    num = int(s[0])
    val = s[1]
    n2.write('%s %s\n' % (int(num/1000), val))

n2.close()
