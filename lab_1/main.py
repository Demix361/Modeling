from decimal import Decimal, Overflow, ROUND_DOWN
from polynomial import find_picar_pols, solve_pol, print_pol
from prettytable import PrettyTable


class PolMember:
    def __init__(self, power, denominator):
        self.power = power
        self.denominator = denominator


# Численный метод - явная схема
def numerical_explicit_table(beg, end, step):
    x = beg
    table = [(x, Decimal(0))]

    while x + step <= end:
        if table[-1][1] is not None:
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
        return None


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
    if y_old is not None:
        d = 1 - 4 * h * (y_old + h * (h + x) ** 2)
        if d < 0:
            return None
        else:
            return (1 - pow(d, Decimal(0.5))) / (2 * h)
    else:
        return None


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


def calculate(beg, end, step, picar_iters):
    beg = Decimal(beg)
    end = Decimal(end)
    step = Decimal(step)
    
    table = []
    header = ['X']
    for i in picar_iters:
        header.append(str(i) + ' приближение Пикара')
    header += ['Явная схема', 'Неявная схема']

    num_ex_res = numerical_explicit_table(beg, end, step)
    num_im_res = numerical_implicit_table(beg, end, step)
    picar_res, pols = picar_table(beg, end, step, picar_iters)

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
            table[i][j] = round(float(table[i][j]), 7)
        new_table.add_row(table[i])

    return new_table


def main():
    # beg = float(input('Введите начальное значение X: '))
    beg = 0  # ???
    end = 1  # float(input('Введите конечное значение X: '))
    step = 0.01  # float(input('Введите шаг: '))
    picar_iters = [3, 4]  # list(map(int, input("Введите через пробел интересующие итерации для метода Пикара: ").split(" ")))

    table, header, pols = calculate(beg, end, step, picar_iters)
    p_table = prettytable_output(table, header)

    print(p_table)
    for i in picar_iters:
        print_pol(pols[i - 1])


if __name__ == '__main__':
    main()
