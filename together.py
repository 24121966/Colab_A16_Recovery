# ----------------------------------------------
# together.py THE SHADOW CODE EDITION
# \U0001F422 "Festina Lente - Žuri polako kroz faktore" \U0001F422
# \U0001F422 "Let the code speak where the face is hiden" \U0001F422
# /data/data/com.termux/files/home/myenv/bin/python
# -*-coding-8-*-
# --------------------------------------------

import os
import sys
import time
import multiprocessing
import sympy
import gmpy2

# \xff\xd8\xff za .jpeg/.jpg - magični potpis
from multiprocessing import Process
from multiprocessing import Queue

TARGET_UUID="1768862631534"

MAGICI={
    ".jpg":b"\xff\xd8\xff",
    ".png":b"\x89PNG\r\n\x1a\n",
    ".mp4":b"\x00\x00\x00\x18ftyp",
    ".webp":b"RIFF",
    ".mp3":b"ID3",
    ".mp3_alt1":b"\xff\xfb",
    ".mp3_alt2":b"\xff\xf3",
    ".mp3_alt3":b"\xff\xf2",
    ".aac_ultra":b"\xff\xf1" # (ADTS)
}

def skener_za_izmucenu_loptu(q_signal):
    putanje=[
        f"/sdcard/Android/.Trash/com.sec.android/gallery3d/uuid/{TARGET_UUID}",
        f"/sdcard/DCIM/.thumbnails/.thumb_{TARGET_UUID}"
    ]
    counter=0
    for p in putanje:
        if os.path.exists(p):
            try:
                with open(p,"rb") as f:
                    data=f.read()
                    for ext,potpis in MAGICI.items():
                        if data.startswith(potpis):
                            counter+=1
                            q_signal.put(f"{ext}_{counter}",data)
            except Exception:
                continue
    q_signal.put(("KRAJ",None))

def glavni_kontrolor():
    razmjena=Queue()
    p=Process(target=skener_za_izmucenu_loptu,
        args=(razmjena,))
    p.start()
    print("Šime: Štiperica je pokrenuta. Čekam bajtove...")
    while True:
        try:
            res,data=razmjena.get(timeout=None)
            if res=="KRAJ":
                break
            putanja=f"/sdcard/Download/USKRSLA/{res}.jpg"
            with open(putanja,"wb") as f:
                f.write(data)
            print("Šime: Izvukao sam {res} iz brloga!")
        except KeyboardInterrupt:
            break
        except Exception:
            break
    p.join()
    print("Šime: Brlog je potpuno ispražnjen. Završena likvidacija.")
if __name__ == "__main__":
    glavni_kontrolor()
