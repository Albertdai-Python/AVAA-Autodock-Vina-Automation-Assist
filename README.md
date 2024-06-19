
# AVAA-Autodock-Vina-Automation-Assist
# Modules to install
**Python**
- pubchempy
- requests
- openbabel-wheel

**Vina**
- version 1.0.2
# File syntax
**Required Files:**
ligands.txt
params.txt
protein files *(.pdbqt format)*
#
***Params.txt***

    3n80:
    center_x = 75
    center_y = 61
    center_z = 63
    
    size_x = 80
    size_y = 80
    size_z = 80
    
    energy_range = 4
    
    exhaustiveness = 8
    -----div-----
    4wb9:
    center_x = -10
    center_y = -40
    center_z = -20
    
    size_x = 80
    size_y = 80
    size_z = 80
    
    energy_range = 4
    
    exhaustiveness = 8
#
***Ligands.txt***

    quercetin
    disulfiram
    acamprosate
    aspirin
    sesamin
    thiamine
    fluoxetin
#
# Instructions
- Set up directories in main.py 
	- op_dir *(operating directory)*
	- out_dir *(outputting directory)*
	- vina_dir *(directory of vina executable)*
- Files you will see after operation
	- log.txt *(last docking operation)*
	- analysis.txt *(docking results)*
	- **In results folder**:
		- pdbqt output files
	- the ligands
# Note
- You will see the docking progress as how many proteins and ligands elapsed
- You can also adjust the iteration number via the var *iteration* in the declaration part
