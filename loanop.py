import numpy as np

def compound(p, r, dt, n='daily'):
    if n == 'daily':
        m = 365
    elif n == 'monthly':
        m = 12
    elif n == 'annualy':
        m = 1
    else:
        return p * np.exp(r * dt / 12)
    return p * (1 + r / m) ** (m * dt / 12)


def getMinPayment(princ, r, t=120, compounding='daily'):
    payment = compound(princ, r, t, n=compounding) / t

    while True:
        payment_old = payment

        p = simulateMonthlyRepayment(payment, princ, r,
                                     term=t, n=compounding)

        if abs(p) > 0.01:
            payment += p / t
        else:
            break

#     print(p, m, payment)
    return round(payment,2)


def loadLoanCSV(filename, cols=None, skiprow=0):
    datatype = {'names': ('loan', 'princ', 'rate',
                        'interest', 'term', 'minpay'),
                'formats': ('|U16', np.float, np.float,
                            np.float, np.float, np.float)
                }
    loans = np.loadtxt(filename, dtype=datatype, delimiter=',',
                        usecols=cols, skiprows=skiprow)

    return loans


def simulateMonthlyRepayment(payment, p, r, term=120, n='daily'):
    m = 0
    while m < term:
        p = compound(p, r, 1, n='daily')
        p -= payment
        m += 1
    return p
