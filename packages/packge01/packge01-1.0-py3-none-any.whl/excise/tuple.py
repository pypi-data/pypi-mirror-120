import copy

# 原始对象
a = [1, 2, 3, 4, ['a', 'b']]
# 对b赋值, 地址的传递
b = a
# 浅拷贝
c = copy.copy(a)
c1 = a.copy()
# 深拷贝
d = copy.deepcopy(a)
# 修改a对象
a.append(5)
a[4].append('c')
print('a= ', a)
print('b= ', b)
print('c= ', c)
print('c1= ', c1)
print('d= ', d)
