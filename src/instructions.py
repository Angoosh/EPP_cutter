

def ROR():
	return(1)
def ROL():
	return(2)
def MST():
	return(3)
def MVP(type, motor, value):
	val0 = 0
	val1 = 0
	val2 = 0
	val3 = 0
	val = hex(value)
	if len(val) < 3:
		val0 = value
	elif len(val) < 5:
		val = val.split('x')[-1]
		val0 = int(val[2:4],16)
		val1 = int(val[0:2],16)
	elif len(val) < 7:
		val = val.split('x')[-1]
		val0 = int(val[4:6],16)
		val1 = int(val[2:4],16)
		val2 = int(val[0:2],16)
	elif len(val) < 9:
		val = val.split('x')[-1]
		val0 = int(val[6:8],16)
		val1 = int(val[4:6],16)
		val2 = int(val[2:4],16)
		val3 = int(val[0:2],16)
	if type == "COORD":
		type = 2
	elif type == "REL":
		type = 1
	else:
		type = 0
	return(4, type, motor, val3, val2, val1, val0)

