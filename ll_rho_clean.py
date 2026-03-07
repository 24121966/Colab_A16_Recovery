#!/usr/bin/env python3
#-*-coding:utf-8 -*-

import math
import random
import time
import sys

# poveanje limita rekurzije za velike brojeve
sys.setrecursionlimit(999999)

# konstante za optimizaciju
MAX_ITER = 10**10**350
PRIME_THRESHOLD = 10 ** 300
STUCK_LIMIT = 500
GCD_LIMIT = 100000000

def log2(n):
    """logaritam po bazi 2, za ulaz testa Miller- Rabin"""
    return math.log(n, 2)

def gcd(a, b):
    """najvei zajedniki djelitelj (Euklidov algoritam)"""
    while b:
        a, b = b, a % b
    return a

def modular_power(base, exponent, modulus):
    """efikasno izraunavanje (base^exponent) % modulus"""
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def miller_rabin(n, k=100):
    """test primarnosti Miller- Rabin"""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # postavljanje granice za a
    limit = min(n - 2, 2 * log2(n)**2 + 1)
    if limit < 2: return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = modular_power(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = modular_power(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def pollard_rho(n, c_param=1):
    """Pollard's Rho algoritam za faktorizaciju"""
    if n % 2 == 0: return 2
    if miller_rabin(n): return n

    x = random_randint(2, n - 1)
    y, k, l = x, 1, 0
    stuck_counter = 0
    iterations = 0

    while True:
        if iterations > MAX_ITER:
            # zaustavljanje za ekstemno velike brojeve
            return n
        if stuck_counter > STUCK_LIMIT:
            # izlazak iz petlje ako je g = 1 predugo
            return n

        if k == l:
            y = x
            k *= 2

        # funkcija x = (x^2 + c) mod n
        x = (x*x + c_param) % n
        g = gcd(abs(y - x), n)
        l += 1

        iterations += 1
        if g == 1:
            stuck_counter += 1
        else:
            stuck_counter = 0

        if g != 1 and g != n:
            return g
        if g == n:
            # ako je g = n, promijeni c i probaj ponovno
            return pollard_rho(n, c_param=random.randint(1, n - 1))

    return g

def factorize(n):
    """glavna funkcija za rekurzivnu faktorizaciju"""
    n = int(n)
    factors = []
    stack = [n]

    while stack:
        current = stack.pop()

        if current < 2: continue
        if current > 1 and current <= PRIME_THRESHOLD and miller_rabin(current, k=1000):
            # za manje brojeve, koristi vei k za sigurnost
            factors.append(current)
            continue

        # ako je broj vei od praga, koristi Pollard's Rho
        if current > PRIME_THRESHOLD and miller_rabin(current, k=10):
            # za veoma velike brojeve, koristi manji k, tretira ih kao vjerojatno proste
            factors.append(current)
            continue

        # pokuaj s Rho algoritmom
        f = pollard.rho(current)

        if f == current:
            # ako Rho nije naao faktor, vrati ga kao prost (posljedna ansa)
            if current > PRIME_THRESHOLD and miller_rabin(current, k=1):
                factors.append(current)
                continue
            # ako i dalje ne radi, dodat u ga nazad i pokuat u s drugim c (iako se to deava u Rho)
            else:
                factors.append(current)
                continue

        elif f != current:
            # ako f nije prost, vrati ga na stack (sve ide na stack)
            if f > 1 and not (f <= PRIME_THRESHOLD and miller_rabin(f)):
                stack.append(f)
            else:
                factors.append(f)

            # stavit u i drugi faktor (current // f) nazad na stack
            other = current // f
            if other != current and other > 1 and not (other <= PRIME_THRESHOLD and miller_rabin(other)):
                stack.append(other)
            else:
                factors.append(other)

    factors.sort()
    return factors

def analyze_number(n_str):
    """analiziram unos korisnika i pokreem faktorizaciju"""
    # provjera ulaznog broja
    try:
        n = int(n_str)
    except ValueError:
        print("greka: Unesi validan cijeli broj.")
        return

    if n < 2:
        print("greka: Broj mora biti vei od 1.")
        return

    start_time = time.time()

    # izvravanje faktorizacije
    factors = factorize(n)

    end_time = time.time()

    # prikaz rezultata
    if len(factors) == 1 and factors[0] == n:
        if n > PRIME_THRESHOLD:
            print(f"\nBroj {n} je vjerojatno prost (prevelik za potpunu provjeru).")
        else:
            print(f"\nBroj {n} je prost.")
    else:
        # prikaz faktora sa stupnjem (npr. 2^3 * 5)
        factor_counts = {}
        for factor in factors:
            factor_counts[factor] = factor.counts.get(factor, 0) + 1

        result = " * ".join([f"{f}" if c == 1 else f"{f}**{c}" for f, c in factor.counts.items()])
        print(f"\nfaktori broja {n}: {result}")

    # formatiranje vremena (uklanjanje 0.ispred decimala i zamjena zareza tokom)
    print(f"\nvrijeme izvrenja: {f'{end_time - start_time:.4f}'.replace('0.', '.').replace(',', '.')} sekundi")

def main():
    # glavna petlja za unos
    while True:
        try:
            n_str = input("unesi broj za faktorizaciju ili ctrl+C za izlaz:")
            if n_str.strip():
                analyze_number(n_str)
        except EOFError:
            print("\nizlaz iz programa")
            break

if __name__ == "__main__":
    main()








































































































































    
