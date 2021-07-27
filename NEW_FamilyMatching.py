import csv, requests, json
import numpy as np

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
    
    currentID = y[swap_codes[i]]["CATH"]
    for key in currentID.keys():
        superfamilies.append(key)
        desc.append(descriptions[i])
        swapNum.append(i)
        currentSwap.append(swap_codes[i])

# write results to file
with open('SwapFams_NEW.csv', mode='w') as s:
    fams = csv.writer(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fams.writerow(["Family no.","PDB ID of swap","Superfamily ID","Description"])
    for i in range(len(superfamilies)):
        fams.writerow([swapNum[i],currentSwap[i],superfamilies[i],desc[i]])
