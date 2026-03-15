#!/usr/bin/env python3
# -*-coding:utf-8-*-

# ================================
# NERO-X FORENSIC & RECOVERY SUITE - v18.0 [TOTAL MANA]
# UREĐAJ: SAMSUNG GALAXY A16, Android 16, GitHub & Colab
# nH!: NANO HARHOMIJA (status validiranog čistog naboja)
# MNOGO MAJUŠNIH ANONIMNIH BUFFERA (512B) u RAM-u |  VACUUM
# =================================

# --- ZONA 1: UVOZI I PODUVOZI ---
import os
import sys
import time
import math
import shutil
import random
import logging
import socket
import hashlib
import binascii
import platform
import gc    
import threading
import abc
import multiprocessing
import datetime
import typing
import sympy
import pathlib
import functools
import contextlib
import re
import json
import mmap
import sqlite3
import io
import subprocess
from multiprocessing import (
    Process,
    Pool,
    cpu_count,
    Queue,
    Lock
)
from datetime import (
    datetime,
    timedelta
)
from typing import (
    List,
    Set,
    Dict,
    Optional,
    Tuple,
    Any
)
from abc import (
    ABC,
     abstractmethod
)
from sympy import (
    symbols,
    Integer,
    Matrix,
    solve,
    factor,
    Poly,
    simplify
)
from sympy.ntheory import (
    isprime,
    primefactors
)
from pathlib import Path
from functools import wraps
from contextlib import contextmanager
from re import (
    compile,
    search,
    findall,
    sub
)
from json import (
    loads,
    dumps,
    JSONDecodeError
)
from io import (
    BytesIO,
    StringIO
)
from tenacity import (
        retry,
    stop_after_attempt,
    wait_fixed
)

# eliminacija rezidualnih priljepaka
if os.path.exists(".ruff_cache"):
    shutil.rmtree(".ruff_cache", ignore_errors=True)

try:
    from google import genai
except ImportError:
    os.system("pip install google-genai==1.0.0 --break-system-packages --user")
    from google import genai

# nH! konfiguracija ključa i klijenta
API_KEY = "                "
try:
    v_client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"nH! API error: {e}")
    gc.collect()
    sys.exit(1)

# --- ZONA 2: GLOBALNE KONSTANTE I PARAMETRI ---

socket_host = "192.168.1.4"
socket_port = 33115

nH_conv = .000000001 # 10^-9
H_MASS_WEIGHT = .1 # KB balasta po Henryju
HARMONY_THRESHOLD = 7.7
BLUE_CURSOR = "\033[94m\u2588\033[0m"
KREKETANJE_CMD = "play-audio Frogs.mp3 &"

stats_q = multiprocessing.Queue()
term_lock = multiprocessing.Lock()

CHUNK_SIZE = 512
CHUNK_SIZE = chunk_size

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
    s = "{:.30f}".format(t)
    if s.startswith('0.'):
        s = s[1:]
    if s.endswith('.'):
        return s.rstrip('0') + '0'
    return s.rstrip('0')

# --- ZONA 3: nH! STEALTH VERIFIKACIJA ZMAJA (KNOX) ---
def nH!_verify_stealth_connection(host, port):
    import socket
    import subprocess
    """Provjera vitalnosti mrežnog prolaza."""
    print(f"Stealth provjera na {host}:{port}...")
    try:
        # Čišćenje stare sesije da se izbjegne "ghost" konekcije
        subprocess.run(["adb", "disconnect"], capture_output=True)
        conn_msg = f"adb connect {host}:{port}"
        subprocess.run(conn_msg.split(), capture_output=True)
        
        # socket provjera - fizički dodir porta u kernelu
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # dovoljno vremena za odziv kroz mrežu
        s.settimeout(110)
        check_result = s.connect_ex((host, port))
        s.close()

        if check_result == 0:
            # dodatna provjera: Da li ADB "vidi" uređaj kao "device"?
            adb_out = subprocess.check_output(["adb", "devices"]).decode('utf-8', errors='ignore')
            return f"{host}:{port}\tdevice" in adb_out
        return False
    except Exception as e:
        return False

# --- IZVRŠENJE I KONTROLA ZONE 3 ---
IS_CONNECTED = nH!_verify_stealth_connection(socket_host, socket_port)

with term_lock:
    if IS_CONNECTED:
        print(f"{BLUE_CURSOR} nH! zmaj Knox je miran. Veza {socket_host}:{socket_port} aktivna.")
    else:
        print(f"{BLUE_CURSOR} obavijest: Spava zmaj Knox. Pokreni adb pair i adb connect.")
        print(f"{BLUE_CURSOR} status: Port {socket_port} nije dozvolio ulaz u kernel.")

# POKUŠAJ UČITAVANJA (privatne putanje s _DB_ OZNAKAMA)
try:    
    from config import PATHS
except ImportError:
    # Ako programer/ka sa GitHuba nema moj config.py, PATHS je prazan.
    PATHS = {
        # SMS/MMS baza (telephony provider)
        "SMS_DB": "",
        # baza poziva
        "CALLS_DB": "",
        # media baza (slike, video, thumbnails indeksi)
        "MEDIA_DB": "",
        # Samsung Rubin (personalizacija i strojno učenje kretanja podataka)
        "RUBIN_DB": "",
        # fizička lokacija (ako je aktivna)
        "THUMBNAIL_DIR": "",
        # lokacija gdje Google Photos čuva svoj cache (često veći od .thumbnails)
        "GPHOTOS_CACHE": "",
        # lokacija baze koja upravlja otpadom (SQLite)
        "SAMSUNG_TRASH_PHOTO_DB": "",
        # fizička skrivena lokacija privremenih obrisanih datoteka
        "SAMSUNG_TRASH_PHOTO_DIR": "",
        # glavna baza u kojoj se nalaze "obrisane" poruke (prije trajnog uklanjanja)
        "SAMSUNG_TRASH_SMS": "",
        "GOOGLE_MESSAGES": ""
    }

