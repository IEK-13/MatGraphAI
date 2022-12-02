# importing module
from pandas import *
from pubchempy import *
# reading CSV file
data = read_csv("FORMAX_SMILES.csv")

# converting column data to list
smiles = data['smiles'].tolist()
mol = data['name']

for i in range(len(smiles)):
    # if i % 2 ==0:
    #     print(smiles[i]+","+mol[i])
    for compound in get_compounds(smiles[i], 'smiles'):
        if compound.cid != None:
            print(mol[i], smiles[i])
