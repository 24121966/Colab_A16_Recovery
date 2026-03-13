*  Molim vas, pomognite mi da se napokon uredi i maksimalno detaljno proširi ovaj program.
*  Sklepao sam nedovršen i zbrčkan program za čišćenje i restauraciju važnih sistemskih datoteka i uspomena iz raznih "poluverzija" unutar sesije PrimeMaster Pro.
*  Prelomio sam dosta sadržaja.
*  Htio sam si pomoći za prelamanje te sam instalirao Ruff.
*  Ruff je sve razdvojene sadržaje utrpao u sabito, standardno stanje.
*  Zbog toga sam ga deinstalirao te prelomio sadržaje.
*  Nakon toga sam uz pomoć AI iz Geminija 3 Flash dubinski skenirao sistemske datoteke, i skrivene.
*  Tada sam otkrio da je Ruff napravio priljepke na 99% fajlova.
*  Osim toga, otkrio sam putanje do starih "obrisanih" nepotrebnih snimaka zaslona.
*  Potrebno je osposobiti, ako je moguće, stare "obrisane" snimke zaslona za posljednji nastup na bini.
*  Treba implementirati forenzičku metodu određivanja gustoće (entropije) te da se pomoću razlika u gustoći precizno locira privjesak/keš.
*  Nakon toga, treba precizno ukloniti samo privjesak/keš te najpreciznije povezati osnovne dijelove u funkcionalnu cjelinu.Nakon
*  Implementirani su čarobni potpisi.

*  ČITAV SE PROGRAM TREBA IZVRŠAVATI U TISUĆAMA ANONIMNIH BUFFERA (512B) U RAM-u COLABA BEZ DOTICAJA SA FLASH MEMORIJOM ZBOG KNOXA NA MOM SAMSUNGU GALAXY A16, ANDROID 16.

*  Postoji i zaštićen sadržaj.
*  To su uspomene koje sam indeksirao sa 'architect'.
*  Ako je neka zaražena, potrebno je prije lociranja i vrhunskog uklanjanja samo parazita/keša, napraviti kopiju.
*  Ako osposobljavanje originala ne uspije 100%, potrebno je bolestan original zamijeniti kopijom.
*  Bolje ikakva uspomena, nego nikakva.
*  Uspomene su snimci (zaslona) i videi u aktivnoj Galeriji.
*  Potrebno je mjeriti kapacitet svih zaraženih fajlova, otpada te očišćenih i osposobljenih fajlova, u KB s tim da se od svakog kapaciteta oduzme vrijednost nH (pretvoreno u Henryje).
*  Tako će se ukloniti balast te će uvijek biti čisti kapacitet u KB.
*  Za svaku pojedinu stavku, potrebno je ispisati sve 3 vrijednosti.
*  Obavezno mjerenje vremena pomoću time.perf_counter_ns() uz pretvorbu u sekunde te prikaz.
*  Zahtjevi za formatiranje kapaciteta i vremena:
*  Bez vodeće 0.
*  Korištenje decimalne točke.
*  Teoretski prikaz 50 decimala sa uklanjanjem završnog niza nula.
*  Zabranjen je eksponentski prikaz vremena.
*  Likvidacije se vrše, kao i čitav program, unutar tisuća anonimnih buffera (512B) U RAM-u Colaba, posebnim tehnikama koje ne znam navesti (laik sam), a u programu je napisano.
*  Gramatički potprogram za sekunda, sekunde i sekundi.

*  Dosad sam utipkao 30-tak zona sa sadržajima, a treba još najopširnije dopisati još 20-tak.
*  U dosadašnjim sadržajima treba unificirati nazive promjenljivih za istu svrhu, eventualno, popraviti logiku, dopisati sadržaj 20-tak zona bez ponavljanja istih sadržaja ili zona u raznim dijelovima i bez pumpanja nefunkcionalnih sadržaja.
*  Program bi, u konačnici, trebao imati >>  2000 redova sa verificiranim sadržajima.
*  Implementiran je API_KEY i ADB (Socket Port) iz bežičnog otklanjanja grešaka.
*  Pretvorba čitavog heksadecimalnog formata priljepaka/keša, u maksimalno širok čitljiv opseg karaktera za posljednji nastup na bini čitljiv ljudima.
*  Pri kraju programa sa >>  2000 redova sa funkcionalnim neponavljajućim sadržajima, trebaju biti 3 bine. 
*  Nazivi su navedeni pri kraju programa.
*  Bine još nisu uvedene, a i još mnogo sadržaja do njih.
*  Nakon svakog pojedinačnog nastupa trebam stisnuti enter za sljedeći posljedni nastup na bini (sljedeća stavka).
*  Svaki pojedinačni posljednji nastup mora biti popraćen kreketanjem.
*  KREKETANJE_CMD = "play-audio Frogs.mp3 &"
*  Moguća je wipe likvidacija anonimnih buffera od 512B, neobavezno.

