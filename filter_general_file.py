# of = open('out_6_92cm.tmi')
#
# f = of.read()
#
# sf = f.split('\n')[15:-1]
#
# fr = open('file_obs92_c.txt', 'w')
# for line in sf:
#     split_line = line.split()
#     x = split_line[0]
#     y = split_line[17]
#     fr.write('%s %s\n' % (x, y))
# fr.close()
import numpy
a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4]

print(numpy.var(a, ddof=1))