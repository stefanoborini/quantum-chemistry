
from theochempy._theochempy import Units
from theochempy._theochempy import Measure

class Element:
    def __init__(self,atomic_number,symbol, mass):
        self._atomic_number = atomic_number
        self._symbol = symbol
        self._mass = mass
    def symbol(self):
        return self._symbol
    def atomicNumber(self):
        return self._atomic_number
    def mass(self):
        return self._mass
__elements=[]

X = Element(0,'X', 0.0)
__elements.append(X);

H = Element(1,'H', Measure.Measure(1.0078246, Units.dalton) )
__elements.append(H)

He = Element(2,'He', Measure.Measure(4.002601, Units.dalton) )
__elements.append(He)

Li = Element(3,'Li', Measure.Measure(7.01600, Units.dalton) )
__elements.append(Li)

Be = Element(4,'Be', Measure.Measure(9.01218, Units.dalton) )
__elements.append(Be)

B = Element(5,'B', Measure.Measure(11.009307, Units.dalton) )
__elements.append(B)

C = Element(6,'C', Measure.Measure(12.0, Units.dalton) ) 
__elements.append(C)

N = Element(7,'N', Measure.Measure(14.0030738, Units.dalton))
__elements.append(N)

O = Element(8,'O', Measure.Measure(15.9949141, Units.dalton))
__elements.append(O)

F = Element(9,'F', Measure.Measure(18.9984022, Units.dalton))
__elements.append(F)

Ne = Element(10,'Ne', Measure.Measure(19.992441, Units.dalton))
__elements.append(Ne)

Na = Element(11,"Na", Measure.Measure(22.9898, Units.dalton))
__elements.append(Na)

Mg = Element(12,'Mg', Measure.Measure(23.98504, Units.dalton))
__elements.append(Mg)

Al = Element(13,'Al', Measure.Measure(26.98153, Units.dalton))
__elements.append(Al)

Si = Element(14,'Si', Measure.Measure(27.976929, Units.dalton))
__elements.append(Si)

P = Element(15,'P', Measure.Measure(30.973764, Units.dalton))
__elements.append(P)

S = Element(16,'S', Measure.Measure(31.9720727, Units.dalton))
__elements.append(S)

Cl=Element(17,'Cl', Measure.Measure(34.9688531, Units.dalton))
__elements.append(Cl)

Ar=Element(18,'Ar', Measure.Measure(39.962386, Units.dalton))
__elements.append(Ar)

K=Element(19,'K', Measure.Measure(38.96371, Units.dalton))
__elements.append(K)

Ca=Element(20,'Ca', Measure.Measure(39.96259, Units.dalton))
__elements.append(Ca)

Sc=Element(21,'Sc', Measure.Measure(44.95592, Units.dalton))
__elements.append(Sc)

Ti=Element(22,'Ti', Measure.Measure(48.0, Units.dalton ))
__elements.append(Ti)

V=Element(23,'V', Measure.Measure(50.9440, Units.dalton))
__elements.append(V)

Cr=Element(24,'Cr', Measure.Measure(51.9405, Units.dalton))
__elements.append(Cr)

Mn=Element(25,'Mn', Measure.Measure(54.9380, Units.dalton))
__elements.append(Mn)

Fe=Element(26,'Fe', Measure.Measure(55.9349, Units.dalton))
__elements.append(Fe)

Co=Element(27,'Co', Measure.Measure(58.9332, Units.dalton))
__elements.append(Co)

Ni=Element(28,'Ni', Measure.Measure(57.9353, Units.dalton))
__elements.append(Ni)

Cu=Element(29,'Cu', Measure.Measure(62.9296, Units.dalton))
__elements.append(Cu)

Zn=Element(30,'Zn', Measure.Measure(63.9291, Units.dalton))
__elements.append(Zn)

Ga=Element(31,'Ga', Measure.Measure(68.9257, Units.dalton))
__elements.append(Ga)

Ge=Element(32,'Ge', Measure.Measure(73.9219, Units.dalton))
__elements.append(Ge)

As=Element(33,'As', Measure.Measure(74.9216, Units.dalton))
__elements.append(As)

Se=Element(34,'Se', Measure.Measure(79.9165, Units.dalton))
__elements.append(Se)

Br=Element(35,'Br', Measure.Measure(78.91839, Units.dalton))
__elements.append(Br)

Kr=Element(36,'Kr', Measure.Measure(83.91151, Units.dalton))
__elements.append(Kr)

Rb=Element(37,'Rb', Measure.Measure(84.9117, Units.dalton))
__elements.append(Rb)

Sr=Element(38,'Sr', Measure.Measure(87.9056, Units.dalton))
__elements.append(Sr)

Y=Element(39,'Y', Measure.Measure( 88.9059, Units.dalton))
__elements.append(Y)

