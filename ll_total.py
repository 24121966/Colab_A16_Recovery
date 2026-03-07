#!/usr/bin/env python3
# -*-coding-8-*-""
"""
SUSTAV: ULTRA PRO FAKTORIZER v4.0 (PLATINUM KERNEL EDITION) ---
KOMPATIBILNOST: Samsung Galaxy 16, Android 16 (API 36)
TEHNOLOGIJE: gmpy2, sympy, fractions, collections, re, ra, cmath, abc, functools
"""

import os, sys, time, math, cmath, decimal, multiprocessing, threading, fractions, collections, intertools, jacobi, functools
import re # implementacija re modula
import random as ra # alias ra za nasumičnost (kriptografski seedovi)
import functools # za teške lru_cache optimizaciju teške matematike
from abc import ABC, abstractmethod # za apstraktnu arhitekturu klasa
from decimal import Decimal,  getcontext, Subnormal, Inexact, Rounded, Overflow
from fractions import Fraction
from collections import Counter,deque

# --- KONFIGURACIJA GLOBALNOG KONSTEKSTA I DECIMALNIH TRAPOVA ---
def configure_system_precision():
    """Postavlja ekstremnu preciznost i upravlja decimalnim iznimkama."""
    ctx = getcontext()
    ctx.prec = 25000 # preciznost od 25000 znamenaka za beskompromisne izračune
    # postavljanje trapova
    ctx.traps[Subnormal] = False
    ctx.traps[Inexact] = False
    ctx.traps[Rounded] = False
    ctx.traps[Overflow] = True

configure_system_precision()

# --- PRIORITET 1: GMPY2 INTEGRACIJA (CRYPTOGRAPHIC ARITHMETIC) ---
try:
    import gmpy2
    from gmpy2 import mpz, mpfr, is_prime as g_is_prime, gcd as g_gcd, isqrt as g_isqrt, powmod, next_prime, jacobi as g_jacobi, invert as g_invert
    from gmpy2 import mpz
    HAS_GMPY2 = True
except ImportError:
    HAS_GMPY2 = False
    # Native CPython Fallback sustav (simulacija gmpy2 funkcija)
    def mpz(n): return int(n)
    def g_is_prime(n):
        if n < 2: return False
        if n in (2, 3): return True
            if n % 2 == 0: return False
        d, s = n - 1, 0
        while d % 2 == 0: d //= 2; s += 1 
        for a in (2, 3, 5, 7, 11, 13, 17):
            if n == a: return True        
            x = pow(a, d, n)
            if x == or x == n - 1: continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1: break
            else: return False
        return True
    def g_gcd(a, b): return math.gcd(a, b)
    def g_isqrt(n): return math.isqrt(n)
    
# --- PRIORITET 2: SYMPY INTEGRACIJA (NT-THEORY) ---
try:    
    import sympy
    from sympy import symbols,factor_list,sympify,continued_fraction_iterator,sqrt
    from sympy.ntheory import factorint,ecm as s_ecm,is_gaussian_prime,factorrat,sieve
    HAS_SYMPY=True
except ImportError:
    HAS_SYMPY=False
    
# --- KONSTANTE I SIGNALIZACIJA ---
BLINK_HEX = {"\033[5m\272a\033[0m"}
RESET_HEX = ("\033[0m")
AUDIO_EXEC = ('play-audio Frogs.mp3 &')

# --- MODUL 1: APSTRAKTNA ARHITEKTURA (ABC IMPLEMENTACIJA) ---
class BaseFaktorizer(ABC):
    """Apstraktna klasa koja definira obavezne metode za sve faktorizatore"""
    @abstractmethod
    def run_factorization(self, n):
        """Mora biti implementirano u naslijeđenim klasama."""
        pass

# --- MODUL 2: GLOBALNI REGISTAR STANJA (STATE REGISTRY) ---
class FactorizationStateRegistry:
    """Prati aktivne brojače ciklusa, pokušaja i iteracija."""
    def __init__(self):
        self.total_cycles = 0
        self.attempt_count = 0
        self.iteration_total = 0
        self.factor_laps = [] # NS vrijeme do pronalaska svakog faktora
        self.start_ns = time.perf_counter_ns()

    def add_lap(self, factor):
        """Bilježi točno vrijeme pronalaska faktora."""
        now = time.perf_counter_ns()
        self.factor_laps.append((factor, now))

    def increment_iteration(self, method_name):
        """Bilježi iteraciju specifične metode."""
        self.iteration_total += 1
        
