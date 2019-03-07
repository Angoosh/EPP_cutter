import math

#vypocet checksum
def parameter(b1, b2, b3, b4, b5, b6, b7, b8):
    CHECKSUM = b1+b2+b3+b4+b5+b6+b7+b8
    b9 = CHECKSUM
    if b9 > 255:
        i = b9/256
        i = math.floor(i)
        b9 = int(b9-i*256)

    return(b1, b2, b3, b4, b5, b6, b7, b8, b9)
