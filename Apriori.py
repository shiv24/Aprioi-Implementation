'''
Created on Jan 29, 2019

@author: shiv
'''
import sys 
import itertools
import copy

  
def apriori_gen(llast, gcount):
    nmap = {}
    for first in llast.keys():
        for second in llast.keys():
            if first != second:
                if gcount == 1:
                    flist = [first]
                    slist = [second]
                else:
                    flist = []
                    for f in first:
                        flist.append(f)
                    flist.sort()
                    slist = []
                    for s in second:
                        slist.append(s)
                    slist.sort()
                    
                thelen = len(slist)
                cont = False
                if thelen>1:
                    for n in range(thelen - 1):
                        if flist[n] == slist[n]:
                            cont = True
                        else:
                            cont = False 
                            break
                elif thelen<=1:
                    cont= True
                if cont:
                    set1 = frozenset(flist)
                    set2 = frozenset(slist)
                    outset = (set1 | set2)
                    if has_infrequent_subset(outset, llast):
                            nmap[outset] = 0
    return nmap
                   
def has_infrequent_subset(c, lastList):
    if len(c) <= 2:
        return True
    mysets = itertools.combinations(c, len(c) - 1)
    for item in mysets:
        if frozenset(item) in lastList:
            continue 
        else:
            return False
    return True
     
def findTopConfidence(sample, klist):
    print("Confidence chart")
    print("___________________________________________")
    hold = []
    for group in klist.keys():
        mylist = []
        for i in group:
            mylist.append(i)
        mylist.sort()
        
        total = klist[group]
        denom = 0
        for l in mylist:
            newset = set()
            newleft = copy.deepcopy(mylist)
            if l == mylist[0]:
                newset = sample[mylist[-1]]
            else:
                newset = sample[mylist[0]]
            for j in mylist:
                if j != l:
                    newset= newset.intersection(sample[j])
            denom = len(newset)
            if denom != 0:
                newleft.remove(l)
                confidence = float(total)/float(denom)
                hold.append((confidence, newleft, l))
    
    sorted_by_confidence = sorted(hold, key=lambda tup: tup[0])
    for final in range(-1,-6,-1):
        display = sorted_by_confidence[final]
        print(str(display[1]) + "--->"+ str(display[2])+ " : " + str(display[0]))
        
#Use any file instead of browsing.txt with transaction list
with open('browsing.txt', 'r') as myfile:
    sample = {}
    count = 0
    for line in myfile:
        line = line.strip()
        line = line.split()
        for word in line:
            if word in sample:
                sample[word].add(count)
            else:
                sample[word] = {count}          

        count += 1        
min_sup = 100 
l1 = {}

for key in sample.keys():
    if len(sample[key]) >= min_sup:
        l1[key] = len(sample[key]) 
ln = l1
gcount = 1 


while len(ln) is not 0:
    ck = apriori_gen(ln,gcount)
    for key in ck.keys():
        for e in key:
            theval = e
            break
        newset = sample[theval]
        for item in key:
            newset = newset.intersection(sample[item])
        newlen = len(newset)
        if newlen >= min_sup:
            ck[key] = newlen
        else:
            del ck[key]
    
    if gcount <= 2:
        print("")
        print("for k= " + str(gcount+1))
        findTopConfidence(sample,ck)
        
    
    gcount += 1
    ln = ck


