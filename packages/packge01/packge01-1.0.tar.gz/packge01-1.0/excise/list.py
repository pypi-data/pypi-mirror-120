# 定义空列表
lt = list()

# 增加5给元素
lt = [1, 2, 3, 4, 5]
lt[1] = '修改第二个元素'
lt.insert(1, "2位置增加元素")
# 删除第一个元素
# del lt[0]
# 删除1-3位置元素
# [1, '2位置增加元素', '修改第二个元素', 3, 4, 5]
del lt[1:3]
# [1, 3, 4, 5]

# 判断it是否有0
print(0 in lt)

lt.append(0)
# 返回0的索引
print(lt)
print(lt.index(0))
print(len(lt))
print(lt.clear())