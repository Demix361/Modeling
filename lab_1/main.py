from decimal import Decimal, Overflow, ROUND_DOWN
from polynomial import find_picar_pols, solve_pol, print_pol, solve_pol_mp
from prettytable import PrettyTable
from time import time
from multiprocessing import Process, Queue, Pool


class PolMember:
    def __init__(self, power, denominator):
        self.power = power
        self.denominator = denominator


# Численный метод - явная схема
def numerical_explicit_table(beg, end, step):
    x = beg
    table = [(x, Decimal(0))]

    while x + step <= end:
        if table[-1][1] != 'переполнение':
            y = numerical_explicit(x, table[-1][1], step)
        else:
            y = None

        x += step

        table.append((x, y))

    return table


# Численный метод - явная схема
def numerical_explicit(x, y_old, h):
    try:
        y = y_old + h * (x ** 2 + y_old ** 2)
        return y
    except Overflow:
        return 'переполнение'


# Численный метод - неявная схема
def numerical_implicit_table(beg, end, step):
    x = beg
    table = [(x, Decimal(0))]

    while x + step <= end:
        x += step
        y = numerical_implicit(x, table[-1][1], step)

        table.append((x, y))

    return table


# Численный метод - неявная схема
def numerical_implicit(x, y_old, h):
    if y_old != 'D < 0':
        d = 1 - 4 * h * (y_old + h * (h + x) ** 2)
        if d < 0:
            return 'D < 0'
        else:
            return (1 - pow(d, Decimal(0.5))) / (2 * h)
    else:
        return 'D < 0'


# Возвращает таблицу с нужными приближениями Пикара
def picar_table(beg, end, step, iterations):
    x = beg
    table = []

    pols = find_picar_pols(max(iterations))

    while x <= end:
        table.append([x])

        for it in iterations:
            table[-1].append(solve_pol(pols[it - 1], x))

        x += step

    return table, pols


# ========================================== many queues

def picar_table_mp_v3(beg, end, step, iterations, p_amount):
    x = beg
    procs = []
    x_q = Queue()
    pols = find_picar_pols(max(iterations))
    y_qs = [Queue() for i in iterations]

    while x <= end:
        x_q.put(x)
        x += step

    for i in range(p_amount):
        proc = Process(target=picar_proc_v3, args=(x_q, pols, iterations, y_qs))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    x_q.close()

    table = []
    y_arr = [[] for i in range(len(iterations))]

    for i in range(len(iterations)):
        while not y_qs[i].empty():
            y_arr[i].append(y_qs[i].get())

    for i in range(len(iterations)):
        y_arr[i].sort()

    for q in y_qs:
        q.close()

    j = 0
    while x <= end:
        table.append([x])
        for i in range(len(iterations)):
            table[-1].append(y_arr[i][j])
        x += step
        j += 1

    return table, pols


def picar_proc_v3(x_q, pols, iterations, y_qs):
    n = len(iterations)

    while not x_q.empty():
        x = x_q.get()

        for i in range(n):
            y_qs[i].put(solve_pol(pols[iterations[i] - 1], x))
# ==========================================



# ================================================= Pool - memory error
def picar_table_mp_v2(beg, end, step, iterations):
    x = beg

    pols = find_picar_pols(max(iterations))
    args = []

    while x <= end:
        args.append([x, pols, iterations])

    with Pool() as pool:
        table = pool.starmap(picar_proc_v2, args)

    table.sort()

    return table, pols


def picar_proc_v2(x, pols, iterations):
    res = [x]

    for it in iterations:
        res.append(solve_pol(pols[it - 1], x))

    return res
# =================================================



#======================================================== default mp - not working why???
def picar_table_mp(beg, end, step, iterations, p_amount):
    x = beg
    x_arr = []
    while x <= end:
        x_arr.append(x)
        x += step

    table = []
    procs = []
    q = Queue()
    pols = find_picar_pols(max(iterations))

    for i in range(p_amount):
        proc = Process(target=picar_proc, args=(x_arr, pols, iterations, i, p_amount, q))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print('here')

    while not q.empty():
        table += q.get()

    q.close()
    q.join_thread()

    table.sort()

    return table, pols


def picar_proc(x_arr, pols, iterations, p_num, p_amount, q):
    res = []

    for i in range(p_num, len(x_arr), p_amount):
        res.append([x_arr[i]])
        print(x_arr[i])

        for it in iterations:
            res[-1].append(solve_pol(pols[it - 1], x_arr[i]))

    q.put(res)
#========================================================



def calculate(beg, end, step, picar_iters):
    beg = Decimal(beg)
    end = Decimal(end)
    step = Decimal(step)
    
    table = []
    header = ['X']
    for i in picar_iters:
        header.append(str(i) + ' приближение Пикара')
    header += ['Явная схема', 'Неявная схема']

    #t_1 = time()
    num_ex_res = numerical_explicit_table(beg, end, step)
    #print(time() - t_1)

    #t_1 = time()
    num_im_res = numerical_implicit_table(beg, end, step)
    #print(time() - t_1)

    t_1 = time()
    picar_res, pols = picar_table_mp_v3(beg, end, step, picar_iters, 8)
    print('picar: ', time() - t_1)

    size = len(num_ex_res)
    for i in range(size):
        table.append([])
        table[-1].append(num_ex_res[i][0])

        for j in range(len(picar_iters)):
            table[-1].append(picar_res[i][j + 1])
        table[-1].append(num_ex_res[i][1])
        table[-1].append(num_im_res[i][1])

    return table, header, pols


def prettytable_output(table, header):
    new_table = PrettyTable()
    new_table.field_names = header

    for i in range(len(table)):
        for j in range(len(table[0])):
            if type(table[i][j]) is Decimal:
                table[i][j] = round(float(table[i][j]), 7)

        new_table.add_row(table[i])

    return new_table


def main():
    beg = 0
    end = 2  # float(input('Введите конечное значение X: '))
    step = 0.0001  # float(input('Введите шаг: '))
    picar_iters = [3]  # list(map(int, input("Введите через пробел интересующие итерации для метода Пикара: ").split(" ")))

    t = time()

    table, header, pols = calculate(beg, end, step, picar_iters)
    p_table = prettytable_output(table, header)

    print(p_table)
    for i in picar_iters:
        print_pol(pols[i - 1])

    print(time() - t)


if __name__ == '__main__':
    main()
