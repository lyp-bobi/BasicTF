


if __name__ == '__main__':
    #read the data
    f= open('PET.txt', 'r')
    y=[]
    line = f.readline()
    while line:
        x = line.split(' ')
        y.append(x)
        line= f.readline()
    #print(y)

    #training use Ordinary Linear Regression
    