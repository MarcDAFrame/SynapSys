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
    # for key, value in dictionary.items():
    #     dictlist.append(value)
    # return dictlist
    dictlist = list(dictionary.values())
    return dictlist