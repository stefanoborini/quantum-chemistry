import Elements

Dummy = Elements.X
X = Dummy

Hydrogen = Elements.H
H = Hydrogen

Helium = Elements.He
He = Helium

Lithium = Elements.Li
Li = Lithium

Berillium = Elements.Be
Be = Berillium

Boron = Elements.B
B = Boron

Carbon = Elements.C
C = Carbon

Nitrogen = Elements.N
N = Nitrogen

Oxygen = Elements.O
O = Oxygen

Fluorine = Elements.F
F = Fluorine

def getElementBySymbol(symbol):
	for e in Elements.allElements():
		if e.symbol() == symbol:
			return e
	return None

def getElementByAtomicNumber(atnum):
	for e in Elements.allElements():
		if e.atomicNumber() == atnum:
			return e
	return None
