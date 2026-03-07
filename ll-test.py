#-*-coding:utf-8-*-

from gmpy2 import mpz

def llt(v_p):
    try:
        v_p = int(v_p)
        if v_p < 3:
            print("Eksponent mora biti veći od 2.")
            return "NEVALIDAN"
        v_m = mpz(2)**v_p - 1
        v_s = mpz(4)
        for i in range(v_p - 2):
            v_s = (v_s * v_s - 2) % v_m
            if i % 1000 == 0:
                print(f"računam: {i}/{v_p-2}...", end="\r")
        if v_s == 0:
            return "PROST"
        else:
            return "SLOŽEN"
    except ValueError:
        return "GREŠKA"

while True:
    p_input = input("\nunesi p (ili 'q' za kraj):").lower()
    if p_input == 'q' or p_input == 'exit':
        print("Pucchia via! Izlazim...")
        break

    rezultat = llt(p_input)
    if rezultat == "GREŠKA":
        print("greška: Unesi ispravan cijeli broj!")
    else:
        print(f"\nrezultat: {rezultat}")
