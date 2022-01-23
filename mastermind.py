import numpy as np
import random

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = "\033[93m"
BLUE = "\033[94m"
BLACK = "\033[37m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
ENDC = '\033[0m'


def is_correct(answer, code):
    return all((a==c for a,c in zip(answer, code)))

def check(answer, code):
    control = []
    for a, c in zip(answer, code):
        if a==c:
            control.append('+')
        elif a in code:
            control.append('o')
    return sorted(control)

if __name__ == "__main__":
    symbols = [str(i) for i in range(8)]
    random.shuffle(symbols)
    code = symbols[:4]
    print("Welkom bij kraak-de-code! Om te beginnen, "
        "geeft 4 cijfers in van 0 tem 7, en druk enter. "
        "Na iedere poging geeft een '+' aan dat een getal "
        "op de juiste plek staat. Een 'o' geeft aan dat een getal "
        " in de code zit, maar niet op de juiste plaats.")

    i = 0
    while True:
        i += 1
        answer = input()[:4]
        print("\033[A                             \033[A")

        if is_correct(answer, code):
            print(f"correct! {GREEN}{answer}{ENDC}")
            break
        control = "".join(check(answer, code))
        print(f"{i:2d}: {answer} | {control}")