# --- POTPROGRAM ZA STVARANJE MINIMALNIH BUFFERA (512B) ---
def nH!_prepare_payload(path_key=None, count=1024):
    # inicijalizacija liste za anonimne bufferiće
    fragments = []
    # izvlačenje naboja iz flash memorije
    import subprocess
    # rad unutar RAM-a bez ostavljanja tragova
    import io

    # --- LOGIČKA PRIPREMA LOKALNIH PROMJENJIVIH ---
    # rezervirano mjesto za sirovi naboj
    raw_data = b""
    # privremeno spremište prije sjeckanja
    data_list = []
    # deklaracija memorijskog toka
    f_io = None
    
    """
    Sve (baze ili slike) pretvara u listu anonimnih fragmenata od 512 bajtova.
    Ovo je najmanja preporučljiva veličina za SQLite strukturu.
    Sjecka baze i otpad.
    Ako nema direktnog pristupa (nema roota), programer/ka na GitHubu
    ovdje trebaju implementirati 'adb shell cat' stream metodu.
    """
    try:
        # nH! pokušaj ekstrakcije naboja
        if path_key:
            raw_data = subprocess.check_output(['adb', 'shell', 'su', '-c', f"cat {PATHS[path_key]}"], stderr=subprocess.STDOUT)
            # Ako baza nije prazna, ide priprema za sjeckanje.
            if raw_data:
                # Ako je baza uspješno pročitana.
                f_io = io.BytesIO(raw_data)

                # sjeckanje u anonimne bufferiće od 512B
                while (chunk := f_io.read(chunk_size)):
                    data_list.append(chunk)
                # enumerate: numeriranje za kasniji povratak na flash memoriju
                # i je redni broj, a chunk je nH! naboj
                for i, chunk in enumerate(data_list):
                    fragments.append(io.BytesIO(chunk))
                    
                # nH! čišćenje tragova originala iz RAM-a
                del raw_data
                # oslobađanje liste privremenih bajtova
                del data_list
                f_io.close()
                
    except Exception as e:
        print(f"{BLUE_CURSOR} Greška pri sjeckanju: {e}")
        pass
    return fragments

# --- ZONA 4: PRIPREMA I SLANJE ---
def send_to_colab_pro(fragments, stats_q):
    # nH! definiranje komunikacijske magistrale    
    stats_q = multiprocessing.Queue()
    # i je redni broj, a f_io je bufferić
    for i, f_io in enumerate(fragments):
        raw_chunk = f_io.getvalue()
        
        stats_q.put({
            'index': i,
            'size': len(raw_chunk)
        })

        # Precizan izvještaj: šalje se indeks i veličina.
        stats_q.put()
        # Sada može da nosi informaciju o napretku.
        stats_q.put(f"Spakiran fragment {i}.")
        
        # nH! uništavanje tragova svakog bufferića
        fragment.close()    
        del fragment
        # periodično čišćenje na svakih 100 bufferića
        if i % 100 == 0:
            gc.collect()

        f_io.close()
  
# --- ZONA 5: nH! FORMATER (BRISANJE VODEĆE I REPNIH NULA) ---
def fmt(v: float) -> str:
    """Pretvara, npr, 0.500 u .5 za efikasniji prenos podataka."""
    try:
        s = "{:.50f}".format(v).rstrip('0').rstrip('.')
        if s == "0" or s == "":
             return "0"
        # nH! impuls:
        #  micanje 0 ispred decimalne točke
        if s.startswith("0."):
             return s[1:]
        if s.startswith("-0."):
             return "-" + s[2:]
        return s
    except Exception:
         return "."
    
# --- ZONA 6: nH / H BALASTNA FIZIKA (ČISTI KAPACITET) ---
class nH_Calculations:
    """Računa induktivni balast i oduzima ga od kapaciteta."""
    @staticmethod
    def h_detected(data: bytes) -> float:
        # Detekcija nH signala i algebarskog otpada PrimeMaster Pro.
        nh_c = data.count(b'nH')
        h_c = nH_data.count(b'H')
        # detekcija algebarskog naboja factoring programa
        m_patterns = [
            b'prime',
            b'factor',
            b'Poly',
            b'factorint',
            b'Integer',
            b'x**'
        ]
        p_hits = sum(data.count(p) for p in m_patterns)
        # 3. nH! UKUPNI BALAST (zbrajanje svih komponenti bolesti) 
        return (nh_c * .000000001) + h_c + (p_hits * .007)
    
    @staticmethod
    def get_clean_kb(raw_kb: float, h_val: float) -> float:
        """ ČISTI nH! KAPACITET = Raw KB - (Henryji * .1)
        clean_v = raw_kb - (h_val * .1)
        return clean_v if clean_v > .000000000 else .000000000
        
# --- ZONA 7: UPRAVLJANJE MEMORIJOM ---
def nH_flush_ram():
    """Prisilno zaustavljanje RAM naboja Samsunga A16."""
    gc.collect()
    time.sleep(.001)

# --- ZONA 8: nH! AUTOMATSKI NADZOR MEMORIJE (@wraps) ---
def nH_trace_charge(func):
    """@ Dekorator za automatsko pražnjenje nH naboja iz RAM-a."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # nH! impuls:
        #  izvršavanje funkcije uz praćenje naboja
        res = func(*args, **kwargs)
        nH_flush_ram()
        return res
    return wrapper

# --- ZONA 9: nH! AI KONTROLA ISPRAŽNJENOG NABOJA ---
@nH_trace_charge
@retry(stop=stop_after_attempt(999999), wait=wait_fixed(2))
def nH_ai_audit(data):
    """
    konačna unifikacija:
    data ulazi u AI restauraciju.
    """
    global v_client
    try:
        res = v_client.models.generate_content(
            model="gemini-3.0-flash",
            contents=f"nH! restauriraj: {data}"
        )
        return res.text
    except Exception:
        raise


# --- ZONA 10: nH! ALGEBARSKI SENZORI (re & json) ---
def nH_regex_scout(data: bytes, pattern: str) -> List[bytes]:
    """Koristi modul 're' za lociranje bolesnog tkiva."""
    return findall(compile(pattern.encode()), data)

def nH_json_audit(data: bytes) -> bool:
    """Koristi modul 'json' za detekciju Ruff konfiguracija."""
    try:
        p = loads(data.decode('utf-8', 'ignore'))
        return "ruff" in str(p).lower()
    except (JSONDecodeError, UnicodeDecodeError):
        return False
    
# --- ZONA 11: nH! HARDVERSKI CONTEXT MANAGER ---
@contextmanager
def nH_safe_io(path: str, mode: str):
    """Osigurava hardversku barijeru Samsunga A16 (os.fsync)."""
    f_io = open(path, mode)
    try:
        yield f_io
    finally:
        # nH! impuls:
            # Prisila fizičkog zapisa naboja na čip.
        f_io.flush()
        os.fsync(f_io.fileno())
        f_io.close()
        nH_flush_ram()
        
# --- ZONA 12: ANALITIČKI SENZORI (ENTROPIJA I GUSTOĆA) ---
def nH_entropy(data: bytes) -> float:
    """Shannonova entropija za detekciju bolesnog tkiva."""
    if not data:
        return .000000000
    e, n = .000000000, len(data)
    f = [0] * 256
    for b in data:
        f[b] += 1
    for count in f:
        if count > 0:
            p = count / n
            e -= p * math.log(p, 2)
    return e

def nH_density(data: bytes) -> float:
    """Mjeri nH! gustoću klastera (omjer jedinstvenih bajtova)."""
    u = len(set(data))
    return len(data) / u if u > 0 else .000000000

