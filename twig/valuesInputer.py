temp = []
num = int(input())
for i in range(1, num+1):
    temp.append(i)

f = open('values', 'w+')
for item in temp:
    f.write("%s\n" % item)
