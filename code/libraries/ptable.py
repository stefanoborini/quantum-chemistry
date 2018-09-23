class Element:
	def __init__(self,atnum,symbol,rcov,rbo,rvdw,maxbnd,red,green,blue,mass):
		self.atomicNumber = atnum
		self.symbol = symbol
		self.covalentRadius = rcov
		self.bohrRadius = rbo
		self.vanDerWaalsRadius = rvdw
		self.maxBondOrder = maxbnd
		self.color = (red,green,blue)
		self.atomicMass = mass
		

class PTable:
	"""
	Periodic table data. Ok ok... no isotopes at all... who cares for now?
	"""
	def __init__(self):
		
		self.__elements=[]
		self.__elements.append(Element(0,'X',0.000,0.000,0.000,0,0.07,0.50,0.70,0.000));
		self.__elements.append(Element(1,'H',0.230,0.330,1.200,1,1.00,1.00,1.00,1.008));
		self.__elements.append(Element(2,'He',0.930,0.700,1.400,0,0.85,1.00,1.00,4.003));
		self.__elements.append(Element(3,'Li',0.680,1.230,1.820,1,0.80,0.50,1.00,6.941));
		self.__elements.append(Element(4,'Be',0.350,0.900,1.700,2,0.76,1.00,0.00,9.012));
		self.__elements.append(Element(5,'B',0.830,0.820,2.080,3,1.00,0.71,0.71,10.812));
		self.__elements.append(Element(6,'C',0.680,0.770,1.950,4,0.50,0.50,0.50,12.011));
		self.__elements.append(Element(7,'N',0.680,0.700,1.850,4,0.05,0.05,1.00,14.007));
		self.__elements.append(Element(8,'O',0.680,0.660,1.700,2,1.00,0.05,0.05,15.999));
		self.__elements.append(Element(9,'F',0.640,0.611,1.730,1,0.70,1.00,1.00,18.998));
		self.__elements.append(Element(10,'Ne',1.120,0.700,1.540,0,0.70,0.89,0.96,20.180));
		self.__elements.append(Element(11,'Na',0.970,1.540,2.270,1,0.67,0.36,0.95,22.990));
		self.__elements.append(Element(12,'Mg',1.100,1.360,1.730,2,0.54,1.00,0.00,24.305));
		self.__elements.append(Element(13,'Al',1.350,1.180,2.050,6,0.75,0.65,0.65,26.982));
		self.__elements.append(Element(14,'Si',1.200,0.937,2.100,6,0.50,0.60,0.60,28.086));
		self.__elements.append(Element(15,'P',0.750,0.890,2.080,5,1.00,0.50,0.00,30.974));
		self.__elements.append(Element(16,'S',1.020,1.040,2.000,6,1.00,1.00,0.19,32.067));
		self.__elements.append(Element(17,'Cl',0.990,0.997,1.970,1,0.12,0.94,0.12,35.453));
		self.__elements.append(Element(18,'Ar',1.570,1.740,1.880,0,0.50,0.82,0.89,39.948));
		self.__elements.append(Element(19,'K',1.330,2.030,2.750,1,0.56,0.25,0.83,39.098));
		self.__elements.append(Element(20,'Ca',0.990,1.740,1.973,2,0.24,1.00,0.00,40.078));
		self.__elements.append(Element(21,'Sc',1.440,1.440,1.700,6,0.90,0.90,0.90,44.956));
		self.__elements.append(Element(22,'Ti',1.470,1.320,1.700,6,0.75,0.76,0.78,47.867));
		self.__elements.append(Element(23,'V',1.330,1.220,1.700,6,0.65,0.65,0.67,50.942));
		self.__elements.append(Element(24,'Cr',1.350,1.180,1.700,6,0.54,0.60,0.78,51.996));
		self.__elements.append(Element(25,'Mn',1.350,1.170,1.700,8,0.61,0.48,0.78,54.938));
		self.__elements.append(Element(26,'Fe',1.340,1.170,1.700,6,0.50,0.48,0.78,55.845));
		self.__elements.append(Element(27,'Co',1.330,1.160,1.700,6,0.44,0.48,0.78,58.933));
		self.__elements.append(Element(28,'Ni',1.500,1.150,1.630,6,0.36,0.48,0.76,58.693));
		self.__elements.append(Element(29,'Cu',1.520,1.170,1.400,6,1.00,0.48,0.38,63.546));
		self.__elements.append(Element(30,'Zn',1.450,1.250,1.390,6,0.49,0.50,0.69,65.39));
		self.__elements.append(Element(31,'Ga',1.220,1.260,1.870,3,0.76,0.56,0.56,69.723));
		self.__elements.append(Element(32,'Ge',1.170,1.188,1.700,4,0.40,0.56,0.56,72.61));
		self.__elements.append(Element(33,'As',1.210,1.200,1.850,3,0.74,0.50,0.89,74.922));
		self.__elements.append(Element(34,'Se',1.220,1.170,1.900,2,1.00,0.63,0.00,78.96));
		self.__elements.append(Element(35,'Br',1.210,1.167,2.100,1,0.65,0.16,0.16,79.904));
		self.__elements.append(Element(36,'Kr',1.910,1.910,2.020,0,0.36,0.72,0.82,83.80));
		self.__elements.append(Element(37,'Rb',1.470,2.160,1.700,1,0.44,0.18,0.69,85.468));
		self.__elements.append(Element(38,'Sr',1.120,1.910,1.700,2,0.00,1.00,0.00,87.62));
		self.__elements.append(Element(39,'Y',1.780,1.620,1.700,6,0.58,1.00,1.00,88.906));
		self.__elements.append(Element(40,'Zr',1.560,1.450,1.700,6,0.58,0.88,0.88,91.224));
		self.__elements.append(Element(41,'Nb',1.480,1.340,1.700,6,0.45,0.76,0.79,92.906));
		self.__elements.append(Element(42,'Mo',1.470,1.300,1.700,6,0.33,0.71,0.71,95.94));
		self.__elements.append(Element(43,'Tc',1.350,1.270,1.700,6,0.23,0.62,0.62,98.0));
		self.__elements.append(Element(44,'Ru',1.400,1.250,1.700,6,0.14,0.56,0.56,101.07));
		self.__elements.append(Element(45,'Rh',1.450,1.250,1.700,6,0.04,0.49,0.55,102.906));
		self.__elements.append(Element(46,'Pd',1.500,1.280,1.630,6,0.00,0.41,0.52,106.42));
		self.__elements.append(Element(47,'Ag',1.590,1.340,1.720,6,0.88,0.88,1.00,107.868));
		self.__elements.append(Element(48,'Cd',1.690,1.480,1.580,6,1.00,0.85,0.56,112.412));
		self.__elements.append(Element(49,'In',1.630,1.440,1.930,3,0.65,0.46,0.45,114.818));
		self.__elements.append(Element(50,'Sn',1.460,1.385,2.170,4,0.40,0.50,0.50,118.711));
		self.__elements.append(Element(51,'Sb',1.460,1.400,2.200,3,0.62,0.39,0.71,121.760));
		self.__elements.append(Element(52,'Te',1.470,1.378,2.060,2,0.83,0.48,0.00,127.60));
		self.__elements.append(Element(53,'I',1.400,1.387,2.150,1,0.58,0.00,0.58,126.904));
		self.__elements.append(Element(54,'Xe',1.980,1.980,2.160,0,0.26,0.62,0.69,131.29));
		self.__elements.append(Element(55,'Cs',1.670,2.350,1.700,1,0.34,0.09,0.56,132.905));
		self.__elements.append(Element(56,'Ba',1.340,1.980,1.700,2,0.00,0.79,0.00,137.328));
		self.__elements.append(Element(57,'La',1.870,1.690,1.700,12,0.44,0.83,1.00,138.906));
		self.__elements.append(Element(58,'Ce',1.830,1.830,1.700,6,1.00,1.00,0.78,140.116));
		self.__elements.append(Element(59,'Pr',1.820,1.820,1.700,6,0.85,1.00,0.78,140.908));
		self.__elements.append(Element(60,'Nd',1.810,1.810,1.700,6,0.78,1.00,0.78,144.24));
		self.__elements.append(Element(61,'Pm',1.800,1.800,1.700,6,0.64,1.00,0.78,145.0));
		self.__elements.append(Element(62,'Sm',1.800,1.800,1.700,6,0.56,1.00,0.78,150.36));
		self.__elements.append(Element(63,'Eu',1.990,1.990,1.700,6,0.38,1.00,0.78,151.964));
		self.__elements.append(Element(64,'Gd',1.790,1.790,1.700,6,0.27,1.00,0.78,157.25));
		self.__elements.append(Element(65,'Tb',1.760,1.760,1.700,6,0.19,1.00,0.78,158.925));
		self.__elements.append(Element(66,'Dy',1.750,1.750,1.700,6,0.12,1.00,0.78,162.50));
		self.__elements.append(Element(67,'Ho',1.740,1.740,1.700,6,0.00,1.00,0.61,164.930));
		self.__elements.append(Element(68,'Er',1.730,1.730,1.700,6,0.00,0.90,0.46,167.26));
		self.__elements.append(Element(69,'Tm',1.720,1.720,1.700,6,0.00,0.83,0.32,168.934));
		self.__elements.append(Element(70,'Yb',1.940,1.940,1.700,6,0.00,0.75,0.22,173.04));
		self.__elements.append(Element(71,'Lu',1.720,1.720,1.700,6,0.00,0.67,0.14,174.967));
		self.__elements.append(Element(72,'Hf',1.570,1.440,1.700,6,0.30,0.76,1.00,178.49));
		self.__elements.append(Element(73,'Ta',1.430,1.340,1.700,6,0.30,0.65,1.00,180.948));
		self.__elements.append(Element(74,'W',1.370,1.300,1.700,6,0.13,0.58,0.84,183.84));
		self.__elements.append(Element(75,'Re',1.350,1.280,1.700,6,0.15,0.49,0.67,186.207));
		self.__elements.append(Element(76,'Os',1.370,1.260,1.700,6,0.15,0.40,0.59,190.23));
		self.__elements.append(Element(77,'Ir',1.320,1.270,1.700,6,0.09,0.33,0.53,192.217));
		self.__elements.append(Element(78,'Pt',1.500,1.300,1.720,6,0.96,0.93,0.82,195.078));
		self.__elements.append(Element(79,'Au',1.500,1.340,1.660,6,0.80,0.82,0.12,196.967));
		self.__elements.append(Element(80,'Hg',1.700,1.490,1.550,6,0.71,0.71,0.76,200.59));
		self.__elements.append(Element(81,'Tl',1.550,1.480,1.960,3,0.65,0.33,0.30,204.383));
		self.__elements.append(Element(82,'Pb',1.540,1.480,2.020,4,0.34,0.35,0.38,207.2));
		self.__elements.append(Element(83,'Bi',1.540,1.450,1.700,3,0.62,0.31,0.71,208.980));
		self.__elements.append(Element(84,'Po',1.680,1.460,1.700,2,0.67,0.36,0.00,209.0));
		self.__elements.append(Element(85,'At',1.700,1.450,1.700,1,0.46,0.31,0.27,210.0));
		self.__elements.append(Element(86,'Rn',2.400,2.400,1.700,0,0.26,0.51,0.59,222.0));
		self.__elements.append(Element(87,'Fr',2.000,2.000,1.700,1,0.26,0.00,0.40,223.0));
		self.__elements.append(Element(88,'Ra',1.900,1.900,1.700,2,0.00,0.49,0.00,226.0));
		self.__elements.append(Element(89,'Ac',1.880,1.880,1.700,6,0.44,0.67,0.98,227.0));
		self.__elements.append(Element(90,'Th',1.790,1.790,1.700,6,0.00,0.73,1.00,232.038));
		self.__elements.append(Element(91,'Pa',1.610,1.610,1.700,6,0.00,0.63,1.00,231.036));
		self.__elements.append(Element(92,'U',1.580,1.580,1.860,6,0.00,0.56,1.00,238.029));
		self.__elements.append(Element(93,'Np',1.550,1.550,1.700,6,0.00,0.50,1.00,237.0));
		self.__elements.append(Element(94,'Pu',1.530,1.530,1.700,6,0.00,0.42,1.00,244.0));
		self.__elements.append(Element(95,'Am',1.510,1.070,1.700,6,0.33,0.36,0.95,243.0));
		self.__elements.append(Element(96,'Cm',1.500,0.000,1.700,6,0.47,0.36,0.89,247.0));
		self.__elements.append(Element(97,'Bk',1.500,0.000,1.700,6,0.54,0.31,0.89,247.0));
		self.__elements.append(Element(98,'Cf',1.500,0.000,1.700,6,0.63,0.21,0.83,251.0));
		self.__elements.append(Element(99,'Es',1.500,0.000,1.700,6,0.70,0.12,0.83,252.0));
		self.__elements.append(Element(100,'Fm',1.500,0.000,1.700,6,0.70,0.12,0.73,257.0));
		self.__elements.append(Element(101,'Md',1.500,0.000,1.700,6,0.70,0.05,0.65,258.0));
		self.__elements.append(Element(102,'No',1.500,0.000,1.700,6,0.74,0.05,0.53,259.0));
		self.__elements.append(Element(103,'Lr',1.500,0.000,1.700,6,0.78,0.00,0.40,262.0));
		self.__elements.append(Element(104,'Rf',1.600,0.000,1.700,6,0.80,0.00,0.35,261.0));
		self.__elements.append(Element(105,'Db',1.600,0.000,1.700,6,0.82,0.00,0.31,262.0));
		self.__elements.append(Element(106,'Sg',1.600,0.000,1.700,6,0.85,0.00,0.27,263.0));
		self.__elements.append(Element(107,'Bh',1.600,0.000,1.700,6,0.88,0.00,0.22,264.0));
		self.__elements.append(Element(108,'Hs',1.600,0.000,1.700,6,0.90,0.00,0.18,265.0));
		self.__elements.append(Element(109,'Mt',1.600,0.000,1.700,6,0.92,0.00,0.15,268.0));
		self.__elements.append(Element(110,'Uun',1.600,0.000,1.700,6,0.95,0.00,0.11,269.0));
      
	def getElementBySymbol(self,symbol):
		for e in self.__elements:
			if e.symbol.lower() == symbol.lower():
				return e
		return None

	def getElementByAtomicNumber(self,atnum):
		return self.__elements[atnum]