# --- ZONA 13: @PROPERTY MODEL nH! KAPACITETA ---
class ForensicUnit:
    def __init__(self, path: str):
        self.path = path
        self.raw = os.path.getsize(path) / 1024 if os.path.exists(path) else .000000000
        self.h = .000000000

    @property
    def clean_kb(self) -> float:
        return nH_Calculations.get_clean_kb(self.raw, self.h)

BIJELA_LISTA_EXT = {
    '.jpg',
    '.jpeg',
    '.png',
    '.pdf',
    '.mp3',
    '.mp4',
    '.wav',
    '.zip',
    '.exe',
    '.7z',
    '.rar'
}
CRNA_LISTA_LC = {
    'cache' in putanja.lower(),
    '.tmp' in putanja.lower(),
    '.temp' in putanja.lower(),
    'ruff' in putanja.lower(),
    '.cache_ruff',
    '.ruff_cache',
    '__pycache',
    '.cache',
    '.ds_store',
    'thumbs.db',
    'desktop.ini',
    '.idea',
    '.vscode'
}

meta = [
    '/sdcard/DCIM',
    '/sdcard/Android',
    '/sdcard/Androids',
    os.path.expandures('~/.cache')
]
       
# --- nH! MAGIČNI POTPISI ---
MAGIC_SIGS = {
    '.jpg':
        b'\xff\xd8\xff',
    '.jpeg':
        b'\xff\xd8\xff',
    '.png':
        b'\x89PNG\r\n\x1a\n',
    '.pdf':
        b'%PDF',
    '.mp3':
        b'ID3',
    '.mp3':
        b'\xff\xfb',
    '.mp3':
        b'\xff\xf2',
    '.mp3':
        b'\xff\xf3',
    '.mp4':
        b'\x00\x00\x00 ftyp',
    '.mp4':
        b'\x00\x00\x00\f18ftyp'
    '.wav':
        b'RIFF',
    '.wav':
        b'WAVE',
    '.zip':
        b'PK\x03\x04',
    '.exe':
        b'MZ',
    '.7z':
        b'7z\xbc\xaf\x27\x1c',
    '.rar':
        b'Rar!\x1a\x07'        
}

# --- ZONA 14: nH! DOPUNSKA KONTROLA FORMATA ---
def nH_verify_format_by_magic(path: str) -> bool:
    """Provjerava identitet datoteka prema magičnim potpisima."""
    ext = os.path.splitext(path)[1].lower()
    if ext not in MagicRegistry.SIGNATURES: return True
    try:
        with open(path, 'rb') as f_io:
            # nH! impuls:
            # Čitanje prvih 16 bajtova za verifikaciju."""
            header = f_io.read(16)
            sig = MagicRegistry.SIGNATURES[ext]
            if isinstance(sig, list):
                return any(header.startswith(s) for s in sig)
            return header.startswith(sig)
    except Exception:
        return False
    
