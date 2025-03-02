import subprocess
from subprocess import STDOUT, PIPE
import os
import glob
import sympy
from generate import getExpr, remove_leading_zeros, calculate
import time
from colorama import Fore, Back, Style
import signal

def execute_java(stdin, name):
    cmd = ['java', '-jar', name]
    start_time = time.time()
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    end_time = time.time()
    stdout, stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip(), end_time - start_time


def evaluate(string1, poly, name):
    out, t = execute_java(poly, name)
    outChange = out.replace('^', '**')
    string2 = sympy.parse_expr(outChange)
    if (sympy.simplify(string1).equals(string2)):
        if (len(str(string1).replace(" ", "").replace("**", "^")) < len(out)):
            print(name + ": " + Fore.YELLOW + "Problem\n" + Fore.WHITE)
            print("Expected length is " + str(len(str(string1).replace(" ", "").replace("**", "^"))) + " but got " + str(len(out)))
            print("Answer:\n" + str(string1).replace(" ", "").replace("**", "^") + "\n\n" + name + ":\n" + out)
            # input("")
        else:
            print(name + ": " + Fore.GREEN + "Accepted" + Fore.WHITE)
        return True, t
    else:
        print(name + ": " + Fore.RED + "Wrong\n" + Fore.WHITE)
        print("Origin:\n" + str(poly) + "\n\n" + "Answer:\n" + str(string1).replace(" ", "").replace("**", "^") + "\n\n" + name + ":\n" + out)
        return False, t

print("============ INITIALIZATION ============")
x = sympy.Symbol('x')
directory = './'
jar_files = glob.glob(os.path.join(directory, '*.jar'))
for jar_file in jar_files:
    print(jar_file)

times = {}
for jar_file in jar_files:
    times[jar_file] = 0

input("Press Enter to continue...")

print("=========== EVALUATION BEGIN ===========")
os.system('cls' if os.name == 'nt' else 'clear')
i = 0
while True:
    i += 1
    print("-->   epoch " + str(i))
    poly, ans = getExpr(1)
    # ans = calculate(poly)
    # print("Best answer: " + str(ans))
    for jar_file in jar_files:
        try:
            res, t = evaluate(ans, poly, str(os.path.basename(jar_file)))
            if (res == False):
                exit()
            times[jar_file] += t
            pass
        except Exception as e:
            print("Origin Input: " + poly)
            print(os.path.basename(jar_file) + ": no output or output is illegal")
            print(e)
            exit()
    
    time.sleep(0.75)
    os.system('cls' if os.name == 'nt' else 'clear')

print("=========== EVALUATION END ===========")
for jar_file in jar_files:
    print(jar_file + " " + str(times[jar_file]/i))