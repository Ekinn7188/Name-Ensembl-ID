import pandas as pd
import numpy as np
import argparse

from pybiomart import Server

from sys import exit
import re

#########################
### How to Run Script ###
#########################
#
# 1. $ pip install pybiomart
# 2. $ pip install argparse
# There aren't anaconda installations for these libraries.
#
# 3. $ py Name_Gene.py [-h] [-o OUTPUT] [-n NAME | -i INDEX] input
# 
# positional arguments:
#  input                 The .csv file, which contains a column with ensembl gene ids.
#
# options:
#  -h, --help            show this help message and exit
#  -o OUTPUT, --output OUTPUT
#                        Output file. Defaults to ./output.csv.
#  -n NAME, --name NAME  Column name for ensmbl id list.
#  -i INDEX, --index INDEX
#                        Column index for ensmbl id list. (1-indexed) Defaults to 1.

#########################
### Register arguments ###
##########################

parser = argparse.ArgumentParser()

parser.add_argument("input", help="The .csv file, which contains a column with ensembl gene ids.")
parser.add_argument("-o", "--output",  help="Output file. Defaults to ./output.csv.", default="output.csv")

group = parser.add_mutually_exclusive_group()
group.add_argument("-n", "--name", help="Column name for ensembl id list.")
group.add_argument("-i", "--index", type=int, help="Column index for ensmbl id list. (1-indexed) Defaults to 1.", default=1)

args = parser.parse_args()

###################################
### Load .csv and prepare input ###
###################################

try:
    data = pd.read_csv(args.input)
except FileNotFoundError:
    print(f"{args.input} could not be found.")
    exit()

# If Gene name exists, get rid of it because it's being used later
try:
    data = data.drop(columns=["Gene name"])
except:
    pass

# Get rid of potential NaN rows
data = data.dropna()

#############################
### Load ensembl database ###
#############################

try:
    server = Server(host='http://www.ensembl.org')
    
    dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
                 .datasets['hsapiens_gene_ensembl'])
except:
    print("There was an issue connecting to http://www.ensembl.org. Try again later.")
    exit()

##################################
### Convert Genes IDs to names ###
##################################

try:
    col_name = args.name if args.name else data.columns[args.index-1]
    input = data[col_name].tolist()
except IndexError:
    print(f"Error: Index value of {args.index} is too {'large' if args.index > len(data.columns) else 'small'}. Values must be in range [{1},{len(data.columns)}].")
    exit()
except KeyError:
    print(f"Error: Column name '{col_name}' is not defined in the input file ({args.input}).")
    exit()
    
# Check if input is in the right format.
if re.search("^(ENSG)([0-9]{11})(\.([0-9]+))?$", str(input[0])) is None:
    print(f"Error: Input row is not valid.")
    exit()
    
# Query the ensembl database for the gene names.
def find_gene_name(id: list[str]) -> pd.DataFrame:
    versioned = False
    
    query = id
    # Support versioned gene ids
    if len(query) > 15:
        query = [x[:15].strip() for x in id]
        versioned = True
    
    result = dataset.query(attributes=['ensembl_gene_id','external_gene_name'], 
                         filters={'link_ensembl_gene_id': query})
    
    # Result is returned in sorted order, so to match version number back with name, sort the list of inputs 
    if versioned:
        id.sort()
        result['Gene stable ID'] = id
        
    return result

response = pd.DataFrame(columns=['Gene stable ID', 'Gene name'])

print("Finding Gene Names")
for i in range(0,len(input), 250):
    response = pd.concat([response, find_gene_name(input[i:i+250])])
    
response = response.rename(columns={"Gene stable ID": col_name})

#################################
### Write data to output file ###
#################################

# Place output into the main dataframe.
data = data.merge(response,how='left',left_on=[col_name], right_on=[col_name])

# Place column directly to the right of the ID column
gene_name_index = data.columns.get_loc(col_name)+1
columns = data.columns.to_series()
columns = pd.concat([columns[:gene_name_index], pd.Series(["Gene name"]), columns[gene_name_index:len(columns)-1]])
data = data[columns]

# Remove any unnamed text from the header before saving
unnamed = {x:"" for x in data.columns[data.columns.str.startswith('Unnamed:')]}
data = data.rename(columns=unnamed)

data.to_csv(args.output, index=False)

print("Done!")