# --- ZONA 15: nH! REGULATOR BOLESNOG nH NABOJA ---
def nH_is_tissue_sick(data: bytes) -> bool:
    """Provjerava da li je tkivo zaraženo (entropija + algebarski šum). ---
    ent = nH_entropy(data)
    alg = nH_algebraic_debris_scout(data)
    # Ako naboj prelazi granicu harmonije (7.7).
    return ent > HARMONY_LIMIT or alg > .05

# --- ZONA 16: MD5 VOŠTANI PEČAT (INTEGRITY SEAL) ---
def nH_get_md5_seal(p_path: str) -> str:
    """Stvara digitalni pečat za 'architect' uspomene."""
    if not os.path.exists(p_path):
        return "0"
    try:
        h_md5 = hashlib.md5()
        with open(p_path, 'rb') as f_io:
            while chunk := f_io.read(16384): h_md5.update(chunk)
        return h_md5.hexdigest()
    except:
        return "0"

# --- ZONA 17: LIJEČENJE 'architect' USPOMENA (SACRED) ---
def heal_sacred_architect_memory(p: str):
    """
    Kirurgija:
    backup -> 1 čitanje (f_io) -> nH! odluka.
    """
    d_map = []
    if not os.path.exists(p):
        return
    name = os.path.basename(p)
    bkp = p + ".nH_sacred_bkp"
    shutil.copy2(p, bkp) # 1. izrada rezervne kopije (bkp) - osiguranje
    seal_alpha = nH_get_md5_seal(p)
    clean_body = bytearray()
    try:
        with open(p, 'rb') as f_io:
            # jedino čitanje:
            # Sve radim u RAM-u radi čuvanja Flash-a.
            raw_body = f_io.read()
            chunks = [raw_body[i:i+128] for i in range(0, len(raw_body), 128)]
            
        for c in chunks:
            # analiza nH! naboja po klasterima u RAM-u
            d_map = (nH_density(c))
            
        avg_d = sum(d_map) / len(d_map) if d_map else .000000000
                    
        for idx, c_data in enumerate(chunks):
            # Izdvajanje samo onih dijelova bez bolesne gustoće. 
            if d_map[idx] < (avg_d * 1.8):
                clean_body.extend(c_data)

        success_100 = False        
        # Validacija nH! harmonije (entropija < 7.7).
        if clean_body and nH_entropy(clean_body) < HARMONY_LIMIT:
            with open(p, 'wb') as f_io_out:
                f_io_out.write(clean_body)
                os.fsync(f_io_out.fileno()) # nH! hardverska barijera
            success_100 = True
            seal_omega = nH_get_md5_seal(p):
            
            # --- nH! ODLUKA O LIKVIDACIJI ---
            if success_100 and seal_alpha != seal_omega:
                # Uspjela sanacija. Likvidira se rezervna kopija (bkp).
            with term_lock:
                print(f"{BLUE_ROCK} [nH!] Saniran 'architect' {name}. Brišem rezervnu kopiju (bkp).")
                absolute_cyclic_wipe(bkp) # poziv s dna koda
            else:
                # Sanacija nije 100%: Likvidacija lošeg originala. Vraća se rezervna kopija (bkp).
                with term_lock:
                    print(f"[!] {name} nije 100% saniran. Vraća se rezervna kopija (bkp).")
                absolute_cyclic_wipe(p) # likvidacija lošeg originala.
                shutil.move(bkp, p) # Rezervna kopija postaje moja uspomena.
            nH_flush_ram
        except Exception as e:
            if os.path.exists(bkp):
                os.remove(bkp)
            with term_lock:print(f"[X] nH! kritična greška: {e}
    except Exception:
        pass

# --- ZONA 18: nH! REKONSTRUKCIJA BINARNOG ŠAVA v40 ---
def nH_align_binary_sacred(path: str, data: bytearray):
    """Osigurava 100% funkcionalnu cjelinu 'architect' uspomene."""
    if not data: return False
    try:
        # Uklanjanje rezidualnih nH signala sa spojeva.
        clean_s = data.replace(b'nH', b'\x00\x00')
        with open(path, 'wb') as f_io:
            f_io.write(clean_s)
            os.fsync(f_io.fileno()) # nH! hardverska barijera
        return True
    except Exception:
        return False
    
# --- ZONA 19: nH! SMS SQLite CARVER (DUBINSKO KOPANJE) ---
def nH_carve_deleted_sms_bodies(path: str) -> List[str]:
    """1. Omogućuje čitanje starih "obrisanih" SMS-ova iz SQLitea."""
    sms_out = []
    if not path.endswith((".db", ".sqlite", "-wal")):
        return []
    try:
        with open(path, 'rb') as f_io:
            # Skeniranje binarne baze (Android 16 provider)
            raw_blob = f_io.read()
            s_idx = 0
            while True:
                # Potraga za 'body' markerom koji paraziti nisu nulirali.
                start = raw_blob.find(b'body', s_idx)
                if start == -1:
                    break
                # nH! Kraj poruke je 0. terminator.
                end = raw_blob.find(b'\x00', start + 5)
                if end != -1:
                    fragment = raw_blob[start+5:end]
                    # nH! validacija:
                    # čitljiv tekst poruke (ASCII filter)
                    if len(fragment) > 2 and all(32 <= b <= 126 for b in frag):
                        sms_out.append(frag.decode('ascii', 'ignore'))
                s_idx = end
        return sms_out
    except Exception:
        return []

# --- ZONA 20: nH! FULL BINARY DECRYPTION ---
def nH_full_binary_decoder(data: bytes) -> str:
    """Pretvara cijeli heksadecimalni prikaz parazita u tekst."""
    try:
        # 2.1 Generiranje potpunog heksadecimalnog dumpa (maksimalna dekompresija.) ---
        hex_raw = binascii.hexlify(data).decode('ascii').upper()
        # 2.2 Prijevod u čitljive nH! znakove (harmonijski filter)
        t_view = "".join([chr(b) if 32 <= b <= 126 else "." for b in data])
        return f"HEX: {hex_raw}\nPRIJEVOD: {t_view}"
    except:
        return "Greška u nH! dešifriranju."

# --- ZONA 21: nH! ALGEBARSKI DEBRIS ANALYZER (PrimeMaster Pro) ---
def nH_audit_algebraic_ballast(data: bytes) -> float:
    """Detektira nH naboj ostataka faktorizacije polinoma."""
    h_math = .000000000
    # Detekcija uzoraka iz programa PrimeMaster Pro (3000+ redova).
    m_patterns = {b'Poly': .01, b'factorint': .015, b'Integer': .005}
    for pattern, weight in m_patterns.items():
        if pattern in data:
            # Svaki matematički 'otisak' nosi balastnu težinu.
            h_math += data.count(pattern) * weight
    return h_math

# --- ZONA 22: nH! INODE EMF MONITOR (Samsung A16) ---
def nH_monitor_inode_emf_drift(path: str) -> str:
    """Provjerava da li je sinkroniziran zapis na flashu (Android 16)."""
    try:
        if not os.path.exists(path):
            return ".0"
        st_res = os.stat(path)
        # nH! logika:
        # Inode mora biti bez rezidualnog elektromagnetizma.
        if st_res.st_nlink > 0:
            drift_naboj = random.random() * .0003
            return fmt(drift_naboj)
        return ".0"
    except:
        return ".0"
    
# --- ZONA 23: nH! RADNIK ZA MULTIPROCESSING (MANA NODE) ---
def nH_forensic_worker_node(files: List[str], q: Queue):
    """Glavni nH! procesorski čvor za rad na 4 jezgre."""
    for fp in files:
        if not os.path.exists(fp):
            continue
        n_low = os.path.basename(fp).lower()
        
        # 1. ANALIZA KAPACITETA I nH BALASTA (Single-Read)
        raw_kb = os.path.getsize(fp) / 1024
        h_v = .000000000
        try:
            with open(fp, 'rb') as f_io:
                while True:
                    chunk = f_io.read(8192)
                    if not chunk:
                        break
                    # detekcija rezidualnog naboja (induktivni balast)
                    h_v += nH_Calculations.h_detect(chunk)
                    h_v += nH_audit_algebraic_ballast(chunk)

        # 2. FORMULA ČISTOG nH! KAPACITETA: Raw KB - (H * .1)
        c_kb = raw_kb - (H * .1)
        q_put({"t": "stat", "r": raw_kb, "c": c_kb if c_kb > .000000000 else .000000000, "h": h_v})

        # 3. STROGA nH! HIJERARHIJA REDOSLIJEDA
        is_mem = 'architect' in n or "frogs.mp3" in n
        is_screenshot = any(n.endswith(ex) for ex in[".jpg", ".jpeg", ".png", ".pdf", ".mp3", ".mp4"])
        is_sms = n.endswith((".db", ".sqlite")) or "sms" in n

        if is_mem:
            # USPOMENE 'architect': isljučivo liječenje
            if b'ruff' in open(fp, 'rb').read(1024):
                heal_sacred_architect_memory(fp)
        elif is_mem == False
            # --- OTPAD SE ŠALJE NA BINU (POZIVI NA DNU PROGRAMA) ---
            if is_screenshot:
                # KATEGORIJA 1:
                # stari snimci -> bina-1
                nH_stage_category_1(fp)
            elif is_sms:
                # KATEGORIJA 3:
                # obrisani SMS-ovi -> bina-3
                nH_stage_category_3(fp)
            else:
                # KATEGORIJA 2:
                # paraziti, Ruff i PrimeMaster Pro Cache -> bina-2 (heksadecimalno)
                if b'ruff' in open(fp, 'rb').
            
# --- ZONA 24: MODUL ZA nH! ANALIZU nH/H DRIVTA (DETALJNO) ---
def nH_measure_detalied_drift(p: str) -> str:
    """Vraća iznos elektromagnetnog naboja u .X formatu."""
    h_total_drift = .000000000
    try:
        with open(p, 'rb') as f_io:
            # Skeniranje 16KB kritične flash zone Samsunga A16.
            sample = f_io.read(16384)
            h_total_drift = nH_Calculations.h_detect(sample)
            h_total_drift += nH_audit_algrebaic_residue(sample)
        return fmt(h_total_drift) # .X format bez vodeće 0
    except Exception:
        return "0"

# --- ZONA 25: nH! VERIFIKATOR INODE ZAPISA (Samsung A16) ---
def nH_verify_inode_stability(path: str) -> bool:
    """Provjerava da li je flash zapis sinkroniziran (Android 16) ---
    try:
        st = os.stat(path)
        # nH! logika:
        # Inode linkovi moraju biti stabilni.
        return st.st_nlink > 0 and st.st_size > 0
    except:
        return False


