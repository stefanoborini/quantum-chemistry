import sys
import subprocess

def bwrap_xyz2inchi():
    try:
        xyz = sys.argv[1]
        inchi = sys.argv[2]
        p = subprocess.Popen(["babel", "-ixyz", xyz, "-oinchi", inchi])
        return p.wait()
    except:
        return 1



def bwrap_xyz2smiles():
    try:
        xyz = sys.argv[1]
        smiles = sys.argv[2]

        p = subprocess.Popen(["babel", "-ixyz", xyz, "-osmiles", "-"], stdout=subprocess.PIPE)
        p.wait()
        smiles_string = p.stdout.readline().split("\t")[0]

        f = file(smiles,"w")
        f.write(smiles_string)
        f.close()
        return 0
    except:
        return 1

def bwrap_xyz2molweight():
    import openbabel

    try:
        xyz = sys.argv[1]
        weight = sys.argv[2]

        obconv = openbabel.OBConversion()
        obconv.SetInFormat("xyz")
        obmol = openbabel.OBMol()

        obconv.ReadFile(obmol,xyz)
        w = obmol.GetMolWt()

        f = file(weight,"w")
        f.write(str(w))
        f.close()
        return 0
    except Exception, e :
        return 1


