# ----------------------------------------------------------------------------------------------
# ll_rho.py - THE SHADOW CODE EDITION
# IN HONOR OF ANONYMOUS TERMUX DEVS & THE KIRKMAN PROTOCOL
# \U0001F422 "Festina Lente - Žuri polako kroz faktore" \U0001F422
# \U0001F422 "Let the code speak where the face is hidden" \U0001F422
#/data/data/com.termux/files/home/myenv/bin/python
#-*-coding:utf-8-*-
import os
import math
import sys
import multiprocessing
import sympy
from sympy import isprime
try:
    import gmpy2
    from gmpy2 import mpz
    V_MOTOR="gmpy2 AKTIVAN (TURBO)\U0001F407"
except ImportError:
    from math import gcd
    V_MOTOR="NATIVE PYTHON\U0001F422"
v_akt=os.path.expanduser('~/myenv/bin/activate_this.py')
if os.path.exists(v_akt) and not sys.prefix.endswith('myenv'): 
    exec(open(v_akt).read(),{'__file__':v_akt}) 

def f_get_ram_proc():
    try:
        with open('/proc/meminfo','r') as f:
            v_sadrzaj=f.read()
            v_total=0
            v_avail=0
            for line in v_sadrzaj.splitlines():
                if 'MemTotal:' in line:
                    v_total=int(line.split()[1])
                if 'MemAvailable:' in line:
                    v_avail=int(line.split()[1])
            if v_total>0:     
                return round(100*(1-v_avail/v_total),1)
            return "N/A"
    except Exception:
        return "N/A"
                    
import random
import time
import collections
import datetime
import decimal
import select
# import sympy
import mpmath
# import multiprocessing
from collections import deque
from datetime import datetime
from sympy import sympify
from sympy import factorint
from sympy import factor_list
from sympy import I
from sympy import Integer
from sympy import Rational
# from sympy import isprime
from mpmath import mp
from mpmath import mpf
from mpmath import mpc
from multiprocessing import Pool
from multiprocessing import processes
from decimal import Decimal

if multiprocessing.cpu_count()>2: 
    from concurrent.futures import ProcessPoolExecutor 
    from concurrent.futures import as_completed 
else: 
    pass
     
# ---TURBO MOTOR: gmpy2 SEKCIJA
try: 
    import gmpy2
    from gmpy2 import mpz
    from gmpy2 import mpf
    from gmpy2 import gcd
    from gmpy2 import powmod
    from gmpy2 import next_prime
    from gmpy2 import is_prime
    from gmpy2 import isqrt
    from gmpy2 import is_square
    from gmpy2 import jacobi
    from gmpy2 import bit_length
    from gmpy2 import div
    from gmpy2 import mod
    from gmpy2 import gcdext
    from gmpy2 import iroot
    from gmpy2 import invert
    from gmpy2 import is_strong_selfridge_prp
    from gmpy2 import bit_scan0
    from gmpy2 import bit_scan1
    from gmpy2 import is_perfect
    from gmpy2 import mpfr
    from gmpy2 import hamdist
    from gmpy2 import popcount
    from gmpy2 import fac
    from gmpy2 import random_state
    from gmpy2 import mpz_urandomb
    from gmpy2 import mpz_rrandomb
    from gmpy2 import get_context
    from gmpy2 import set_context
    from gmpy2 import mpq
    from gmpy2 import mpc
    from gmpy2 import agm
    from gmpy2 import num_digits
    from gmpy2 import get_emax_max
    from gmpy2 import get_emin_min
    from gmpy2 import mpfr_ramdom
    from gmpy2 import random_state
    from gmpy2 import get_context
    from gmpy2 import set_context    
    g_abs=gmpy2.abs
    get_context().precision=min(5000000,get_max_precision())
    get_context().emax,get_context().emin=get_emax_max(),get_emin_min()
    get_context().emax=get_emax_max()
    get_context().emin=get_emin_min()    
    # G_STATUS ="AKTIVAN (MAX SPEED) \U0000F407"
except ImportError:
    import math
    from math import gcd
    from math import isqrt
    from math import prod
    from decimal import getcontext as get_context
    from decimal import Decimal
    from decimal import ROUND_FLOOR
    mpz=int
    g_abs=abs
    get_context=decimal.getcontext    
    ROUND_FLOOR=decimal.ROUND_FLOOR
    get_context().prec=5000000
    # G_STATUS="NATIVE PYTHON \U00001F422"
     
