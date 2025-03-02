import random
import sympy
import re
from functools import lru_cache
expPool = [0, 0, 0, 1, 1, 1, 2, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8]
numPool = [0, 0, 1, 1, 2, 3, 114514, 2147483647, 2147483648, 2147483649, 4294967296, 998244353]

def genDate(deepNum):
    string = getExpr(deepNum)
    if (len(string) > 1000):
        return genDate(deepNum)
    return string


def remove_leading_zeros(text):
    return re.sub(r'\b0+(\d+)', r'\1', text)

@lru_cache(maxsize=None)
def calculate(string):
    return sympy.sympify(sympy.expand(remove_leading_zeros(string.replace('^','**').replace(" ", "").replace("\t","")), hints=pow))


def getExpr(deepNum):
    string, ans = getTerm(deepNum)
    termNum = random.randint(1, 5)
    r = random.uniform(0, 1)
    if (r < 0.35):
        string = getWhite() + "+" + getWhite() + string
    elif (r < 0.7):
        string = getWhite() + "-" + getWhite() + string
        ans = calculate("-(" + str(ans) + ")")
    else:
        string = getWhite() + string

    for i in range(termNum - 1):
        res = getTerm(deepNum)
        if (random.randint(0, 1)):
            string = string + getWhite() + "+" + getWhite() + res[0]
            ans = calculate(str(ans) + "+" + str(res[1]))
        else:
            string = string + getWhite() + "-" + getWhite() + res[0]
            ans = calculate(str(ans) + "-(" + str(res[1]) + ")")
    return string, ans


def getTerm(deepNum):
    string, ans = getFactor(deepNum)
    factorNum = random.randint(1, 5)
    r = random.uniform(0, 1)
    if (r < 0.35):
        string = getWhite() + "+" + getWhite() + string
    elif (r < 0.7):
        string = getWhite() + "-" + getWhite() + string
        ans = calculate("-(" + str(ans) + ")")
    else:
        string = getWhite() + string
    
    for i in range(factorNum - 1):
        res = getFactor(deepNum)
        string = string + getWhite() + "*" + getWhite() + res[0]
        ans = calculate("(" + str(ans) + ")*(" + str(res[1]) + ")")
    return string, ans


def getFactor(deepNum):
    r = random.uniform(0,1)
    if (deepNum > 0):
        if (r < 0.45):
            return getConFactor()
        elif (r < 0.9):
            return getPowFactor()
        else:
            return getExprFactor(deepNum - 1)
    else:
        if (r < 0.5):
            return getConFactor()
        else:
            return getPowFactor()


def getConFactor():
    string = ""

    rSign = random.uniform(0,1)
    if (rSign < 0.3):
        string = getWhite() + "+"
    elif (rSign <0.6):
        string = getWhite() + "-"

    rValue = random.uniform(0,1)
    if (rValue < 0.1):
        string = string + getZero() + str(random.choice(numPool))
    elif (rValue < 0.3):
        string = string + getZero() + str(random.randint(0,15))
    elif (rValue < 0.4):
        string = string + getZero() + str(random.randint(2147483647,4147483647))
    else:
        string = string + getZero() + str(random.randint(0, 100))

    return string, calculate(string)


def getPowFactor():
    string = ""
    string = string + getWhite() + "x" + getWhite() + "^"

    if (random.uniform(0,1) < 0.5):
        string = string + getWhite() + "+"
    string = string + str(random.choice(expPool))

    return string, calculate(string)


def getExprFactor(deepNum):
    res = getExpr(deepNum)
    if (random.uniform(0,1) < 0.3):
        return "(" + res[0] + ")", res[1]
    exp = str(random.choice(expPool))
    string = getWhite() + "(" + getWhite() + res[0] + getWhite() + ")" + getWhite() + "^" + exp
    ans = calculate("(" + str(res[1]) + ")^" + exp)
    return string, ans


def getWhite():
    string = ""
    r = random.uniform(0,1)
    if (r < 0.9):
        string = ""
    else:
        if (random.uniform(0,1) < 0.9):
            num = random.randint(1,2)
        else:
            num = random.randint(3,5)

        for _ in range(num):
            flag = random.randint(0,1)
            if flag == 0:
                string = string + ' '
            else:
                string = string + '\t'

    return string


def getZero():
    string = ""
    if (random.uniform(0, 1) < 0.8):
        return string

    num = random.randint(1,3)
    for i in range(num):
        string = string + "0"

    return string