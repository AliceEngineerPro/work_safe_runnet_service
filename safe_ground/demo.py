# 生成器的send用法 generator.send(value)
def test():
    i = 1
    while i < 100:
        temp = yield i ** 2
        print(temp)
        i += 1


t = test()
print(t.__next__())
# send的作用相当于使生成器继续运行，并且传递的参数为yield的返回值(程序中即temp的值)
print(t.send("Hello World"))
print(t.__next__())  # 相当于send(None) 此时temp = None