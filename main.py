# -------------------------------------------------- #
#               Developed by TCFSH 12430             #
# -------------------------------------------------- #
# imports
import os
import pubchempy as pcp
import requests
from openbabel import openbabel
import shutil
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# manual inputs
iterations = 5
device = 'MAC'
path_div = r"\\"
op_dir = r"/Users/albertdai/Desktop/Docker"
out_dir = r"/Users/albertdai/Desktop/Results"
# #vina_dir = r"/Users/albertdai/Desktop/vina_1.2.5_mac_x86_64"
vina_dir = r"/Users/albertdai/Desktop/vina"
url = r"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"
if device == 'MAC':
    path_div = '/'

# setting up (variable declaration)
proteins = []
ligands = []
config = {}
results = {}

# parsing
os.chdir(op_dir)
content = os.listdir(op_dir)
for i in content:
    if 'protein' in i and '.pdbqt' in i:
        proteins.append(i.removeprefix('protein').removesuffix('.pdbqt'))
    elif i == 'ligands.txt':
        with open(i, 'r') as f:
            ligands = f.read().split('\n')
            f.close()
    elif i == 'params.txt':
        with open(i, 'r') as f:
            text = f.read().split('\n-----div-----\n')
            for p in range(len(text)):
                temp_info = text[p].split(':\n')
                config[temp_info[0]] = temp_info[1]
            f.close()
    else:
        pass

#scrape sdf from pubchem and convert to pdbqt
checked_ligands = []
conv = openbabel.OBConversion()
conv.SetInAndOutFormats('sdf', 'pdbqt')
print(f'Grabbing files from pubchem (num={len(ligands)})')

for i in range(len(ligands)):
    if f'{ligands[i]}.pdbqt' in content:
        pass
    else:
        print(f'Getting ligand: {ligands[i]} ({i+1} out of {len(ligands)})')
        chem_id = pcp.get_compounds(ligands[i], 'name', record_type = '3d')
        if chem_id:
            chem_id = chem_id[0].cid
            checked_ligands.append(ligands[i])
            try:
                response = requests.get(f'{url}{chem_id}/SDF')
                response.raise_for_status()
                molecule = openbabel.OBMol()
                conv.ReadString(molecule, response.text)
                pdbqt_text = conv.WriteString(molecule)
                with open(f'{ligands[i]}.pdbqt', 'w') as f:
                    f.write(pdbqt_text)
                    f.close()
            except (requests.exceptions.RequestException, pcp.PubChemHTTPError) as error:
                print(f'Error occurred while downloading {ligands[i]}: {error}')
        else:
            print(f'Unable to grab {ligands[i]}')

# preparing config file and docking
for i in range(len(proteins)):
    results[proteins[i]] = {}
    for j in range(len(ligands)):
        max_affinity = 0
        for iter_var in range(iterations):
            with open('config.txt', 'w') as f:
                f.write(f'receptor = protein{proteins[i]}.pdbqt\nligand = {ligands[j]}.pdbqt\n\n{config[proteins[i]]}')
                f.close()
            print('--------------------------------------------------\n--------------------------------------------------')
            print(f'Docking Protein: {proteins[i]} with Ligand: {ligands[j]} for the {iter_var+1} time\nProgress:\n({i+1} out of {len(proteins)} proteins)\n({j+1} out of {len(ligands)} ligands)')
            print('--------------------------------------------------\n--------------------------------------------------')
            os.system(rf'{vina_dir} --receptor protein{proteins[i]}.pdbqt --ligand {ligands[j]}.pdbqt --config config.txt --log log.txt --out output_{proteins[i]}_{ligands[j]}_{iter_var}.pdbqt')
            with open('log.txt', 'r') as f:
                txt = f.read().split('\n')
                if True:
                    max_affinity += float([k for k in txt[27].split(' ') if k][1])/iterations
                    print(f'Successfully obtained docking results for {proteins[i]} & {ligands[j]} ({iter_var+1}/{iterations})')
                    shutil.move(op_dir+path_div+fr'output_{proteins[i]}_{ligands[j]}_{iter_var}.pdbqt', out_dir+path_div+fr'output_{proteins[i]}_{ligands[j]}_{iter_var}.pdbqt')
                    f.close()
                else:
                    max_affinity = False
                    print(f'Error with autodock vina results for {proteins[i]} & {ligands[j]}')
                    f.close()
        if max_affinity:
            results[proteins[i]][ligands[j]] = str(int(max_affinity*10)/10)
        else:
            results[proteins[i]][ligands[j]] = 'ERROR'

# write results
str = ''
prot = list(results.keys())
itm = list(results.values())
for i in range(len(prot)):
    str += f'{prot[i]}\n'
    for j in list(itm[i].keys()):
        str += f'{j}: {itm[i][j]}\n'
with open('analysis.txt', 'w') as f:
    f.write(str)
    f.close()