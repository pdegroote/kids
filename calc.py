import random
import datetime
import operator
from typing import Tuple

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
MAX_SUM = 20
TYPES = {'add':'+', 'sub':'-'}
OPS = {'add':operator.add, 'sub':operator.sub}

def get_number(upper=None):
    upper = upper if upper is not None else MAX_SUM
    return random.randint(0, upper)

def get_type():
    types = list(TYPES.keys())
    return types[random.randint(0,len(types)-1)]

def generate(type: str='SUM')-> Tuple[int,int,int]:
    a = get_number()
    b = get_number(upper=MAX_SUM-a) if type == 'add' else get_number(upper=a)
    c = OPS[type](a, b)
    return a, b, c

def main():
    score = 0
    total = 10
    current = 0

    answer = input("Naam: ")
    report = open(f"logs/calc_{answer}_{'_'.join(str(datetime.datetime.now()).split()).split('.')[0]}.txt", 'w')

    t = get_type()
    a, b, c = generate(t)
    while True:
        answer = input(f"{a} {TYPES[t]} {b} = ")
        try:
            result = int(answer)
            correct = result == c
            if correct:
                print(f"{OKGREEN}Proficiat!{ENDC}")
                report.write(f"+ {a} {TYPES[t]} {b} = {result}\n")
            else:
                print(f"{FAIL}Fout, het juiste antwoord was {a} {TYPES[t]} {b} = {OPS[t](a, b)}{ENDC}")
                report.write(f"- {a} {TYPES[t]} {b} != {result}\n")
            score += correct
            t = get_type()
            a, b, c = generate(t)
            current += 1
        except:
            print("Resultaat is geen getal, probeer opnieuw")
        
        if current == total:
            msg = f"===== Testje afgelopen! ======\nJe score is: {score} / {total}\n"
            print(msg)
            report.write(msg)
            score = 0
            current = 0
        
        report.flush()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Sommetjes")
    parser.add_argument("--max", type=int, default=20, help="Grootste getal dat in de sommetjes mag voorkomen.")
    parser.add_argument("--bewerkingen", default="+-", help="Bewerkingen die mogen voorkomen")
    args = parser.parse_args()
    MAX_SUM = args.max
    TYPES = dict()
    for op in args.bewerkingen:
        if op=='+':
            TYPES['add'] = '+'
        elif op=='-':
            TYPES['sub'] = '-'
    main()
