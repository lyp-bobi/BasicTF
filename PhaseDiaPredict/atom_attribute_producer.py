import os

list = os.listdir("./LookupData")

#print(list)

atom = [[]]
for i in range(112):
    atom.append([])

for i in range(0,len(list)):
    path=os.path.join("./LookupData",list[i])
    if(os.path.isfile(path)) and (list[i].find(".table"))>0:
        file = open(path)
        line = file.readline()  # 调用文件的 readline()方法
        j=0
        while line:
            line = line.strip()
            atom[j].append(line)
            line = file.readline()
        file.close()
