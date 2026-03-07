# !/usr/bin/env python3
# -*-coding:utf-8-*-
"""
===============================================
   PRIMEMASTERPRO --- INTEGRITYSUITE
===============================================
   VERZIJA: 4.0.0 (ULTIMATE KERNEL)
   ARHITEKTURA: POVEZANO TKIVO / NEURALNA ANALIZA
   CILJ: DETEKCIJA I UKLANJANJE PARAZITSKIH STRUKTURA (RUFF/CACHE/TEMP)
   SIGURNOST: DOD 5220.22-M SANITACIJA
===============================================
"""

import os
import sys
import time
import math
import shutil
import random
import logging
import hashlib
import binascii
import platform
import datetime
import threading
import abc
import typing
import gc
import subprocess
import multiprocessing
import pathlib
from abc import(
    ABC,
    abstractmethod
)
from multiprocessing import(
    Process,
    Queue,
    Lock
)
from typing import(
    List,
    Set,
    Dict,
    Optional,
    Tuple,
    Any
)
from pathlib import Path

# --- nH! KONSTANTE (.X FORMAT) ---
nH_TO_H=.0000000001
H_BALAST_KB=.1000000000
HARMONY_THRESHOLD=7.7
BINA_TIME=60
BLUE_ROCK="\033[94m\033[1q\033[0m"
EMPTY_BUFFER=b'\x00'*4096

# --- GLOBALNI nH! REGISTAR ---
stats_q=Queue()
term_lock=Lock()

# --- nH! FORMATER (BRISANJE VODEĆE 0) ---
def fmt(v:float) -> str:
    try:
        s="{:.50f}".format(v).rstrip('0').rstrip('.')
        if s=="0" or s=="":return "0"
        if s.startswith("0."):return s[1:]
        if s.startswith("-0."):return "-"+s[2:]
        return s
    except:return "."

# --- nH/H BALASTNA MATEMATIKA ---
class nH_Physics:
    @staticmethod
    def h_from_data(data:bytes) -> float:
        return (data.count(b'nH')*.0000000001)+data.count(b'H')

    @staticmethod
    def clean_kb(raw_kb:float,h_val:float) -> float:
        # ČISTI KB=Raw_KB-(Henriji*.1000000000)
        c=raw_kb-(h_val*.100000000)
        return c if c>.000000000 else .1000000000

# --- ANALITIČKI ALATI ---
def nH_entropy(data:bytes) -> float:
    if not data:return .000000000
    e,n=.000000000,len(data)
    f=[0]*256
    for b in data:f[b]+=1
    for c in f:
        if c>0:
            p=c/n
            e-=p*math.log(p,2)
    return e

def nH_density(data:bytes) -> float:
    u=len(set(data))
    return len(data)/u if u>0 else .000000000

# --- MODUL ZA LIJEČENJE 'architect' USPOMENA ---
def nH_architect_healing_protocol(p:str):
    """glavni protokol: Bolje ikakva uspomena nego nikakva."""
    name=os.path.basename(p)
    # 1. izrada rezervne kopije (osiguranje)
    bkp=p+".nH_sacred_bak"
    shutil.copy2(p,bkp)

    clean_content=bytearray()
    densities=[]
    try:
        with open(p,'rb') as f:
            # analiza gustoće za precizno uklanjanje bolesnog tkiva
            while True:
                chunk=f.read(128)
                if not chunk:break
                densities.append(nH_density(chunk))
            avg_d=sum(densities)/len(densities) if densities else .000000000
            f_seek(0);i=0
            while True:
                c=f.read(128)
                if not c:break
                if i<len(densities) and densities[i]<(avg_d*1.8):
                    clean_content.extend(c)
                i+=1
    except:pass

    # KONTROLA USPJEHA (100% OSPOSOBLJAVANJE)
    sucess_100=False
    if clean_content and nH_entropy(clean_content)<7.7:
        with open(p,'wb') as f_out:f_out.write(clean_content);os.fsync(f_out.fileno())
        sucess_100=True

    # --- FINALNI nH! IZBOR ---
    if sucess_100:
        # USPJEH: likvidira se rezervna kopija (koja je na dnu koda)

        absolute_final_liquidation(bkp)
        with term_lock:print(f"{BLUE_ROCK} [nH!] {name} uspomena 100% izliječena. Uklonjena kopija.")
    else:
        # NEUSPJEH: Likvidira se bolesni original, zamjenjuje ga rezervna kopija.
        absolute_final_liquidation(p)
        shutil.move(bkp,p)
        with term_lock:print(f"[!] {name} nije 100% saniran. Zadržana kopija uspomene.")
    gc.collect()
