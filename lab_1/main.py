

# Численный метод - явная схема
def numerical_explicit_table(beg, end, step):
    x = beg
    table = [(x, 0)]

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
    except OverflowError:
        return None


# Численный метод - неявная схема
def numerical_implicit_table(beg, end, step):
    x = beg
    table = [(x, 0)]

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
            return (1 - pow(d, 0.5)) / (2 * h)
    else:
        return None


def picar(beg, end, step, iteration):
    pass


def calculate(beg, end, step, picar_iters):
    table = []
    header = ['X'] + picar_iters + ['Явная схема', 'Неявная схема']

    num_ex_res = numerical_explicit_table(beg, end, step)
    num_im_res = numerical_implicit_table(beg, end, step)

    size = len(num_ex_res)
    for i in range(size):
        table.append([])
        table[-1].append(num_ex_res[i][0])
        table[-1].append(num_ex_res[i][1])
        table[-1].append(num_im_res[i][1])

    return table, header


def main():
    # beg = float(input('Введите начальное значение X: '))
    beg = 0  # ???
    end = 3 #float(input('Введите конечное значение X: '))
    step = 0.06 #float(input('Введите шаг: '))
    picar_iters = []#list(map(int, input("Введите через пробел интересующие итерации для метода Пикара: ").split(" ")))

    table, header = calculate(beg, end, step, picar_iters)
    print(header)
    for i in table:
        print(i)


def test():
    res = numerical_explicit_table(0, 100000000, 10000000)
    print(res)


if __name__ == '__main__':
    main()
    # test()