Zr=Element(40,'Zr', Measure.Measure(89.9043, Units.dalton))
__elements.append(Zr)

Nb = Element(41,'Nb',Measure.Measure(92.906, Units.dalton))
__elements.append(Nb)

Mo = Element(42,'Mo',Measure.Measure(97.9055, Units.dalton))
__elements.append(Mo)

Tc = Element(43,'Tc',Measure.Measure(98.0, Units.dalton))
__elements.append(Tc)

Ru = Element(44,'Ru',Measure.Measure(101.9037, Units.dalton))
__elements.append(Ru)

Rh = Element(45,'Rh',Measure.Measure(102.906, Units.dalton))
__elements.append(Rh)

#I = Element(53,'I',)
#__elements.append(I)

def allElements():
    return __elements

# Pd = Element(46,'Pd',1.500,1.280,1.630,6,0.00,0.41,0.52,106.42));
     #O  107.90389D0, 106.90509D0, 113.9036D0, 114.9041D0, 120.D0,
     #1  120.9038D0, 129.9067D0, 126.90466D0, 131.90416D0, 132.9051D0,
     #2  137.9050D0, 138.9061D0, 139.9053D0, 140.9074D0, 141.9075D0,
     #3  145.D0, 151.9195D0, 152.9209D0, 157.9241D0, 159.9250D0,
     #4  163.9288D0, 164.9303D0, 165.9304D0, 168.9344D0, 173.9390D0,
     #5  174.9409D0, 179.9468D0, 180.9480D0, 183.9510D0, 186.9560D0,
     #6  192.D0, 192.9633D0, 194.9648D0, 196.9666D0, 201.970625D0,
     #7  204.9745D0, 207.9766D0, 208.9804D0, 209.D0, 210.D0,
     #8  222.D0, 223.D0, 226.D0, 227.D0, 232.D0, 231.D0, 238.D0 /
     # DATA (AMASS(I),I = 93,103)
     #1/ 237.D0, 244.D0, 243.D0,
     #2  247.D0, 247.D0, 251.D0, 252.D0, 257.D0,
     #3  258.D0, 259.D0, 260.D0/
