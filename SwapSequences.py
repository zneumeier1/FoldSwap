# Author: Zachariah Neumeier
# July 19th, 2021
# Bourne Lab at UVA
#
# This code takes a "swap.txt" file from 3DSwap here(http://caps.ncbs.res.in/3dswap/3dswap_download_list.txt)
# and compiles a list of the PDB codes from the file along with their
# matching sequence details from 3DSwap. These details include hinge regions, secondary
# major regions, swapped regions, and full sequences. Note that some pieces are missing from
# the 3DSwap database. Number of regions may vary (up to 8 per swap).


import csv, requests, json, re
import numpy as np
from bs4 import BeautifulSoup

print("Working...")

swap_codes = np.empty(293, dtype=object)

def inBounds (arr, index):
    if(index >= 0 and index < len(arr)):
        return True

with open("swap.txt") as sp:
    swaps = csv.reader(sp, delimiter="\t")
    swaps = list(swaps)
    # removefirst lines that are comments and unnecessary labels
    for x in range(8):
        swaps.pop(0)
    # append swap domain codes
    for i in range(len(swap_codes)):
        swap_codes[i] = swaps[i][1].lower()

with open('SwapSequences.csv', mode='w') as s:
    swapReg = csv.writer(s, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    swapReg.writerow(["Entry no.","PDB ID of swap","Hinge Region Chain 1","Hinge Region 1","Hinge Region Chain 2","Hinge Region 2",
                      "Hinge Region Chain 3","Hinge Region 3","Hinge Region Chain 4","Hinge Region 4","Hinge Region Chain 5","Hinge Region 5",
                      "Hinge Region Chain 6","Hinge Region 6","Hinge Region Chain 7","Hinge Region 7","Hinge Region Chain 8","Hinge Region 8",
                      "Secondary Major Chain 1","Secondary Major Region 1","Secondary Major Chain 2","Secondary Major Region 2",
                      "Secondary Major Chain 3","Secondary Major Region 3","Secondary Major Chain 4","Secondary Major Region 4",
                      "Secondary Major Chain 5","Secondary Major Region 5","Secondary Major Chain 6","Secondary Major Region 6",
                      "Secondary Major Chain 7","Secondary Major Region 7","Secondary Major Chain 8","Secondary Major Region 8",
                      "Swapped Region Chain 1","Swapped Region 1","Swapped Region Chain 2","Swapped Region 2",
                      "Swapped Region Chain 3","Swapped Region 3","Swapped Region Chain 4","Swapped Region 4","Swapped Region Chain 5",
                      "Swapped Region 5","Swapped Region Chain 6","Swapped Region 6","Swapped Region Chain 7","Swapped Region 7",
                      "Swapped Region Chain 8","Swapped Region 8","Full Sequence Chain 1","Full Sequence 1","Full Sequence Chain 2",
                      "Full Sequence 2","Full Sequence Chain 3","Full Sequence 3","Full Sequence Chain 4","Full Sequence 4",
                      "Full Sequence Chain 5","Full Sequence 5","Full Sequence Chain 6","Full Sequence 6","Full Sequence Chain 7",
                      "Full Sequence 7","Full Sequence Chain 8","Full Sequence 8"])
    
    for i in range(len(swap_codes)):
        newURL = 'http://caps.ncbs.res.in/cgi-bin/mini/databases/3Dswap/get_3ds_seq.cgi?id=' + swap_codes[i]
        r = requests.get(newURL)
        info = r.text

        soup = BeautifulSoup(info, 'html.parser')
        tag = soup.find("table", border='0', align=False, cellpadding=False, cellspacing=False, width=False)
        tag2 = tag.find_all("tr")
        
        # counter for four row table
        count = 1
        # chain and sequence holders
        hrc = []
        hr = []
        smc = []
        smr = []
        src = []
        sr = []
        fsc = []
        fs = []
        
        # loop over rows in table from webpage
        for r in tag2:
            entr = r.find_all("td")
            entr = entr[1].contents
            chains = int(len(entr) / 4)
            # loop for number of chains in that row
            for j in range(chains):
                # save as variables, remove line breaks
                chn = entr[0][6]
                aa = entr[2]
                aa = aa.replace('\n','')
                aa = aa.replace('\r','')
                # use count to determine which column info corresponds with
                if count == 1:
                    hrc.append(chn)
                    hr.append(aa)
                elif count == 2:
                    smc.append(chn)
                    smr.append(aa)
                elif count == 3:
                    src.append(chn)
                    sr.append(aa)
                elif count == 4:
                    fsc.append(chn)
                    fs.append(aa)
                # pop used data at beginning of row so next chain info at index 0
                entr.pop(0)
                entr.pop(0)
                entr.pop(0)
                entr.pop(0)
            count = count + 1
        # append blank entries just to make sure no out of bounds errors with indexing
        for x in range(8):
            hrc.append("None")
            hr.append("None")
            smc.append("None")
            smr.append("None")
            src.append("None")
            sr.append("None")
            fsc.append("None")
            fs.append("None")
        # write the row for the one 3DSwap entry (one PDB ID)
        swapReg.writerow([i+1,swap_codes[i],hrc[0],hr[0],hrc[1],hr[1],hrc[2],hr[2],hrc[3],hr[3],hrc[4],hr[4],hrc[5],hr[5],hrc[6],hr[6],hrc[7],hr[7],
                          smc[0],smr[0],smc[1],smr[1],smc[2],smr[2],smc[3],smr[3],smc[4],smr[4],smc[5],smr[5],smc[6],smr[6],smc[7],smr[7],src[0],
                          sr[0],src[1],sr[1],src[2],sr[2],src[3],sr[3],src[4],sr[4],src[5],sr[5],src[6],sr[6],src[7],sr[7],fsc[0],fs[0],fsc[1],
                          fs[1],fsc[2],fs[2],fsc[3],fs[3],fsc[4],fs[4],fsc[5],fs[5],fsc[6],fs[6],fsc[7],fs[7]])
    
print('Done.')
