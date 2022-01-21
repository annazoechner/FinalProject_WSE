#!/usr/bin/env python

import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Column names
conf1 = "Helix"
conf2 = "Sheet"
conf3 = "Other"

# Parse arguments
parser = argparse.ArgumentParser(
    description="""FILE is a file with rows and columns 'Helix', 'Sheet',
    'Other' in tab-separated format. The script plots the rows as distinct
    labels on the x-axis, and the columns as multibars."""
)
parser.add_argument("infile", metavar="FILE", help="Input file")
args = parser.parse_args()


# Read file
df = pd.read_csv(args.infile, sep="\t", encoding = "utf-8")

df.columns = ["Index","AA","Helix","Sheet","Other"]
df = df.drop(df.columns[[0]], axis=1)
print(df)

df.index = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q",
            "R", "S", "T", "V", "W", "Y"]

df.plot.bar(xlabel="Amino acids", ylabel="Relative frequency [%]")

plt.savefig("AA_freq_table.pdf")
