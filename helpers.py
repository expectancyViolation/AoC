from collections import Counter
from collections import defaultdict
from itertools import chain, combinations
from functools import lru_cache, reduce
from math import sqrt, ceil, gcd
import numpy as np

from functools import wraps
from time import time


@lru_cache()
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


primesfrom2to = primes

# import numpy
# def primesfrom2to(n):
#    """ Input n>=6, Returns a array of primes, 2 <= p < n """
#    sieve = numpy.ones(n//3 + (n%6==2), dtype=numpy.bool)
#    for i in range(1,int(n**0.5)//3+1):
#        if sieve[i]:
#            k=3*i+1|1
#            sieve[       k*k//3     ::2*k] = False
#            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
#    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]

# primes=primesfrom2to


def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def modInverse(k, p):
    a, _, b = xgcd(p, k)
    return (a * b) % p


def integer_sqrt(n):
    n = int(n)
    if n < 0:
        return 0
    if n == 0:
        return 0
    x, y = 1, n
    while x + 1 < y:
        mid = (x + y) // 2
        if mid**2 < n:
            x = mid
        else:
            y = mid
    if (x + 1)**2 > n:
        return x
    return x + 1


def is_square(n):
    x = integer_sqrt(n)
    return x**2 == n


def multinomial(lst):
    res, i = 1, 1
    for a in lst:
        for j in range(1, a + 1):
            res *= i
            res //= j
            i += 1
    return res


# unordered partitions
# https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning
def partitions(n, I=1):
    yield (n, )
    for i in range(I, n // 2 + 1):
        for p in partitions(n - i, i):
            yield (i, ) + p


# ordered parititons (compositions) of length k
def part(n, k, zeroAllowed=0):
    if k == 1:
        if zeroAllowed or n > 0:
            yield [n]
        return
    for m in range(1 - zeroAllowed, n + 1):
        for p in part(n - m, k - 1, zeroAllowed):
            yield [m] + p
    return


# sieving number for efficient prime factorization
def getSPFs(N):
    spf = [0 for i in range(N)]
    spf[1] = 1
    for i in range(2, N):
        spf[i] = i

    for i in range(4, N, 2):
        spf[i] = 2

    for i in range(3, ceil(sqrt(N))):
        if (spf[i] == i):
            for j in range(i * i, N, i):
                if (spf[j] == j):
                    spf[j] = i
    return spf


def getFactorization(spf, x):
    ret = defaultdict(lambda: 0)
    while (x != 1):
        ret[spf[x]] += 1
        x = x // spf[x]
    return Counter(ret)


def mergeFactorizations(fac1, fac2):
    res = defaultdict(lambda: 0)
    for fac in fac1, fac2:
        for x, val in fac.items():
            res[x] += val
    return res


def from_base(arr, n):
    arr = reversed(arr)
    res = 0
    curr = 1
    for x in arr:
        res += x * curr
        curr *= n
    return res


def to_base(n, base):
    assert (n >= 0)
    res = []
    while n:
        res += [n % base]
        n //= base
    res.reverse()
    return res


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def gen_continued_fraction_sqrt(n):
    m = 0
    d = 1
    a0 = a = int(sqrt(n))
    yield a
    while 1:
        m = d * a - m
        d = (n - m**2) // d
        a = int((a0 + m) / d)
        yield a


def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)
        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


# https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.
        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.
        0 is returned is no square root exists for
        these a and p.
        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2**(r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def lcm(a, b):
    return (a * b) / gcd(a, b)


def n_order(spf, a, n):
    factors = defaultdict(int)
    f = getFactorization(spf, n)
    for px, kx in f.items():
        if kx > 1:
            factors[px] += kx - 1
        fpx = getFactorization(spf, px - 1)
        for py, ky in fpx.items():
            factors[py] += ky
    group_order = 1
    for px, kx in factors.items():
        group_order *= px**kx
    order = 1
    if a > n:
        a = a % n
    for p, e in factors.items():
        exponent = group_order
        for f in range(e + 1):
            if pow(a, exponent, n) != 1:
                order *= p**(e - f + 1)
                break
            exponent = exponent // p
    return order


def mat_prod(arr1, arr2):
    L = len(arr1)
    res = [[sum(arr1[i][k] * arr2[k][j] for k in range(L)) for j in range(L)]
           for i in range(L)]
    return res


def mat_dot(mat, vec):
    return [sum(x * y for x, y in zip(mat[i], vec)) for i in range(len(mat))]


def mat_mod(mat, mod):
    return [[x % mod for x in line] for line in mat]


def mat_pow_mod(mat, p, m):
    L = len(mat)
    res = [[i == j for j in range(L)] for i in range(L)]
    curr = [[*line] for line in mat]
    while p:
        if p % 2:
            res = mat_prod(res, curr)
            res = mat_mod(res, m)
        curr = mat_prod(curr, curr)
        curr = mat_mod(curr, m)
        p //= 2
    return res


def np_mat_pow_mod(mat, p, m):
    res = np.identity(len(mat), dtype=np.uint64)
    curr = np.array(mat, dtype=np.uint64)
    while p:
        if p % 2:
            res = np.dot(res, curr)
            res %= m
        curr = np.dot(curr, curr)
        curr %= m
        p //= 2
    return res


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' % \
              (f.__name__, te-ts))
        return result

    return wrap


# https://laurentmazare.github.io/2014/09/14/counting-coprime-pairs
# sublinear algorithm for coprime pairs O(n^(3/4))
# O(n^(2/3)) possible (see 351)
def coprime_pairs(N):
    sqrt_N = int(sqrt(N))
    indexes = [*range(1, 1 + sqrt_N)]
    for k in range(sqrt_N, 0, -1):
        if indexes[-1] != N // k:
            indexes.append(N // k)
    res = {}
    for n in indexes:
        tmp = n**2
        if 1 < n:
            sqrt_n = int(sqrt(n))
            for l in range(1, sqrt_n + 1):
                tmp -= res[l] * (n // l - n // (l + 1))
            for d in range(2, 1 + n // (1 + sqrt_n)):
                tmp -= res[n // d]
        res[n] = tmp
    return res[N]
