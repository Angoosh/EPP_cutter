#instrukcni sada desky TMCM 6110 - pouzivane instrukce
import config

#prevod mm-kroky
motorsteps = config.glob()[3]
microstepping = config.glob()[4]
screwpitch = config.glob()[5]

stepsmm = int((motorsteps*microstepping)/screwpitch)

#instrukce rotace doprava
def ROR(motor, value):
    val0 = 0
    val1 = 0
    val2 = 0
    val3 = 0
    val = "%08x" % value
    val = val.split('x')[-1]
    val0 = int(val[6:8],16)
    val1 = int(val[4:6],16)
    val2 = int(val[2:4],16)
    val3 = int(val[0:2],16)
    return(1, 0, motor,val3, val2, val1, val0)

#instrukce rotace doleva
def ROL(motor, value):
    val0 = 0
    val1 = 0
    val2 = 0
    val3 = 0
    val = "%08x" % value
    val = val.split('x')[-1]
    val0 = int(val[6:8],16)
    val1 = int(val[4:6],16)
    val2 = int(val[2:4],16)
    val3 = int(val[0:2],16)
    return(2, 0, motor,val3, val2, val1, val0)

#instrukce zastaveni motoru
def MST(motor):
    return(3, 0, motor, 0, 0, 0, 0)

#instrukce prejeti na konkretni pozici
def MVP(typ, motor, value):
    value = int(value*stepsmm)
    if value < 0:
        value = (4294967295 + value)
    val0 = 0
    val1 = 0
    val2 = 0
    val3 = 0
    val = "%08x" % value
    val = val.split('x')[-1]
    val0 = int(val[6:8],16)
    val1 = int(val[4:6],16)
    val2 = int(val[2:4],16)
    val3 = int(val[0:2],16)
    if typ == "COORD":
        typ = 2
    elif typ == "REL":
        typ = 1
    else:
        typ = 0 #Absolute
    return(4, typ, motor, val3, val2, val1, val0)

#instrukce hledani referencni pozice
def RFS(typ, motor):
    if typ == "START":
        typ = 0
    elif typ == "STOP":
        typ = 1
    elif typ == "STATUS":
        typ = 2
    else:
        print("Not applicable")
    return(13, typ, motor, 0, 0, 0, 0)

#instrukce nastaveni parametru osy
def SAP(typ, motor, value):
    val0 = 0
    val1 = 0
    val2 = 0
    val3 = 0
    val = "%08x" % value
    val = val.split('x')[-1]
    val0 = int(val[6:8],16)
    val1 = int(val[4:6],16)
    val2 = int(val[2:4],16)
    val3 = int(val[0:2],16)
    return(5, typ, motor, val3, val2, val1, val0)

#instrukce ziskani parametru osy
def GAP(typ, motor):
    return(6, typ, motor, 0, 0, 0, 0)

#instrukce nastaveni IO
def SIO(out, value):
    if value == True:
        value = 1
    else:
        value = 0
    return(14, out, 2, 0, 0, 0, value)

#instrukce ziskani stavu IO
def GIO(port, bank):
    return(15, port, bank, 0, 0, 0, 0)


