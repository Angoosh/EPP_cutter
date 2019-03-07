#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import pickle
import getpass

#otevreni souboru se jmenem a heslem
creds = open("creds.pickle", "rb")
user = pickle.load(creds)
passwd = pickle.load(creds)
creds.close()

#zadani uzivatelskeho jmena a jeho zasifrovani
i = input("Username: ")
u = base64.b64encode(i.encode('utf-8'))

#zadani hesla a porovnavani jmena a hesla s daty ze souboru a vytvoreni docasneho souboru s informacemi pro CLI/GUI
x = 0
for x in range (0,3):
    i = getpass.getpass()
    p = base64.b64encode(i.encode('utf-8'))
    if u == user and p == passwd:
        OK = "OK"
        f = open("sec.pickle", "wb")
        pickle.dump(OK, f)
        f.close()
        break
    else:
        print("No match")