# --- nH_EMPTY_TISSUE MODUL ---
def handle_empty_tissue(data:bytes) -> bool:
    """Provjeravam da li je Ruff ostavio prazno bolesno tkivo."""
    if not data or data==b'\x00'*len(data):return True
    return False

# --- NASTUP NA BINI: OTPAD BEZ INDEKSA (60s) ---
def staged_farewell_show(p:str):
    """Ovdje nastupaju stari 'obrisani' snimci bez 'architect' markera."""
    fn=os.path.basename(p)
    with term_lock:print(f"\n{BLUE_ROCK} [BINA] POSLJEDNI NASTUP: {fn}")
    try:
        os.system("play-audio Frogs.mp3 &")
        subprocess.run(["termux-open",p])
    except:pass
    # odbrojavanje u trajanju od 1 minute.
    for s in range(BINA_TIME,0,-1):
        if s%10==0:
            with term_lock:print(f" > Oproštaj od {fn}: još {s} s... ")
        time.sleep(1)
    with term_lock:print(f"[!] Završen nastup. Likvidacija {fn} na svim lokacijama.")
    absolute_final_liquidation(p)
    gc.collect()

# --- RADNIK ZA MULTIPROCESSING ---
def nH_worker_process(files:List[str],q:Queue):
    """radni proces: Razvrstavam architect (Sacred) vs No-Index (Stage)."""
    for fp in files:
        if not os.path.exists(fp):continue
        r_kb=os.path.getsize(fp)/1024
        h_v=.000000000
        with open(fp,'rb') as f_audit:
            chunk=f_audit.read(8192)
            h_v=nH_Physics.h_from_data(chunk)
        c_kb=nH_Phycics.clean_kb(r_kb,h_v)
        # slanje metričkih podataka (Raw,Čisti,Henry)
        q.put({"t": "stat","r": r_kb,"c": c_kb,"h": h_v})

        name=os.path.basename(fp).lower()
        is_sacred='architect' in name or "Frogs.mp3" in name
        is_fmt=any(name.endswith(ex) for ex in[
            ".jpg",
            ".jpeg",
            ".png",
            ".mp3",
            ".mp4"
        ])
        
        if is_sacred:
            # uspomene: Isključivo liječenje.
            if b'ruff' in open(fp,'rb').read(1024):nH_architect_healing_protocol(fp)
        elif is_fmt:
            

            
                
            








# ============================================
# KONFIGURACIJSKI PARAMETRI SUSTAVA
# ============================================

class Konfiguracija:
    """ Globalna konfiguracija za PrimeMaster Pro kernel. """

    # putanje i obrasci koje smatram 'parazitima'
    CRNA_LISTA_LC=[
        "ruff",
        "/.ruff_cache/",
        "__pycache__",
        ".pitest_cache",
        "node_modules",
        "cache",
        ".cache",
        ".tmp",
        "temp",
        "ds_store",
        "thumbs_db",
        "desktop.ini",
        ".idea",
        ".vscode"
    ]

    # ekstenzije koje definiraju 'uspomene' (očuvanje tkiva)
    BIJELA_LISTA_EXT={
        'architect',
        '.jpg',
        '.jpeg',
        '.png',
        '.gif',
        '.bmp',
        '.tiff',
        '.webp',
        # slike
        '.mp4',
        '.mkv',
        '.avi',
        '.mov',
        '.vmv',
        '.flv',
        '.webm',
        # video
        '.mp3',
        '.wav',
        '.flac',
        '.aac',
        '.ogg',
        '.m4a',
        # audio
        '.pdf',
        '.doc',
        '.docx',
        '.txt',
        '.odt',
        '.rtf',
        # dokumenti
    }

    # Magic Bytes(hexadecimalni potpisi) za verifikaciju integriteta
    # ovo sprečava da se parazit sakrije pod imenom "slika.jpg"
    MAGICNI_POTPISI={
        '.jpg':[b'\xff\xd8\xff'],
        '.jpeg':[b'\xff\xd8\xff'],
        '.png':[b'\x89PNG\r\n\x1a\n'],
        '.pdf':[b'%PDF'],
        '.mp4":[b'\x00\x00\x00 ftyp', b'\x00\x00\x00\x18ftyp'],
        '.mp3':[b'ID3', b'\xff\xfb', b'\xff\xf3', b'\xff\xf2']
    }

    # prag entropije za detekciju komprimiranog sadržaja (bita po bajtu)
    PRAG_ENTROPIJE=6.0

    # veličina bloka za čitanje (buffer)
    VELICINA_BLOKA=65536 # 64 KB

