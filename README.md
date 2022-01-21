---
Project authors: Sophie Binder, Noura Chelbat Ajouid, Anna Zöchner
---

# Short description

This is the final assignment of the lecture "Weitere Softwareentwicklung" within the Master "Biodata Science". In this assignment, 
we have to put into practice the learning material about Git and GitHub as well as about how to organize a research project within computational biology. 
This project is based on Exercise 12 from Ekmekci et al., 2016: “An Introduction to Programming for Bioscientists: A Python-Based Primer”.
We were given the task to organize and develop the needed resources for a mini-project where the frequency of aminoacids within different proteins could be 
an indicator of the type of secondary structure of such proteins.

# This was our approach

* Creation of a potential project hierarchy. Create all directories, subdirectories and text files.
* Install Git and get a GitHub account that can be accessed by the group members and lecturer (https://github.com/annazoechner/FinalProject_WSE/)
* Create a local Git repository where to clone the project with all its contained files and subdirectories.
* Conducting the pipeline: running the bash and python scripts, solve bugs and completing the missing code lines. Generate an additional conda environment file.
* Push/pull every change to the GitHub account

# Installation/usage instructions

Required Environment: 
- numpy (1.18.1) 
- matplotlib (3.1.1) 
- pandas (1.0.3)
- Python (3.7.6) 
- Online access to PDB database 
- Biopython (1.76) (Terminal command: # conda install -c conda-forge biopython)
- xssp (`mkdssp` executable, 3.0.5) 
     
Required packages/modules: 
- Bio.PDB -> crystal structures of biological macromolecules 
- PDBList -> from Bio.PDB

The environment is also provided as `requirements.txt`

#Project structure description

1. Project hierarchy:directories and subdirectories as well as text files within this project main directory

-------FinalProject
		|
		----FinalProjectnotes.txt
		|
		
		|
		----README.md
		|
		|
		....01_download/
		|
		....02_parse_pdb/
		|
		
		|
		----doc/
		|
		----bin/
		|
		