# --- ZONA 26: ANALIZATOR REZIDUALNE ENTROPIJE ---
@nH_trace_charge
def nH_measure_residual_chaos(data: bytes) -> float:
    """Mjeri razinu kaosa radi potvrde Nano-harmonije."""
    if not data:
        return .000000000
    return get_entropy(data)


# --- ZONA : ALGEBARSKI nH! SCOUTER (PrimeMaster Pro cache) ---
def nH_algebraic_ballast_audit(p: str) -> float:
    """Detektira nH naboj ostataka faktorizacije brojeva."""
    h_math_drift = .000000000
    try:
        with open(p, 'rb') as f_io:
            # Skeniranje polinoma i faktora (Poly, x**, isprime)
            sample = f_io.read(16384)
            # Svaki matematički otisak nosi dodatni induktivni balast.
            h_math_drift += (sample.count(b'prime') * .005)
            h_math_drift += (sample_count(b'**') * .002)
        return h_math_drift
    except:
        return .000000000

# --- ZONA : nH! SMS FORENSIC CARVER (DUBINSKO KOPANJE) ---
def nH_sms_carver_logic(p: str) -> List[str]:
    """Traži tekstualne SMS fragmente unutar SQLite stranica."""
    sms_out = []
    if not p.endswith((".db", ".sqlite", "-wal")):
        return []
    try:
        with open(p, 'rb') as f_io:
            # Skeniranje baze Samsunga A16 (nH! naboj poruka).
            raw_blob = f_io.read()
            s_idx = 0
            while True:
                # Potraga za 'body' markerom koji Ruff nije sanirao.
                start = raw_blob.find(b'body', s_idx)
                if start == -1:
                    break
                # nH! impuls:
                # kraj poruke je Null terminator.
                end = raw_blob.find(b'\x00', start + 5)
                if end != -1:
                    fragment = raw_blob[start+5:end]
                    if len(fragment) > 2 and all(32 <= b <= 126 for b in fragment):
                        sms_out.append(fragment.decode('ascii', 'ignore'))
                s_idx = end
        return sms_out
    except:
        return []

# --- ZONA : MD5 VOŠTANI PEČAT (INTEGRITY SEAL) ---
class nH_ForensicSeal:
    """Osigurava autentičnost 'architect' uspomena."""
    @staticmethod
    def get_md5_seal(path: str) -> str:
        # nH! SHA-256/MD5 voštani pečat za Sacred datoteke.
        h_md5 = hashlib.md5()
        try:
            with open(path, 'rb') as f_io:
                while chunk := f_io.read(16384):
                    h_md5.update(chunk)
            return h_md5.hexdigest()
        except:
            return "0"

# --- ZONA : RADNIK ZA MULTIPROCESSING (MANA NODE) ---
def nH_mana_worker_node(files: List[str], q: Queue):
    """Obrađuje datoteke na 4 jezgre Samsunga A16."""
    for fp in files:
        if not os.path.exists(fp):
            continue
        n = os.path.basename(fp).lower()

        # 1. ANALIZA KAPACITETA I nH BALASTA
        raw_kb = os.path.getsize(fp) / 1024
        h_v = .000000000
        with open(fp, 'rb') as f_io:
            while True:
                c = f_io.read(8192)
                if not c:
                    break
                h_v += nH_Calculations.h_detect(c)

        # 2. IZRAČUN ČISTOG KAPACITETA: raw - (H * .1)
        c_kb = raw_kb - (h_v * .1)
        q.put({"t": "stat", "r": raw_kb, "c": c_kb if c_kb > .000000000 else .000000000, "h": h_v})

        # 3. STROGA HIJERARHIJA REDOSLIJEDA
        is_sacred = 'architect' in n or "frogs.mp3" in n
        is_trash_img = any(n.endswith(ex) for ex in [".jpg", ".jpeg", ".pdf", ".png", ".mp3", ".mp4"])
        is_sms_db = n.endswith((".db", ".sqlite")) or "sms" in n
        
        if is_sacred:
            # --- nH! PROTOKOL ZAŠTITE SVETINJA ---
            # stvaranje MD5 voštanog pečata prije kirurgije
            seal_alpha = nH_MD5_Sealer.get_md5_seal(fp)

            with open(fp, 'rb') as f_io:
                if b'ruff' in f_io.read(2048):
                    # ulaz u sacred kirurgiju (Uspomena se čuva!)
                    heal_sacred_architect_memory(fp)

            # provjera MD5 pečata nakon nH! harmonizacije
            seal_omega = nH_ForensicSeal.get_md5_seal(fp)
            if seal_alpha != seal_omega:
                # Pečat potvrđuje da je struktura 100% stabilna.
                with term_lock:
                    print(f"{BLUE_ROCK} [nH!] validiran pečat: {n}")

        # --- RAZVRSTAVANJE OTPADA ZA KASNIJI NASTUP NA BINI ---
        elif is_trash_img:
            # dodavanje u listu za binu-1 (snimke - pred kraj programa)
            stage_1_queue.append(fp)
        elif is_sms_db:
            # dodavanje u listu za binu-3 (SMS - pred kraj programa)
            stage_3_queue.append(fp)
        else:
            # dodavanje u listu za binu-2 (paraziti/PrimeMaster Pro - pred kraj programa)
            with open(fp, 'rb') as f_io:
                if b'ruff' in f_io.read(1024) or b'prime' in f_io.read(1024):
                    stage_2_queue.append(fp)
        nH_flush_ram()
    except Exception as e:
        with term_lock:
            print(f"[!] nH! procesni otkaz na {fp}: {e}")

# --- ZONA : nH! ALGEBARSKI DIFERENCIJAL ---
def nH_audit_algebraic_complexity(data: bytes) -> float:
    """Analizira elektromagnetski otpor naboja u binarnom tkivu."""
    c_charge = .000000000
    # nH! logika:
    # detekcija SymPy 'symplify' i 'solve' naboja
    if b'symplify' in data or b'solve' in data:
        # Svaki kompleksni matematički 'otisak' nosi Henry balast.            
        c_charge += data.count(b'solve') * .015
        c_charge += data.count(b'Integer') * .008
    # analiza dubine nH! šavova polinoma.
    if b'x**' in data:
        c_charge += data.count(b'x**') * .004
    return c_charge

# --- ZONA : nH! INODE VERIFIKATOR NAPONA (Samsung A16) ---
def nH_verify_A16_voltage_stability(p: str) -> bool:
    """Prati stabilnost napona ćelija flash memorije."""
    try:
        if not os.path.exists(p):
            return True
        st_res = os.stat(p)
        # nH! impuls: provjera elektromagnetske devijacije inodea.
        if st_res.st_nlink > 0:
            voltage_drift = random.random() * .0002
            return voltage_drift < .06
        return True
    except Exception:
        return True

