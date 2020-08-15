# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 19:03:49 2019

@author: kapla
"""

import random

PREDMET = ["AT", "EP"]
OTAZKA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

x = random.randint(0,19)
y = random.randint(0, 1)

print(str(PREDMET[y])+": "+str(OTAZKA[x]))

"""
EP:
    1: Historie IA32
    2: Adresace
    3: Přeruseni
    4: GPU
    5: Network SW
    6: Network HW
    7: MOBO
    8: Paměti
    9: HDD
    10: Zalohovaci media
    11: Monitory
    12: Tiskarny
    13: Vstupni periferie
    14: Vyrovnavaci pameti
    15: SSD
    16: OOP
    17: Algoritmizace
    18: Pole
    19: Soubory
    20: GUI
    
AT:
    1: Regulacni obvod + LT
    2: Kombinacni Log obv
    3: Sekvencni log obv
    4: Teplota, poloha, rychlost a zrychleni
    5: Tlak, tlakova diference, prutok
    6: Pojem PLC, rozdeleni PLC
    7: Cyklus PLC, prog jazyky
    8: LD, realizace log fci
    9: SS motory a komutatorove motory
    10: Asynch a synch motory
    11: Stat soust 0 a 1 radu
    12: Stat soust 2 a vyssich radu
    13: Astat soust, identifikace soust
    14: Nespojite reg
    15: Spojite reg PID
    16: stabilita a jakost RO
    17: Navrh reg, presnost reg
    18: ST, podminkove vetveni
    19: ST, cykly
    20: Rizeni spojite soust diskretnim reg
"""