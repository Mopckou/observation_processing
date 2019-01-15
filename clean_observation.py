of = open('file_obs92cm.txt')

f = of.read()

sf = f.split('\n')

new_obs = []
print(len(sf))
for num, v in enumerate(sf[:-1]):  # удаляем повторяющиеся элементы
    if v == sf[num + 1]:
        continue
    new_obs.append(v)

print(len(new_obs))

new_obs2 = []
for num, v in enumerate(new_obs[:-1]):  # удаляем элементы с одинаковым временем
    vlist = v.split()
    x = vlist[0]
    y = vlist[1]

    vlist2 = new_obs[num + 1].split()
    x2 = vlist2[0]
    y2 = vlist2[1]

    if x == x2:
        continue
    new_obs2.append(v)

print(len(new_obs2))

o = open('file_obs92c_new.txt', 'w')
y_old = 0
for i in new_obs2:  # записываем значения в файл
    vlist = i.split()
    x = int(vlist[0])
    y = float(vlist[1])

    if y > 3 or y < 1.6:
        o.write("%s %s\n" % (x, y_old))
    elif y == 0:
        o.write("%s %s\n" % (x, y_old))
    else:
        o.write("%s %s\n" % (x, y))
    x_old = x
    y_old = y
o.close()