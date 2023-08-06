#coding:UTF-8
import time
import os
import random
import getpass
__all__ = ['versions','checkClass','wait','randint','garbledCode','pausePrint','captcha','judge','how','shutdown','hideInput']
"""
"""
print("Welcome use civilianM,enter 'how()' can View introduction. version：1.14.97")
def how():
    print("""欢迎使用civilianM库，同时欢迎你来访此处！
以下是civilianM库中的函数，我也会在有空的时间更新！
	checkClass(objects,need)
		该函数可以检查需检测对象的类型
			#checkClass("91874",'int') False
		"need"可选参数：'str','int','list','dict','float','tuple'
	wait(t)
		该函数和sleep没有区别
			#wait(0.3)
		't'必须是浮点数或整数
	randint(mins,maxs)
		该函数和randint没有区别
			#randint(1,4)
	garbledCode(digit,types)
		该函数可以产生一个乱码
			#garbledCode(30)  55ebaca550cfde7ff55fa800cf266c
		'digit'必须是整数
		'types'可以是None，也可以是Upper
			#garbledCode(30,types='Upper') AD224AFDFE82EE5691C05C598C86EB
	pausePrint(content,pause=0.2)
		该函数可以每0.2秒（可更改）打出一个字
			#pausePrint('Hello',pause=0.3) H -> He -> Hel -> Hell -> Hello
		'pause'必须是整数或浮点数
	captcha()
		该函数可以生成验证码，captcha全称（Completely Automated Public Turing Test to Tell Computers and Humans Apart）
			#captcha() 7TPh
		该函数无任何参数
	judge(ask,right,return_,r2=None)
		判断。
			#judge('1+1=','2','truefalse') 1+1=3 False
		r2是第二个正确答案
			#judge("Install?(Y/N)",'Y','yesno',r2='N') Install?(Y/N)N 'no'
		'return_'可选参数：'truefalse','yesno'
		当return_是'truefalse'，如果回复不是right和r2，会返回None，如果回复是r2，返回False，如果回复等于right，返回True
		当return_是'yesno'，如果回复不是right和r2，会返回None，如果回复是r2，返回'no'，如果回复等于right，返回'yes'
	shutdown()
                                该函数亿分危险！
                                Watch out!
                hideInput(con)
                                该函数可以隐藏信息
                                                #a=hideInput('password:")/print(a)          password:       1948
	就这样，不见不散！""")
"""show version"""
def versions():
    print("1.14.97")
"""
This function can check any return value
Have's parameter:
    str
    list
    dict
    int
    float
Example:
    i = 123
    l = [123]
    checkClass(i,'int') True
    checkClass(l,'str) False
"""
def checkClass(objects,need):
    if need == 'str':
        return type(objects) is type('')
    elif need == 'list':
        return type(objects) is type([])
    elif need == 'dict':
        return type(objects) is type({})
    elif need == 'int':
        return type(objects) is type(1)
    elif need == 'float':
        return type(objects) is type(0.1)
    elif need == 'tuple':
        return type(objects) is type(())
    else:
        raise AttributeError("In checkClass this function,No "+str(need)+" this attribute")

#Sleep
def wait(t):
    if checkClass(t,'float') or checkClass(t,'int'):
        time.sleep(t)
    else:
        raise ValueError("You enter's result must is a int/float-number")

#Randomly generated number
def randint(mins,maxs):
    if checkClass(mins,'int') == False or checkClass(maxs,'int') == False:
        raise ValueError("You enter's result must is a int/float-number")
    if maxs == mins:
        raise ValueError("Max-number cannot equal to min-number")
    elif mins > maxs:
        raise ValueError("Min-number cannot greater than max-number")
    return random.randint(mins,maxs)

"""
A Garbled code,You can say this is UUID,But this isnt,Because UUID have '-'
This function haves type:(Example)
    None : bf10c5b5fa826fa52e2d0f
    Upper:BF10C5B5FA826FA52E2D0F
"""
def garbledCode(digit=20,types=None):
    result = ""
    if types == None or types == 'Upper':
        pass
    else:
        raise AttributeError('GarbledCode this function has not have '+str(types)+'  this parameter')
    np= ""
    standard = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f']
    if checkClass(digit,'int')==False:
        raise ValueError("You enter's result must is a not string number!")
    for n in range(digit):
        np = standard[randint(0,15)]
        if types == 'Upper':
            if checkClass(np,'str'):
                result += np.upper()
            else:
                result += str(np)
        else:
            result += str(np)
    return result

"""
In:cm.pausePrint('123456')
Out:123456(have sleep)
"""
def pausePrint(*content,pause=0.2):
    if checkClass(pause,'float') or checkClass(pause,'int'):
        for tex in content:
            for prin in tex:
                print(prin,end='',flush=True)
                wait(pause)
            print(" ",flush=True,end="")
        print("\n",flush=True,end="")
    else:
        raise ValueError("You enter's result must is a int/float-number")
    
"""
Completely Automated Public Turing Test to Tell Computers and Humans Apart(CAPTCHA)
IN: cm.captcha()
OUT:JD8y
"""
def captcha():
    capt = ''
    N = [1,2,3,4,5,6,7,8,9,0,'a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M',
         'n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z']
    for n in range(4):
        capt += str(N[randint(0,57)])
    return capt

"""
Judge.
in :b =  cm.judge(ask='HOW ARE YOU:',right='32',return_='yesno')
out: HOW ARE YOU : 32
out: yes
if 'fuck' this parameter have value,that have two answer,if answer !== any answer,else return None
"""
def judge(ask,right,return_,r2=None):
    if return_ == 'yesno' or return_ == 'truefalse':
        pass
    else:
        raise AttributeError('judge this function has not have '+str(return_)+'  this parameter')
    if checkClass(right,'str') == False:
        right = str(right)
    n = input(ask)
    if n == right:
        if return_ == 'yesno':
            return 'yes'
        elif return_ == 'truefalse':
            return True
        else:
            raise IOError("unknown error")
    elif r2 != None and n != right :
        if n != right and n != r2:
            return None
        if return_ == 'yesno':
            return 'no'
        elif return_ == 'truefalse':
            return False
        else:
            raise IOError("unknown error")
    else:
        if return_ == 'yesno':
            return 'no'
        elif return_ == 'truefalse':
            return False
        else:
            raise IOError("unknown error")
"""
Watch out your computer,because if this code is action,your computer will shutdown
"""
def shutdown():
    os.system("shutdown -p")
"""Hide content"""
def hideInput(con):
    getpass.getpass(con)
    
