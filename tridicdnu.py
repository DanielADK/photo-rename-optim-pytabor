import os
slozky = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
for name in slozky:
    dirName = "data/"+str(name)+".den"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Vytvářím: " , dirName)
