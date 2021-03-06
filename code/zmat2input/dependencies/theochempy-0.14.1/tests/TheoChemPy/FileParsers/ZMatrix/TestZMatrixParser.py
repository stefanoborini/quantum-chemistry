# @author Stefano Borini
# @license Aristic License 2.0
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy.FileParsers import ZMatrix 
from theochempy._theochempy.IO import FileReader
from theochempy._theochempy import Units
from theochempy._theochempy import Math


def moduleDir():
    return os.path.dirname(__file__)

class TestZMatrixParser(unittest.TestCase):
    def testInit(self): # fold>>
        parser = ZMatrix.ZMatrixParser()
        self.assertNotEqual(parser, None)
    # <<fold
    def testParseFile(self): # fold>>
        parser = ZMatrix.ZMatrixParser()
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")
        parser.parseFile(filename)

        self.assertFalse(parser._infile is None)
        self.assertFalse(parser._parameters is None)
        self.assertFalse(parser._zmatrix is None)
        self.assertFalse(parser._distance_units is None)
        self.assertFalse(parser._angle_units is None)
        self.assertFalse(parser._basis is None)
        self.assertFalse(parser._symmetries is None)
    # <<fold
    def testParseParametersSection(self): # fold>>
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")
        f = FileReader.FileReader(filename)
        params = ZMatrix._parseParametersSection(f)
        valid_data = {'R38': '1.08', 'R39': '1.08', 'R34': '1.07960213', 'R35': '1.08', 'R36': '1.08', 'R37': '1.08', 'R30': '1.07949168', 'R31': '1.0787856', 'R32': '1.54', 'R33': '1.07811168', 'R4': '1.80206569', 'R5': '1.8448968', 'R6': '1.08199628', 'R7': '1.76839634', 'R2': '1.19576559', 'R3': '1.53312447', 'R8': '1.07858004', 'R9': '1.08259096', 'R16': '1.38765396', 'R17': '1.07358923', 'R14': '1.38054101', 'R15': '1.38471258', 'R12': '1.39340179', 'R13': '1.39044518', 'R10': '1.07869792', 'R11': '1.48957644', 'R18': '1.07323301', 'R19': '1.07512119', 'A40': '110.02', 'D14': '-179.79472963', 'D15': '178.86904242', 'D16': '1.05496966', 'D17': '-179.76567536', 'D10': '-121.94534813', 'D11': '-177.95494878', 'D12': '21.21675983', 'D13': '-178.44654244', 'D18': '-177.24354928', 'D19': '179.73244443', 'A33': '109.22613503', 'A32': '106.016903', 'A31': '105.9007008', 'A30': '110.12220894', 'A37': '110.02', 'A36': '110.02', 'A35': '110.02', 'A34': '110.12358948', 'A39': '110.02', 'A38': '110.02', 'D29': '67.71385394', 'D28': '-109.45854506', 'D21': '179.68183354', 'D20': '-179.11647443', 'D23': '-116.43966678', 'D22': '116.05379021', 'D25': '-126.17156573', 'D24': '87.05344984', 'D27': '124.70856793', 'D26': '127.71831196', 'A20': '119.72327648', 'A21': '119.90669975', 'A22': '105.58712546', 'A23': '105.92258212', 'A24': '115.24875957', 'A25': '101.05663993', 'A26': '103.4496195', 'A27': '122.33914213', 'A28': '123.98317478', 'A29': '109.86517848', 'R40': '1.08', 'D38': '179.0', 'D39': '120.0', 'D36': '120.0', 'D37': '-120.0', 'D34': '119.3672904', 'D35': '179.0', 'D32': '-155.75576458', 'D33': '-119.44715865', 'D30': '-121.59454892', 'D31': '119.03753102', 'A15': '120.01221455', 'A14': '120.26266887', 'A17': '119.05794639', 'A16': '119.84605838', 'A11': '121.74447654', 'A10': '109.13117206', 'A13': '122.97326956', 'A12': '117.41320957', 'A19': '119.9917391', 'A18': '120.82810526', 'A3': '118.33351953', 'A5': '111.57603219', 'A4': '111.78682756', 'A7': '108.02130357', 'A6': '111.51694325', 'A9': '104.79349303', 'A8': '109.3110954', 'R29': '1.54', 'R28': '1.43261165', 'R27': '1.42894607', 'R26': '1.56849371', 'D40': '-120.0', 'R25': '1.57337162', 'R24': '1.45504444', 'D8': '62.46718009', 'D9': '118.66525397', 'D6': '113.3724925', 'D7': '-62.30804556', 'D4': '75.67592699', 'D5': '-128.40691686', 'R23': '1.43879487', 'R22': '1.43815155', 'R21': '1.07568689', 'R20': '1.07486465'}
        self.assertEqual(len(params.keys()), len(valid_data.keys()))
        for key, value in params.items():
            self.assertEqual(valid_data.has_key(key), True)
            self.assertEqual(valid_data[key], value)

            
        f.close()
        # <<fold
    def testParseZMatrixSection(self): # fold>>
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")
        f = FileReader.FileReader(filename)
        parameters= {'R38': '1.08', 'R39': '1.08', 'R34': '1.07960213', 'R35': '1.08', 'R36': '1.08', 'R37': '1.08', 'R30': '1.07949168', 'R31': '1.0787856', 'R32': '1.54', 'R33': '1.07811168', 'R4': '1.80206569', 'R5': '1.8448968', 'R6': '1.08199628', 'R7': '1.76839634', 'R2': '1.19576559', 'R3': '1.53312447', 'R8': '1.07858004', 'R9': '1.08259096', 'R16': '1.38765396', 'R17': '1.07358923', 'R14': '1.38054101', 'R15': '1.38471258', 'R12': '1.39340179', 'R13': '1.39044518', 'R10': '1.07869792', 'R11': '1.48957644', 'R18': '1.07323301', 'R19': '1.07512119', 'A40': '110.02', 'D14': '-179.79472963', 'D15': '178.86904242', 'D16': '1.05496966', 'D17': '-179.76567536', 'D10': '-121.94534813', 'D11': '-177.95494878', 'D12': '21.21675983', 'D13': '-178.44654244', 'D18': '-177.24354928', 'D19': '179.73244443', 'A33': '109.22613503', 'A32': '106.016903', 'A31': '105.9007008', 'A30': '110.12220894', 'A37': '110.02', 'A36': '110.02', 'A35': '110.02', 'A34': '110.12358948', 'A39': '110.02', 'A38': '110.02', 'D29': '67.71385394', 'D28': '-109.45854506', 'D21': '179.68183354', 'D20': '-179.11647443', 'D23': '-116.43966678', 'D22': '116.05379021', 'D25': '-126.17156573', 'D24': '87.05344984', 'D27': '124.70856793', 'D26': '127.71831196', 'A20': '119.72327648', 'A21': '119.90669975', 'A22': '105.58712546', 'A23': '105.92258212', 'A24': '115.24875957', 'A25': '101.05663993', 'A26': '103.4496195', 'A27': '122.33914213', 'A28': '123.98317478', 'A29': '109.86517848', 'R40': '1.08', 'D38': '179.0', 'D39': '120.0', 'D36': '120.0', 'D37': '-120.0', 'D34': '119.3672904', 'D35': '179.0', 'D32': '-155.75576458', 'D33': '-119.44715865', 'D30': '-121.59454892', 'D31': '119.03753102', 'A15': '120.01221455', 'A14': '120.26266887', 'A17': '119.05794639', 'A16': '119.84605838', 'A11': '121.74447654', 'A10': '109.13117206', 'A13': '122.97326956', 'A12': '117.41320957', 'A19': '119.9917391', 'A18': '120.82810526', 'A3': '118.33351953', 'A5': '111.57603219', 'A4': '111.78682756', 'A7': '108.02130357', 'A6': '111.51694325', 'A9': '104.79349303', 'A8': '109.3110954', 'R29': '1.54', 'R28': '1.43261165', 'R27': '1.42894607', 'R26': '1.56849371', 'D40': '-120.0', 'R25': '1.57337162', 'R24': '1.45504444', 'D8': '62.46718009', 'D9': '118.66525397', 'D6': '113.3724925', 'D7': '-62.30804556', 'D4': '75.67592699', 'D5': '-128.40691686', 'R23': '1.43879487', 'R22': '1.43815155', 'R21': '1.07568689', 'R20': '1.07486465'}
        zmat, distance_unit, angle_unit = ZMatrix._parseZMatrixSection(f, parameters)
        valid_data = [('O', '1'), ('C', '2', '1', '1.19576559'), ('C', '3', '2', '1.53312447', '1', '118.33351953'), ('S', '4', '3', '1.80206569', '2', '111.78682756', '1', '75.67592699'), ('P', '5', '3', '1.8448968', '2', '111.57603219', '4', '-128.40691686'), ('H', '6', '3', '1.08199628', '2', '111.51694325', '4', '113.3724925'), ('C', '7', '4', '1.76839634', '3', '108.02130357', '2', '-62.30804556'), ('H', '8', '7', '1.07858004', '4', '109.3110954', '3', '62.46718009'), ('H', '9', '7', '1.08259096', '4', '104.79349303', '8', '118.66525397'), ('H', '10', '7', '1.07869792', '4', '109.13117206', '8', '-121.94534813'), ('C', '11', '2', '1.48957644', '1', '121.74447654', '3', '-177.95494878'), ('C', '12', '11', '1.39340179', '2', '117.41320957', '1', '21.21675983'), ('C', '13', '11', '1.39044518', '2', '122.97326956', '12', '-178.44654244'), ('C', '14', '12', '1.38054101', '11', '120.26266887', '2', '-179.79472963'), ('C', '15', '13', '1.38471258', '11', '120.01221455', '2', '178.86904242'), ('C', '16', '14', '1.38765396', '12', '119.84605838', '11', '1.05496966'), ('H', '17', '12', '1.07358923', '11', '119.05794639', '14', '-179.76567536'), ('H', '18', '13', '1.07323301', '11', '120.82810526', '15', '-177.24354928'), ('H', '19', '14', '1.07512119', '12', '119.9917391', '16', '179.73244443'), ('H', '20', '15', '1.07486465', '13', '119.72327648', '11', '-179.11647443'), ('H', '21', '16', '1.07568689', '14', '119.90669975', '12', '179.68183354'), ('O', '22', '4', '1.43815155', '3', '105.58712546', '7', '116.05379021'), ('O', '23', '4', '1.43879487', '3', '105.92258212', '7', '-116.43966678'), ('O', '24', '5', '1.45504444', '3', '115.24875957', '2', '87.05344984'), ('O', '25', '5', '1.57337162', '3', '101.05663993', '24', '-126.17156573'), ('O', '26', '5', '1.56849371', '3', '103.4496195', '24', '127.71831196'), ('C', '27', '25', '1.42894607', '5', '122.33914213', '3', '124.70856793'), ('C', '28', '26', '1.43261165', '5', '123.98317478', '3', '-109.45854506'), ('C', '29', '27', '1.54', '25', '109.86517848', '5', '67.71385394'), ('H', '30', '27', '1.07949168', '25', '110.12220894', '29', '-121.59454892'), ('H', '31', '27', '1.0787856', '25', '105.9007008', '29', '119.03753102'), ('C', '32', '28', '1.54', '26', '106.016903', '5', '-155.75576458'), ('H', '33', '28', '1.07811168', '26', '109.22613503', '32', '-119.44715865'), ('H', '34', '28', '1.07960213', '26', '110.12358948', '32', '119.3672904'), ('H', '35', '29', '1.08', '27', '110.02', '25', '179.0'), ('H', '36', '29', '1.08', '27', '110.02', '35', '120.0'), ('H', '37', '29', '1.08', '27', '110.02', '35', '-120.0'), ('H', '38', '32', '1.08', '28', '110.02', '26', '179.0'), ('H', '39', '32', '1.08', '28', '110.02', '38', '120.0'), ('H', '40', '32', '1.08', '28', '110.02', '38', '-120.0')]
        self.assertEqual(len(zmat), len(valid_data))
        for index in xrange(len(zmat)):
            self.assertEqual(zmat[index], valid_data[index])

        self.assertEqual(distance_unit, Units.angstrom) 
        self.assertEqual(angle_unit, Units.degrees) 
        f.close()
        # <<fold
    def testParseBasisSection(self): # fold>>

        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")
        f = FileReader.FileReader(filename)
        zmat = [('O', '1'), ('C', '2', '1', '1.19576559'), ('C', '3', '2', '1.53312447', '1', '118.33351953'), ('S', '4', '3', '1.80206569', '2', '111.78682756', '1', '75.67592699'), ('P', '5', '3', '1.8448968', '2', '111.57603219', '4', '-128.40691686'), ('H', '6', '3', '1.08199628', '2', '111.51694325', '4', '113.3724925'), ('C', '7', '4', '1.76839634', '3', '108.02130357', '2', '-62.30804556'), ('H', '8', '7', '1.07858004', '4', '109.3110954', '3', '62.46718009'), ('H', '9', '7', '1.08259096', '4', '104.79349303', '8', '118.66525397'), ('H', '10', '7', '1.07869792', '4', '109.13117206', '8', '-121.94534813'), ('C', '11', '2', '1.48957644', '1', '121.74447654', '3', '-177.95494878'), ('C', '12', '11', '1.39340179', '2', '117.41320957', '1', '21.21675983'), ('C', '13', '11', '1.39044518', '2', '122.97326956', '12', '-178.44654244'), ('C', '14', '12', '1.38054101', '11', '120.26266887', '2', '-179.79472963'), ('C', '15', '13', '1.38471258', '11', '120.01221455', '2', '178.86904242'), ('C', '16', '14', '1.38765396', '12', '119.84605838', '11', '1.05496966'), ('H', '17', '12', '1.07358923', '11', '119.05794639', '14', '-179.76567536'), ('H', '18', '13', '1.07323301', '11', '120.82810526', '15', '-177.24354928'), ('H', '19', '14', '1.07512119', '12', '119.9917391', '16', '179.73244443'), ('H', '20', '15', '1.07486465', '13', '119.72327648', '11', '-179.11647443'), ('H', '21', '16', '1.07568689', '14', '119.90669975', '12', '179.68183354'), ('O', '22', '4', '1.43815155', '3', '105.58712546', '7', '116.05379021'), ('O', '23', '4', '1.43879487', '3', '105.92258212', '7', '-116.43966678'), ('O', '24', '5', '1.45504444', '3', '115.24875957', '2', '87.05344984'), ('O', '25', '5', '1.57337162', '3', '101.05663993', '24', '-126.17156573'), ('O', '26', '5', '1.56849371', '3', '103.4496195', '24', '127.71831196'), ('C', '27', '25', '1.42894607', '5', '122.33914213', '3', '124.70856793'), ('C', '28', '26', '1.43261165', '5', '123.98317478', '3', '-109.45854506'), ('C', '29', '27', '1.54', '25', '109.86517848', '5', '67.71385394'), ('H', '30', '27', '1.07949168', '25', '110.12220894', '29', '-121.59454892'), ('H', '31', '27', '1.0787856', '25', '105.9007008', '29', '119.03753102'), ('C', '32', '28', '1.54', '26', '106.016903', '5', '-155.75576458'), ('H', '33', '28', '1.07811168', '26', '109.22613503', '32', '-119.44715865'), ('H', '34', '28', '1.07960213', '26', '110.12358948', '32', '119.3672904'), ('H', '35', '29', '1.08', '27', '110.02', '25', '179.0'), ('H', '36', '29', '1.08', '27', '110.02', '35', '120.0'), ('H', '37', '29', '1.08', '27', '110.02', '35', '-120.0'), ('H', '38', '32', '1.08', '28', '110.02', '26', '179.0'), ('H', '39', '32', '1.08', '28', '110.02', '38', '120.0'), ('H', '40', '32', '1.08', '28', '110.02', '38', '-120.0')]
        basis = ZMatrix._parseBasisSection(f, zmat)
        valid_data = {1: 'ziopeppe', 2: 'ziopeppe', 3: 'ziopeppe', 4: 'ziopeppe', 5: 'ziopeppe', 6: 'ziopeppe', 7: 'ziopeppe', 8: 'ziopeppe', 9: 'ziopeppe', 10: 'ziopeppe', 11: 'ziopeppe', 12: 'ziopeppe', 13: 'ziopeppe', 14: 'ziopeppe', 15: 'ziopeppe', 16: 'ziopeppe', 17: 'ziopeppe', 18: 'ziopeppe', 19: 'ziopeppe', 20: 'ziopeppe', 21: 'ziopeppe', 22: 'ziopeppe', 23: 'ziopeppe', 24: 'ziopeppe', 25: 'ziopeppe', 26: 'ziopeppe', 27: 'ziopeppe', 28: 'ziopeppe', 29: 'ziopeppe', 30: 'ziopeppe', 31: 'ziopeppe', 32: 'ziopeppe', 33: 'ziopeppe', 34: 'ziopeppe', 35: 'ziopeppe', 36: 'ziopeppe', 37: 'ziopeppe', 38: 'ziopeppe', 39: 'ziopeppe', 40: 'ziopeppe'}
        self.assertEqual(len(basis.keys()), len(valid_data.keys()))
        for key, value in basis.items():
            self.assertEqual(valid_data.has_key(key), True)
            self.assertEqual(valid_data[key], value)

        f.close()
        # <<fold
    def testParseSymmetrySection(self): # fold>>
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")
        f = FileReader.FileReader(filename)
        sym = ZMatrix._parseSymmetrySection(f)
        valid_data = ['X','Z']
        self.assertEqual(len(sym), len(valid_data))
        for index in xrange(len(sym)):
            self.assertEqual(sym[index], valid_data[index])

            
        f.close()
        # <<fold
    def testCartesianCoords(self): # fold>>
        zmat= [('O', '1'), ('C', '2', '1', '1.19576559'), ('C', '3', '2', '1.53312447', '1', '118.33351953'), ('S', '4', '3', '1.80206569', '2', '111.78682756', '1', '75.67592699'), ('P', '5', '3', '1.8448968', '2', '111.57603219', '4', '-128.40691686'), ('H', '6', '3', '1.08199628', '2', '111.51694325', '4', '113.3724925'), ('C', '7', '4', '1.76839634', '3', '108.02130357', '2', '-62.30804556'), ('H', '8', '7', '1.07858004', '4', '109.3110954', '3', '62.46718009'), ('H', '9', '7', '1.08259096', '4', '104.79349303', '8', '118.66525397'), ('H', '10', '7', '1.07869792', '4', '109.13117206', '8', '-121.94534813'), ('C', '11', '2', '1.48957644', '1', '121.74447654', '3', '-177.95494878'), ('C', '12', '11', '1.39340179', '2', '117.41320957', '1', '21.21675983'), ('C', '13', '11', '1.39044518', '2', '122.97326956', '12', '-178.44654244'), ('C', '14', '12', '1.38054101', '11', '120.26266887', '2', '-179.79472963'), ('C', '15', '13', '1.38471258', '11', '120.01221455', '2', '178.86904242'), ('C', '16', '14', '1.38765396', '12', '119.84605838', '11', '1.05496966'), ('H', '17', '12', '1.07358923', '11', '119.05794639', '14', '-179.76567536'), ('H', '18', '13', '1.07323301', '11', '120.82810526', '15', '-177.24354928'), ('H', '19', '14', '1.07512119', '12', '119.9917391', '16', '179.73244443'), ('H', '20', '15', '1.07486465', '13', '119.72327648', '11', '-179.11647443'), ('H', '21', '16', '1.07568689', '14', '119.90669975', '12', '179.68183354'), ('O', '22', '4', '1.43815155', '3', '105.58712546', '7', '116.05379021'), ('O', '23', '4', '1.43879487', '3', '105.92258212', '7', '-116.43966678'), ('O', '24', '5', '1.45504444', '3', '115.24875957', '2', '87.05344984'), ('O', '25', '5', '1.57337162', '3', '101.05663993', '24', '-126.17156573'), ('O', '26', '5', '1.56849371', '3', '103.4496195', '24', '127.71831196'), ('C', '27', '25', '1.42894607', '5', '122.33914213', '3', '124.70856793'), ('C', '28', '26', '1.43261165', '5', '123.98317478', '3', '-109.45854506'), ('C', '29', '27', '1.54', '25', '109.86517848', '5', '67.71385394'), ('H', '30', '27', '1.07949168', '25', '110.12220894', '29', '-121.59454892'), ('H', '31', '27', '1.0787856', '25', '105.9007008', '29', '119.03753102'), ('C', '32', '28', '1.54', '26', '106.016903', '5', '-155.75576458'), ('H', '33', '28', '1.07811168', '26', '109.22613503', '32', '-119.44715865'), ('H', '34', '28', '1.07960213', '26', '110.12358948', '32', '119.3672904'), ('H', '35', '29', '1.08', '27', '110.02', '25', '179.0'), ('H', '36', '29', '1.08', '27', '110.02', '35', '120.0'), ('H', '37', '29', '1.08', '27', '110.02', '35', '-120.0'), ('H', '38', '32', '1.08', '28', '110.02', '26', '179.0'), ('H', '39', '32', '1.08', '28', '110.02', '38', '120.0'), ('H', '40', '32', '1.08', '28', '110.02', '38', '-120.0')]
        basis = {1: 'ziopeppe', 2: 'ziopeppe', 3: 'ziopeppe', 4: 'ziopeppe', 5: 'ziopeppe', 6: 'ziopeppe', 7: 'ziopeppe', 8: 'ziopeppe', 9: 'ziopeppe', 10: 'ziopeppe', 11: 'ziopeppe', 12: 'ziopeppe', 13: 'ziopeppe', 14: 'ziopeppe', 15: 'ziopeppe', 16: 'ziopeppe', 17: 'ziopeppe', 18: 'ziopeppe', 19: 'ziopeppe', 20: 'ziopeppe', 21: 'ziopeppe', 22: 'ziopeppe', 23: 'ziopeppe', 24: 'ziopeppe', 25: 'ziopeppe', 26: 'ziopeppe', 27: 'ziopeppe', 28: 'ziopeppe', 29: 'ziopeppe', 30: 'ziopeppe', 31: 'ziopeppe', 32: 'ziopeppe', 33: 'ziopeppe', 34: 'ziopeppe', 35: 'ziopeppe', 36: 'ziopeppe', 37: 'ziopeppe', 38: 'ziopeppe', 39: 'ziopeppe', 40: 'ziopeppe'}
        
        correct_xyz_values= [
                                ( 0.000000,   0.000000,   0.000000),
                                ( 0.000000,   0.000000,   1.195766),
                                ( 0.000000,  -1.349456,   1.923391),
                                ( 1.621325,  -2.134657,   1.876428),
                                (-1.365297,  -2.439684,   1.330929),
                                (-0.158306,  -1.226977,   2.986714),
                                ( 2.026186,  -2.453087,   0.184708),
                                ( 2.088908,  -1.517992,  -0.349143),
                                ( 2.992674,  -2.939658,   0.218641),
                                ( 1.275497,  -3.098994,  -0.242915),
                                (-0.045204,   1.265933,   1.979479),
                                (-0.533680,   2.401462,   1.336414),
                                ( 0.403207,   1.359643,   3.292295),
                                (-0.597596,   3.606984,   2.006135),
                                ( 0.354029,   2.573946,   3.955982),
                                (-0.153165,   3.692661,   3.317898),
                                (-0.861678,   2.323006,   0.317171),
                                ( 0.830536,   0.509936,   3.789503),
                                (-0.987053,   4.477529,   1.509787),
                                ( 0.715077,   2.644282,   4.965948),
                                (-0.197764,   4.632662,   3.838967),
                                ( 2.539972,  -1.155496,   2.391803),
                                ( 1.471529,  -3.390844,   2.561763),
                                (-1.048516,  -3.254624,   0.167883),
                                (-2.529159,  -1.396026,   1.152880),
                                (-1.795402,  -3.219920,   2.621826),
                                (-3.230544,  -1.236483,  -0.081823),
                                (-1.546054,  -4.614470,   2.834973),
                                (-4.066300,  -2.496198,  -0.375469),
                                (-2.532201,  -1.056284,  -0.885034),
                                (-3.876572,  -0.383166,   0.053368),
                                (-2.609783,  -5.087066,   3.843305),
                                (-0.553897,  -4.740236,   3.237631),
                                (-1.643163,  -5.155431,   1.905741),
                                (-4.611233,  -2.371268,  -1.299505),
                                (-3.419595,  -3.356630,  -0.463953),
                                (-4.770040,  -2.668026,   0.425547),
                                (-2.491175,  -6.142661,   4.038370),
                                (-2.505447,  -4.545523,   4.771877),
                                (-3.598893,  -4.913407,   3.445935),
                                ]
        
        cartesian = ZMatrix._cartesianCoords(zmat, basis)
        self.assertEqual(len(zmat), len(cartesian))
        self.assertEqual(len(cartesian), len(correct_xyz_values))
        
        for index, entry in enumerate(cartesian):
            self.assertEqual(len(entry), 3)
            self.assertEqual(entry[0], zmat[index][0])
            self.assertEqual(entry[1].__class__, Math.Vector3)
            self.assertAlmostEqual(entry[1][0], correct_xyz_values[index][0], 6)
            self.assertAlmostEqual(entry[1][1], correct_xyz_values[index][1], 6)
            self.assertAlmostEqual(entry[1][2], correct_xyz_values[index][2], 6)
            self.assertNotEqual(entry[2], None)



    







        # <<fold

if __name__ == '__main__':
    unittest.main()
    
