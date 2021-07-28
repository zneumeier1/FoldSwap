# Author: Zachariah Neumeier
# July 27th, 2021
# Bourne Lab at UVA
#
# This code takes a "SwapSequences.csv" file from the repo (created with SwapSequences.py)
# and creates another file that displays the location in the full sequence where each data
# piece (hinge region, swapped region, secondary major region) is located, or returns -1
# meaning that the given data piece is not found in the full sequence


import csv
import numpy as np

print("Working...")

# ID and sequence holders
swapID = np.empty(293, dtype=object)
hr = np.empty(shape=(8,293), dtype=object)
smr = np.empty(shape=(8,293), dtype=object)
sr = np.empty(shape=(8,293), dtype=object)
fs = np.empty(shape=(8,293), dtype=object)
# chain holders
hrc = np.empty(shape=(8,293), dtype=object)
smc = np.empty(shape=(8,293), dtype=object)
src = np.empty(shape=(8,293), dtype=object)
fsc = np.empty(shape=(8,293), dtype=object)

def inBounds (arr, index):
    if(index >= 0 and index < len(arr)):
        return True

with open("SwapSequences.csv") as ss:
    seq = csv.reader(ss)
    seq = list(seq)
    # remove first line that contains labels
    seq.pop(0)
    # append sequence information
    for i in range(293):
        swapID[i] = (seq[i][1])
        # for loop to get all 8 pieces of info for each label
        for k in range(0,16,2):
            ind = int(k/2)
            # sequence info
            hr[ind][i] = (seq[i][k+3])
            smr[ind][i] = (seq[i][k+19])
            sr[ind][i] = (seq[i][k+35])
            fs[ind][i] = (seq[i][k+51])
            # chain info
            hrc[ind][i] = (seq[i][k+2])
            smc[ind][i] = (seq[i][k+18])
            src[ind][i] = (seq[i][k+34])
            fsc[ind][i] = (seq[i][k+50])

