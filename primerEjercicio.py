from math import sqrt, pi, e


def getData():
    a = float(input('Ingrese el límite inferior de la integral:\n-> '))
    b = float(input('\nIngrese el límite superior de la integral:\n-> '))
    if a > b:
        return '\nEl límite inferior no puede ser mayor al superior'
    miu = float(input('\nIngrese el valor de miu:\n-> '))
    sigma = float(input('\nIngrese el valor de sigma:\n-> '))
    if sigma < 0:
        return '\nSigma no puede ser menor a 1'
    delta = (b - a)/1000
    return a, b, miu, sigma, delta


def sumRiemman():
    a, b, miu, sigma, delta = getData()
    result = 0
    while a <= b:
        func1 = 1/(sigma*(sqrt(2*pi)))
        func2 = e ** (-(1/2) * (((a - miu)/sigma) ** 2))
        func = func1 * func2 * delta
        result += func
        a += delta
    return result

res = sumRiemman()
print(f'\n\nEl resaultado es: {res}')
