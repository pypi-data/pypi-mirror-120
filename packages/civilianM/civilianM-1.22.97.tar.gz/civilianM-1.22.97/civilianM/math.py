#coding:UTF-8
#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : aux / math
#Now version: V1.22.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
import math
import civilianM
def pi():
    return math.pi
def add(n1,n2):
    if civilianM.checkClass(n1,'float') or civilianM.checkClass(n1,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    if civilianM.checkClass(n2,'float') or civilianM.checkClass(n2,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    return n1+n2
def sub(n1,n2):
    if civilianM.checkClass(n1,'float') or civilianM.checkClass(n1,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    if civilianM.checkClass(n2,'float') or civilianM.checkClass(n2,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    return n1-n2
def mul(n1,n2):
    if civilianM.checkClass(n1,'float') or civilianM.checkClass(n1,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    if civilianM.checkClass(n2,'float') or civilianM.checkClass(n2,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    return n1*n2
def div(n1,n2):
    if civilianM.checkClass(n1,'float') or civilianM.checkClass(n1,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")
    if civilianM.checkClass(n2,'float') or civilianM.checkClass(n2,'int'):
        pass
    else:
        raise ValueError("You enter's result must is a int/float-number")

    try:
        return n1/n2
    except:
        raise AttributeError("Cant divide 0")
def how():
    print("""欢迎使用civilianM.math库
            函数介绍：
            add(num1,num2) / 1+1 = 2
            sub(num1,num2) / 1-1=0
            mul(num1,num2) / 3*3 = 9
            div(num1,num2) / 4/2 =2""")