with open('HingeLocations.csv', mode='w') as s:
    hingeL = csv.writer(s, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    hingeL.writerow(["Entry no.","PDB ID of swap","Hinge Region","Index in full seq. 1","Index in full seq. 2",
                     "Index in full seq. 3","Index in full seq. 4","Index in full seq. 5","Index in full seq. 6",
                     "Index in full seq. 7","Index in full seq. 8"])
    for i in range(293):
        for k in range(8):
            if hr[k][i] != '' and hr[k][i] != "None":
                if hr[k][i] != hr[k-1][i]:
                    hinI = []
                    for j in range(8):
                        if fs[j][i] != "None" and fs[j][i] != '':
                            index = fs[j][i].find(hr[k][i])
                            if index == -1:
                                hinI.append("Not found")
                            else:
                                hinI.append(index)
                        else:
                            hinI.append("None")
                    hingeL.writerow([i,swapID[i],hr[k][i],hinI[0],hinI[1],hinI[2],hinI[3],hinI[4],hinI[5],hinI[6],hinI[7]])

with open('SwappedRegionLocations.csv', mode='w') as s:
    swapL = csv.writer(s, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    swapL.writerow(["Entry no.","PDB ID of swap","Swapped Region","Index in full seq. 1","Index in full seq. 2",
                     "Index in full seq. 3","Index in full seq. 4","Index in full seq. 5","Index in full seq. 6",
                     "Index in full seq. 7","Index in full seq. 8"])
    for i in range(293):
        for k in range(8):
            if sr[k][i] != '' and sr[k][i] != "None":
                if sr[k][i] != sr[k-1][i]:
                    srI = []
                    for j in range(8):
                        if fs[j][i] != "None" and fs[j][i] != '':
                            index = fs[j][i].find(sr[k][i])
                            if index == -1:
                                srI.append("Not found")
                            else:
                                srI.append(index)
                        else:
                            srI.append("None")
                    swapL.writerow([i,swapID[i],sr[k][i],srI[0],srI[1],srI[2],srI[3],srI[4],srI[5],srI[6],srI[7]])


# with open('SwapSequences.csv', mode='w') as s:
#     swapReg = csv.writer(s, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#     swapReg.writerow(["Entry no.","PDB ID of swap","Hinge Region Chain 1","Hinge Region 1","Hinge Region Chain 2","Hinge Region 2",
#                       "Hinge Region Chain 3","Hinge Region 3","Hinge Region Chain 4","Hinge Region 4","Hinge Region Chain 5","Hinge Region 5",
#                       "Hinge Region Chain 6","Hinge Region 6","Hinge Region Chain 7","Hinge Region 7","Hinge Region Chain 8","Hinge Region 8",
#                       "Secondary Major Chain 1","Secondary Major Region 1","Secondary Major Chain 2","Secondary Major Region 2",
#                       "Secondary Major Chain 3","Secondary Major Region 3","Secondary Major Chain 4","Secondary Major Region 4",
#                       "Secondary Major Chain 5","Secondary Major Region 5","Secondary Major Chain 6","Secondary Major Region 6",
#                       "Secondary Major Chain 7","Secondary Major Region 7","Secondary Major Chain 8","Secondary Major Region 8",
#                       "Swapped Region Chain 1","Swapped Region 1","Swapped Region Chain 2","Swapped Region 2",
#                       "Swapped Region Chain 3","Swapped Region 3","Swapped Region Chain 4","Swapped Region 4","Swapped Region Chain 5",
#                       "Swapped Region 5","Swapped Region Chain 6","Swapped Region 6","Swapped Region Chain 7","Swapped Region 7",
#                       "Swapped Region Chain 8","Swapped Region 8","Full Sequence Chain 1","Full Sequence 1","Full Sequence Chain 2",
#                       "Full Sequence 2","Full Sequence Chain 3","Full Sequence 3","Full Sequence Chain 4","Full Sequence 4",
#                       "Full Sequence Chain 5","Full Sequence 5","Full Sequence Chain 6","Full Sequence 6","Full Sequence Chain 7",
#                       "Full Sequence 7","Full Sequence Chain 8","Full Sequence 8"])
#     
#     for i in range(len(swap_codes)):
#         newURL = 'http://caps.ncbs.res.in/cgi-bin/mini/databases/3Dswap/get_3ds_seq.cgi?id=' + swap_codes[i]
#         r = requests.get(newURL)
#         info = r.text
# 
#         soup = BeautifulSoup(info, 'html.parser')
#         tag = soup.find("table", border='0', align=False, cellpadding=False, cellspacing=False, width=False)
#         tag2 = tag.find_all("tr")
#         
#         # counter for four row table
#         count = 1
#         # chain and sequence holders
#         hrc = []
#         hr = []
#         smc = []
#         smr = []
#         src = []
#         sr = []
#         fsc = []
#         fs = []
#         
#         # loop over rows in table from webpage
#         for r in tag2:
#             entr = r.find_all("td")
#             entr = entr[1].contents
#             chains = int(len(entr) / 4)
#             # loop for number of chains in that row
#             for j in range(chains):
#                 # save as variables, remove line breaks
#                 chn = entr[0][6]
#                 aa = entr[2]
#                 aa = aa.replace('\n','')
#                 aa = aa.replace('\r','')
#                 # use count to determine which column info corresponds with
#                 if count == 1:
#                     hrc.append(chn)
#                     hr.append(aa)
#                 elif count == 2:
#                     smc.append(chn)
#                     smr.append(aa)
#                 elif count == 3:
#                     src.append(chn)
#                     sr.append(aa)
#                 elif count == 4:
#                     fsc.append(chn)
#                     fs.append(aa)
#                 # pop used data at beginning of row so next chain info at index 0
#                 entr.pop(0)
#                 entr.pop(0)
#                 entr.pop(0)
#                 entr.pop(0)
#             count = count + 1
#         # append blank entries just to make sure no out of bounds errors with indexing
#         for x in range(8):
#             hrc.append("None")
#             hr.append("None")
#             smc.append("None")
#             smr.append("None")
#             src.append("None")
#             sr.append("None")
#             fsc.append("None")
#             fs.append("None")
#         # write the row for the one 3DSwap entry (one PDB ID)
#         swapReg.writerow([i+1,swap_codes[i],hrc[0],hr[0],hrc[1],hr[1],hrc[2],hr[2],hrc[3],hr[3],hrc[4],hr[4],hrc[5],hr[5],hrc[6],hr[6],hrc[7],hr[7],
#                           smc[0],smr[0],smc[1],smr[1],smc[2],smr[2],smc[3],smr[3],smc[4],smr[4],smc[5],smr[5],smc[6],smr[6],smc[7],smr[7],src[0],
#                           sr[0],src[1],sr[1],src[2],sr[2],src[3],sr[3],src[4],sr[4],src[5],sr[5],src[6],sr[6],src[7],sr[7],fsc[0],fs[0],fsc[1],
#                           fs[1],fsc[2],fs[2],fsc[3],fs[3],fsc[4],fs[4],fsc[5],fs[5],fsc[6],fs[6],fsc[7],fs[7]])
#
print('Done.')