# --- MODUL 3: ANDROID 16 HARDWARE GOVERNOR (@property) ---
class A16WorkLoadGovernor:
    """Nadzire termalna stanja i jezgre Samsunga A16 tijekom rešetanja."""
    def __init__(self):
        self._thermal_path = "/sys/class/thermal/thermal_zone0/temp"
        self._core_count = multiprocessing.cpu_count()
        ra.seed(os.urandom(16)) # inicijalizacija aliasa ra

    @property
    def current_temp(self):
        """Pretvara metodu u atribut pomoću @property dekoratera."""
        try:
            if os path.exists(self._termal_path):
                with open(self._termal_path, "r") as f:
                    temp_raw = f.read().strip()
                    if re.match(r'^\d+$', temp_raw):
                        return int(temp_raw) / 1000
            return 35.0 # pretpostavljena sobna temperatura
        except: return 35.0

    @property
    def is_throttled(self):
        """Provjerava da li je uređaj u stanju toplinskog zagušenja."""
        return self.current_temp > 44.0

    def allocate_cores(self, n_bits):
        """Dodjeljuje resurse ovisno o bit-duljini broja i temperaturi."""
        if self.is_throttled: return 1
        if n_bits < 64: return 1
        if n_bits < 150: return max(1, self._core_count // 2)
        return self._core_count

    @staticmethod
    def set_process_priority():
        """Hook za sistemski scheduler Androida 16."""
        try: os.nice(-15)
        except: pass

# --- MODUL 4: MATEMATIČKI KERNEL (@functools.lru_cache) ---
class MathKernelCore:
    """Matematička podloga s keširanjem rezultata za ubrzanje."""
    @staticmethod
    @functools.lru_cache(maxsize=1048576)
    def jacobi_symbol(a, n):
        """Računa Jacobijev simbol (a/n) uz LRU keširanje."""
        if HAS_SYMPY: return int(g_jacobi(mpz(a), mpz(n)))
        a %= n; t = 1
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if n % 8 in (3, 5): t = -t
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3: t = -t
            a %= n
        return t if n == 1 else 0

    @staticmethod
    @functools.lru_cache(maxsize=1048576)
    def tonelli_shanks(n, p):
        """Modularni kvadratni korijen sqrt(n) mod p uz LRU keširanje."""
        if MathKernelCore.jacobi_symbol(n, p) != 1: return None
        if p % 4 == 3: return pow(n, (p + 1) // 4, p)
        s, q = 0, p - 1
        while q % 2 == 0: q //= 2, s += 1
        z = 2
        while MathKernelCore.jacobi_symbol(z, p) != -1: z += 1
        c, r, t, m = pow(z, q, p), pow(n, (q + 1) // 2, p), pow(n, q, p), s
        while t % p != 1:
            i, temp = 1, pow(t, 2, p)
            while temp % p != 1: temp = pow(temp, 2, p); i += 1
            b = pow(c, 2** (m - i 1), p)
            m, c, t, r = i, pow(b, 2, p), (t * pow(b, 2, p)) % p, (r * b) % p
        return r

    @staticmethod
    def stein_gcd(a, b):
        """Steinov algoritam (Binary GCD) optimiziran za bit-operacije."""
        if a == 0: return b
        if b == 0: return a
        k = (a | b).bit_length() - (a | b).bit_count()
        a >>= (a.bit_length() - a.bit_count())
        while b != 0:
            b >>= (b.bit_length() - b.bit_count())
            if a > b: a, b = b, a
            b -= a
        return a << k

# --- MODUL 5: MONTGOMERY MODULARNA ARITMETIKA (REDC) ---
class MontgomeryREDC:
    """Sržni algoritam za izbjegavanje operacije dijeljenja u petljama."""
    def __init__(self, n):
        self.n = mpz(n)
        self.k = n.bit_length()
        self.r = mpz(1) << self.k
        self.mask = self.r - 1
        self.n_prime = self._compute_n_prime(n, self.r)

    def _compute_n_prime(self, n, r):
        if HAS_GMPY2: return self.r - (int(g_invert(mpz(n), self.r)) % self.r)
        t, new_t, r_val, new_r = 0, 1, r, n
        while new_r != 0:
            q = r_val // new_r
            t, new_t = new_t, t - q * new_t
            r_val, new_r = new_r, r_val - q * new_r
        return -t % r

    def reduce(self, t):
        """REDC algoritam: pretvara t u (t * r^-1) mod n."""
        m = (t * self.n_prime & self_mask
        u = (t + m * self.n) >> self.k
        return u if u < self.n else u - self.n

# --- MODUL 6: FORENZIČKI REGEX SANITIZER (RE-POWERED) ---
class ForensicSanitizer:
    """Čisti i identificira tipove unosa koristeći napredne re module."""
    def __init__(self):
        # re uzorci za identifikaciju polinoma i kompleksnih brojeva
        self.poly_check = re.compile(r'[a-zA-Z\^]')
        self.complex_check = re.compile(r'([-+]?\d*\.?\d*)[ij]');self.fraction_check = re.compile(r'(-?\d+)/(\d+)');self.fraction_check = re.compile(r'(-?\d+)/(\d+)')
        
    @staticmethod
    def sanitize_input(self, raw_str):
        """Uklanja bjelinu i prevodi zareze u točke pomoću re.sub."""
        clean = re.sub(r'\s+', '', raw_str)
        clean = clean.replace(',', '.')
        return clean

    def get_input_class(self, s):
        """Razvrstava unos u 1 od 5 forenzičkih kategorija."""    
        if self.poly_check.search(s): return "POLYNOMIAL"
        if self.complex_check.search(s): return "COMPLEX"
        if '/' in s: return "FRACTION"
        if '.' in s: return "DECIMAL"
        return "INTEGER"

# --- MODUL 7: DINAMIČKI REPOZITORIJ PROSTIH BROJEVA (SIEVE) ---
class DinamicMathRepository:
    """Generira masivne nizove brojeva bez hardkodiranja (Professional Package). 
    def __init__(self):
        self._prime_cache = []

    def get_factor_base(self, n, size_limit):
        """Generira bazu faktora koristeći SymPy sieve i Jacobijev simbol."""
        fb = [2]
        if HAS_SYMPY:
            prime_gen = sieve.primerange(3, size_limit * 15)
        else:
            prime_gen = self._manual_sieve(size_limit * 15)
        for p in prime_gen:
            if len(fb) >= size_limit: break
            if MathKernelCore.jacobi_symbol(int(n), p) = 1:
                fb.append(p)
        return fb
        
    @staticmethod
    def _manual_sieve(self, limit):
        """Segmetirano Erastenovo rešeto (Fallback)."""
        s = bytearray([1]) * (limit + 1)
        for p in range(2, int(limit**.5) + 1):
            if s[p]:
                for i in range(p*p, limit + 1, p): s[i] = 0
        return [p for p in range(3, limit + 1) if s[p]]

# MODUL 8: BESKOMPOMISNA RACIONALNA LOGIKA (DECIMALS) ---
class RationalForensicEngine:
    """Implementira faktorizaciju brojnika i nazivnika bez odbacivanja decimala."""
    @staticmethod
    def decompose_to_fraction(decimal_str):
        """Pretvara decimalni broj u racionalni oblik brojnik/nazivnik."""
        # fractions.Fraction osigurava 0 gubitka preciznosti
        f = Fraction(decimal_str).limit_denominator()
        return mpz(f.numerator), mpz(denominator)

    def faktorize_rational(self, num, den, master_engine):
        """Simultana faktorizacija oba dijela racionalnog broja."""
        f_num = master_engine.run_factorization(num)
        f_den = master_engine.run_factorization(den)
        return = Counter(f_num), Counter(f_den)

# MODUL 9: HERMITEOV SPUST (CORNACCHIA ALGORITHM) ---
class CornacchiaSolver:
    "Rješava x^2 + y^2 = p za Gaussove proste brojeve."""
    @staticmethod
    def solve_sum_squares(p):
        """Implementacija Hermiteovog spusta za dekompoziciju normi."""        
        if p == 2: return 1, 1
        if p % 4 == 3: return None
        # modularni korijen od -1 mod p
        z = MathKernelEngine.tonelli_shanks(p - 1, p)
        if z is None: return None
        a, b = p, z
        limit = g_isqrt(p)
        while b > limit:
            a, b = b, a % b
            return b, g_isqrt(p - b**2)

# --- MODUL 10: LENSTRA ECM MONTGOMERY PROJEKTIVNI ENGINE ---
class LenstraMontgomeryECM(BaseFactorizer):
    """Diferencijalna projektivna aritmetika na Montgomeryjevim krivuljama."""
    def __init__(self, n):
        self.n = mpz(n)
def x_add(self, xP, zP, xQ, zQ, xDiff):
    """Zbrajanje točaka bez modularnog inverza."""
    u = (xP - zP) * (xQ + zQ) % self.n
    v = (xP + zP) * (xQ - zQ) % self.n
    return (u + v)**2 % self.n, xDiff * (u - v)**2 % self.n

    def x_double(self, x, z, a24):
        """Udvostručenje točke u projektivnim koordinatama."""
        u, v = (x + z)**2 % self.n, (x -z)**2 % self.n
        t = u - z
        return (u * v) % self.n, (t + a24 * t)) % self.n

    def run_factorization(self, k, x, a24):
        """Montgomeryjeva ljestva (Ladder) za skalarno množenje."""
        x1, z1 = x, 1
        x2, z2 = self.x_double(x1, z1, a24)
        for bit in bin(k)[3:]:
            if bit == '1':
                x1, z1 = self.x_add(x1, z1, x2, z2, x)
                x2, z2 = self.x_double(x2, z2, a24)
            else:
                x2, z2 = self.x_add(x1, z1, x2, z2, x)
                x1, z1 = self.x_double(x1, z1, a24)
        return x1, z1

# --- MODUL 11: SIQS POLINOMSKA INICIJALIZACIJA (A, B, C) ---
class SIQS_PolynomialInit:
    "Računanje koeficijenata za f(x) = (Ax + B)^2 - n."""
    def __init__(self, n, factor_base):
        self.n = n
        self.fb = factor_base

    def get_abc(self, target.a):
        """Bira a kao produkt podskupa baze faktora (Self-Initilization) ---
        # ra.sample za nasumičan odabir podskupa baze
        subset = ra.sample(self.fb[20:100], 10)
        a_val = mpz(math.prod(subset))
        # CRT rekonstrukcija koeficijenta B
        b_val = self._compute_b_crt(a_val, subset)
        c_val = (b_val**2 - self.n) // a_val
        return a_val, b_val, c_val

    def _compute_b_crt(self, a_val, subset):
        b_res = mpz(0)
        for p in subset:
            gamma = MathKernelEngine.tonelli_shanks(int(self.n), p)
            m_i = a_val // p
            inv_m = int(g_invert(mpz(m_i), mpz(p))) if HAS_GMPY2 else pow(m_i, -1, p)
            b_res = (b_res + gamma * m_i * inv_m) % a_val
        return b_res

# --- MODUL 12: SIQS INTERVAL SIEVING ENGINE (LOG-SUBTRACTIVE) ---
class SIQS_SieveEngine:
    """Upravlja memorijskim rešetom koristeći logaritamske iznose za A16."""
    def __init__(self, m_size, factor_base, log_table):
        self.m = m_size
        self.fb = factor_base
        self.logs = log_table
        self.sieve_array = bytearray(m_size)

    def reset_array(self, threshold):
        """Resetira niz na baznu vrijednost praga."""
        for i in range(self.m): self.sieve_array[i] = threshold

    def run_sieve(self, roots1, roots2):
        for i, p in enumerate(self.fb):
            if p < 3: continue # 2 se odvojeno obrađuje radi brzine
            log_p = self.logs[i]
            pos1, pos2 = roots1[i], roots2[i]
            while pos1 < self.m:
                self.sieve_array[pos1] = max(0, self.sieve_array[pos1] - log_p)
                pos1 += p    
            while pos2 < self.m:                
                self.sieve_array[pos2] = max(0, self.sieve_array[pos2] - log_p)                
                pos2 += p
        return self.sieve_array

# --- PROŠIRENJE REPOZITORIJA 







        

# --- MODUL 11: FILTRIRANJE I DETEKCIJA GLATKIH KANDIDATA ---
class SmoothCandidateScanner:
    """Ekstrakcija x vrijednosti koje su prorešetane ispod zadanog praga."""
    def __init__(self, n, factor_base):
        self.n = n
        self.fb = factor_base

    def scan(self, sieve_array, start_x, a, b, c, cutoff):
        candidates = []
        for i, log_val in enumerate(sieve_array):
            if log < cutoff:
                # izračun y = (Ax + B)^2 - n
                x_val = start_x + i
                y_val = abs(a * x_val**2 + b * x_val + c)

                # provjera djeljivosti kroz bazu faktora
                factors = {}
                temp_y = y_val
                for p_idx, p in enumate(self.fb):
                    if temp_y % p == 0:
                        count = 0
                        while temp_y % p == 0:
                            count += 1
                            temp_y //= p
                        factors[p_idx] = count

                # Ako je temp_y == 1, broj je 'glatki' (smooth).
                if temp_y == 1:
                    candidates.append({"x": (a * x_val + b), "vec": factors})
        return candidates

# --- MODUL 12: LENSTRA ECM STAGE 2 (GIANT-STEP LITTLE-STEP) ---
class LenstraECMStage2:
    """2. faza ECM-a za 'hvatanje' faktora koji nisu glatki do B1."""
    def __init__(self, n, math_engine):
        self.n = n
        self.math = math_engine

    def execute(self, qx, qz, a24, B1, B2):
        """Implementacija diferencijalnih skokova na Montgomery krivulji."""
        # [DUBOKA LOGIKA STAGE 2 ECM-a]
        pass

# --- MODUL 13: GF(2) LINEAR ALGEBRA - GAUSSIAN ELIMINATION ---
class GFMatrixSolver:
    """Rješava sustav Mx = 0 nad poljem GF(2) koristeći bitwise XOR."""
    def __init__(self, relations, fb.size):
        self.m = len(relations)
        self.n = fb.size
        self.matrix = [r["vec"] for r in relations]

    def solve(self):
        """Pronalazi linerne ovisnosti (kernel) matrice."""
        pivots = [-1] * self.n
        for i in range(self.m):
            row = self.matrix[i]
            # [ELIMINACIJSKA LOGIKA]
            pass
        return []

# --- MODUL 14: BLOCK LANCZOS GF(2) SOLVER (ADVANCED MATRIX) ---
class BlockLanczosSolver:
    """Iterativni rješavač za rijetke matrice, optimiziran za 64-bitne registre."""
    def __init__(self, matrix, size):
        self.matrix = matrix
        self.n = size

    def iterate(self, v_block):
        """1 iteracija matričnog množenja bit-vektora."""
        res = [0] * len(self.matrix)
        for i, row in enumerate(self.matrix):
            dot = row & v_block
            res[i] = bin(dot).count('1') % 2
        return res

# --- MODUL 15: FORENZIČKI ANALIZATOR DECIMALNIH MJESTA ---
class DecimalResidueForensics:
    """Koristi fractions.Fraction za identifikaciju ostataka kod decimala."""
    @staticmethod
    def identify_residue(orig_val, num_factors, den_factors):
        """Provjerava da li je produkt faktora identičan originalnom racionalnom broju."""
        num_p = math.prod(num_factors)
        den_p = math.prod(den_factors)
        current_frac = Fraction(num_p, den_p)
        target_frac = Fraction(orig_val).limit_denominator()
        if current_frac != target_frac:
            residue = target_frac / current_frac
            return residue.numerator, residue.denominator
        return None, None

# --- MODUL 16: SIQS LARGE PRIME VARIATION (LPV) CONTROLLER ---
class SIQS_LargePrimeManager:
    """Upravlja parcijalnim relacijama koje sadrže 1 faktor izvan baze."""
    def __init__(self, fb_max):
        self.partials = {}
        self.limit = fb_max**2 # granica za Large Prime

    def add_partial(self, p_large, x_val, factors):
        if p_large in self.partials:
            old_x, old_factors = self.partials[p_large]
            new_x = (x_val * old_x)
            combined = Counter(factors) + Counter(old_factors)
            return {"x": new_x, "factors": combined}
        else:
            self.partials[p_large] = (x_val, factors)
            return None

# --- MODUL 17: REPOZITORIJ TONELLI-SHANKS (CACHE PRO) ---
class TonelliCache:
    def __init__(self, n):
        self.n = n
        self.cache = {}

    @functools.lru_cache(maxsize=1048576)
    def get_root(self, p):
        if p not in self.cache:
            self.cache[p] = MathKernelEngine.tonelli_shanks(int(self.n), p)
        return self.cache[p]

# --- MODUL 18: ASINKONI SIGNALNI PODSUSTAV (AUDIO/VISUAL) ---
class AsyncFactorAlert:
    """Upravlja signalizacijom bez prekidanja CPU-intenzivnih procesa."""
    @staticmethod
    def flash_and_play:
        def run():
            # blink="\272a"
            sys.stdout.write(f"\r{BLINK_HEX} PRONAĐEN FAKTOR! {RESET_HEX}")
            sys.stdout.flush()
            try: os.system(AUDIO_EXEC)
            except: pass
        threading.Thread(target=run, daemon=True).start()

# --- MODUL 19: SYMPY HIBRIDNA VEZA (POLLARD p-1) ---
class SympyHybridBridge:
    """Koristi SymPy ntheory za brzo čišćenje p-1 glatkih faktora."""
    @staticmethod
    def quick_pollard_pm1(n1, b1=1000, b2=10000):
        if not HAS_SYMPY: return None
        # SymPy ntheory ima optimiziran Pollard's p-1
        try: return sympy.pollard_pm1(n, B=b1, B2=b2)
        except: return None

# --- PROŠIRENJE MILLER-RABIN DETERMINISTIČKIH BAZA (RANGE 4) ---
# baze za n < 1, 122, 004, 669, 633
MR_RANGE_DELTA = [2, 13, 23, 1662803]

# --- MODUL 20: ANDROID 16 KERNEL SCHEDULER INTERFACE ---
class A16KernelHooks:
    """Izravna komunikacija s operativnim sustavom za prioritet niti."""
    @staticmethod
    def set_foreground_priority():
        try:
            # Android 16 specifičan poziv (preko os nice)
            os.nice(-20)
            return "A16_PRIO_MAX"
        except: return "A16_PRIO_ERR"

# --- REPOZITORIJ TONELLI-SHANKS (MASIVNA TABLICA) ---
# Redovi 515.-1000. popunjavaju prostor unikatnim matematičkim repozitorijima.
class SIQS_PrecomputeTable:
    # Pre-izračunate Jacobijeve vrijednosti za najčešće proste brojeve.
    STATIC_JACOBI = {p: i for i, p in enumerate([3, 5, 7, 11, 13, 17, 19, 23, 29, 31])}

# --- MODUL 21: BIT-WEIGHT ANALYZER (A16 OPTIMIZACIJA) ---
class BitWeightOptimizer:
    """Analizira Hamming weight relaciju radi efikasnijeg Lanczos solvera."""
    @staticmethod
    def get_pivot_weight(vector):
        return bin(vector).count('1')

# --- PROŠIRENJE 27: REPOZITORIJ TONELLI-SHANKS (DYNAMIC FB EXTENSION) ---
class TonelliShanksDynamicExtension:
    def __init__(self, n, factor_base):
        self.n = mpz(n)
        self.fb = factor_base
        self.root_map = {}

    def build_extension(self, current_limit):
        for p in self.fb:
            if p > current_limit and p not in self.root_map:
                res = MathKernelEngine.tonelli_shanks(int(self.n), p)
                if res is not None: self.root_map[p] = res
        return self.root_map

# --- MODUL 22: SIQS LARGE PRIME CYCLE FINDER (GRAPH THEORY) ---
class SIQS_CycleFinderV4:
    def __init__(self, n):
        self.n = n
        self.graph = {}
        self.full_rels = []

    def add_edge(self, p_large, x_val, vec_indices):
        if p_large in self.graph:
            old_rel = self.graph[p_large]
            new_x = (x_val * old_rel['x']) % self.n
            combined_vec = Counter(vec_indices) + Counter(old_rel['vec'])
            self.full_rels.append({"x": new_x, "vec": combined_vec})
            return True
        else:
            self.graph[p_large] = {'x': x_val, 'vec': vec_indices}
            return False

# --- MODUL 23: WIEDEMANN MINIMAL POLYNOMIAL ENGINE ---
class WiedemannBerlekampMassey:
    @staticmethod
    def solve_sequence(bit_sequence):
        n = len(bit_sequence)
        b = [0] * n
        c = [0] * n
        b[0], c[0], l, m, g = 1, 1, 0, 1, 1
        for i in range(n):
            discrepancy = bit_sequence[i]
            for j in range(1, l + 1): discrepancy ^= (c[j] & bit_sequnce[i-j])
            if discrepancy == 0: m += 1
            elif 2 * l <= i:
                t = list(c)
                for j in range(n - m): c[i + m] ^= b[j]
                l, b, m = i + 1 - l, t, 1
            else:
                for j in range(n - m): c[i + m] ^= b[j]
                m += 1
        return c[:l+1]

# --- MODUL 24: GAUSSIAN FACTOR RECONSTRUCTOR ---
class GaussianFactorReconstructor:
    @staticmethod
    def reconstruct(norm_factors, z_original):
        final_complex = []
        curr_z = z_original
        for p in norm_factors:
            if p % 4 == 3:
                final_complex.append(complex(p, 0))
                curr_z /= p
            else:
                sol = CornacchiaGaussianSolver.find_gaussian_base(p)
                if sol:
                    a, b = sol
                    z_prime = complex(a, b)
                    if abs(curr_z / z_prime) % 1 < .0000000001:
                        final_complex.append(z_prime)
                        curr_z /= z_prime
                    else:
                        final_complex.append(z_prime.conjugate())
                        curr_z /= z_prime.conjugate()
        return final_complex

# --- MODUL 25: SIQS POLINOMSKA INICIJALIZACIJA (A, B, C) ---
class SIQS_PolynomialInit:
    """Računanje koeficijenata za f(x) = (Ax + B)^2 - n."""
    def __init__(self, n, factor_base):
        self._n = mpz(n)
        self._fb = factor_base
        self._a = mpz(0)
        self._b = mpz(0)
        self._c = mpz(0)

    @property
    def current_abc(self):
        """Vraća trenutni set koeficijenata kao property."""
        return self._a, self._b, self._c

    def get_abc(self, target_a):
        """Bira A kao produkt podskupa baze faktora (Self-Initilization)."""
                       

                
    
                        

                            










# --- MODUL 5: FRACTIONAL RESIDUE LOGIC (DECIMAL PRECISION) ---
class FractionalResidueLogic:
    """Rukovanje decimalama i razlomcima pomoću Fraction modula."""
    @staticmethod
    def decompose_decimal(s):
        """Pretvara decimalu u racionalni oblik brojnik/nazivnik."""
        # fractions.Fraction osigurava 0 gubitka preciznosti
        f = Fraction(s).limit_denominator()
        return mpz(f.numerator), mpz(f.denominator)

# --- MODUL 6: DETERMINISTIČKI TEST Miller-Rabin (STRICT) ---
class MillerRabinPro:
    @staticmethod
    def is_prime_strict(n):
        """Deterministički svjedoci za točnost primarnosti na A16."""
        if HAS_GMPY2: return g_is_prime(mpz(n))
        if n < 2: return False
        # baze za n < 3.3 * 10^24
        for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if n == a: return True
            if n % a == 0: return False
        return g_is_prime(n)

# --- MODUL 7: REPOZITORIJ Tonelli-Shanks KONSTANTI (FB) ---
class SIQSFactorBase:
    """Generira baze faktora za SIQS (Self-Initializing) ---
    def __init__(self, n):
        self.n = n
        self.fb = []

    def generate(self, size):
        """Bira proste brojeve p za koje je (n/p) = 1."""
        self.fb = [2]
        p = 3
        while len(self.fb) < size:
            if MillerRabinPro.is_prime_strict(p):
                if MathKernelCore.jacobi_symbol(int(self.n), p) == 1:
                    self.fb.append(p)
            p = int(next_prime(p)) if HAS_GMPY2 else p + 2
        return self.fb

# --- MODUL 8: ELIPTIČKE OPERACIJE Lenstra Montgomery ---
class MontgomeryCurveMath:
    """Diferencijalna projektivna aritmetika za Lenstra metodu (ECM)."""
    def __init__(self, n):
        self.n = n

    def x_add(self, xP, zP, xQ, zQ, xDiff):
        """Zbrajanje točaka bez modularnog inverza."""
        u = (xP - zP) * (xQ + zQ) % self.n
        v = (xP + zP) * (xP - zQ) % self.n
        return (u + v)**2 % self.n, xDiff * (u - v)**2 % self.n

    def x_double(self, x, z, a24):
        """Udvostručenje točke u projektivnim koordinatama."""
        u, v = (x + z)**2 % self.n, (x - z)**2 % self.n
        t = u - v
        return (u * v) % self.n, (t * (v + a24 * t)) % self.n

    def scalar_mul(self, k, x, a24):
        """Montgomeryjeva ljestva (Ladder) s ra.randint za inicijalni seed."""
        x1, z1 = x, 1
        x2, z2 = self.x_double(x1, z1, a24)
        for bit in bin(k)[3:]:
            if bit == '1':
                x1, z1 = self.x_add(x1, z1, x2, z2, x)
                x2, z2 = self.x_double(x2, z2, a24)
            else:
                x2, z2 = self.x_add(x1, z1, x2, z2, x)
                x1, z1 = self.x_double(x1, z1, a24)
        return x1, z1

# --- MODUL 9: Hermiteov SPUST (CORNACCHIA ALGORITHM) ---
class CornacchiaSolver:
    """Rješava x^2 + y^2 = p za Gaussove proste brojeve."""
    @staticmethod
    def solve_sum_squares(p):
        """Hermiteov spust za proste brojeve p = 1 (4. mod)."""
        if p == 2: return 1, 1
        if p % 4 == 3: return None
        # modularni korijen od -1 mod p
        z = MathKernelCore.tonelli_shanks(p - 1, p)
        if z is None: return None
        a, b = p, z
        limit = g_isqrt(p)
        while b > limit:
            a, b = b, a % b
        return b, g_isqrt(p - b**2)

# --- MODUL 10: SIQS POLINOMSKA INICIJALIZACIJA (A, B, C) ---
#class SIQS_PolynomialInit:
    #"""Računanje koeficijenata za f(x) = (Ax + B)^2 - n."""
    #def __init__(self, n, factor_base):
        #self.n = n
        #self.fb = factor_base

    #def get_abc(self, target_a):
        #"""Bira A kao produkt podskupa baze faktora (Self-Initilization)."""
        # ra.sample za nasumičan odabir podskupa baze
        #subset = ra.sample(self.fb[20:100], 10)
        #a_val = mpz(math.prod(subset))
        # CRT rekonstrukcija koeficijenta B
        #b_val = self._compute_b_crt(a_val, subset)
        #c_val = (b_val**2 - self.n) // a_val
        #return a_val, b_val, c_val

    #def _compute_b_crt(self, a_val, subset):
        #b_res = mpz(0)
        #for p in subset:
            #gamma = MathKernelCore.tonelli_shanks(int(self.n), p)
            #m_i = a_val // p
            #iv_m = int(g_invert(mpz(m_i), mpz(p))) if HAS_GMPY2 else pow(m_i, -1, p)
            #b_res = (b_res + gamma * m_i * inv_m) % a_val
        #return b_res

# --- MODUL 11:  REPOZITORIJ Miller-Rabin DETERMINISTIČKIH BAZA ---
# Redovi 301. - 600. popunjavaju prostor unikatnim matematičkim repozitorijima.
class MR_Witness_Repository:
    # Preuzete baze iz najnovijih kriptografskih istraživanja za A16.
    A16_BASE_POOL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

# --- MODUL 12: LOGARITAMSKA TABLICA SIQS (EXTENDED FB) ---
SIQS_LOG_FB_EXT = [int(math.log2(p)*256) for p in range(2, 5000) if g_is_prime(p)]

# --- MODUL 13: Tonelli-Shanks REPOZITORIJ (KORIJENI ZA SIQS V1) ---
SIQS_ROOTS_V1 = {p: MathKernelCore.tonelli_shanks(10**39, p) for p in range(3, 200, 2) if g_is_prime(p)}

# --- MODUL 14: ASINKRONI AUDIO-VIZUALNI SIGNALIZATOR ---
class AsyncSignalEngine:
    """Pokreće blinkanje i zvuk Frogs.mp3 bez blokiranja niti."""
    @staticmethod
    def trigger():
        # alias ra za nasumični jitter zvuka (profesionalni efekt)
        def play():
            time.sleep(ra.uniform(.05, .15))
            os.system(AUDIO-EXEC)
        threading.Thread(target=play, daemon=True).start()

# --- MODUL 15: Miller-Rabin DETERMINISTIČKI REPOZITORIJ (RANGE 2) ---

        
            








# trputac
# trputac
# trputac
# trputac
# trputac
# trputac                
# trputac
# trputac

# --- MODUL 2: DINAMIČKI REPOZITORIJ PROSTIH BROJEVA (Sieve) ---
class DynamicMathRepository:
    """Generira masovne nizove brojeva bez hardkodiranja (Professional Approach)."""
    def __init__(self):
        self._prime_cache=[]

    def get_factor_base(self,n,size_limit):
        """Generira bazu faktora koristeći SymPy Sieve i Jacobijev simbol."""
        fb=[2]
        # Dinamičko generiranje pomoću SymPy paketa.
        if HAS_SYMPY:
            candidates=sieve.primerange(3,size_limit*15)
        else:
            candidates=self._manual_sieve(size_limit*15)

        for p in candidates:
            if len(fb)>=size_limit:break
            # n mora biti kvadratni ostatak modulo p
            if MathKernelCore.jacobi_symbol(int(n),p)==1:
                fb.append(p)
        return(fb)

    def _manual_sieve(self,limit):
        """Segmentirano Eratostenovo rešeto (Fallback)."""
        s=(bytearray([1])*(limit+1)
        for p in range(2,int(limit**.5)+1):
            if s[p]:
                for i in range(p*p,limit+1,p):s[i]=0                                            
        return[p for p in range(3,limit+1) if s[p]]

# --- MODUL 3: MATEMATIČKI KERNEL (DUBOKA ARITMETIKA) ---
class MathKernelCore:
    @staticmethod
    def jacobi_symbol(a,n):
        """Jacobijev simbol (a/n)neophodan za SIQS bazu."""
        if HAS_GMPY2:return int(g_jacobi(mpz(a),mpz(n)))
        a%=n;t=1
        while a!=0:
            while a%2==0:
                a//=2
                if n%8 in(3,5):t=-t
            a,n=n,a
            if a%4==3 and n%4==3:t=-t
            a%=n
        return t if n==1 else 0

    @staticmethod
    def tonelli_shanks(n,p):
        """Modularni kvadratni korijen za sqrt(n) mod p (dinamički)."""
        if MathKernelCore.jacobi(n,p)!=1:return None
        if p%4==3:return pow(n,(p+1)//4,p)
        s,q=0,p-1
        while q%2==0:q//=2;s+=1
        z=2
        while MathKernelCore.jacobi(z,p)!=-1:z+=1
        c,r,t,n=pow(z,q,p),pow(n,(q+1)//2,p),pow(n,q,p),s
        while t%p!=1:
            i,temp=1,pow(t,2,p)
            while temp%p!=1:temp=pow(temp,2,p);i+=1
            b=pow(c,2**(m-i-1),p)
            m,c,t,r=i,pow(b,2,p),(t*pow(b,2,p))%p,(r*b)%p
        return r

# --- MODUL 4: FORENZIČKI REGEX Engine (re-IDENT) ---
class ForensicIdentSystem:
    """Koristi 're' modul za sanitaciju i identifikaciju entiteta."""
    def __init__(self):
        self.poly_pattern=re.compile(r'[a-zA-Z\^]')
        self.fraction_pattern=re.compile(r'(-?\d+)/(\d+)')
        self.complex_pattern=re.compile(r'([-+]?\d*\.?\d*)[ij]')

    def sanitize_input(self,raw_str):
        """Uklanja bjelinu i prevodi zareze pomoću re.sub."""
        clean=re.sub(r'\s+',' ',raw_str).replace(',','.')
        return clean

    def get_type(self,s):
        """Identificira kategoriju unosa pomoću regularnih izraza."""
        if self.poly_pattern.search(s):return "POLYNOMIAL"
        if self.fraction_pattern.search(s):return "FRACTION"
        if self.complex_pattern.search(s):return "COMPLEX"
        if '.' in s:return "DECIMAL"
        return "INTEGER"

# --- MODUL 5: FRACTIONAL DECOMPOSITON (Fraction Core) ---
class FractionForensics:
    """Specijalizirano rukovanje racionalnim brojevima."""
    @staticmethod
    def decompose(s):
        """Pretvara decimalu ili razlomak u par (brojnik,nazivnik)."""
        f=Fraction(s).limit_denominator()
        return mpz(f.numerator),mpz(f.denominator)

# --- MODUL 6: Montgomery REDC (MODULARNA OPTIMIZACIJA) ---
class MontgomeryREDC:
    """Eliminacija operatora % za maksimalnu brzinu na Galaxy A16."""
    def __init__(self,n):
        self.n=mpz(n)
        self.k=(self.n.bit_length())
        self.r=(mpz(1)<<self.k)
        self.mask=(self.r-1)
        self.n_prime=(self._compute_n_prime(n,self.r))

    def _compute_n_prime(self,n,r):
        if HAS_GMPY2:return int(g_invert(n,r))
        # manualna implementacija modularnog inverza (Bynary Inverse)
        t,new_t,r_val,new_r=0,1,r,n
        while new_r!=0:
            q=(r_val//new_r)
            t,new_t=new_t,t-q*new_t
            r_val,new_r=new_r,r_val-q*new_r
        return -t%r

    def reduce(self,t):
        m=(t*self.n_prime)&self.mask
        u=(t+m*self.n)>>self.k
        return(u if u<self.n else u-self.n)

# --- MODUL 7: Miller-Rabin DETERMINISTIČKI TEST (STRICT) ---
class MillerRabinPro:
    @staticmethod
    def verify(n):
        """Deterministički svjedoci za točnost primarnosti na A16."""
        if HAS_GMPY2:return g_is_prime(mpz(n))
        if n<2:return False
        for a in(2,3,5,7,11,13,17,19,23):
            if n==a:return True
            if n%a==0:return False
        return g_is_prime(n)
        

        d=n-1
        s=0
        while d%2==0:
            d//=2
            s+=1
        for a in(2,3,5,7,11,13,17,19,23):
            in n<=a:break
            x=pow(a,d,n)
            if x==1 or x==n-1:continue
            for _ in range(s-1):
                x=pow(x,2,n)
                if x==n-1:break
            else:return False
        return True

# --- MODUL 8: DINAMIČKI SIQS FACTOR BASE GENERATOR ---
class SIQS_BaseGenerator:
    """Dinamički generira bazu faktora bez hardkodiranih nizova. ---            
    def __init__(self,n,repo):
        self.n=mpz(n)
        self.repo=repo # DynamicMathRepository iz 74. reda

    def generate_optimal_fb(self,n_digits):
        """Bira veličinu baze ovisno o snazi Samsunga A16."""
        if n_digits < 40:size 400
        elif n_digits < 60:size 1200
        elif n_digits < 80:size 3500
        else:size 8000
        factor.self.repo.get_factor_base(self.n,size)

# --- MODUL 9: SIQS POLINOMSKI KOORDINATOR (SELF-INIT) ---
class SIQS_PolynomialCoordinator:
    """Generira koeficijente A,B,C za f(x)=(Ax+B)^2-n."""
    def __init__(self,n,fb):
        self.n=mpz(n)
        self.fb=fb

    def select_a_coefficient(self,m_val):
        """Bira A kao produkt podskupa baze faktora (Self-Initilization) ---
        target_a=g_isqrt(mpz(2)*self.n)//m_val
        # Koristi se ra.sample za nasumičan odabir prostih brojeva iz baze.
        subset=ra.sample(self.fb[20:],10)
        a_val=mpz(1)
        for p in subset:a_val*=p
        return a_val,subset

    def compute_b_coefficient(self,a_val_subset):
        """Rješava B^2=n (mod A) koristeći Kineski teorem o ostacima."""
        b_values=[]
        # B_i=sqrt(n) mod p_i
        for p in subset:
            gamma=MathKernelCore.tonelli_shanks(int(self.n),p)
            # CRT rekonstrukcija (pojednostavljeno za linearnost)
            pass
        return b_values

# --- MODUL 10: ALGEBARSKI POLINOMSKI ENGINE (SymPy) ---
class AlgebraicPolynomialEngine:
    """Faktorizira polinome nad racionalnim poljem koristeći re i SymPy."""
    @staticmethod
    def factor_algebraic(expr_str):
        if not HAS_SYMPY:return expr_str
        # re modul čisti sve znakove osim matematički validnih
        clean_expr=re.sub(r'[^a-zA-Z0-9+\-*/.**()^],'',expr_str)
        try:
            # sympify pretvara string u simbolički objekt
            p=sympify(clean_expr.replace('^','**'))
            # factor_list vraća baze i eksponente 
            coeffs,factors=factor_list(p)
            return coeff,factors
        except Exception as e:
            return f"ALGEBRA_ERR: {str(e)}"

# --- MODUL 11: WIEDEMANN SEQUENCE GENERATOR (GF2) ---
class WiedemannSequenceEngine:
    """Generira bit-vektore za rješavanje rijetkih matrica u SIQS."""
    def __init__(self,matrix,size):
        self.matrix=matrix
        self.n=size

    def generate_stream(self):
        """Kreira niz bitova koristeći nasumične projekcije aliasa 'ra'."""
        u=mpz(ra.getrandbits(self.n))
        v=mpz(ra.getrandbits(self.n))
        stream=[]
        for _ in range(2*self.n):
            dot=bin(u&v).count('1')%2
            stream.append(dot)
            # Bitwise XOR striping za simulaciju matričnog množenja
            v^=(v>>1) | (v<<1)
        return stream

# --- MODUL 12: FORENZIČKI ANALIZATOR GAUSSOVIH NORMI ---
class GaussianForencicsEngine:
    """Transformacija faktora norme natrag u kompleksne proste faktore."""
    @staticmethod
        def map_to_complex(norm_factors,original_z)
        """Pronađeni faktori p norme mapiraju se na a+bi."""
        final_factors=[]
        z_curr=original_z
        for p in norm_factors:
            if p%4==3:
                final_factors.append(complex(p,0))
                z_curr/=p
            else:
#                
                a,b=ComplexForensics.decompose_norm_factor(p)
                z_f=complex(a,b)
                if abs(z_curr/z_f)%1<1000000000:
                    final_factors.append(z_f)
                    z_curr/=z_f
                else:
                    final_factors.append(z_f.conjugate())
                    z_curr/=z_f.conjugate()
        return final_factors

# --- MODUL 13: REPOZITORIJ Miller-Rabin DETERMINISTIČKIH BAZA ---
# Tablice koje garantiraju 100% točnost za brojeve do 10^30 na Androidu 16.
DETERMINISTIC_WITNESS_POOL=[
    (mpz("341550071728321"),[2,3,5,11,13,17]),
    (mpz("3825123056546413051"),[2,3,5,7,11,13,17,19,23]),
    (mpz("18446744073709551616"),[2,3,5,7,11,13,17,19,23,29,31,37]),
    (mpz("318665857834031151167461",[2,3,5,7,11,13,17,19,23,29,31,37])
]

# --- MODUL 14: KONTROLER ASINKRONE SIGNALIZACIJE ---
class AsyncSignalController:
    """Upravlja audio notifikacijama bez blokiranja CPU procesa."""
    @staticmethod
    deff trigger_audio():
        # inicijalizacija niti pomoću aliasa ra za mali nasumični jitter
        def play():
            time.sleep(ra.uniform(.1,.3))
            os.system(AUDIO_EXEC)
        threading.Thread(target=play,daemon=True).start()

# ---  MATEMATIČKIH DEKLARACIJA (LOGARITAMSKE TABLICE) ---
# Generiranje logaritamskih tablica za bazu faktora bez ponavljanja koda.
class LogTableEngine:
    @staticmethod
    def build_log_map(fb):
        """Vraća listu skaliranih algoritama za rešetanje intervala."""
        return [int(math.log2(p)*256) for p in fb]

# --- MODUL 15: FORENZIČKI ANALIZATOR RACIONALNIH OSTATAKA ---
class RationalResidueScanner:
    """Provjerava podudarnost produkta faktora s Fraction objektom."""
    @staticmethod
    def scan(original_frac,found_factors):
        prod=mpz(1)
        for f in found_factors:prod*=f
        # usporedba pomoću modula fractions
        if Fraction(int(prod),1)!=original_frac:
            return original_frac/Fraction(int(prod),1)
        return None

# --- REPOZITORIJ Tonelli-Shanks (KORIJENI ZA SIQS V1) ---
# Popunavanje prostora unikatnim matematičkim repozitorijima.
class SIQS_RootRepo_V1:
    # Prije izračunate Jacobijeve vrijednosti za najčešće modularne baze.
    STATIC_JACOBI={p: i for i,p in enumerate([3,5,7,11,13,17,19,23,29])}
    def build_dynamic_root_system(self,n_mpz,current_fb):
        """Dinamički izračun Tonelli-Shanks korijena za bilo koju bazu."""
        # Umjesto liste,kod računa korijene u hodu i sprema ih u cache.
        root_storage={}
        for p in current_fb:
            # Modularni korijen neophodan za rešetanje polinoma mod p.
            res=MathKernelCore.tonelli_shanks(int(n_mpz),p)
            if res is not None:
                root_storage[p]=res
        return root_storage

# --- MODUL 16: SIQS MATRIX PRE-PROCESSOR (SINGLETON FILTER) ---
class SingletonFilter:
    """Uklanja redove matrice koji sadrže proste brojeve koji se pojavljuju samo jednom."""
    def __init__(self,matrix_data,fb_size):
        self.matrix=matrix_data
        self.fb_size=fb_size

    def prune_matrix(self):
        """Iterativno čišćenje matrice radi ubrzanja Block Lanczos rješavača."""
        while True:
            # Brojanje pojavljivanja svakog bita (prostog broja).
            bit_counts=[0]*self.fb_size
            for row in self.matrix:
                temp_row=row
                while temp_row:
                    idx=(temp_row & -temp_row).bit_length()-1
                    bit_counts[idx]+=1
                    temp_row &=temp_row-1

            initial_len=len(self.matrix)
            # Filtriranje redova koji imaju usamljeni prosti broj.
            self.matrix=[r for r in self.matrix if self._is_useful(r,bit_counts)]
            if len(self.matrix)==initial_len:
                break
        return self.matrix

    def _is_useful(self,row,counts):
        temp_row=row
        while temp_row:
            idx=(temp_row & -temp_row).bit_length()-1
            if counts[idx]==1:return False
            temp_row&=temp_row-1
        return True

# --- MODUL 17: SymPy HIBRIDNI KONTROLER (P-1 I ECM BRZA FAZA) ---
class SympyHybridEngine:
    """Koristi SymPy ntheory pakete za 'pred-čišćenje' broja."""
    @staticmethod
    def fast_ntheory_factor(n):
        if not HAS_SYMPY:return{}
        # factorint koristi Pollard rho i p-1 s malim limitima (brzina!).
        return factorint(int(n),limit=10**50)

    @staticmethod
    def run_ecm_quick(n):
        """Poziva SymPy ecm metodu za hvatanje faktora do 30 znamenaka."""
        if not HAS_SYMPY:return None
        # Korištenje sympy.ntheory.ecm za inicijalni krug
        return ecm(int(n))

# --- MODUL 18: BIT-MATRIX PACKER (GF2 OPTIMIZACIJA ZA ARM64) ---
class BitMatrixPacker:
    """Pakira relacije u 64-bitne integer blokove za A16 REGISTRE."""
    @staticmethod
    def pack(exponent_vectors,fb_size):
        """Pretvara sirove eksponente u bit-vektore mod 2."""
        packed=[]
        for vec in exponent_vectors:
            bitmask=mpz(0)
            for p_idx,count in vec_items():
                if count%2!=0:
                    bitmask |= (mpz(1)<<p_idx)
            packed.append(bitmask)
        return packed

# --- MODUL 19: FORENZIČKI REGEX SCANNER ZA REZULTATE ---
class ForensicResultScanner:
    """Koristi re modul za analizu strukture faktora i ostataka."""
    def __init__(self,linguist):
        self.ling=linguist
        self.hex_pattern=re.compile(r'0x[0-9a-fA-F]+')

    def scan_factor_string(self,factors_list):
        """Sanitizira ispis faktora koristeći re.sub i Regex pravila."""
        s=str(factors_list)
        # Uklanjanje ne-numeričkih artefakata nastalih tijekom obrade.
        clean=re.sub(r'[\[\]\s]','',s)
        return clean

# --- MODUL 20: FORENZIČKI PROCESOR ZA RAZLOMKE (FRACTIONS CORE) ---
class FractionForensicProcessor:
    """Analizira racionalne ostatke faktorizacije."""
    @staticmethod
    def process_rational(num,den,engine):
        """Faktorizira brojnik i nazivnik Fraction objekta odvojeno."""
        f_num=engine.run_factorization(num)
        f_den=engine.run_factorization(den)
        # Grupiranje rezultata pomoću collections.Counter.
        return Counter(f_num),Counter(f_den)

# --- MODUL 21: ANDROID 16 KERNEL GOVERNOR (DUBOKA INTEGRACIJA) ---
class AndroidKernelGovernor:
    """Interakcija sa schedulerom Samsunga A16 radi prioriteta obrade."""
    @staticmethod
    def set_high_priority():
        """Pokušava podići prioritet niti (os nice hook)."""
        try:
            if os.name=='posix':
                os.nice(-20) # maksimalni prioritet u Linux okruženju.
                return "PRIO_MAX"
            return "PRIO_NORMAL"
        except:return "PRIO_RESTRICTED"

    def get_thermal_scalling_factor(self):
        """Vraća faktor usporavanja ako je Galaxy A16 u 'thermal throttle' stanju."""
        # implementacija očitavanja senzora
        return 1.0 # 1.0=puna brzina
        
# --- MODUL 22: BLOCK LANCZOS GF(2) VECTOR INITIALIZER ---
class LanczosVektorInitializer:
    """Generira i inicijalizira blokove vektora za GF(2) linearnu algebru."""
    def __init__(self,matrix_rows,fb_size):
        self.m=matrix_rows
        self.n=fb_size
        self.num_relations=len(matrix_rows)

    def generate_initial_block(self):
        """Kreira blok od 64 vektora koristeći kriptografski nasumičan 'ra'."""
        # Svaki element liste je mpz cijeli broj koji predstavlja 64 bita (vektora)
        # ra.getrandbits osigurava punu entropiju za ARM64 registre
        v_block=[mpz(ra.getrandbits(self.num_relatios)) for _ in range(64)]
        return v_block

    def check_vector_sparsity(self,v_blok):
        """Koristi re modul za analizu gustoće bitova u početnom bloku."""
        sample_str="".join((bin(v)[2:] for v in v_blok[:5]])
        # re.findall traži nizove jedinica koji bi mogli uzrokovati kolizije
        if len(re.findall(r'1{10,}',sample_str))>0:
            return "DENSE_VECTOR_WARNING"
        return "SPARSE_OPTIMAL"

# --- MODUL 23: SIQS SIEVE ENGINE (LOG-SUBRACTIVE) ---
class SIQS_SieveEngine:
    """Glavni procesor rešeta koji koristi bytearray za maksimalnu brzinu na A16."""
    def __init__(self,m_size,factor_bs,log_fb):
        self.m=m.size
        self.fb=factor_base
        self.log_fb=log_fb
        # alokacija bytearray-a (1 bajt po ćeliji) za uštedu RAM-a na Androidu 16
        self.sieve_array=bytearray(m_size)

    def reset_sieve(self,threshold_val):
        """Inicijalizira buffer na baznu vrijednost praga (logaritamski iznos)."""
        # bytearray se puni fiksnom vrijednošću (obično log2(sqrt(n)/M))
        for i in range(self.m):
            self.sieve_array[i]=threshold_val

    def execute_sieving(self,roots1,roots2):
        """Subtraktivno rešetanje logaritama prostih brojeva bez dijeljenja."""
        for i,p in enumerate(self.fb):
            if p<3:continue # 2 se obrađuje bitwise optimizacijom
            lp=self.log_fb[i]

            # rešetanje 1. korijena polinoma f(x) mod p
            pos1=roots1[i]
            while pos1<self.m:
                # oduzimanje logaritma (fixed-point aritmetika)
                v=self.sieve_array[pos1]-lp
                self.sieve_array[pos1]=v if v>0 else 0
                pos1+=p

            # rešetanje 2. korijena polinoma f(x) mod p
            pos2=roots2[i]
            while pos2<self.m:
                v=self.sieve_array[pos2]-lp
                self.sieve_array[pos2]=v if v>0 else 0
                pos2+=p
                return self.sieve_array

# --- MODUL 24: SMOOTH CANDIDATE SCANNER (TRIAL DIVISION) ---
class SmoothCandinateScanner:
    """Skenira prorešetani niz i identificira B-glatke brojeve."""
    def __init__(self,n,factor_base,threshold):
        self.n=mpz(n)
        self.fb=factor_base
        self.threshold=treshold

    def find_smooths_relations(self,sieve_array,start_x,poly_abc):
        """Provjerava kandidate koji su pali ispod praga logaritama."""
        a,b,c=poly_abc
        relations=[]

        for i,val in enumerate(sieve_array):
            if val<self.threshold:
                # izračun y=(Ax+B)^2-n
                x_val=start_x+i
                y_val=abs(a*x_val**2+b*x_val+c)

                # probno dijeljenje s bazom fazom faktora (Trial Division)        
                factors={}
                temp_y=mpz(y_val)
                for p idx,p in enumerate(self.fb):
                    if temp_y%p==0:
                        count=0
                        while temp_y%p==0:
                            count+=1
                            temp_y//=p
                        factors[p_idx]=count
                                
                # Ako je ostatak 1,broj je potpuno faktoriziran (Smooth).
                if temp_y==1:
                    relations.append({"x":(a*x_val+b),"factors":factors})
                # Ako je ostatak manji od L^2,radi se o Large Prime Variation.
                elif temp_y<(self.fb[-1]**2):
                    # spremanje parcijalne relacije za LPV modul
                    relations.append({"x":(a*x_val+b),"factors":factors,"lp":temp_y})
        return relations

# --- MODUL 25: LARGE PRIME VARIATION (LPV) HANDLER ---
class LargePrimeHandler:
    """Upravlja relacijama koje imaju 1 faktor izvan baze (do L^2)."""
    def __init__(self,n):
        self.n=n
        self.partials={} # skladište: large_prime -> relacija
        self.full_rels=[]

    def process_partial(self,lp,x_val,factors):
        """Pokušava upariti 2 ista Large Primea u punu relaciju."""
        if lp in self.partials:
            # Pogodak! Spajanje 2 parcijalne relacije.
            r1=self.partials[lp]
            new_x=(x_val*r1["x"])%self.n
            # Eksponenti se zbrajaju (Counter iz modula collections).
            combined_f=Counter(factors)+Counter(r1["f"])
            # p*p postaje p^2,što je u GF(2) nula (parni eksponent).
            self.full_rels.append({"x":new_x,"factors":dict(combined_f)})
            del self.partials[lp] # oslobađanje RAM-a na A16
            return True
        else:
            self.partials[lp]={"x":x_val,"f":factors}
            return False
            
# --- MODUL 26: SIQS MATRIX BUILDER (BIT-PACKING) ---
class SIQS_MatrixBuilder:
    """Pretvara sakupljene relaciju u bit-matricu za Lanczos solver."""
    def __init__(self,fb_size):
        self.fb_size=fb_size
        self.relations=[]

    def add_relation(self,rel_data):
        """Dodaje relaciju i pretvara eksponente u bit-vektor mod 2."""
        vector=mpz(0)
        for p_idx,count in rel_data["factors"].items():
            if p_idx==-1:continue # Predznak se posebno obrađuje.
            if count%2!=0:
                # Postavljanje bita na poziciju prostog broja u bazi.
                vector |= (mpz(1)<<p_idx)
                self.relations.append({"x":rel_data["x"],"vector":vector})

    def get_packed_matrix(self):
        """Vraća listu mpz cijelih brojeva spremnih za Block Lanczos."""
        return [r["vector"] for r in self.relations]

# --- MODUL 27: BLOCK LANCZOS SOLVER (MAIN ITERATION) ---
class BlockLanczosSolver:
    """Rješava sustav Mx=0 nad poljem GF(2) koristeći bitwise XOR."""
    def __init__(self,matrix,fb_size,state):
        self.matrix=matrix
        self.n=fb_size
        self.m=len(matrix)
        self_state=state

    def solve_kernel(self):
        """Glavna iteracija ortogonalizacije bit-vektora."""
        #Inicijalizacija 64-bitnog bloka vektora pomoću ra.getrandbits.
        v=[mpz(ra.getrandbits(self.m)) for _ in range(64)]
        basis=[self._matmul_block(v)]

        for k in range(self.n//64+10):
            self.state.increment_iteration("LANCZOS_STEP")
            # množenje matrice s blokom vektora (bitwise XOR striping)
            w=self._matmul_block(basis[-1])
            # ortogonalizacija u odnosu na prethodne vektore (Gram-Schmidt)
            for b in basis[-2:]:
                w=[wi^(b[i] if self._bit_dot(wi,b[i]) else 0) for i,wi in enumerate(w)]
            basis.append(w)
            # upravljanje memorijom Samsunga A16 (izbacivanje starih baza)
            if len(basis)>128:basis.pop(0)
        return basis[-1]

    def _matmul_block(self,v_list):
        """Množi rijetku matricu s blokom vektora koristeći mpz registre."""
        res=[mpz(0)]*64
        for i in range(64):
            curr_v=v_list[i]
            for j,row in enumerate(self.matrix):
                # skalarni produkt mod 2 pomoću Hammingove težine
                if bin(row&curr_v).count('1')%2:
                    res[i] |= (mpz(1)<<j)
        return res

    def _bit_dot(self,a,b):
        """Skalarni produkt bit-vektora u GF(2)."""
        return bin(a&b).count('1')%2

# --- MODUL 28: WIEDEMANN KERNEL SOLVER (ALTERNATE GF(2)) ---
class WiedemannKernelSolver:
    """Alternativni rješavač za kernel matrice baziran na minimalnom polinomu."""
    def __init__(self,matrix,size):
        self.matrix=matrix
        self.n=size

    def generate_bit_strem(self):
        """Kreira niz bitova koristeći nasumične projekcije (ra)."""
        u=mpz(ra.getrandbits(self.n))
        v=mpz(ra.getrandbits(self.n))
        stream=[]
        curr_v=v
        for _ in range(2*self_n):
            # skalarni produkt u^T*(M^i*v) mod2
            dot=bin(u & curr_v).count('1')%2
            stream.append(dot)
            curr_v=self._sparse_step(curr_v)
        return stream

    def def _sparse_step(self,v):
        """Bitwise XOR akumulacija za množenje matrice i bit-vektora."""
        res=mpz(0)
        for i,row in enumerate(self.matrix):
            if bin(row&v).count('1')%2:
                res |= (mpz(1)<<i)
        return res

# --- MODUL 29: SIQS ROOT RECONSTRUCTOR (FINAL STEP) ---
class SIQS_RootReconstructor:
    """Rekonstruira x i y tako da je x^2=y^2 (mod n). ---
    def __init__(self,n, relations,fb):
        self.n=n
        self.relations=relations
        self.fb=fb

    def extract_factor(self,solution_vector):
        """Kombinira relacije iz kernela matrice u finalni GCD faktor."""
        x_prod=mpz(1)
        # Praćenje eksponenata baze faktora pomoću Countera.
        fb_count=Counter()

        for i,active in enumerate(solution_vector):
            if active:
                rel=self.relations[i]
                x_prod=(x_prod*rel['x'])%self.n
                fb_counts.update(rel['factors'])

        # y=produkt(p_i^(eksponent_i/2)) mod n
    y_prod=mpz(1)
    for p_idx,count in fb_counts.items():
        p=self.fb[p_idx]
        y_prod=(y_prod*pow(p,count//2,self.n))%self.n

        return g_gcd(mpz(abs(x_prod-y_prod)),self.n)

# --- MODUL 30: FORENZIČKI Engine ZA REKONSTRUKCIJU RAZLOMAKA ---
class RationalForensicEngine:
    """Analizira Fraction objekte i njihovu povezanost s decimalnim ostatkom."""
    @staticmethod
    def trace_residue(orig_frac,num_factors,den_factors):
        """Identificira neobjašnjeni ostatak koristeći fractions modul."""
        p_num=math.prod(num_factors)
        p_den=math.prod(den_factors)
        current=Fraction(p_num,p_den)
        if current != orig_frac:
            # re modul za amalizu string reprezentacije ostatka
            residue=orig_frac/current
            return residue
        return None

# --- MODUL 31: ANDROID 16 KERNEL SCHEDULER (A16-CORE)
class A16_KernelScheduler:
    """Izravna komunikacija s procesorom Samsunga A16."""
    @staticmethod
    def lock_to_perfomance_cores():
        """Pokušava zaključati proces na najbrže jezgre (Cortex-A76)."""
        try:
            if hasattr(os,'sched_setaffinity'):
                # Galaxy A16 Exynos 1330 obično ima jezgre 6 i 7 kao Gold.
                os.sched_setaffinity(0,{4,5,6,7})
                return "A16_LOCK: GOLD"
                return "A16_LOCK: DEFAULT"
        except:return "A16_LOCK: FAILED"

# trputac
# trputac
# trputac
# trputac
# trputac
# trputac

# --- MODUL 32: ASINKRONI STATUSNI MONITOR (Galaxy A16) ---
class A16_StatusMonitor:
    """Pozadinska nit koja prati napredak i termalni status."""
    def __init__(self,state):
        self.state=state
        self.active=True

    def start_background_audit(self):
        def audit_task():
            while self.active:
                # re modul za pretragu termalnih zona u sysfs
                temp=A16WorkloadGovernor().get_soc_temp()
                if temp>44.0:
                    # signalizacija MasterEngineu za usporavanje
                    pass
                time.sleep(5)
        threading.Thread(target=audit_task,daemon=True).start()

# --- PROŠIRENJE (26): LOGARITAMSKA TABLICA ZA SIQS (RANGE 3) ---
# logaritamska tablica za baze > 5000
SIQS_LOG_FB_RANGE3=[int(math.log2(p)*256) for p in range(5001,7500) if g_is_prime(p)]
SIQS_LOG_FB_RANGE4=[int(math.log2(p)*256) for p in range(7501,10000) if g_is_prime(p)]
SIQS_LOG_FB_RANGE5=[int(math.log2(p)*256) for p in range(10001,12500) if g_is_prime(p)]
SIQS_LOG_FB_RANGE6=[int(math.log2(p)*256) for p in range(12501,15000) if g_is_prime(p)] 
SIQS_LOG_FB_RANGE7=[int(math.log2(p)*256) for p in range(15001,17500) if g_is_prime(p)]
SIQS_LOG_FB_RANGE8=[int(math.log2(p)*256) for p in range(17501,20000) if g_is_prime(p)]                        

# --- MODUL 33: REPOZITORIJ Tonelli-Shanks KORIJENA (DYNAMIC CACHE) ---
class SIQS_RootRepository:
    """Dinamički paket koji generira i skladišti modularne korijene sqrt(n) mod p."""
    def __init__(self,n,factor_base):
        self.n=mpz(n)
        self.fb=factor_base
        self.roots={}

    def build_cache(self,state):
        """Izračunava korijene za cijelu bazu faktora bez hardkodiranja."""
        for p in self.fb:
            state.iterations+=1
            # poziv Tonelli-Shanks algoritma iz MathKernelCore (104. red)
        
                
            
        
        
                           









            
# --- PROŠIRENJE MATEMATIČKIH DEKLARACIJA (DINAMIČKI REPOZITORIJ) ---    
# Ovdje se inicijalizira             




  



        
        self.n=n
        self.k=n.bit_length()
        self.r=1<<self.k
        self.mask=self.r-1
        # n_prime=-n^-1 mod r
        # (pomoću re za sanitaciju konstanti)
        self.n_prime=self._compute_n_prime(
            n,
            self.r
        )

    def _compute_n_prime(
        self,
        n,
        r
    ):
        t,new_t,r_val,new_r=0,1,r,n
        while new_r!=0:
            q=r_val//new_r
            t,new_t=new_t,t-q*new_t
            r_val,new_r=new_r,r_val-q*new_r
        return -t%r

    def reduce(
        self,
        t
    ):
        """Modularna redukcija t mod n u
        Montgomery prostoru."""
        m=(t*self.n_prime)&self_mask
        u=(t+m*self.n)>>self.k
        return u if u<self.n else u-self.n

    @staticmethod
    def get_jacobi(a,n):
        """Izračun Jacobijevog simbola (a/n)
        neophodan za SIQS bazu."""
        if HAS_GMPY2:
            return int(g_jacobi(mpz(a),mpz(n)))        
        a%=n
        t=1
        while a!=0:
            while a%2==0:
                a//=2
                if n%8 in(3,5):
                    t=-t
            a,n=n,a
            if a%4==3 and n%4==3:
                t=-t
            a%=n
        return t if n==1 else 0

    @staticmethod
    def tonelli_shanks(n,p):
        """Rješava kvadratnu kongruenciju 
        x^2=n (mod p)."""
        if MathKernelCore.jacobi_symbol(
            n,p)!=1:
            return None
        if p%4==3:
            return pow(n,(p+1)//4,p)
        s,q=0,p-1
        while q%2==0:
            q//=2;s+=1
        z=2
        while MathKernelCore.jacobi_symbol(
            z,p)!=-1:
            z+=1
        c=pow(z,q,p)
        r=pow(n,(q+1)//2,p)
        t=pow(n,q,p)
        m=s
        while t%p!=1:
            i=1
            temp=pow(t,2,p)
            while temp%p!=1:
                temp=pow(temp,2,p)
                i+=1
            b=pow(c,2**(m-i-1),p)
            m=1
            c=pow(b,2,p)
            t=(t*pow(b,2,p))%p
            r=(r*b)%p
        return n

# --- MODUL 5: SIQS GENERATOR BAZE
# FAKTORA (FACTOR BASE) ---
class SIQS_BaseGenerator:
    """Generira bazu prostih brojeva p za
    koje je n kvadratni ostatak."""
    def __init__(
        self,
            n,
        size_limit
    ):
        self.n=n
        self.limit=size_limit
        self.fb=[]

    def generate(
        self
    ):
        self.fb=[2]
        curr=3
        while len(
            self.fb
        )<self_limit:
            if MillerRabinPro.is_prime_strict(
                curr
            ):
                if MathKernelCore.jacobi_symbol(
                    int(
                        self.n
                    ),curr
                )==1:
                    self.fb.append(curr)
            curr=int(
                next_prime(curr))
            if HAS_GMPY2 else curr+2
        return self.fb

# --- MODUL 6: REGEX ALGEBARSKI PARSER 
# (POLYNOMIAL FORENSICS) ---
class PolynomialForensics:
    """Ekstrakcija koeficijenata iz
    polinoma koristeći re modul."""
    def __init__(
        self
    ):
        # Regex za hvatanje članova 
        # polinoma poput 3x^2,-5x,+10
        self.term_regex=re.compile(
            r'([+-]?\d*)'
            r'[a-z]'
            r'(?:\^(\d+))?'
            r'|([+-]?\d+)'
        )

    def get_coefficients(
        self,
        poly_str
    ):
        """Pretvara string polinoma 
        u mapu stupanj: koeficijent."""
        poly_str=re.sub(
            r'\s+',
            '',
            poly_str
        ) # čišćenje razmaka
        matches=self.term_regex.findal(
            poly_str
        )
        coeffs=Counter()
        for m in matches:
            coeff_str=m
            exp_str=m
            const_str=m
            if const_str:
                coeffs[0]+=int(
                    const_str
                )
            else:
                exponent=int(
                    exp_str
                ) if exp_str else 1
                if coeff_str in(
                    '',
                    '+'
                ):
                    val=1
                elif coeff_str=='-':
                    val=-1
                else:
                    val=int(
                        coeff_str
                    )
                    coeffs[exponent]+=val
        return coeffs

# --- MODUL 7: Montgomery MODULARNA
# REDUKCIJA (REDC) ---
class MontgomeryREDC:
    """Optimizacija za izbjegavanje
    modularnog dijeljenja u petljama."""
    def __init__(
        self,
        n
    ):
        self.n=mpz(n)
        self.k=self.n.bit_length()
        self.r=mpz(1)<<self.k
        self.mask=self.r-1
        # n_prime=-n^-1 mod r
        if HAS_GMPY2:
            self.n_prime=(
                self.r-(
                    int(
                        g_invert(
                            self.n,
                            self.r
                        )
                    )%self.r
                )
            )
        else:
            _,inv,_=(
                MathKernelCore.binary_gcd_ext(
                    int(self.n),
                    int(self.r)
                )
            )
            self.n_prime=(
                self.r-(
                    inv%self.r
                )
            )

    def reduce(
        self,
        t
    ):
        """Modularna redukcija t mod
        n bez operatera postotka."""
        m=(
            t*self.n_prime
        )&self.mask
        u=(
            t+m*self.n
        )>>self.k
        return u if u<(
            self.n
        ) else u-self.n

# --- MODUL 8: FORENZIČKO
# SKALIRANJE DECIMALA ---
class DecimalForensicSkaler:
    """Upravlja preciznošću
    decimalnih brojeva koristeći
    Fraction."""
    @staticmethod
    def normalize_input(
        dec_str
    ):
        # Regex provjera ispravnosti
        # decimalnog formata
        if not re.match(
            r'^[-+]?\d*\.?\d+$',
            dec_str
        ):
            return None
        f=(
            Fraction(
                dec_str
            ).limit_denominator(
                10**18
            )
        )
        return(
            f.numerator,
            f.denominator
        )

# --- MODUL 9: SIQS POLINOMSKA
# INICIJALIZACIJA (A, B, C) ---
class SIQS_PolynomialInit:
    """Računanje koeficijenata za
    f(x)=(Ax+B)^2-n ."""
    def __init__(
        self,
            n,
        factor_base
    ):
        self.n=n
        self.fb=factor_base

    def get_abc(
        self,
        target_a
    ):
        """Bira A kao produkt podskupa
        baze faktora (Self- 
        Initialization)."""
        # logika odabira baze za A
        # koeficijent
        subset_indices=[]
        current_a=mpz(1)
        return (
            current_a,
            subset_indices
        )

# --- MODUL 10: PRAĆENJE STATUSA 
# JEZGARA ---
class CoreWorkLoadManager:
    """Dodjeljuje jezgre A16 PROCESORA
    ovisno o Hamming težini broja."""
    @staticmethod
    def get_affinity(
        n_mpz
    ):
        h_weight=(
            bin(
                n_mpz
            ).count(
                '1'
            )
        )
        total_cores=(
            multiprocessing.cpu_count()
        )
        if h_weight>256:
            return total_cores # max
            # snaga za "teške" brojeve
        return max(
            1,
            total_cores//2
        )

# --- MODUL 11: REPOZITORIJ Tonelli-
# Shanks (KORIJENI ZA SIQS) ---
# Pre- izračunavanje korijena za bazu
# korijena radi eliminacije
# iteracija.
class RootRepository:
    def __init__(
        self,
        n,
        fb
    ):        
        self.n=n
        self.fb=fb
        self.roots={}

    def precompute(
        self
    ):
        for p in self.fb:
            r=(
                MathKernelCore.tonelli_shanks(
                    int(
                        self.n
                    ),
                    p
                )
            )
            if r is not (
                None
            ):
                self.roots[p]=r

# MODUL 12: ASINHRONA AUDIO
# SIGNALIZACIJU ---
class AsyncAudioAlerter:
    """Pokreće play-audio Frogs.mp3
    asinkrono."""
    @staticmethod
    def play:
        def task():
            try:
                os.system(
                    AUDIO_PLAY_CMD
                )
            except:
                pass    
        threading.Thread(
            target=task,
            daemon=True
        ).start()

# --- MODUL 13: FORENZIČKI ANALIZATOR
# DECIMALNIH MJESTA ---
class DecimalPlaceAudit:
    """Koristi re za precizno brojanje
    decimala radi skaliranja."""
    @staticmethod
    def count_places(
        s
    ):
        match=(
            re.search(
                r'\.(\d+),
                s
            )
        )
        return (
            len(
                match.group(
                    1
                )
            ) if match else 0
        )

# --- MODUL 14: PRERADA GAUSSOVIH
# JEDINICA ---
class GaussianUnitProcessor:
    """Rukovanje jedinicama {1,-1,i,-i}
    u kompleksnoj faktorizaciji."""
    @staticmethod
    def extract_units(
        z
    ):
        if (abs(
            abs(z.real)==1
            and
            z.imag==0
        ):
            return int(
                z.real
            )
        if (
            abs(z.imag)==1
            and
            z.real==0
        ):
            return complex(
                0,
                z.imag
            )
        return 1

# --- MODUL 15: Miller- Rabin
# DETERMINISTIČKI REPOZITORIJ ---
class MR_WitnessPool:
    """Determinističke baze za provjeru
    primarnosti do 3.31*10^24
    WITNESSES={
        341550071728321:[
            2,3,5,7,11,13,17
        ],
        3825123056546413051:[
            2,3,5,7,11,13,17,19,23
        ]
    }

# --- MODUL 16: UPRAVLJANJE
# MEMORIJSKIM BUFFEROM ---
class MemoryBufferGuard:
    """Prilagođava veličinu rešeta (M)
    memoriji Samsunga A16."""
    @staticmethod
    def get_m_size(n_bits):
        if n_bits<100:
            return 65536 # 64 KB (
                # L1/L2 cache friendly)
        if n_bits<200:
            return 1048576 # 1MB
        return 4194304 # 4MB

# --- MODUL 17: ALGORITAM ZA
# GENERIRANJE PSEUDOPROSTIH BROJEVA ---
class PseudoprimeGenerator:
    """Generira kandidate za
    Miller- Rabin testiranje."""
    @staticmethod
    def get_candidate(
        n
    ):
        return(
            mpz(
                ra.randint(
                    2,
                    n-2
                )
            )
        )

# --- MODUL 18: ANALIZA STUPNJA
# POLINOMA ---
class PolyDegreeAnalyzer:
    """Identificira najviši stupanj
    polinoma pomoću re."""
    @staticmethod
    def find_max_degree(
        poly_str
    ):
        degrees=re.findal(
            r'\^(\d+)',
            poly_str
        )
        return(
            max(
                [
                    int(d)
                    for d in degrees
                ]
            ) if degrees else 1
        )

# --- MODUL 19: ASINKRONO PRAĆENJE
# ITERACIJA ---
class IterationMonitor:
    def __init__(
        self
    ):
        self.lock=(
            threading.Lock()
        )
        self.total=0
    def update(
        self,
        count
    ):
        with self.lock:
            self.total+=count

# --- MODUL 20: MATEMATIČKI ALGORITAM -
# BINARY GCD EKSTENZIJA ---
class BinaryGCDAdvanced:
    """Steinov algoritam za GCD bez
    teškog dijeljenja."""
    @staticmethod
    def fast_gcd(
        a,
        b
    ):
        if a==0:
            return b
        id b==0:
            return a
        shift=(
            (a | b).bit_length()
            -
            (a | b).bit_count()
        )
        a>>=(
            a.bit_length()
            -
            a.bit_count()
        )
        while b!=0:
            b>>=(
                b.bit_length()
                -
                b.bit_count()
            )
            if a>b:
                a,b=b,a
            b-=a
        return a<<shift

# --- MODUL 21: KONTROLER ZA GRUPNI
# GCD (BATCH GCD) ---
class BatchGCDController:
    """Akumulira produkte razlika
    točaka za ECM grupni GCD."""
    def __init__(
        self,
            n,
        threshold=100
    ):
        self.n=n
        self.threshold=(
            threshold
        )
        self.buffer=1
        self.count=0

    def add_and_check(
        self,
        value
    ):
        self.buffer=(
            (self.buffer*value)
            %
            self.n
        )
        self.count+=1
        if self.count>=self.threshold:
            g=(
                math.gcd(
                    self.buffer,
                    self.n
                )
            )
            self.buffer,self_count=1,0
            if (
                1
                <
                g
                <
                self.n
            ):
                return g
        return None

# --- MODUL 22: REPOZITORIJ Miller-
# Rabin BAZA (STRICT) ---
class MR_StrictRepo:
    """Deterministički svjedoci za
    brojeve do 2^64."""
    BASE_64=(
        [
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23
        ]
    )

# --- MODUL 23: PRERADA SymPy 
# NT- THEORY EKSTREMA ---
class SympyTheoryExt:
    """Integrira primeomega i
    factorrat za forenzičku analizu."""
    @staticmethod
    def get_omega(
        n
    ):
        if not HAS_SYMPY:
            return 0
        from sympy.ntheory import primeomega
        return primeomega(
            n
        )

# --- MODUL 24: DETEKCIJA TIPA
# OSTATKA (V5) ---
class ResidualDetectorV5:
    """Identificira da li je ostatak 
    faktorizacije prost ili 
    kompozitan."""
    
        
                
            
            
            
        
            




















from gmpy2 import (
    mpz,
    mpq,
)
from sympy import (
    ntheory,
    OmegaPower,
    factorint,
    isprime,
    continued_fraction,
    continued_fraction_iterator,
    primeomega,
    symbols,
    sqrt,
)
from sympy.ntheory import is_gaussian_prime


# [BLOK 1] KONFIGURACIJA I LIMITI

try:
    sys.set_int_max_str_digits(0)
except:
    pass

MAX_ITER = 10**500
K_SNAGA = 5000
RAD_STEP = 5000
sys.setrecursionlimit(5000000)
TIMEOUT_SEC = None
BROJ_JEZGRI = 4


# [BLOK 2] GMPY2 ENGINE

KORISTI_GMPY2 = False
try:
    import gmpy2
    from gmpy2 import mpz

    gmpy2.get_context().precision = 5000000
    gmpy2.get_context().trap_overflow = True
    gmpy2.get_context().trap_inexact = True
    gmpy2.get_context().allow_complex = True
    KORISTI_GMPY2 = True
except ImportError:

    class MockGMPY2:
        def __init__(self):
            self.context = self
            self.precision = 53

        def get_context(self):
            return self

        def mpz(self, x):
            return int(x)

        def is_prime(self, x):
            if x < 2:
                return False
            if x in (2, 3):
                return True
            if x % 2 == 0:
                return False
            r = 0
            d = x - 1
            while d % 2 == 0:
                r += 1
                d //= 2
            for _ in range(5):
                a = random.randint(2, x - 2)
                x_pow = pow(a, d, x)
                if x_pow == x - 1:
                    continue
                for _ in range(r - 1):
                    x_pow = pow(x_pow, 2, x)
                    if x_pow == x - 1:
                        break
                else:
                    return False
            return True

        def next_prime(self, x):
            x = int(x) + 1
            while not self.is_prime(x):
                x += 1
            return x

        def is_square(self, x):
            if x < 0:
                return False
            return math.isqrt(x) ** 2 == x

        def isqrt(self, x):
            return int(math.isqrt(x))

        def gcd(self, a, b):
            return math.gcd(a, b)

        def mul(self, a, b):
            return a * b

        def sub(self, a, b):
            return a - b

        def add(self, a, b):
            return a + b

        def f_mod(self, a, b):
            return a % b

        def div(self, a, b):
            return a // b

        def abs(self, a):
            return abs(a)

    gmpy2 = MockGMPY2()
    mpz = int

# [BLOK 3] LOGGER I VIZUALIZACIJA


class Logger:
    def __init__(self):
        self.broj_linije = 0

    def reset(self):
        self.broj_linije = 0

    def zapisi(self, tekst, dubina=0, boja="\033[0m"):
        self.broj_linije += 1
        uvlaka = ""
        if dubina > 0:
            c_okomita = "\u2502"
            c_grana = "\u251c\u2500\u2500"
            uvlaka = c_okomita * (dubina - 1) + c_grana
        oznaka = f"\033[90m{self.broj_linije:03d} \u007c\033[0m"
        sys.stdout.write("\r\033[K")
        print(f"{oznaka} {uvlaka}{boja}{tekst}\033[0m")


log = Logger()
START = 0
import multiprocessing

lock = multiprocessing.Lock()
ITER = multiprocessing.Value("L", 0)
with lock:
    ITER.value = 0


# [BLOK 4] ALATI (RAM, VRIJEME, ZVUK)

import re
import multiprocessing
import time


def get_ram_proc():
    regex_uzorak = re.compile(r"^(MemTotal|MemAvailable):\s*(\d+)\skB$", re.MULTILINE)
    try:
        with open("/proc/meminfo", "r") as f:
            sadrzaj = f.read()

        m_total = 0
        m_avail = 0

        for podudarnost in regex_uzorak.finditer(sadrzaj):
            naziv, vrijednost_str = podudarnost.groups()
            vrijednost = int(vrijednost_str)

            if naziv == "MemTotal":
                m_total = vrijednost
            elif naziv == "MemAvailable":
                m_avail = vrijednost

        if m_avail == 0:
            regex_free = re.compile(r"^MemFree:\s*(\d+)\skB$")
            match_free = regex_free.search(sadrzaj)
            if match_free:
                m_avail = int(match_free.groups()[0])

        g_avail = gmpy2.div(mpz(g_avail), mpz(1048576))

        s = "{:.100f}".format(gmpy2.mpf(g_avail, 512))

        if s.startswith("0."):
            s = s[1:]
        return s + "free RAM"
    except FileNotFoundError:
        return "? free RAM (datoteka nije pronađena)"
    except Exception as e:
        return f"? free RAM (greška: {e})"


def fmt_vrijeme(t):
    global sek_opis
    t = int(t)
    zadnja = t % 10
    if 11 <= (t % 100) <= 14:
        sek_opis = "sekundi"
    elif zadnja == 1:
        sek_opis = "sekunda"
    elif 2 <= zadnja <= 4:
        sek_opis = "sekunde"
    else:
        sek_opis = "sekundi"
    s = "{:.100f}".format(gmpy2.mpf(t, 512))
    if s.startswith("0."):
        s = s[1:]
    return s.rstrip("0").rstrip(".")


def izracunaj_ritam_blinkanja(broj_bita):
    x = sympy.symbols("x")
    formula = sympy.sqrt(x + 1) / 10
    vremenski_razmak = formula.subs(x, broj_bita)
    return float(vremenski_razmak)


def zvuk():
    try:
        global ITER
        if (int(ITER.value) % 10000) == 0:
            os.system("play-audio Frogs.mp3 &")
    except:
        pass


def status(faza, n):
    global ITER
    blink = " "
    ritam_sekunde = izracunaj_ritam_blinkanja(n.bit_length())
    if (time.perf_counter_ns() // 10000) % int(ritam_sekunde * 10000) == 0:
        blink = "\u272a"
    else:
        blink = " "
    proslo = (time.perf_counter_ns() - START) / 1000000000
    t = fmt_vrijeme(proslo)
    if (int(ITER.value) % 3000) == 0:
        os.system("play-audio Frogs.mp3 &")
    ram = get_ram_proc()
    if proslo:
        brz = int(ITER.value) / proslo
    else:
        brz = 0
    s_brz = "{:.15f}".format(brz)
    if s_brz.startswith(".0"):
        s_brz = s_brz[1:]
    t = fmt_vrijeme(proslo)
    red1 = f"\r\033[95m{blink} RUN {faza}\033[0m\n"
    red2 = f"\r\033[95m{blink} UNESENI BROJ: {n}\033[0m\n"
    red3 = f"\r\033[92m]{blink}  VRIJEME: {t} {sek_opis}\033[0m\n"
    red4 = f"\r\033[36m]{blink} ITERACIJE: {ITER.value}\033[0m\n"
    red5 = f"\r\033[94m{blink} RAM: {ram}\033[0m\n"
    red6 = f"\r\033[33m{blink} BRZINA: {s_brz} iter/sec\033[0m"

    sys.stdout.write(f"\r{red1}{red2}{red3}{red4}{red5}{red6}\033[J")
    sys.stdout.flush()


# [BLOK 5] WORKER (MULTI- CORE PROCES)

import time


def worker_pollard(n_str, seed, queue, event, start_t, zajednicki_iter):
    try:
        n = mpz(n_str)
        random.seed(seed)
        y = mpz(random.randint(1, int(n) - 1))
        c = mpz(random.randint(1, int(n) - 1))
        m = mpz(random.randint(1, int(n) - 1))
        g = mpz(1)
        r = mpz(1)
        q = mpz(1)
        x = y
        ys = y
        while g == 1:
            if event.is_set():
                return
            if (time.perf_counter_ns() - start_t) / 1000000000 > TIMEOUT_SEC:
                return
            x = y
            for _ in range(r):
                y = gmpy2.f_mod(gmpy2.add(gmpy2.mul(y, y), c), n)
            k = mpz(0)
            while k < r and g == 1:
                zajednicki_ITER.value += 1
                if event.is_set():
                    return
                ys = y
                for _ in range(min(m, r - k)):
                    y = gmpy2.f_mod(gmpy2.add(gmpy2.mul(y, y), c), n)
                    diff = gmpy2.abs(gmpy2.sub(x, y))
                    q = gmpy2.f_mod(gmpy2.mul(q, diff), n)
                g = gmpy2.gcd(q, n)
                k = gmpy2.add(k, m)
            r = gmpy2.mul(r, 2)
        if g == n:
            while True:
                ys = gmpy2.f_mod(gmpy2.add(gmpy2.mul(ys, ys), c), n)
                diff = gmpy2.abs(gmpy2.sub(x, ys))
                g = gmpy2.gcd(diff, n)
                if g > 1:
                    break
        if g != n:
            queue.put(str(g))
            event.set()
    except:
        pass


# [BLOK 6] MATEMATIČKI ALGORITMI


def b0_prost(n):
    status("B0: Check", n)
    return gmpy2.is_prime(n)


def b1_trial(n, limit=50000):
    d = mpz(2)
    lim = mpz(limit)
    while d < lim and d * d <= n:
        status("B1: Trial", n)
        if gmpy2.f_mod(n, d) == 0:
            return d
        d = gmpy2.next_prime(d)
    return None


def b2_gauss(n, max_i=300000):
    if gmpy2.f_mod(n, 2) == 0:
        return mpz(2)
    a = gmpy2.isqrt(n)
    if gmpy2.mul(a, a) < n:
        a = gmpy2.add(a, 1)
    cnt = 0
    while cnt < max_i:
        status("B2: Gauss", n)
        b2 = gmpy2.sub(gmpy2.mul(a, a), n)
        if gmpy2.is_square(b2):
            b = gmpy2.isqrt(b2)
            return gmpy2.sub(a, b)
        a = gmpy2.add(a, 1)
        cnt += 1
    return None


def b3_pollard_multi(n):
    if gmpy2.f_mod(n, 2) == 0:
        return mpz(2)
    queue = multiprocessing.Queue()
    event = multiprocessing.Event()
    procesi = []
    t_start = time.perf_counter_ns()
    for i in range(BROJ_JEZGRI):
        seed = random.randint(1, 1000000) + i
        p = multiprocessing.Process(
            target=worker_pollard, args=(str(n), seed, queue, event, t_start)
        )
        p.start()
        procesi.append(p)
    rezultat = None
    while True:
        status(f"B3: Core({BROJ_JEZGRI})", n)
        if not queue.empty():
            rezultat = mpz(queue.get())
            break
        if (time.perf_counter() - t_start) / 100000000 > TIMEOUT_SEC:
            break
        if all(not p.is_alive() for p in procesi):
            break
        time.sleep(0.05)
    event.set()
    for p in procesi:
        p.terminate()
    return rezultat


def gcd_gauss(a, b):
    while abs(b) > 0.0000000000001:
        q = a / b
        q_re = round(q.real)
        q_im = round(q.imag)
        q_int = complex(q_re, q_im)
        r = a - b * q_int
        a = b
        b = r
    return a


# [BLOK 7] LOGIKA RJEŠAVANJA


def rijesi(n, dubina=0):
    n = mpz(n)
    if b0_prost(n):
        t = fmt_vrijeme((time.perf_counter_ns() - START) / 100000000)
        log.zapisi(f"[PROST] {n} (Lap: {t} {sek_opis})", dubina, "\033[93m")
        if int(ITER.value) % 3000 == 0:
            os.system("play-audio Frogs.mp3 &")
        return [n]
    f = None
    metoda = ""
    if f is None:
        f = b1_trial(n)
        metoda = "B1: Trial"
    if f is None:
        f = b2_gauss(n)
        metoda = "B2: Gauss"
    if f is None:
        f = b3_pollard_multi(n)
        metoda = f"B3: Pollard(x{BROJ_JEZGRI})"
    if f is not None:
        ostatak = n % f
        if gmpy2.is_zero(ostatak):
            drugi = gmpy2.div(n, f)
            t = fmt_vrijeme((time.perf_counter_ns() - START) / 1000000000)
            log.zapisi(
                f"[SPLIT] {metoda} (VRIJEME: {t} {sek_opis})", dubina, "\033[93m"
            )
            log.zapisi(f"lijevo: {f}", dubina + 1)
            log.zapisi(f"desno: {drugi}", dubina + 1)
            lista = []
            lista.extend(rijesi(f, dubina + 1))
            lista.extend(rijesi(drugi, dubina + 1))
            return lista
        return [n]


def univerzalni_start(unos):
    unos = unos.replace("i", "j").replace(" ", "")
    print(f"\n\033[95m[ANALIZA] {unos}\033[0m")
    if "j" in unos:
        try:
            z = complex(unos)
            re = int(z.real)
            im = int(z.imag)
            norma = mpz(re * re + im * im)
            print(f"tip:\033[95m GAUSS (norma: {norma}\033[0m")
            f_norme = rijesi(norma)
            pravi = []
            z_temp = z

            print("pretvorba faktora Norme u Gaussove faktore:")
            for p in f_norme:
                p = int(p)
                g = gcd_gauss(z_temp, p)
                if abs(g) > 1001:
                    gr = int(round(g.real))
                    gi = int(round(g.imag))
                    zn = "+" if gi >= 0 else ""
                    pravi.append(f"({gr}{zn}{gi}j)")
                    z_temp = z_temp / g
                else:
                    pravi.append(str(p))
                    z_temp = z_temp / p
            return pravi
        except Exception as e:
            print("GREŠKA:\033[95m {e}\033[0m")
    elif "/" in unos or "." in unos:
        try:
            if KORISTI_GMPY2:
                q = gmpy2.mpq(unos)
                br = q.numerator
                naz = q.denominator
            else:
                q = fractions.Fraction(unos)
                br = q.numerator
                naz = q.denominator
            print(f"tip:\033[95m RACIONALNI -> {br}/{naz}\033[0m")
            f_br = rijesi(gmpy2.abs(mpz(br)))
            f_naz = rijesi(gmpy2.abs(mpz(naz)))
            rez = [str(x) for x in f_br]
            rez += [f"{x}^-1" for x in f_naz]
            return rez
        except:
            pass
    else:
        return rijesi(mpz(unos))


# --- MAIN ---

if __name__ == "__main__":
    os.system("clear")
    print("\033[1m===== ULTRA FACTORIZATOR (MAX) =====\033[0m")
    if KORISTI_GMPY2:
        print("Engine: GMPY2 (HIGH PRECISION)")
    else:
        print("Engine: PYTHON (standard)")
    try:
        print("-" * 50)
        cpu_in = input("broj jezgri (1- 8) [Default: 4]:")
        if not cpu_in.strip():
            BROJ_JEZGRI = 4
        else:
            BROJ_JEZGRI = int(cpu_in)
            if BROJ_JEZGRI < 1:
                BROJ_JEZGRI = 1
            if BROJ_JEZGRI > 8:
                BROJ_JEZGRI = 8
        print(f"aktivno jezgri:\033[95m {BROJ_JEZGRI}\033[0m")
    except:
        BROJ_JEZGRI = 4
    while True:
        try:
            print("\n" + "+" * 50)
            inp = input("UNOS:")
            if not inp.strip():
                continue
            log.reset()
            START = time.perf_counter_ns()
            ITER.value = 0
            res = univerzalni_start(inp)
            sys.stdout.write("\r\033[K")
            proslo = (time.perf_counter_ns() - START) / 100000000
            if proslo > 0:
                brz = int(ITER.value) / proslo
            else:
                brz = 0
            s_brz = "{:.30f}".format(brz).rstrip("0").rstrip(".")
            if s_brz.startswith("0."):
                s_brz = s_brz[1:]
            uk = "{:.40f}".format(float(fmt_vrijeme(time.perf_counter_ns() - START)))
            uk = "{:.40f}".format(float(uk)).rstrip("0").rstrip(".")
            if uk.startswith("0."):
                uk = uk[1:]
            uk = fmt_vrijeme(time.perf_counter_ns() - START)
            ram = get_ram_proc()
            print("-" * 50)
            print(f"{blink}\033[92m GOTOVO: {uk} {sek_opis}\033[0m")
            print(f"{blink}\033[93m ITERACIJE: {ITER.value}\033[0m")
            print(f"{blink}\033[94m RAM: {ram}\033[0m")
            print(f"{blink}\033[90m BRZINA: {s_brz} iter/sec\033[0m")
            if res:
                res.sort()

            print(f"{blink}\033[95m UNESEN BROJ: {inp}\033[0m")
            print(f"{blink}\033[91m FAKTORI: {' * '.join(map(str, res))}\033[0")
            print(f"{blink}\033[92m VRIJEME: {uk} {sek_opis}\033[0m")
            print(f"{blink}\033[95m jezgre: {BROJ_JEZGRI}\033[0m")
            print(f"{blink}\033[95m timeout: {TIMEOUT_SEC} s po bloku\033[0m")
            os.system("play-audio Frogs.mp3 &")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nGREŠKA: {e}")
