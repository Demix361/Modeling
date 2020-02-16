from decimal import Decimal


h = Decimal(0.1)
y_old = Decimal(1.2)
x = Decimal(0.61)

d = 1 - 4 * h * (y_old + h * (h + x) ** 2)
r = (1 - pow(d, Decimal(0.5))) / (2 * h)

print(type(r))

