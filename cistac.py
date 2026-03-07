# posveta: Ovaj je program napisan za tebe,
# da kroz kod i razum pronađemo put,
# dok vrijeme teče i istina vreba,
# u svakom je redu smisao zasut,
# za vječnost što nam zapravo treba.

import os
import time
import datetime
import gmpy2
import sympy
from multiprocessing import Pool

# --- GLOBALNI REGISTAR ---
gmpy2.get_context().precision=100000

META_POTPISI={
    
# podešavanje preciznosti
gmpy2.get_context().precision=50000

def provjera_integriteta_osnove(
    lokacija
):
    if(
        os.path.exists(
            lokacija
        )
    ):
        return True
    return False

def procesor_tkiva(
    putanja
):
    ime=os.path.basename(
        putanja
    ).lower()

    if(
        "architect" in ime
        or "gmpy2" in ime
    ):
        return "SVETINJA: ZAŠTIĆENO"

    if(
        "cache" in putanja.lower()
        or "/.ruff_cache" in putanja.lower()
        or ".tmp" in putanja.lower()
        or "temp" in putanja.lower()
        or "ruff" in putanja.lower()
        or ime.startswith('.')
    ):
        starost=time.ctime(
            os.path.getmtime(
                putanja
            )
        )
        return f"METASTAZA: {starost}"

    return "ZDRAVO"

def obavi_sjeckanje(
    putanja,
    ukupna_masa
):
    potvrda=input(
        f"""Da li je za fajl {putanja} potrebno brisanje
    





def obavi_sjeckanje(
    putanja
):
    try:
        velicina=os.path.getsize(
            putanja
        )
        nule=sympy.Integer(
            velicina
        )
        with open(
            putanja,
            "wb",
            buffering=0
        ) as f:
            f.write(
                b'\x00'*velicina
            )
            f.flush()
            os.fsync(
                f.fileno()
            )
        os.remove(
            putanja
        )
        return f"UNIŠTENO ({nule} B)"
    except Exception:
        return "GREŠKA"
        
def procesor_tkiva(
    putanja
):
    ime=os.path.basename(
        putanja
    ).lower()
    
    if (
        "architect" in ime
         or "gmpy2" in ime
    ):
        return "SVETINJA: ZAŠTIĆENO"
    
    if (
        "cache" in putanja.lower()
        or "/.ruff_cache/" in putanja.lower()
        or ".tmp" in putanja.lower()
        or "temp" in putanja.lower()
        or "ruff" in ime
        or ime.startswith('.')
    ):
        starost=time.ctime(
            os.path.getmtime(
                putanja
            )
        )
        print(
            f"""\n--- POZDRAV SAMOSTALNOJ METASTAZI
             ---"""
        )
        print(
            f"""LOKACIJA: {putanja}"""
        )
        print(
            f"""STAROST: {starost}"""
        )
        poruka=input(
            """Što želim poručiti ovom parazitu?"""
        )
        potvrda=input(
            f"""Poslije '{poruka}',
            potrebno brisanje? (y/n):"""
        )
        if (
            potvrda.lower()=='y'
        ):
            return obavi_sjeckanje(
                putanja
            )
        else:
            return "POMILOVANA METASTAZA"
            
    ekst_ususpomene=(
        '.png',
        '.jpg',
        '.jpeg',
        '.mp3',
        '.mp4',
        '.pdf'
    )
    
    if (
        putanja.lower().endswith(
            ekst_ususpomene
        )
    ):
        print(
            f"""\nANALIZA (Adobe Acrobat/Media):
            {putanja}"""
        )
        subprocess.run(
            [
                "termux-open",
                putanja
            ]
        )
        izbor=input(
            """Izmučena lopta (zvuka)? (y=DA/n=NE):"""
        )
        
        if (
            izbor.lower()=='y'
        ):
            return obavi_sjeckanje(
                putanja
            )
        else:
            return "SPAŠENA USPOMENA"
    
    return "OSTALO: IGNORIRANO"
    
if __name__ == "__main__":
    vrijeme=datetime.datetime.now()
    print(
        f"""--- START: {vrijeme} ---"""
    )
    
    meta=[    
        "/sdcard/DCIM",
        "/sdcard/Android",
        "/sdcard/Androids",
        "/data/data/com.termux/files/home",
        os.path.expanduser("~/.cache")
    ]
    datoteke=[]
    for lokacija in meta:
        if (
            os.path.exists(
                lokacija
            )
        ):
            for koren,dirs,fajlovi in os.walk(
                lokacija
            ):
                print(
                    f"""PUTANJA: {koren}"""
                )

                if (
                    ".trash" in koren.lower()
                    or ".cache" in koren.lower()
                    or "cache" in koren.lower()
                    or "temp" in koren.lower()
                ):
                    input(
                        """ --- PRONAĐEN BRLOG! ---
                        """
                    )

                for f in fajlovi:
                    datoteke.append(
                        os.path.join(
                            koren,
                        f
                    )
                )

    ukupna_masa=sympy.Integer(0)
    obrisana_masa=sympy.Integer(0)
    
    for stavka in datoteke:
        try:
            velicina_fajla=os.path.getsize(
                stavka
            )
            ukupna_masa+=sympy.Integer(
                velicina_fajla
            )
            rezultat=procesor_tkiva(
                stavka
            )
            print(
                f"""STATUS: {rezultat}"""
            )
            if (
                "UNIŠTENO" in rezultat
                or "KEŠ" in rezultat
            ):
                obrisana_masa+=sympy.Integer(
                    velicina_fajla
                )
            input("""
                Pritisni ENTER za nastavak..."""
            )        
        except Exception as e:
            print(f"GREŠKA U {stavka}: {e}")
            continue
    
    if (
        ukupna_masa>0
    ):
        postotak=(
            obrisana_masa/ukupna_masa
        )*100
        cist_postotak=postotak.evalf(
            30
        )
        prikaz=format(
            cist_postotak,
            'g'
        )
        print(
            f"""
            \n --- FINALNA DIJAGNOSTIKA ---    
            OSLOBOĐENO: {obrisana_masa} B
            EFIKASNOST ČIŠĆENJA:
            {prikaz}%
            """
        )
    else:
        print(
            f"""
            \n --- OČIŠĆEN SISTEM ---
            """
        )