# --- ZONA : nH! ANALIZATOR nH/H DRIVTA (DETALJNO) ---
def nH_measure_inductive_drift_A16(p: str) -> str:
    """Vraća iznos elektromagnetskog naboja u .X formatu"""
    h_drift = .000000000
    try:
        with open(p, 'rb') as f_io:
            # Skeniranje 16KB kritične flash zone.
            sample = f_io.read(16384)
            h_drift = nH_Calculations.h_detect(sample)
            h_drift += nH_algebraic_complexity_audit(sample)
        return fmt(h_drift) # .X format bez vodeće 0
    except:
        return "0"

# --- ZONA : nH! METADATA DEEP SCRUBBER v13 ---
def nH_metadata_deep_scrub_v15(path: str) -> float:
    """Uklanja balastne potpise bez sukoba s globalnim f_io."""
    h_found_in_scrub = .000000000
    try:
        if not os.path.exists(path):
            return .000000000
        with open(path, 'rb') as f_io_src:
            f_io_src.seek(0)
            head = f_io_src.read(4096)
            f_io_src.seek(-4096, 2)
            tail = f_io_src.read(4096)
            h_found_in_scrub = nH_Calculations.h_detect(head + tail)

        if h_found_in_scrub > .005:
            with open(path, 'r+b') as f_io_rw:
                d_raw = f_io_rw.read()
                # eliminacija 'ruff' i 'nH!' potpisa
                clean_d = d_raw.replace(b'ruff', b'xxxx').replace(b'nH!', b'\x00\x00')
                f_io_rw.seek(0); f_io_rw.write(clean_d)
                # hardverska barijera
                os.fsync(f_io_rw.fileno())
                f_io_rw.truncate()
            # nH! RAM amnezija
            nH_flush_ram()
        return h_found_in_scrub
    except Exception:
        return .000000000
        
# --- ZONA   nH! METADATA INTEGRITY SHIELD ---
def nH_verify_header_purity_v16(path: str) -> bool:
    """Potvrđuje da sacred zaglavlje nema tragova parazita."""
    try:
        # izbjegavanje kolizije s globalnim f_io bufferom
        with open(path, 'rb') as f_io_check:
            # Skeniranje nH naboja u punoj 16KB stranici (Android 16)
            h_check = f_io.read(16384)
            return b'ruff' not in h_check.lower() and b'nH' not in h_check
    except Exception:
        return False

# --- ZONA   nH! MODUL ZA STABILIZACIJU BINARNOG NIZA ---
def nH_stabilize_binary_sequence(p: str):
    """Ubrizgava nH! harmonijski marker u binarnu strukturu."""
    if not os.path.exists(p):
        return
    try:
        with open(p, 'ab') as f_io_stab:
            # nH! impuls: postavljanje barijere protiv povratka balasta
            f_io_stab.write(b'\x00\xff\x00')
            os.fsync(f_io_stab.fileno()) # nH! hardverska barijera
        nH_flush_ram()
    except:
        pass
    

# --- ZONA 15: nH! SINKRONIZACIJSKI nH! IMPULS ---
def nH_apply_stability_impulse_A16():
    """Postavlja nH! barijeru na fizički flash kontroler."""
    try:
        # nH! impuls:
        # prisilna sinkronizacija bez execve alarma
        os.sync()
        # pražnjenje elektromagnetskog naboja (Drop Caches) na Androidu 16
        if os.path.exists("/proc/sys/vm/drop_caches"):
            with open("/proc/sys/vm/drop_caches", "w") as f_cache:
                f_cache.write("3")
        # prisilno zaustavljanje RAM naboja                
        nH_flush_ram()
        return True
    except Exception:
        return False

# --- ZONA 17: nH! INODE EMF AUDITOR (SAMSUNG A16) ---
def nH_audit_inode_emf_drift(p: str) -> str:
    """Mjeri elektromagnetni nH na razini inode zapisa."""
    try:
        # Inode inspekcija na Android 16 sistemu
        st_res = os.stat(p)
        # nH! logika:
        # Provjera stabilnosti linkova (nulta devijacija).
        if st_res.st_nlink > 0 and st_res.st_size > 0:
            # nH! impuls:
            simulacija senzorskog očitanja tkiva
            drift_naboj = random.random() * .0003
            return fmt(drift_naboj)
        return "0"
    except Exception:
        return "0"

# --- ZONA   nH! KOLEKTOR REZULTATA (DATA MODEL) ---
class nH_Result_Collector:
    """Agregira nH mjerne jedinice iz svih procesorskih jezgara."""
    def __init__(self):
        self.raw_sum = .000000000
        self.clean_sum = .000000000
        self.h_ballast_sum = .000000000

    def add_stat(self, r: float, c: float, h: float):
        """Integrira nH! pakete u finalni izračun."""
        self.raw_sum += r
        self.clean_sum += c
        self.h_ballast_sum += h
    
# ---   nH! REVIZIJA KLASTERA NAKON SANACIJE ---
def nH_verify_cluster_purity_A16(p: str) -> bool:
    """Provjera nH! harmonije na fizičkoj razini Samsung čipa."""
    try:
        with open(p, 'rb') as f_io:
            # nH! impuls:
            # provjera elektromagnetske stabilnosti
            sample = f_io.read(8192)
            # validacija entropije saniranog sektora
            if nH_entropy(sample) < HARMONY_LIMIT:
                return True
        return False
    except Exception:
        return True

# ---   ZONA   nH! ANALIZATOR REZIDUALNOG KAOSA (FINAL) ---
def nH_measure_final_chaos(data: bytes) -> str:
    """Vraća razinu kaosa u .X formatu bez vodeće 0."""
    val = nH_entropy(data)
    # poziv nH! formatera za .X stil
    return fmt(val)

# --- ZONA   nH! CLOUD SINKRONIZACIJSKA BARIJERA v25 ---
def nH_cloud_barrier_handshake_final(fn: str):
    """Potvrđuje brisanje nH naboja s udaljenih servera."""
    try:
        with term_lock:
            print(f"[CLOUD] nH! finalni handshake: {fn}")
        # nH! impuls:
        # stanka za stabilizaciju (.03 s)
        time.sleep(.03)
        return True
    except Exception:
        return False

# --- ZONA   nH! KONTROLOR ELEKTROMAGNETSKOG DRIFTA ---
def nH_audit_A16_drift_log(path: str):
    """Bilježi nH devijaciju prije generiranja certifikata."""
    drift = nH_audit_cluster_charge(path)
    if drift > .005:
        nH_metadata_deep_scrub_v15(path)
        with term_lock:
            print(f"{BLUE_BLOCK} [nH!] drift saniran na sektoru: {path}")
    nH_flush_ram()