# -- GLOBALNA PODEŠAVANJA --
get_context().rounding=ROUND_FLOOR
mp.dps=5000
ENORM_ITER=10**500
K_SNAGA=10**5000
RAD_STEP=5000
def f_format_vremena(v_sec_raw):
    global v_sek_opis
    v_it=int(v_sec_raw)
    v_zadnja=v_it%10
    if 11<=(v_it%100)<=14:
        v_sek_opis="sekundi"
    elif v_zadnja==1:  
        v_sek_opis="sekunda"
    elif 2<=v_zadnja<=4:
        v_sek_opis="sekunde"
    else:
        v_sek_opis="sekundi"
    v_vrijeme_str=format(v_sec_raw,'f').rstrip('0').rstrip('.').lstrip('0')
    return v_vrijeme_str
def provjeri_brzo(n):
    """brza dijagnostika kroz gmpy2 arsenal"""
    v_n=mpz(n)
    if gmpy2.is_strong_selfridge_prp(v_n):
        return "PROST",[v_n]
    v_korijen=isqrt(v_n)
    if gmpy2.is_square(v_n):
        return "SAVRŠENI KVADRAT",[v_korijen,v_korijen] 
    for v_prost in[2,3,5,7,11,13,17,19,23,29,31,37]: 
        if gmpy2.f_mod(v_n,v_prost)==0:
            return "MALI FAKTOR",[mpz(v_prost),v_n//v_prost]
    return "SLOŽEN",[]
def pollard_rho_algoritam(n):
    if not(n&1):return 2
    v_n_mpz=mpz(n)
    v_it=0
    if gmpy2.is_strong_selfridge_prp(v_n_mpz):return n
    v_x=gmpy2.mpz_urandomb(gmpy2.random_state(),gmpy2.bit_length(n))%(n-2)+2
    v_y=v_x
    v_c=gmpy2.mpz_urandomb(gmpy2.random_state(),gmpy2.bit_length(n))%(n-1)+1
    v_g=mpz(1)
    
    while v_g==1:
        v_it+=1
        v_x=(gmpy2.powmod(v_x,2,n)+v_c)%n
        v_y=(gmpy2.powmod(v_y,2,n)+v_c)%n 
        v_y=(gmpy2.powmod(v_y,2,n)+v_c)%n
        v_g=gcd(abs(v_x-v_y),n)
        if v_g==n:
            return pollard_rho_algoritam(n)
    v_g_final=v_g
    return v_g_final,v_it
def obradi_ulaz(v_u): 
    try: 
        # SymPify iz 27. reda pretvara tekst u broj 
        v_s=sympify(v_u) 
        if hasattr(v_s,'is_integer') and v_s.is_integer:
            # PREBACUJEM U MPZ ZA MAKSIMALNU BRZINU
            return "INT",gmpy2.mpz(str(v_s)),24 
        if "I" in str(v_s): 
            return "GAUSS",v_s 
        # mpfr iz 38. reda za decimalnu preciznost 
        return "MALI FAKTOR",[int(f) for f,e in sympy.factorint(int(v_s)).items() for _ in range(e)]
    except Exception: 
            return "ERROR",str(v_u)

def f_gauss_rho_izvrsitelj(v_n,v_limit_rho,v_preciznost_gauss):
    import sympy
    import time
    import gmpy2
    v_pocetak_vrijeme=time.perf_counter()
    v_n_mpz=gmpy2.mpz(v_n)
    if gmpy2.is_prime(v_n_mpz):
        return (v_n_mpz,f_format_vremena(time.perf_counter()-v_pocetak_vrijeme))
    v_faktor=pollard_rho_algoritam(v_n_mpz)
    v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)
    return (v_faktor,v_p)                    
