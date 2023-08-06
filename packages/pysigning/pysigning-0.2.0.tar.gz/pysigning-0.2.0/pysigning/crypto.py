import operator
import random
import math

def invmod(a, n):
    n0 = n
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, b, c, n = n, c, b - q*c, r
    # at this point a is the gcd of the original inputs
    if a == 1:
        if b < 0:
            b += n0
        return b
    raise ValueError("Not invertible")

def bit_length(n): # return the bit size of a non-negative integer
    assert n >= 0
    bits = 0
    while n >> bits: bits += 1
    return bits


def jacobi(a, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0


def is_prime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False

    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True

    for i in range(8):#number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


class Integer(int):
    def inverse(self, n):
        return invmod(self, n)
    def gcd(self, a):
        return math.gcd(self, a)
    def fail_if_divisible_by(self, a):
        if self % a == 0:
            raise ValueError(f"{self} divisible by {a}")
    def size_in_bits(self):
        return bit_length(self)
    def is_even(self):
        return self % 2 == 0
    def is_perfect_square(self):
        return math.isqrt(self)**2 == self
    @staticmethod
    def random_range(min_inclusive, max_exclusive, randfunc=None):
        return Integer(random.randrange(min_inclusive, max_exclusive))
    @staticmethod
    def jacobi_symbol(a, n):
        return jacobi(a, n)
    def __irshift__(self, n):
        return Integer(operator.__irshift__(int(self), n))
    def __add__(self, n):
        return Integer(int(self) + n)
    def __sub__(self, n):
        return Integer(int(self) - n)


def test_probable_prime(candidate, randfunc=None):
    return is_prime(int(candidate))


# monkeypatch to prevent crashing on MacOS 11.4

import Crypto.Math.Primality
Crypto.Math.Primality.test_probable_prime = test_probable_prime
Crypto.Math.Primality.Integer = Integer

from Crypto.PublicKey import RSA
RSA.test_probable_prime = test_probable_prime
RSA.Integer = Integer

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
