#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 14:21:19 2019

@author: angoosh
"""

import pickle
import base64

#konzolovy vstup na uzivatelske jmeno a heslo
u = input("Username: ")
p = input("Password: ")
pr = input("Repeat password: ") #osetreni nespravne zadaneho hesla
for x in range (0,3):
    if p != pr:
        pr = input("Wrong, again: ")
    else:
        break

#zasifrovani jmena a hesla
u = base64.b64encode(u.encode('utf-8'))
p = base64.b64encode(p.encode('utf-8'))

#ulozeni jmena a hesla do souboru
creds = open("creds.pickle", "wb")
pickle.dump(u, creds)
pickle.dump(p, creds)
creds.close()