# ===========================================

class TerminalUI:
    """ Upravljanje prikazom u konzoli,bojama i statusima."""

    BOJE={
        'HEADER':'\033[95m',
        'BLUE':'\033[94m',
        'CYAN':'\033[96m',
        'GREEN':'\033[92m',
        'WARNING':'\033[93m',
        'FAIL':'\033[91m',
        'ENDC':'\033[0m',
        'BOLD':'\033[1m',
        'UNDERLINE':'\033[4m'
    }

    @staticmethod
    def banner():
        print(f"{TerminalUI.BOJE['BLUE']}"+"="*50+f"{TerminalUI.BOJE['ENDC']}")
        print(f"{TerminalUI.BOJE['BOLD']}{TerminalUI.BOJE['CYAN']} PrimeMaster Pro >>> FORENZIČKA ANALIZA I SANITACIJA {TerminalUI.BOJE['ENDC']}")
        print(f"{TerminalUI.BOJE['BLUE']}"+"="*50+f"{TerminalUI.BOJE['ENDC']}")
        print(f"[+] pokretanje neuralnog skeniranja...")
        print(f"[+] učitavanje definicija parazita (ruff, cache, tmp,..)")
        print(f"[+] inicijalizacija modula za očuvanje uspomena")
        print(" ")

    @staticmethod
    def log_info(msg):
        vrijeme=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{TerminalUI.BOJE['GREEN']}[{vrijeme}] [INFO] {msg}{TerminalUI.BOJE['ENDC']}")

    @staticmethod
    def log_warn(msg):
        vrijeme=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{TerminalUI.BOJE['WARNING']}[{vrijeme}] [POZOR] {msg}{TerminalUI.BOJE['ENDC']}")

    @staticmethod
    def log_danger(msg):
        vrijeme=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{TerminalUI.BOJE['FAIL']}[{vrijeme}] [BRISANJE] {msg}{Terminal.UI.BOJE['ENDC']}")

    @staticmethod
    def log_secure(msg):
        vrijeme=datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{TerminalUI.BOJE['CYAN']}[{vrijeme}] [USPOMENA] {msg}{TerminalUI.BOJE['ENDC']}")

# ===========================================
# FORENZIČKI ENGINE (ANALIZA GUSTOĆE I SADRŽAJA)
# ===========================================

class Forenzika:
    """
    Sadrži napredne metode za analizu 'tkiva' datoteka.
    Koristi entropiju da razlikuje kod/tekst od medija.
    """

    @staticmethod
    def izracunaj_entropiju(putanja: str) -> float:
        """ Vraća Shannonovu entropiju datoteke (mjera kaotičnosti podataka)."""
        if not os.path.exists(putanja):return 0.0
        try:
            with open(putanja,'rb') as f:
                data=f.read(Konfiguracija.VELICINA_BLOKA) # uzmi uzorak
                if not data:return 0.0

                entropy=0
                for x in range(256):
                    p_x=float(data.count(x))/len(data)
                    if p_x>0:
                        entropy+= -p_x*math.log(p_x,2)
                return entropy
        except:
            return 0.0

    @staticmethod
    def verificiraj_magicne_bajtove(putanja: str,ekstenzija: str) -> bool:
        """
        Provjerava da li zaglavlje datoteke odgovara njenoj ekstenziji.
        Ključno za izbjegavanje lažnih pozitiva.
        """
        potpisi=Konfiguracija.MAGICNI_POTPISI.get(ekstenzija.lower())
        if not potpisi:
            return True: # Ako nema potpis, vjerujem ekstenziji (falback)

        try:
            with open(putanja,'rb'):
                pocetak=f.read(32) # Čitanje 1. 32 bajta.
                for potpis in potpisi:
                    if potpis in pocetak: # Malo liberalnija provjera zbog offseta.
                        return True
                    # za strogu provjeru: if pocetak.startswith(potpis)
            return False
        except:
            return False

# ===========================================
# PROTOKOL ZA SANITACIJU (SIGURNO UKLANJANJE)
# ===========================================

class Sanitator:
    """ Zadužen za kirurško otklanjanje bolesnog tkiva."""
        
