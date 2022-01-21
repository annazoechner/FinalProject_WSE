#!/usr/bin/env python

"""Parse pdb files and determine for each amino acid how often
it participates in different secondary structures. Write results
as tsv file.
"""

import logging
import argparse
from Bio.PDB import PDBParser, DSSP
from Bio import Data
import pandas as pd
import os
import warnings

# ignore warnings
warnings.filterwarnings('ignore')

# Create logger
logging.basicConfig(
    level=logging.NOTSET, format=" %(levelname)-7s:: %(message)s"
)  # configure root logger
logger = logging.getLogger(__name__)  # create custom logger
logger.setLevel(logging.DEBUG)  # set level for custom logger

# Parse arguments
# parser = argparse.ArgumentParser(
#     description="""FILE is a file with rows and columns 'Helix', 'Sheet',
#     'Other' in tab-separated format. The script plots the rows as distinct
#     labels on the x-axis, and the columns as multibars."""
# )
# parser.add_argument("infile", metavar="FILE", help="Input file")
# args = parser.parse_args()
# infile = args.infile

# https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ
# "How do I determine secondary structure?" -> DSSP codes
DSSP_codes = dict(
    [
        ("Helix", "H"),
        ("Bridge", "B"),
        ("Strand", "E"),
        ("3-10 Helix", "G"),
        ("Pi-Helix", "I"),
        ("Turn", "T"),
        ("Bend", "S"),
        ("Other", "-"),
    ]
)

#helix = ["H", "G", "I"]
#sheet = ["B", "E"]
#other = ["S", "T", "C"]

#protein_letters = Data.CodonTable.IUPACData.protein_letters
#protein_list = list(protein_letters)

# Amino acid dictionary
# will be filled after creating the dssp

#amino_dict = {}
#for key in protein_list:
#    amino_dict[key] = [0,0,0]

# {'A'}: [0,0,0],
# {'C'}: [0,0,0]

# protein_id = infile.split('/')[(-1)].split('.')[0].lstrip('pdb')

def parse_pdb(id, file):
    """
    Run DSSP and parse secondary structure.
    
    Key arguments:
    id -- protein id
    file -- *ent-File
    
    Returns:
    DSSP object -- is accessed by a tuple (chain id, residue id)
    """
    p = PDBParser()
    structure = p.get_structure(id, file)
    model = structure[0]
    # perfom dssp
    dssp = DSSP(model, file)
    return dssp

# DSSP data is accessed by a tuple - (chain id, residue id)
# a_key = list(dssp.keys())[0] 
# print(dssp[a_key]) 
# The dssp data returned for a single residue is a tuple 

def get_seq_struct(dssp):
    """
    Extract amino acid sequence and secondary structure types from dssp data.
    
    Key arguments:
    dssp -- DSSP object
    
    Returns:
    seq_list -- List containing amino acid sequence
    sec_struct_list -- List containing secondary structure types
    """
    sequence = ''
    sec_structure = ''
    for z in range(len(dssp)):
        a_key = list(dssp.keys())[z]
        sequence += dssp[a_key][1]
        sec_structure += dssp[a_key][2]
    seq_list = list(sequence)
    sec_struct_list = list(sec_structure)
    return seq_list, sec_struct_list

#print(sequence)
#print(sec_structure)

#seq_list = list(sequence)
#sec_struct_list = list(sec_structure)


# Convert amino_dict to dataframe
# freq_df = pd.DataFrame.from_dict(amino_dict)


# Count amino acid for secondary structure
def fill_freq_table(seq_list, sec_struct_list, freq_df):
    """
    Count amino acid for secondary structures (Helix, Sheet, Other).
    
    Key arguments:
    seq_list -- List of the amino acid sequence
    sec_struct_list -- List of the secondary structure types
    freq_df -- Dataframe of amino acid dictionary
    
    Returns:
    freq_df -- Dataframe with frequencies of amino acids for secondary structures
    """
    # Create lists for each secondary structure with corresponding dssp codes
    helix = ["H", "G", "I"]
    sheet = ["B", "E"]
    # other = ["S", "T", "C"]
    for i in range(len(sec_struct_list)): 
        aa = seq_list[i]
        ss = sec_struct_list[i]
        if ss in helix:
            freq_df[aa][0] +=1
        elif ss in sheet:
            freq_df[aa][1] +=1
        else:
            freq_df[aa][2] +=1           
    freq_df = freq_df.transpose()
    freq_df.set_axis(['Helix', 'Sheet', 'Other'], axis='columns', inplace=True)
    return freq_df

# Relative counts
# Each element divided by total sum multiplied by 100
        
def relative_counts(freq_df):
    """
    Calculate relative counts of amino acids for secondary structures
    
    Key arguments:
    freq_df -- Dataframe with frequencies of amino acids for secondary structures
    
    Returns:
    rel_freq -- Dataframe with relative counts of amino acids for secondary structures
    """
    tot_sum = freq_df.values.sum()
    rel_freq = round((freq_df/tot_sum)*100, 2) 
    rel_freq.reset_index(inplace=True)
    
    results = rel_freq.rename(columns = {'index':'AA'})
    return results
               

def main(pdb_dir):
    #args = parser.parse_args()
    print(pdb_dir)
    #parser.add_argument("infile", metavar="FILE", help="Input file")
    #infile = args.infile
    logger.info(f"Directory with PDB files: {pdb_dir}")
    
    # Create list of all protein letters
    protein_letters = Data.CodonTable.IUPACData.protein_letters
    protein_list = list(protein_letters)

    # Amino acid dictionary
    # will be filled after creating the dssp

    amino_dict = {}
    for key in protein_list:
        amino_dict[key] = [0,0,0]
    
    # Extract protein id from filename
    for infile in os.listdir(pdb_dir):
        protein_id = infile.split('/')[(-1)].split('.')[0].lstrip('pdb')
        infile_fullpath = os.path.join(pdb_dir, infile)

        logger.info("Parse pdb files and extract sequence and structure info")
        dssp = parse_pdb(protein_id,infile_fullpath)
        seq_list = (get_seq_struct(dssp))[0]
        sec_struct_list = (get_seq_struct(dssp))[1]
        #print(a.seq_list())   
    
        logger.info("Fill dataframe with frequencies of amino acids in secondary structure and calculate relative frequencies")
        # Convert amino_dict to dataframe
        df = pd.DataFrame.from_dict(amino_dict)
        freq_df = fill_freq_table(seq_list, sec_struct_list, df)
        results = relative_counts(freq_df)
    
    # Create .tsv of the results
    logger.info("Save results in tsv-file")
    results.to_csv("AA_freq_table.tsv", sep="\t")   
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""The script outputs a table of AA frequencies in
        different secondary structures, as determined by the DSSP algorithm.""")
    parser.add_argument(
        "pdb_dir", metavar = "DIR", help = "Directory with pdb/ent files", 
        default = "./results")
    #parser.add_argument("infile", metavar="FILE", help="Input file")
    args = parser.parse_args()
    main(args.pdb_dir)
        





