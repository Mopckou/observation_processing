# a = [5, 1, 6, 8, 9, 4, 3, 10, 2, 7, 11, 15, 12, 18, 19, 20, 55, 66, 33, 21]
#
# # def section_sort(a, n):
# #     elems = len(a)
# #     for min in range(0, elems - 1):
# #         ind = min
# #
# #         for j in range(min + 1, elems):
# #             if a[j] < a[ind]:
# #                 ind = j
# #
# #         tmp = a[min]
# #         a[min] = a[ind]
# #         a[ind] = tmp
# #
# # section_sort(a, 10)
# # print(a)
#
# # def binary_search(a, value):
# #     n = len(a)
# #     if n == 1:
# #         if a[0] == value:
# #             return True
# #         else:
# #             return False
# #     print(a)
# #     if a[n//2] < value:
# #         return binary_search(a[(n//2):], value)
# #     elif a[n//2] > value:
# #         return binary_search(a[0:(n//2)], value)
# #     elif a[n//2] == value:
# #         return True
# #     else:
# #         return False
# #
# # b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # print(binary_search(b, 10))
#
# def concat(a, b):
#     return a.extend(b)
#
# def concat2(i, n):
#     a = []
#     a.append(i)
#     a.extend(n)
#     return a
#
# def merge(a, b):
#     if not a:
#         return b
#
#     if not b:
#         return a
#
#     if a[0] < b[0]:
#         return concat2(a[0], merge(a[1:], b))
#
#     elif a[0] > b[0]:
#         return concat2(b[0], merge(a, b[1:]))
#
#
# def __merge(a, b):
#     new_massive = []
#     for i in range(0, len(a)+len(b)):
#         if not a:
#             break
#
#         if not b:
#             break
#
#         if a[0] < b[0]:
#             new_massive.append(a[0])
#             a.pop(0)
#         elif a[0] > b[0]:
#             new_massive.append(b[0])
#             b.pop(0)
#
#     if a:
#         new_massive.extend(a)
#     if b:
#         new_massive.extend(b)
#
#     return new_massive
#
#
# def merge_sort(a):
#     if len(a) == 1:
#         return a
#     middle = len(a)//2
#
#     lefthalf = a[0: middle]
#     righthalf = a[middle:]
#     return merge(merge_sort(lefthalf), merge_sort(righthalf))
#
#
# c = [1, 4, 7, 9, 11, 14, 16, 17, 18]
# d = [2, 3, 5, 8, 10, 12, 13]
#
# #print(__merge(c, d))
#
# print(merge_sort(a))

a = [1, 2, 3]
b = [4, 5, 6]
c = []
c.extend(a)
c.extend(b)
print(c)

#[8128, 11359, 8314, 11181, 8098, 11367, 8284, 11172, 18147, 18318, 21855, 8034, 11265, 21088, 8221, 11087, 8004, 11274, 8191, 11078, 21088]
#[8004, 8034, 8098, 8128, 8191, 8221, 8284, 8314, 11078, 11087, 11172, 11181, 11265, 11274, 11359, 11367, 18147, 18318, 21088, 21088, 21855]

a = [(2, 0), (1, 0), (2, 3), (4, 0), (1, 3)]

print(sorted(a, key=lambda x: (x[1], x[0])))
import datetime
c = [('14:02:42.862', 2, 432423), ('14:02:42.724', 2, 23425), ('15:02:43.000', 2, 33333), ('-14:-02:-43.1-38', 1, 54), ('12:02:43.276', 3, 4444444), ('14:02:43.414', 2), ('14:02:43.552', 0)]
def f(val):
    try:
        d = datetime.datetime.strptime(val, '%H:%M:%S.%f')
    except:
        d = datetime.datetime.strptime('0:0:0.0', '%H:%M:%S.%f')

    return d
#t = datetime.datetime.strptime(x, '%H:%M:%S.%f')
# [('14:02:43.552', 0), ('14:02:43.138', 1), ('14:02:42.724', 2), ('14:02:42.862', 2), ('14:02:43.414', 2), ('15:02:43.000', 2), ('12:02:43.276', 3)]

c = sorted(c, key=lambda x: (x[1], f(x[0])))
print(c)