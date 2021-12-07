import concurrent.futures
import argparse
import math
from time import time


def get_solution(arg_a, arg_b, D, flag = True):
    return (-arg_b + math.sqrt(D)) / (2 * arg_a) if flag else (-arg_b - math.sqrt(D)) / (2 * arg_a)


def check_type_int(input_data):
    while True:
        try:
            int(input_data)
            return int(input_data)
        except ValueError:
            return None
# python QuadraticEquation.py -a 2 -b 2 -c 3
# python QuadraticEquation.py -a 1 -b 7 -c 6

parser = argparse.ArgumentParser(description="QuadraticEquation")
parser.add_argument("-a", dest="a")
parser.add_argument("-b", dest="b")
parser.add_argument("-c", dest="c")
args = parser.parse_args()
arg_a = check_type_int(args.a)
arg_b = check_type_int(args.b)
arg_c = check_type_int(args.c)


def one_thread():
    print("Решение задачи однопоточно: ")
    time1 = time()
    D = arg_b * arg_b - 4 * arg_a * arg_c
    solution1 = None
    solution2 = None
    for i in range(1000):
        if arg_a == 0 and arg_b != 0:
            solution1 = -arg_c / arg_b
        elif D == 0:
            solution1 = -arg_b / (2 * arg_a)
        elif D > 0:
            solution1 = get_solution(arg_a, arg_b, D)
            solution2 = get_solution(arg_a, arg_b, D, False)
        else:
            pass
    if solution1 is None:
        print("Корней нет")
    elif solution2 is not None:
        print(str(solution1) + " " + str(solution2))
    else:
        print(solution1)
    print(time() - time1)


def multi_thread():
    print("Решение задачи многопоточно: ")
    time2 = time()
    D = arg_b * arg_b - 4 * arg_a * arg_c
    solution1 = None
    solution2 = None
    for i in range(1000):
        if arg_a == 0 and arg_b != 0:
            solution1 = -arg_c / arg_b
        elif D == 0:
            solution1 = -arg_b / (2 * arg_a)
        elif D > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                solution1 = executor.submit(get_solution, arg_a, arg_b, D)
                solution2 = executor.submit(get_solution, arg_a, arg_b, D, False)
        else:
            pass
    if solution1.result() is None:
        print("Корней нет")
    elif solution2.result() is not None:
        print(str(solution1.result()) + " " + str(solution2.result()))
    else:
        print(solution1.result())
    print(time() - time2)


if arg_a is None:
    print("Введено некорректное значение коэффициента а")
elif arg_b is None:
    print("Введено некорректное значение коэффициента b")
elif arg_c is None:
    print("Введено некорректное значение коэффициента c")
else:
    one_thread()
    multi_thread()