#__elements.append(Element(47,'Ag',1.590,1.340,1.720,6,0.88,0.88,1.00,107.868));
#__elements.append(Element(48,'Cd',1.690,1.480,1.580,6,1.00,0.85,0.56,112.412));
#__elements.append(Element(49,'In',1.630,1.440,1.930,3,0.65,0.46,0.45,114.818));
#__elements.append(Element(50,'Sn',1.460,1.385,2.170,4,0.40,0.50,0.50,118.711));
#__elements.append(Element(51,'Sb',1.460,1.400,2.200,3,0.62,0.39,0.71,121.760));
#__elements.append(Element(52,'Te',1.470,1.378,2.060,2,0.83,0.48,0.00,127.60));
#__elements.append(Element(54,'Xe',1.980,1.980,2.160,0,0.26,0.62,0.69,131.29));
#__elements.append(Element(55,'Cs',1.670,2.350,1.700,1,0.34,0.09,0.56,132.905));
#__elements.append(Element(56,'Ba',1.340,1.980,1.700,2,0.00,0.79,0.00,137.328));
#__elements.append(Element(57,'La',1.870,1.690,1.700,12,0.44,0.83,1.00,138.906));
#__elements.append(Element(58,'Ce',1.830,1.830,1.700,6,1.00,1.00,0.78,140.116));
#__elements.append(Element(59,'Pr',1.820,1.820,1.700,6,0.85,1.00,0.78,140.908));
#__elements.append(Element(60,'Nd',1.810,1.810,1.700,6,0.78,1.00,0.78,144.24));
#__elements.append(Element(61,'Pm',1.800,1.800,1.700,6,0.64,1.00,0.78,145.0));
#__elements.append(Element(62,'Sm',1.800,1.800,1.700,6,0.56,1.00,0.78,150.36));
#__elements.append(Element(63,'Eu',1.990,1.990,1.700,6,0.38,1.00,0.78,151.964));
#__elements.append(Element(64,'Gd',1.790,1.790,1.700,6,0.27,1.00,0.78,157.25));
#__elements.append(Element(65,'Tb',1.760,1.760,1.700,6,0.19,1.00,0.78,158.925));
#__elements.append(Element(66,'Dy',1.750,1.750,1.700,6,0.12,1.00,0.78,162.50));
#__elements.append(Element(67,'Ho',1.740,1.740,1.700,6,0.00,1.00,0.61,164.930));
#__elements.append(Element(68,'Er',1.730,1.730,1.700,6,0.00,0.90,0.46,167.26));
#__elements.append(Element(69,'Tm',1.720,1.720,1.700,6,0.00,0.83,0.32,168.934));
#__elements.append(Element(70,'Yb',1.940,1.940,1.700,6,0.00,0.75,0.22,173.04));
#__elements.append(Element(71,'Lu',1.720,1.720,1.700,6,0.00,0.67,0.14,174.967));
#__elements.append(Element(72,'Hf',1.570,1.440,1.700,6,0.30,0.76,1.00,178.49));
#__elements.append(Element(73,'Ta',1.430,1.340,1.700,6,0.30,0.65,1.00,180.948));
#__elements.append(Element(74,'W',1.370,1.300,1.700,6,0.13,0.58,0.84,183.84));
#__elements.append(Element(75,'Re',1.350,1.280,1.700,6,0.15,0.49,0.67,186.207));
#__elements.append(Element(76,'Os',1.370,1.260,1.700,6,0.15,0.40,0.59,190.23));
#__elements.append(Element(77,'Ir',1.320,1.270,1.700,6,0.09,0.33,0.53,192.217));
#__elements.append(Element(78,'Pt',1.500,1.300,1.720,6,0.96,0.93,0.82,195.078));
#__elements.append(Element(79,'Au',1.500,1.340,1.660,6,0.80,0.82,0.12,196.967));
#__elements.append(Element(80,'Hg',1.700,1.490,1.550,6,0.71,0.71,0.76,200.59));
#__elements.append(Element(81,'Tl',1.550,1.480,1.960,3,0.65,0.33,0.30,204.383));
#__elements.append(Element(82,'Pb',1.540,1.480,2.020,4,0.34,0.35,0.38,207.2));
#__elements.append(Element(83,'Bi',1.540,1.450,1.700,3,0.62,0.31,0.71,208.980));
#__elements.append(Element(84,'Po',1.680,1.460,1.700,2,0.67,0.36,0.00,209.0));
#__elements.append(Element(85,'At',1.700,1.450,1.700,1,0.46,0.31,0.27,210.0));
#__elements.append(Element(86,'Rn',2.400,2.400,1.700,0,0.26,0.51,0.59,222.0));
#__elements.append(Element(87,'Fr',2.000,2.000,1.700,1,0.26,0.00,0.40,223.0));
#__elements.append(Element(88,'Ra',1.900,1.900,1.700,2,0.00,0.49,0.00,226.0));
#__elements.append(Element(89,'Ac',1.880,1.880,1.700,6,0.44,0.67,0.98,227.0));
#__elements.append(Element(90,'Th',1.790,1.790,1.700,6,0.00,0.73,1.00,232.038));
#__elements.append(Element(91,'Pa',1.610,1.610,1.700,6,0.00,0.63,1.00,231.036));
#__elements.append(Element(92,'U',1.580,1.580,1.860,6,0.00,0.56,1.00,238.029));
#__elements.append(Element(93,'Np',1.550,1.550,1.700,6,0.00,0.50,1.00,237.0));
#__elements.append(Element(94,'Pu',1.530,1.530,1.700,6,0.00,0.42,1.00,244.0));
#__elements.append(Element(95,'Am',1.510,1.070,1.700,6,0.33,0.36,0.95,243.0));
#__elements.append(Element(96,'Cm',1.500,0.000,1.700,6,0.47,0.36,0.89,247.0));
#__elements.append(Element(97,'Bk',1.500,0.000,1.700,6,0.54,0.31,0.89,247.0));
#__elements.append(Element(98,'Cf',1.500,0.000,1.700,6,0.63,0.21,0.83,251.0));
#__elements.append(Element(99,'Es',1.500,0.000,1.700,6,0.70,0.12,0.83,252.0));
#__elements.append(Element(100,'Fm',1.500,0.000,1.700,6,0.70,0.12,0.73,257.0));
#__elements.append(Element(101,'Md',1.500,0.000,1.700,6,0.70,0.05,0.65,258.0));
#__elements.append(Element(102,'No',1.500,0.000,1.700,6,0.74,0.05,0.53,259.0));
#__elements.append(Element(103,'Lr',1.500,0.000,1.700,6,0.78,0.00,0.40,262.0));
#__elements.append(Element(104,'Rf',1.600,0.000,1.700,6,0.80,0.00,0.35,261.0));
#__elements.append(Element(105,'Db',1.600,0.000,1.700,6,0.82,0.00,0.31,262.0));
#__elements.append(Element(106,'Sg',1.600,0.000,1.700,6,0.85,0.00,0.27,263.0));
#__elements.append(Element(107,'Bh',1.600,0.000,1.700,6,0.88,0.00,0.22,264.0));
#__elements.append(Element(108,'Hs',1.600,0.000,1.700,6,0.90,0.00,0.18,265.0));
#__elements.append(Element(109,'Mt',1.600,0.000,1.700,6,0.92,0.00,0.15,268.0));
#__elements.append(Element(110,'Uun',1.600,0.000,1.700,6,0.95,0.00,0.11,269.0));
      
