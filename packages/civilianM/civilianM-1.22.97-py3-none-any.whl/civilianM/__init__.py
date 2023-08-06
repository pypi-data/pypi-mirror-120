#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : MAIN
#Now version: V1.22.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
import time
import platform
import os
import random
import winreg
import requests
import json
import getpass
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

__all__ = ['versions','checkClass','wait','randint','garbledCode','pausePrint','captcha',
           'judge','how','shutdown','hideInput','justNow','openFolder','getAddress','checkUpdate']
"""
"""
print("Welcome use civilianM,enter 'how()' can View introduction. version：1.22.97")
def checkUpdate():
    global v
    dd = []
    r = requests.get('https://pypi.org/project/civilianM/#history')
    s = bs(r.text,'lxml')
    d = s.find_all('p',class_='release__version')
    for nn in d:
        ev = nn.text.strip()
        dd.append(ev)
    if dd[0] != versions:
        print('You are using '+versions()+',A new version is available:'+dd[0])
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
                justNow()
                                该函数可以返回当前时间
                                #justNow() 2021921 16:15:31
                getAddress()
                                该函数可以获取你所在IP、运营商、省份、城市、国家
                                    #getAddress()
                openFolder(filename/folder)
                                该函数会打开一个文件夹
	就这样，不见不散！""")
"""show version"""
def versions():
    return "1.22.97"
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
        raise ValueError("You enter's result must is a int-number")
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
"""
Hide content
"""
def hideInput(con):
    a = getpass.getpass(con)
    return a
"""
Return now date
"""
def justNow():
    b = dt.today()
    return b.strftime("%Y-%m-%d %H:%M:%S")
"""
Open a folder
if is not exists,create
"""
def openFolder(fn):
    def efve():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0] + "/"
    if fn:
        nh = efve() + fn
    if not os.path.exists(nh):
            os.mkdir(nh)
    else:
        nh = os.getcwd()

    if platform.system() == "Windows":
        os.startfile(nh)

    return nh + "/"
"""
get address
return:
    {country,province/region,city,ip,isp}
"""
def getAddress():
    try:
        re = requests.get('https://ipw.cn/api/ip/locate')
    except:
        raise IOError("No network connect.Please check network status")
    d = json.loads(re.text)
    PR = d['Address']['Province']
    ISP = "中国"+d['ISP']
    if PR == '广西' or PR == '内蒙古' or PR == '宁夏' or PR == '新疆':
        if PR == '广西':
            PR += '壮族自治区'
        if PR == '内蒙古':
            PR += '自治区'
        if PR == '宁夏':
            PR += '回族自治区'
        if PR == '新疆':
            PR += '维吾尔自治区'
    else:
        PR += '省'
    C = d['Address']['City'] + '市'
    nr = {'Country':d['Address']['Country'],'Province/Region':PR,'City':C,'IP':d['IP'],'ISP':ISP}
    return nr
        
    
    
