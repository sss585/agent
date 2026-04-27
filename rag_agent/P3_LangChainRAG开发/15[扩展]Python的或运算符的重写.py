
class Test(object):
    def __init__(self, name):
        self.name = name

    def __or__(self, other):
        return MySequence(self, other)#左、右#直接用列表没法继续往下传递，只能再包装（用一个类不就行）

    def __str__(self):
        return self.name


class MySequence(object):
    def __init__(self, *args):#self和传入的参1223数
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)

    def __or__(self, other):
        self.sequence.append(other)
        return self

    def run(self):
        for i in self.sequence:
            print(i)


if __name__ == '__main__':#python会为每个文件赋值，作为主程序即为__main__
    a = Test('a')
    b = Test('b')
    c = Test('c')
    e = Test('e')
    f = Test('f')
    g = Test('g')

    d = a | b | c | e | f | g  # a.__or__(b)
    d.run()
    print(type(d))
