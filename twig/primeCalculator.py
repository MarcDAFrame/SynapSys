import time

def a(values):#TEST 1
	temp = []
	for j in values:
		temp.append(all(int(j) % i for i in range(2, int(j))))
	return temp

content = []

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

with open('values') as f:
	content = f.readlines()
for i in range(len(content)):
	content[i] = content[i].rstrip('\n')

#content = valueSpliter(content, 3)

times = []
for i in range(3):
	start = time.time()
	#print()
	temp = a(content)
	times.append(str(time.time() - start))
for j in times:
	print(j)
