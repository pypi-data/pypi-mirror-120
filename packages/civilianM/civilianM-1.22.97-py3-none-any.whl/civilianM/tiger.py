import civilianM as cm
#coding:UTF-8
#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : AUX/ For wang-jin-hu Only
#Now version: V1.22.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
"""
xh="你昧着良心说话！"
bb="不要瞎填"
print("Welcome to use CM,Module for XIAO-HU only")
p = cm.judge("小虎帅吗（Y/N）",'Y','truefalse',r2='N')
if p:
    raise AttributeError(xh)
elif p == None:
    raise AttributeError(bb)
else:
    b = cm.judge("想不想撕票小虎（Y/N）","Y",'truefalse',r2='N')
    if b:
        print("这才对")
    elif p == None:
        raise AttributeError(bb)
    else:
        raise AttributeError(xh)
"""
class n():
    def __init__(self):
        xh="你昧着良心说话！"
        bb="不要瞎填"
        print("Welcome to use CM,Module for XIAO-HU only")
        p = cm.judge("小虎帅吗（Y/N）",'Y','truefalse',r2='N')
        if p:
            raise AttributeError(xh)
        elif p == None:
            raise AttributeError(bb)
        else:
            b = cm.judge("想不想撕票小虎（Y/N）","Y",'truefalse',r2='N')
            if b:
                print("这才对")
                return None
            elif p == None:
                raise AttributeError(bb)
            else:
                raise AttributeError(xh)
#sb = n()
