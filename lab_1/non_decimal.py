from math import ceil
from polynomial_non_decimal import find_picar_pols, solve_pol, print_pol, print_pol_v2
from time import time


def numerical_explicit_v2(x_arr, step):
    n = len(x_arr)
    y_arr = [0]
    error = 'Переполнение'

    for i in range(n - 1):
        y_old = y_arr[-1]

        try:
            y = y_old + step * (x_arr[i] ** 2 + y_old ** 2)
        except OverflowError:
            for i in range(n - i - 1):
                y_arr.append(error)
            break

        y_arr.append(y)

    return y_arr


def numerical_implicit_v2(x_arr, step):
    n = len(x_arr)
    y_arr = [0]
    error_d = 'D < 0'

    for i in range(n - 1):
        y_old = y_arr[-1]

        d = 1 - 4 * step * (y_old + step * x_arr[i + 1] ** 2)

        if d < 0:
            for i in range(n - i - 1):
                y_arr.append(error_d)
            break
        else:
            y = (1 - pow(d, 0.5)) / (2 * step)

        y_arr.append(y)

    return y_arr


def picar_v2(x_arr, iterations):
    n = len(x_arr)
    res = [[0] for i in range(len(iterations))]

    pols = find_picar_pols(max(iterations))

    for i in range(n - 1):
        for j in range(len(iterations)):
            res[j].append(solve_pol(pols[iterations[j] - 1], x_arr[i + 1]))

    return res, pols


def output(s):
    if type(s) == float:
        if s > 1000000:
            return '{:.8e}'.format(s)
        return '{:.8f}'.format(s)
    elif type(s) == int:
        return str(s)
    else:
        return s


def print_table(x_arr, num_ex_arr, num_im_arr, picar_arr, picar_iters):
    output_step = 100
    n = len(x_arr)

    print('|    x    ', end='')
    for it in picar_iters:
        print('|   Пикара ' + str(it) + '    ', end='')
    print('|     Явный     |    Неявный    |')
    print("-" * (45 + 15 * len(picar_iters)))

    for i in range(0, n, output_step):
        print('|{:^9.5f}'.format(x_arr[i]), end='')
        for p in picar_arr:
            print('|{:^15.8f}'.format(p[i]), end='')
        print('|{:^15s}|{:^15s}|'.format(output(num_ex_arr[i]), output(num_im_arr[i])))


def main():
    beg = 0
    end = 1.0
    step = 0.00001
    picar_iters = [1, 2, 3, 4]

    header = ['X']
    for i in picar_iters:
        header.append(str(i) + ' приближение Пикара')
    header += ['Явная схема', 'Неявная схема']
    n = ceil(abs(end - beg) / step) + 1
    x_arr = [step * i for i in range(n)]

    t1 = time()
    num_ex_arr = numerical_explicit_v2(x_arr, step)
    t2 = time()
    num_im_arr = numerical_implicit_v2(x_arr, step)
    t3 = time()
    picar_arr, pols = picar_v2(x_arr, picar_iters)
    t4 = time()

    print(t2 - t1, t3 - t2, t4 - t3)

    print_table(x_arr, num_ex_arr, num_im_arr, picar_arr, picar_iters)
    for i in picar_iters:
        print_pol(pols[i - 1])


if __name__ == '__main__':
    main()
