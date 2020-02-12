

# Класс члена полинома, обладает степенью и знаменателем
class PolMember:
    def __init__(self, power, denominator):
        self.power = power
        self.denominator = denominator


# Решить полином
def solve_pol(pol, x):
    y = 0

    for p in pol:
        y += pow(x, p.power) / p.denominator

    return y


# Умножение двух членов полинома
def pol_mem_mul(mem_1, mem_2):
    res = PolMember(mem_1.power, mem_1.denominator)
    res.power += mem_2.power
    res.denominator *= mem_2.denominator

    return res


# Возведение полинома во вторую степень
def squaring_pol(pol):
    pol_len = len(pol)
    new_pol = []

    for i in range(pol_len):
        for j in range(pol_len):
            new_pol.append(pol_mem_mul(pol[i], pol[j]))

    reduce_pol(new_pol)

    return new_pol


# Печать полинома
def print_pol(pol):
    for i in range(len(pol)):
        print('(x ^ %s) / %s' % (pol[i].power, pol[i].denominator), end='')
        if i != len(pol) - 1:
            print(' + ', end ='')
        else:
            print()


# Приводит однородные члены полинома
def reduce_pol(pol):
    h = len(pol)
    i = 0

    while i < h:
        j = i + 1

        while j < h:
            if pol[i].power == pol[j].power:
                d_1 = pol[i].denominator
                d_2 = pol[j].denominator
                pol[i].denominator = (d_1 * d_2) / (d_1 + d_2)

                pol.pop(j)
                h -= 1
            else:
                j += 1

        i += 1


# Интегрирует член полинома
def integrate_pol_mem(mem):
    res = PolMember(mem.power, mem.denominator)
    res.power += 1
    res.denominator *= res.power

    return res


# Интегрирует полином
def integrate_pol(pol):
    new_pol = []

    for p in pol:
        new_pol.append(integrate_pol_mem(p))

    return new_pol


# Находит все полиномы метода Пикара до заданной точности
def find_picar_pols(max_it):
    picar_pols = []

    # Первое приближение
    picar_pols.append([PolMember(3, 3)])

    for i in range(max_it - 1):
        new_pol = [PolMember(3, 3)]
        new_pol += integrate_pol(squaring_pol(picar_pols[-1]))

        picar_pols.append(new_pol)

    return picar_pols
