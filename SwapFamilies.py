# Author: Zachariah Neumeier
# July 19th, 2021
# Bourne Lab at UVA
#
# This code takes a "swap.txt" file from 3DSwap here(http://caps.ncbs.res.in/3dswap/3dswap_download_list.txt)
# and compiles a list of the PDB codes from the file along with their
# matching CATH superfamilies. Note that some PDB entries may have more 
# than one superfamily while some have none.

# The current method uses the SIFTS API along with pulling data from CATH site for PDB entry. Not all PDB
# entries from swap.txt were found using SIFTS so others use https://www.ebi.ac.uk/pdbe/api/mappings/cath/ + PDB

# Commented in the bottom is another way to match PDB codes with their CATH superfamily: using the PDB CATH uniprot
# file, although this method is not perfect (not all of the needed PDB codes are found in that file)


import csv, requests, json
import numpy as np
from bs4 import BeautifulSoup

print("Working...")

superfamilies = []
swap_codes = []
descriptions = []
desc = []
currentSwap = []
swapNum = []

# open file containing domain swapping info and PDB codes for swaps
with open("swap.txt") as sp:
    swaps = csv.reader(sp, delimiter="\t")
    swaps = list(swaps)
    # removefirst lines that are comments and unnecessary labels
    for x in range(8):
        swaps.pop(0)
    # append swap domain codes
    for i in range(len(swaps)):
        swap_codes.append(swaps[i][1].lower())
        descriptions.append(swaps[i][2])
    
# use API from SIFTS to find CATH superfamily code for each PDB ID
for i in range(len(swap_codes)):
    newURL = 'https://www.ebi.ac.uk/pdbe/api/mappings/cath/' + swap_codes[i]
    r = requests.get(newURL)
    info = r.text
    y = json.loads(info)
    
    # use JSON keys to find superfamilies and append
    currentID = y[swap_codes[i]]["CATH"]
    for key in currentID.keys():
        superfamilies.append(key)
        desc.append(descriptions[i])
        swapNum.append(i+1)
        currentSwap.append(swap_codes[i])
    
    # if no superfamilies found using SIFTS
    # use CATH webpage for a PDB entry
    # beautiful soup captures superfamiles listed in table (or says none found)
    if len(currentID.keys()) == 0:
        temps = []
        toAdd = []
        newURL = 'http://www.cathdb.info/pdb/' + swap_codes[i]
        r = requests.get(newURL)
        info = r.text
        soup = BeautifulSoup(info, 'html.parser')
        # find specific table with superfamily info
        tag = soup.find_all("table", border='0', cellpadding='0', cellspacing='0', width=False)
        tag = tag[1]
        tag = tag.find("tbody")
        tag2 = tag.find_all("tr")
        tableFound = True
        # if table is not found, no superfamily
        if len(tag2) == 0:
            toAdd.append("No Superfamily Found")
            tableFound == False
        if tableFound == True:
            for r in tag2:
                entr = r.find_all("td")
                sFam = entr[2].string
                # no valid entries in table: no superfamily
                if sFam == None or sFam is None:
                    toAdd.append("No Superfamily Found")
                    break
                temps.append(sFam)
            # filter out repeats from table, then add to list
            for temp in temps:
                if temp not in toAdd:
                    toAdd.append(temp)
        # add list for this PDB entry to main lists of entry info
        for entry in toAdd:
            superfamilies.append(entry)
            desc.append(descriptions[i])
            swapNum.append(i+1)
            currentSwap.append(swap_codes[i])

# write results to file
with open('SwapFams_NEW2.csv', mode='w') as s:
    fams = csv.writer(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fams.writerow(["Swap no.","PDB ID of swap","Superfamily ID","Description"])
    for i in range(len(superfamilies)):
        fams.writerow([swapNum[i],currentSwap[i],superfamilies[i],desc[i]])

print("Done.")



# # using the uniprot file to match CATH domains with PDB ids
# 
# # data holders
# matches = []
# swap_codes_spaced = []
# num_families = []
# superfamilies = []
# descriptions = []
# swap_codes = np.empty(293, dtype=object)
# CATH_codes = np.empty(451147, dtype=object)
# 
# # open file containing uniprot info for all CATH domain codes and PDB codes
# with open("pdb_chain_cath_uniprot.tsv") as fd:
#     data = csv.reader(fd, delimiter="\t")
#     data = list(data)
#     # remove first two lines that are unnecessary labels
#     data.pop(0)
#     data.pop(0)
#     # append CATH domain codes
#     for i in range(len(data)):
#         CATH_codes[i] = data[i][3]
# # open file containing domain swapping info and PDB codes for swaps
# with open("swap.txt") as sp:
#     swaps = csv.reader(sp, delimiter="\t")
#     swaps = list(swaps)
#     # removefirst lines that are comments and unnecessary labels
#     for x in range(8):
#         swaps.pop(0)
#     # append swap domain codes
#     for i in range(len(swaps)):
#         swap_codes[i] = swaps[i][1].lower()
#         descriptions.append(swaps[i][2])
#     for codes in CATH_codes:
#         for swap_id in swap_codes:
#             if swap_id in codes:
#                 matches.append(codes)
#                 swap_codes_spaced.append(swap_id)
#     print(matches)
# 
# for i in matches:
#     newURL = 'http://www.cathdb.info/version/v4_3_0/api/rest/domain_summary/' + i
#     r = requests.get(newURL)
#     info = r.text
#     y = json.loads(info)
#     superfamilies.append(y["data"]["superfamily_id"])
# print(superfamilies)
# 
# with open('CATHswapDomains.csv', mode='w') as s:
#     cathSwaps = csv.writer(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     cathSwaps.writerow(["Entry no.","PDB ID","CATH ID","Superfamily ID"])
#     for i in range(len(matches)):
#         cathSwaps.writerow([i+1,swap_codes_spaced[i],matches[i],superfamilies[i]])
#     
# 