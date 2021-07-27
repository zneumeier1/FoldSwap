import csv, requests, json
import numpy as np

matches = []
swap_codes_spaced = []
num_families = []
superfamilies = []
descriptions = []
swap_codes = np.empty(293, dtype=object)
CATH_codes = np.empty(451147, dtype=object)

# open file containing uniprot info for all CATH domain codes and PDB codes
with open("pdb_chain_cath_uniprot.tsv") as fd:
    data = csv.reader(fd, delimiter="\t")
    data = list(data)
    # remove first two lines that are unnecessary labels
    data.pop(0)
    data.pop(0)
    # append CATH domain codes
    for i in range(len(data)):
        CATH_codes[i] = data[i][3]
# open file containing domain swapping info and PDB codes for swaps
with open("swap.txt") as sp:
    swaps = csv.reader(sp, delimiter="\t")
    swaps = list(swaps)
    # removefirst lines that are comments and unnecessary labels
    for x in range(8):
        swaps.pop(0)
    # append swap domain codes
    for i in range(len(swaps)):
        swap_codes[i] = swaps[i][1].lower()
        descriptions.append(swaps[i][2])
    for codes in CATH_codes:
        for swap_id in swap_codes:
            if swap_id in codes:
                matches.append(codes)
                swap_codes_spaced.append(swap_id)
    print(matches)

for i in matches:
    newURL = 'http://www.cathdb.info/version/v4_3_0/api/rest/domain_summary/' + i
    r = requests.get(newURL)
    info = r.text
    y = json.loads(info)
    superfamilies.append(y["data"]["superfamily_id"])
print(superfamilies)

with open('CATHswapDomains.csv', mode='w') as s:
    cathSwaps = csv.writer(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cathSwaps.writerow(["Entry no.","PDB ID","CATH ID","Superfamily ID"])
    for i in range(len(matches)):
        cathSwaps.writerow([i+1,swap_codes_spaced[i],matches[i],superfamilies[i]])
    