if __name__ == "__main__":
    def main():
        v_brojac_ciklusa=0
        v_stanje=gmpy2.random_state()        
    
        # -- POČETAK ALGORITMA --
        while True:
            v_brojac_ciklusa+=1            
            v_unos_raw=input("\033[1;32m\u2328\ufe0f utipkaj broj/eve: \033[0m").strip().replace(' ','') or "1"
            v_j=int(input("\033[1;34m\u2699\ufe0f KOLIKO AKTIVIRATI JEZGARA?\033[0m").strip() or "1")
            v_ram=f_get_ram_proc()
            print(f"CIKLUS:\033[95m {v_brojac_ciklusa}\033[0m")                        
            print(f"RAM:\033[95m {v_ram}\033[0m")            
            v_lista=[v_s.strip() for v_s in v_unos_raw.split(',')]     
        for u_raw in v_lista:
                G_FOUND_FACTORS=set
                v_pokusaji=0
                iter_ukupno=0            
                v_rezultat_obrade=obradi_ulaz(u_raw)    
                v_tip=v_rezultat_obrade[0]
                n=v_rezultat_obrade[1]
                if v_tip=="MALI FAKTOR":
                for f in v_rezultat_obrade[2]:
                        G_FOUND_FACTORS.add(f)
                    n//=sympy.prod(v_rezultat_obrade[2])
                if n==1:continue                
                if sympy.isprime(n):
                    G_FOUND_FACTORS.add(n)
                    n=1
                if n>1:
                    for f in range(2,501):
                        while n%f==0:
                            G_FOUND_FACTORS.add(f)
                            n//=f
                if n==1:continue
                if not sympy.isprime(n):
                    v_pocetak_vrijeme=time.perf_counter()

                    v_pokusaja=0
                    v_brojac_ciklusa=0
                    iter_ukupno=0
                    v_limit_rho=gmpy2.mpz(int(10**9.5))
                    v_preciznost_gauss=gmpy2.npz(100)
                    v_max_ciklusa=15
                    with multiprocessing.Pool(v_j) as (v_p):
                        while v_brojac_ciklusa<v_max_ciklusa:
                            v_brojac_ciklusa+=1
                            iter_ukupno+=(v_j*v_limit_rho)
                            v_rezultati=v_p.starmap(f_gauss_rho_izvrsitelj,[(n,v_limit_rho,v_preciznost_gauss) for _ in range(v_j)])
                            




                    
                    
                v_scale=v_rezultat_obrade[2]        
                n_prikaz=n
                v_pokusaji+=1
                iter_ukupno+=1                
                print(f"\n\033[1;33m\u2ba1 Uzbal ANALIZA:\033[95m{n}\033[0m")
                with processing.Pool(processes=v_j) as pool:
                    v_l=[]
                    for i in range(v_j):
                        v_start=i*v_scale
                        v_end=(i+1)*v_scale   
                        v_l.append(pool.apply_async(f_obradi_blok,(n,v_start,v_end)))
                pool.close()
                pool.join()
                for v_job in v_l:
                    v_res=v_job.get()
                    if v_res:
                        G_FOUND_FACTORS.update(v_res)
                        v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)         
                        v_ram=v_get_ram_proc()
                        v_blink="\u272a" if (iter_ukupno//5000)%2==0 else " "
                    print(f"{v_blink} CIKLUS:\033[95m {v_brojac_ciklusa}\033[0m")
                    print(f"{v_blink}\n\033[1;36m\u2795 UNESENI BROJ:\033[95m {n_prikaz}\033[0m")
                    print(f"{v_blink}\a\033[1;36m\u2795 POKUŠAJ/I:\033[95m {v_pokusaji}\033[0m")
                    print(f"{v_blink}\u2514\u25b6 ITERACIJE:\033[95m {iter_ukupno}\033[0m")
                    print(f"{v_blink}\u2514\u25b6 FAKTOR:\033[95m {G_FOUND_FACTORS}\033[0m")
                    print(f"{v_blink}\u2514\u25b6 RAM:\033[95m {v_ram}\033[0m")
                    print(f"{v_blink}\u2515\u25b6 LAP VRIJEME:\033[95m {v_p}\033[95m")
                    os.system("play-audio Frogs.mp3 &")

                v_proizvod=Decimal('1')
                for f in G_FOUND_FACTORS:
                    v_proizvod*=Decimal(str(f))
                if v_proizvod==Decimal(str(n_prikaz)):
                    v_lista.pop()
                    break
         















                
           #  v_privremeni_rezultat=sympy.factorint(n)
           #  if len(v_privremeni_rezultat)>1 or (len(v_privremeni_rezultat)==1 and list(v_privremeni_rezultat.values())[0]>1):
             #   v_status="MALI FAKTOR"
              #  for v_f1,v_exp in v_privremeni_rezultat.items():
               #     for _ in range(v_exp):


            #if n>1:
             #   while n>1:
              #      v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
               #     print(f"\n\033[1;33m\u2ba1 ANALIZA:\033[95m {n_prikaz}\033[0m")
                #    v_privremeni_rezultat=provjeri_brzo(n)
                 #   v_status=v_privremeni_rezultat[0] 
                  #  v_faktori=v_privremeni_rezultat[1]
                   # if len(v_faktori)==0:
                    #    v_znak_rada=v_blink
                    #else:
                     #   v_znak_rada="\u2705"
                    #if len(v_faktori)>0:
                        #v_trenutni_is=f"{v_faktori[0]}"
                    #else:
                     #   v_trenutni_is="TRAGANJE...\u23f3"
                      #  v_ram=f_get_ram_proc()
                    #if v_status=="PROST":
                     #   v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)
                      #  # os.system('clear')         
                       # v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                        #print(f"{v_blink} CIKLUS:\033[95m {v_brojac_ciklusa}\033[0m")
                        #print(f"{v_blink}\033[1;32m\u2714\ufe0f BROJ {n_prikaz} JE PROST: {n}\033[0m")
                        #rint(f"{v_blink} POKUŠAJ/I:\033[95m {v_pokusaji}\033[0m")
                        #print(f"{v_blink} ITERACIJE:\033[95m {iter_ukupno}\033[0m")
                        #print(f"{v_blink} LAP VRIJEME:\033[95m {v_p} {v_sek_opis}\033[0m")
                        #print(f"{v_blink} RAM:\033[95m {v_ram}% ISKORIŠTENOSTI\033[0m")
                        # os.system("play-audio Frogs.mp3 &")
                        ## input("\n\033[1;32m>>>PRITISNI enter ZA NASTAVAK...\033[0m")                        
                        #G_FOUND_FACTORS.append(n)  
                        #n=1
                    #elif v_status=="MALI FAKTOR":
                        #v_f1=v_faktori
                        #G_FOUND_FACTORS.append(v_f1)
                        #n//=v_f1
                        #v_pokusaji+=1
                        # iter_ukupno+=1
                        #v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                    #if len(v_faktori)==0:
                        #v_znak_rada=v_blink
                    #else:
                        #v_znak_rada="\u2705"
                    #if len(v_faktori)>0:
                        #v_trenutni_is=f"{v_faktori[0]}"
                    #else:
                        #v_trenutni_is="TRAGANJE...\u23f3"
                        #v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)
                        #v_ram=f_get_ram_proc()
                        # os.system('clear')
                        #v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                        #print(f"{v_blink} CIKLUS:\033[95m {v_brojac_ciklusa}\033[0m")
                        #print(f"{v_blink}\n\033[1;36m\u2795 UNESENI BROJ:\033[95m {n_prikaz}\033[0m")
                        #print(f"{v_blink}\a\033[1;36m\u2795 POKUŠAJ/I:\033[95m {v_pokusaji}\033[0m")
                        #print(f"{v_blink}\u2514\u25b6 ITERACIJE:\033[95m {iter_ukupno}\033[0m")
                        #print(f"{v_blink}\u2514\u25b6 FAKTOR:\033[95m {v_trenutni_is[0]}\033[0m")
                        #print(f"{v_blink}\u2514\u25b6 RAM:\033[95m {v_ram}% ISKORIŠTENO\033[0m")
                        #print(f"{v_blink}\u2514\u25b6 LAP TIME:\033[95m {v_p} {v_sek_opis}\033[0m")
                        #os.system("play-audio Frogs.mp3 &")
                        ## input("\n\033[1;32m>>>PRITISNI enter ZA NASTAVAK...\033[0m")
                        # G_FOUND_FACTORS.append(v_faktori[0])
                        # n//=v_faktori[0]  
                        #v_g=mpz(1)
                        #while v_g==1:
                            #v_rez_rho,v_it_rho=pollard_rho_algoritam(n)
                            #v_g=v_rez_rho
                            #v_pokusaji+=v_it_rho
                            #iter_ukupno+=1

                            # PRETVORBA FAKTORA PREINAČENOG BROJA U FAKTORE ORIGINALNOG BROJA       
                            #v_f_pravi=Decimal(str(v_g))/(Decimal(10)**v_scale)
                            #G_FOUND_FACTORS.append(v_g)
                            #n//=v_rez_rho
                            #v_g=mpz(1)
                            #from sympy import isprime
                            #if n>1 and isprime(n):
                                #G_FOUND_FACTORS.append(n)
                                #v_g=mpz(0)
                                #break
                            
                            #v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)
                            #v_ram=f_get_ram_proc()
                            v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                            # os.system('clear')
                        if len(v_faktori)==0:
                            v_znak_rada=v_blink
                        else:
                            v_znak_rada="\u2705"
                        if len(v_faktori)>0:
                            v_trenutni_is=f"{v_faktori[0]}"
                        else:
                            v_trenutni_is="TRAGANJE...\u23f3"
                            v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)
                            v_ram=f_get_ram_proc()
                            # os.system('clear')
                            v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                            print(f"{v_blink} CIKLUS:\033[95m {v_brojac_ciklusa}\033[0m")
                            print(f"{v_blink}\033[1;36m\u2795 BROJ NA OBRADI:\033[95m {n_prikaz}\033[0m")           
                            print(f"{v_blink}\a\033[1;36m\u2795 POKUŠAJ/I:\033[95m {v_pokusaji}\033[0m")
                            print(f"{v_blink}\u2514\u25b6 ITERACIJE:\033[95m {iter_ukupno}\033[0m")
                            print(f"{v_blink}\u2514\u25b6 FAKTOR:\033[95m {v_trenutni_is[0]}\033[0m")
                            print(f"{v_blink}\u2514\u25b6 RAM:\033[95m {v_ram}% ISKORIŠTENO\033[0m")
                            print(f"{v_blink}\u2514\u25b6 LAP VRIJEME:\033[95m {v_p} {v_sek_opis}\033[0m")
                            os.system("play-audio Frogs.mp3 &")
                            # input("\033[1;32m>>>PRITISNI enter ZA NASTAVAK...\033[0m")
                        #if n>1:
                            #G_FOUND_FACTORS.append(decimal.Decimal(str(n))/(decimal.Decimal(10)**v_scale))  
                            #v_prikaz_faktora=[]                        
                            #v_brojac_ciklusa+=1
                            #v_proizvod=Decimal('1')
                            #for f in G_FOUND_FACTORS:
                                #v_proizvod*=Decimal(str(f))
                                #v_s=str(f)
                                #if v_s.startswith('0.'):v_s=v_s[1:]
                                #if v_s.startswith('-0.'):v_s='-'+v_s[2:]
                                #v_prikaz_faktora.append(v_s)
                            #v_provjera=round(v_proizvod*(Decimal(10)**v_scale))
                            #v_status_ver="TOČNO" if v_provjera==n_prikaz else "GREŠKA"
                            #v_sec_raw=time.perf_counter()-v_pocetak_vrijeme
                            #v_it=int(v_sec_raw)
                            if v_it%100>=11 and v_it%100<=14:
                                v_sek_opis="sekundi"
                            else:
                                v_zadnja=v_it%10
                                if v_zadnja==1:
                                    v_sek_opis="sekunda"
                                elif v_zadnja>=2 and v_zadnja<=4:
                                    v_sek_opis="sekunde"
                                else:
                                    v_sek_opis="sekundi"        
                                v_vrijeme_f=f_format_vremena(v_sec_raw)
                                v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                                v_ram=f_get_ram_proc()
                            if len(v_faktori)==0:
                                v_znak_rada=v_blink
                            else:
                                v_znak_rada="\u2705"
                            if len(v_faktori)>0:
                                v_trenutni_is=f"{v_faktori[0]}"
                            else:
                                v_trenutni_is="TRAGANJE...\u23f3"
                                v_p=f_format_vremena(time.perf_counter()-v_pocetak_vrijeme)
                                v_ram=f_get_ram_proc()
                                # os.system('clear')
                                v_blink="\u272a" if (iter_ukupno//10000)%2==0 else " "
                                print(f"{v_blink} CIKLUS:\033[95m {v_brojac_ciklusa}\033[0m")
                                print(f"{v_blink}\n\a\033[1;36m\u2795 KONAČNI FAKTORI:\033[95m {v_prikaz_faktora}\033[0m")
                                print(f"{v_blink}\u2514\u25b6 POKUŠAJI:\033[95m {v_pokusaji}\033[0m")
                                print(f"{v_blink}\u2514\u25b6 ITERACIJE:\033[95m {iter_ukupno}\033[0m")
                                print(f"{v_blink}\u2514\u25b6 UKUPNO VRIJEME OBRADE:\033[95m {v_vrijeme_f} {v_sek_opis}\033[0m")
                                print(f"{v_blink}\u2705\u2696\ufe0f VERIFIKACIJA:\033[95m {v_status_ver}\033[0m")
                                print(f"{v_blink}\U0001F4C8 RAM STATUS:\033[95m {f_get_ram_proc()} % ISKORIŠTENO\033[0m")
                                os.system("play-audio Frogs.mp3 &")
                                input("\n\033[1;32m>>> PRITISNI enter ZA NASTAVAK\033[0m")
                
            
#if __name__ == "__main__":
    #try:
        #main()
    #except KeyboardInterrupt: 
        #print("\n\n\033[1;31m\u2ba0\ufe0f [[G_STATUS]] PRISILNI PREKID -> IZLAZ\033[0m")
        #sys.exit()
