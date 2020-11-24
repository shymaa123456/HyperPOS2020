
"""
#test
a = 12 ** 3

print(a)
aa = "welcome"
print(aa[0]) # w

if a != 144:
    print(False,a)
else:
    print (True,a)


def funcc( aaa ,  aab , aac ):
    print("xxx")
funcc("","","")


class teste:
    pass

class test2:
    def __init__(self, h1, h2):
        print("xxx0")



class oop:
    def  __init__(self,h1,h2):
        self.h11 = h1
        self.h22 = h2

        print(self.h11 * self.h22)
oop(12,22)
000"""

""" 
# class inheritance test
class Obj:
    __width = None
    __height = None

    def dsals(self, widths, heights):
        self.__width = widths
        self.__height = heights
        print(self.__width * self.__height)


class Obj1(Obj):

    def rets(self, widths1, heights1):
        return self.dsals(widths1, heights1)


odd = Obj1()
odd.rets(12, 12)
"""

for x in range(20000):
    print(x)

ii = 1
while ii <= 5:
    """if ii == 2:
        continue
    else:
        break"""

    print(ii)
    ii += 1