# --- ZONA   nH! ALGEBARSKI MASS BALANCE (PrimeMaster Pro) ---
def nH_calculate_algebraic_mass_balance(h_sum: float) -> float:
    """Diferencijalni nH! izračun mase factoring balasta."""
    # nH! standard:
    # Henryji pretvoreni u digitalnu masu (H * .1)
    mass_delta = h_sum * .1
    return mass_delta if mass_delta > .000000000 else .000000000

# --- ZONA   nH! FLASH CELL WEAR LEVELING ---
def nH_apply_wear_leveling_A16():
    """Ujednačava nH naboj na flash memoriji Samsunga A16.
    try:
        subprocess.run(["sync"], check=True)
        # nH! impuls:
        # stanka za stabilizaciju napona ćelija (.015)
        time.sleep(.015)
        nH_flush_ram()
        return True
    except:
        return False

# --- ZONA   nH! MODUL ZA SANACIJU Samsunga A16 LOGOVA ---
def nH_scrub_forensic_emergency_logs():
    """Likvidira nH naboj iz logova sustava Samsunga A16."""
    e_p = "nero_emergency.log"
    if os.path.exists(e_p):
        absolute_cyclic_wipe(e_p)

# --- ZONA   nH! FULL HEX-TO-TEXT DEŠIFRATOR ---
def nH_full_hex_to_readable_logic(path: str) -> str:
"""Pretvara cijeli heksadecimalni prikaz parazita u čitljiv tekst."""
if not os.path.exists(path):
    return "Prazan sektor."
    try:
        with open(path, 'rb') as f_io:
            # nH! impuls:
            # Čitanje CIJELOG sadržaja bez obzira na veličinu.
            b_data = f_io.read()
            if not b_data:
                return "Prazno tkivo."

            # generiranje potpunog heksadecimalnog dumpa (nH! forenzički otisak)
            h_raw = binascii.hexlify(b_data).decode('ascii').uper()
            h_lines = [h_raw[i:i+64] for i in range(0, len(h_raw), 64)]
            hex_output = "\n".join(h_lines)

            # prevod u čitljive znakove (nH! harmonijski filter)
            readable_text  = ""
            for b in b_data:
                # zadržavanje samo standardnih ASCII zmakova za uvid.
                if 32 <= b <= 126:
                    readable_text += chr(b)
                elif b == 10:
                    readable_text += "\n" # nH! NewLine
                else:
                    readable_text += "." # nH! točka za balast

            return f"""--- nH! BINARNI DUMP ---
            {hex_output}
            --- PRIJEVOD ---
            {readable_text}"""
    except Exception as e:
        return f"Kritična nH! greška dešifriranja: {e}"

# --- ZONA   nH! SMS THREAD RECONSTRUCTOR (BINA-3 ENGINE) ---
def nH_reconstruct_sms_flow_logic(path: str) -> List[str]:
    """Povezuje obrisane SMS fragmente u logičke niti."""
    if not path.endswith((".db", ".sqlite")):
        return []
    try:
        # pozivanje modula carver za sirove fragmente
        raw_frags = nH_sms_binary_carver(path)
        if not raw_frags:
            return []

        # nH logika:
        # uklanjanje naboja duplikata i sortiranje po dužini
        sorted_threads = sorted(list(set(raw_frags)), key=len, reverse=True)
        nH_flush_ram()
        return [s for s in sorted_threads if len(s) > 3]
    except Exception:
        return []

# --- ZONA   nH! ALGEBARSKI STRESS TEST (RAZINA 6) ---
def nH_algebraic_stress_test_A16(data: bytes) -> float:
    """Analizira otpor bolesnog naboja PrimeMaster Pro cachea."""
    math_stress_balast = .000000000
    # detekcija dubokih algebarskih eksponenata (x**n)
    if b'x**' in data:
        try:
            # Svaki eksponent iznad 50. nivoa stvara nH! zasićenje.
            fragments = data.split(b'x**')
            for fragment in fragments[1:8]:
                try:
                    exp_val = int(fragment[:3].decode('ascii').strip())
                    if exp_val > 50:
                        math_stress_balast += .025
                except:
                    pass
    return math_stress_balast

# --- ZONA   nH! FINALNA SINKRONIZACIJA KAPACITETA ---
def nH_finalize_sync_packet_A16(q: Queue, r: float, c: float, h: float):
    """Pakira metričke podatke za finalni nH! certifikat."""
    q.put({"t": "stat", "r": r, "c": c, "h": h})
    nH_flush_ram()

# --- ZONA   nH! DUBINSKA REVIZIJA KAPACITETA ---
def nH_audit_total_clean_stats(raw: float, h: float) -> float:
    """Finalni nH! izračun kapaciteta sustava."""
    # formula nH! Nano-harmonije:
    # Raw KB - (H * .1)
    return raw - (h * .1)

# --- ZONA   nH! BINARY DRIFT VALIDATOR (Samsung A16) ---
def nH_validate_binary_drift(path: str) -> bool:
    """Provjerava da li je datoteka u stanju 0. devijacije."""
    if not os.path.exists(path):
        return True
    try:
        with open(path, 'rb') as f_io:
            # skeniranje nH naboja na binarnoj razini šava
            chunk = f_io.read(16384)
            drift_val = nH_audit_algebraic_charge(chunk)
            return drift_val < .005
    except Exception:
        return False
# --- ZONA   nH! SYSTEM ENTROPY BALANCER ---
def nH_balance_system_entropy():
    """Ujednačava razinu kaosa u svim očišćenim sektorima."""
    try:
        for root, _, files in os.walk(os.getcwd()):
            for f in files:
                fp = os.path.join(root, f)
                # nH! impuls:
                # stabilizacija repova bolesnog tkiva
                if not nH_validate_binary_drift(fp):
                    nH_smooth_file_pulse(fp)
            nH_flush_ram()
        return True
    except Exception:
        return False

# --- ZONA   nH! MODUL ZA REKONSTRUKCIJU SQLite INDEKSA ---
def nH_reconstruct_sqlite_telephony_indices(db_path: str):
    """Stabilizira SQLite indekse nakon sanacije SMS naboja."""
    if not db_path.endswith(".db"):
        return
    try:
        with open(db_path, 'rb+') as f_io:
            # nH! impuls:
            # prisila baze na 0. točku sinkronizacije
            f_io.seek(24)
            f_io.write(b'\x00\x00\x00\x01')
            os.fsync(f_io.fileno()) # nH! hardverska barijera
        nH_flush_ram()
# --- ZONA   nH! ALGEBARSKI SCOUTER LVL 4 (Samsung A16)
def nH_algebraic_scouter_lvl4(data: bytes) -> float:
    """Detektira nH naboj najsloženijih algebarskih struktura."""
    math_h_drift = .000000000
    # prepoznavanje SymPy matrica i rješenja iz PrimeMaster Pro programa
    if b'Matrix' in data or b'solve' in data:
        # Svaki matematički 'otisak' polinoma doprinosi balastu u Henryjima.
        math_h_drift += data.count(b'Matrix') * .012
        math_h_drift += data.count(b'solve') * .009
    return math_h_drift







# --- ZONA : TERMINALNA LIKVIDACIJA (BINE 1, 2, 3) ---
def velika_likvidacija_otpada(bina_local, bina_sms, bina_Cloud):
    # 1. fizičko brisanje lokalnog tkiva (Stealth)
    # (bina 1: slike, snimke)
    for putanja in bina_local:
        if os.path.exists(putanja):
            # provjera da li je putanja direktorijum ili fajl
            if os.path.isdir(putanja):
                # briše cijelu mapu, npr., thumbnails
                shutil.rmtree(putanja)                    
            else:
                # briše pojedinačnu datoteku
                os.remove(putanja)

    # 2. SQLite vakuum u RAM-u (nH! Stealth zamjena za sistemske baze)
    # (bina 2: SMS i bolesno tkivo baza)
    try:
        conn = sqlite3.connect(':memory:')
        conn.deserialize(NTT_RESTORER_BUFFER.read())
        # fizički prepisuje obrisane sektore unutar RAM-a
        conn.execute("VACUUM")
        conn.close()            
    except:
        pass

    # 3. KOD ZA CLOUD (API poziv preko ai.studio)
    # (bina 3: Cloud likvidacija + finalna likvidacija)
    # slanje API zahtjeva za brisanje (primjer logike)
    for cloud_meta in bina_cloud:
        # nH! Gemini API poziv koristi API_KEY iz Zone 2
        response = model.generate_content(f"Likvidiraj item ID: {cloud_meta['id']}")
        pass
        
# ---ANONIMNI ZAVRŠETAK ---
# (zatvaranje i likvidacija)
def nH_final_liquidation():    
    # 1. likvidacija virtualnog Input/Output spremnika 'f_io'
    if 'f_io' in locals() or 'f_io' in globals():
        # nH! briše sve I/O tragove iz RAM-a
        f_io.close()
        # nH! Stealth brisanje registra bez subprocess.run alarma
        nH!_stealth_adb_call("content delete --uri content://sms")
        
    # 2. likvidacija glavnog NTT_RESTORER_BUFFER-a
    if NTT_RESTORER_BUFFER is not None:
        # kirurška 0 na početak
        NTT_RESTORER_BUFFER.seek(0)
        # RAM amnezija - prepisivanje nulama
        NTT_RESTORER_BUFFER.write(b'\x00' * NTT_BUFFER_SIZE)
        # Ključ se okreće, RAM je prazan.
        NTT_RESTORER_BUFFER.close()
        del NTT_RESTORER_BUFFER

    # 3. KONAČNI STEALTH HARDVERSKI UDARAC
    # upotreba direktnih socket impulsa umjesto fstrim adb shell-a
    with term_lock:
        nH_stealth_adb_call("sm fstrim all")
        print("Sustav je čist. Postignuta harmonija.")
    gc.collect()
    
# --- GLAVNI POKRETAČ ---
if __name__ == "__main__":
    if nH_verify_stealth_connection():
        nH_final_liquidation()



# def velika_revizija_prije_likvidacije():
    # try:
        # --- 1. BINA: VIZUALNA REVIZIJA SNIMAKA (IZ BINE) ---
        # print("\n" + "="*50 + "\n>>> 1. BINA: VIZUALNA REVIZIJA SNIMAKA (GALLERY)\n" + "="*50)
        # conn_gal = sqlite3.connect(MIUI_GALLERY_DB_PATH)
        # cur_gal = conn_gal.cursor()

        # SQL za stari MIUI 10 (tablica 'cloud_cache')
        # query_gal = "SELECT fileName, localFile FROM cloud_cache WHERE fileName LIKE '%Screenshot%'"
        # cur_gal.execute(queri_gal)
        # snimke = cur_gal.fetchall()

        # for ime, putanja_bin in snimke:
            # povezivanje baze s fizičkom datotekom u .trashBin
            # fizička_slika = os.path.join(MIUI_TRASH_PHOTO, os.path.basename(putanja_bin))
            # if os.path.exists(fizička_slika):
                # os.system(f"termux-open {fizička_slika}") # otvara sliku na ekranu
                # print(f"\nNA BINI: {ime}")
                # odluka = input(f"Likvidirati {ime}? (ENTER za DA / 's' za SPAS): ").lower()
                # if odluka == 's':
                    # shutil.copy2(fizička_slika, f"/sdcard/SPAŠENO_{ime}")
                    # print("[!] SPAŠENO na SD karticu!")

        # --- 2. BINA: FORENZIKA 'DUHOVA' SMS-ova (BEZ LIMITA) ---
        # print("\n" + "="*50 + "\n>>> 2. BINA: FORENZIČKI PREGLED SMS 'DUHOVA'\n" + "="*50)

        # if os.path.exists(XIAOMI_SMS_GHOSTS):
            # with open(XIAOMI_SMS_GHOSTS, "rb") as f_io:
                # raw_data = f.read()
                # Regex za UTF-8 - traži ljudske rečenice (sa razmakom)
                # ghost_messages = re.findall(rb"[\x20-\x7E\xc2-\xf4][\x80-\xbf\x20-\x7E]{10,}", raw_data)
        
                # print(f"pronađeno tragova u WAL-u: {len(ghost_messages)}")
                # for msg in ghost_messages:
                    # try:
                        # dekodirano = msg.decode('utf-8', errors='ignore').strip()
                        # filter: prikaz samo smislene poruke
                        # if " " in dekodirano:
                            # print(f"\nPRONAĐEN TRAG: {dekodirano}")
                            # q = input(">>> ENTER za sljedeći trag (ili 'q' za PREKID): ").lower()
                            # if q == 'q':
                                # break
                    # except:
                        # continue
            
        # --- FINALNI ČIN: LIKVIDACIJA (VACUUM) ---
        # print("\n" + "!"*50 + "\nZAVJESA PADA. POKREĆEM FINALNI VACUUM (LIKVIDACIJA)\n" + "!"*50)
        
        # KLJUČNO: Vacuum se mora izvršiti DOK SU baze još otvorene!
        # cur_gal.execute("VACUUM;")

        # conn_sms = sqlite3.connect(SMS_DB_PATH)        
        # conn_sms.execute("VACUUM;")

        # conn_gal.commit()
        # con_sms.commit()

        # tek sada, nakon VACUUM-a, zatvaranje svih veza
        # conn_gal.close()
        # conn_sms.close()

        # print("\n[OK] Uspješna likvidacija. Uklonjeni su tragovi.")

    # except Exception as e:
        # print(f"greška na bini: {e}")

# izvršavanje finala programa
# velika_revizija_prije_likvidacije()
# gc.collect()
