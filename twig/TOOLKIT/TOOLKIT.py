def getValues():
    #this will get values from the twig
    print('GetValues')

    return [55, 67, 102] #returns a list of values when sent

def valueSpliter(list, numComputers):
    temp = []
    for k in range(numComputers):
        temp.append([])
    for i,j in enumerate(list):
        #temp[].append(i)
        #print(i%6, j)
        temp[i%numComputers].append(j)
        #print(j)
    return temp


def dictToList(dictionary):
    dictlist = list(dictionary.values())
    return dictlist


def intValueQueuer(seq, num):#THIS ONE DOES IT IN SIZE OF SECTION
    out = {}
    last = 0
    loops = int(len(seq) / num+1)
    counter = 0
    while last < len(seq):
        counter+=1
        out[str(counter)+'/'+str(loops)] = (seq[int(last):int(last + num)])
        last += num

    return out