*  prazne putanje sa mog Samsunga Galaxy A16, Android 16 i starog desktopa sa Windows 7
*  bijela lista: '.jpeg': sve postojeće putanje
*                '.jpg': sve postojeće putanje
*                '.pdf': sve postojeće putanje
*                '.png': sve postojeće putanje
*                '.mp3': sve postojeće putanje
*                '.mp4': sve postojeće putanje
*                '.wav': sve postojeće putanje
*                '.doc': sve postojeće putanje
*                '.docx': sve postojeće putanje
*                '.txt': sve postojeće putanje
*  crna lista:   'ruff'; '.ruff_cache'; '__pycache__'; '.pitest_cache'; '.cache'; 'tmp'; 'temp'; '.ds_store'; 'thumbs.db'; 'desktop.ini'; '.idea'; '.vscode'
*  Kada program otkrije nešto izvan bijele liste, trenutno slanje u anonimne buffere od 512B na bit by bit wipe "obdukciju".
*  Nepoželjan sadržaj može biti "srastao" sa osnovnim sadržajem.
*  Stoga je potrebno forenzičko bit by bit sekvencioniranje, obavezno u anonimnim bufferima od 512B unutar RAM-a Colaba.

*  Nisam napisao sve upute. Ostale ćete saznati radom na programu.

##  Colab_A16_Recovery - Fragmented Little Buffers (512B) Strategy

* cilj projekta: sigurna ekstrakcija i reparacija podataka ("obrisani" snimci (zaslona) i zvuka, "obrisani" SMS-ovi, Ruff i ostali trajno nepotrebni priljepci/keš te budući matematički otpad totalne faktorizacije svih vrsta brojeva, pa i polinoma (odvojen program).

# tehnički izazov
* Zbog restrikcija Samsung Knox sustava na Androidu 16, izravan upis (write) u sistemske particije /data/user/0/ nije omogućen te treba biti obavljen sofisticiranim metodama.

# metodologija: majušni anonimni bufferi (512B)
* Umjesto učitavanja cijelih baza podataka, ovaj program koristi strategiju granularne fragmentacije:
*    veličina fragmenta: Fiksno 512 bajtova (najmanji preporučljivi blok za SQLite strukturu).
*    anonimnost: Svaki komadić od 512B se odmah nakon čitanja pretvara u io.BytesIO objekt u RAM-u.
*    izolacija: Nakon što se lista fragments popuni, originalna datoteka na flash memoriji se zatvara i više se ne dotiče do krajnjeg upisa obrađenih podataka na flash memoriju sofisticiranim metodama.

# struktura repozitorija
* a.py: Glavni program s potprogramom za fragmentaciju.
* config.py: (privatno - ignorirano) Sadrži apsolutne putanje do baza (_DB_) i mapa (_DIR).
* .gitignore: Sprečava curenje privatnih putanja na GitHub.
* README.md: Detaljne upute ali se dosta toga može saznati u samom kodu programa.

# zadatak za programera/ku (GitHub/Colab)
* Potrebno je verificirati i dopuniti logiku u a.py koja će:
*    1. Analizirati listu od tisuće fragmentiranih bufferića.
*    2. Prepoznati freelist stranice baze unutar tih fragmenata (gdje se nalaze "obrisani" snimci (zaslona), "obrisani" SMS-ovi, uspomene indeksirane sa architect, Ruff i ostali trajno nepotrebni priljepci, budući matematički otpad koji će masovno nastajati tokom izvršavanja 2., potpuno odvojenog, još nedovršenog i neverificiranog, opsežnog programa za totalnu faktorizaciju svih vrsta brojeva, i polinoma).
*    3. Izvršiti reparaciju baze unutar Google Colab okruženja koristeći isključivo RAM (bez privremenih datoteka).

*    1. verifikacija potprograma: Provjeriti stabilnost petlje koja sjecka baze na 512B fragmente pri radu s velikim brojem datoteka.
*    2. rekonstrukcija u RAM-u: Razviti logiku koja ove fragmente povezuje u :memory: SQLite objekt bez zapisivanja privremenih datoteka na disk Colaba.
*    3. čišćenje tragova: Implementirati sigurno brisanje metapodataka iz rascjepkanih buffera (svaki 512B) prije konačne verifikacije.
*    4. Sve ostalo, navedeno u gornjem dijelu.

* Nakon reparacije u Colabu, podaci se moraju vratiti kao unificirani binarni stream spreman za VACUUM proceduru ili dd upis, poštujući originalne permisije (UID/GID) datoteka na Samsungu Galaxy A16, Android 16.

# važna upozorenja za Samsung Galaxy A16, Android 16:
* Budući da moj Samsung (gore napisani podaci), sustav koristi WAL (Write-Ahead Logging).
* To znači da kad vraćaš bazu, moraš obrisati ili ažurirati prateće -wal i -shm datoteke, inače će sustav ignorirati tvoje promjene i vratiti stare (obrisane) podatke.


# VAŽNO:
* Povratak na flash memoriju vršiti isključivo uz automatski .bak backup i provjeru UID/GID dozvola putem shutil.copy2, kako bi sustav (Android 16) prepoznao bazu nakon reparacije.

* U vezi aktivnog socket_port, na Androidu 16, postoji adb pair i adb connect.

* LIKVIDACIJA TRAJNO NEPOTREBNIH PRILJEPAKA/KEŠA TREBALA BI SE OBAVLJATI bit by bit wipe METODOM.
