import os
import shutil
import glob
import tarfile
# =======================================================================
#run this in any directory add -v for verbose 
#get Pillow (fork of PIL) from pip before running --> pip install Pillow

import sys
from PIL import Image

def compressMe(file, verbose=False):
    filepath = "./"+den+".den/"+file
    oldsize = os.stat(filepath).st_size
    picture = Image.open(filepath)
    dim = picture.size
    
    #set quality= to the preferred quality. 
    #I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
    picture.save("./"+den+".den/C"+file,"JPEG",optimize=True,quality=85)
    
    newsize = os.stat("./"+den+".den/C"+file).st_size
    percent = round((oldsize-newsize)/float(oldsize)*100)
    if (verbose):
        print("Zmenšeno o {2}%".format(oldsize,newsize,percent))
    return percent

# =======================================================================
den = input("Jaký den?: ")
path = os.getcwd()
filenames = os.walk(path)
cislovani = 0
print("{:03d}".format(1))
try:
    os.mkdir("./"+den+".den/Compress")
except FileExistsError:
    print("Složka již existuje")
listOfFiles = filter(os.path.isfile, glob.glob("./"+den+".den/*"))
listOfFiles = sorted(listOfFiles, key=os.path.getmtime)
if os.path.exists(den+".den.tar.gz"):
    os.remove(den+".den.tar.gz")
tf = tarfile.open(den+".den.tar.gz", mode="a")
for file in listOfFiles:
    if file.endswith((".JPG", ".jpg")):
        cislovani += 1
        path = "./"+den+".den/"
        jmeno = "LT2021-D"+den+"-"+format(cislovani, '03d')+".JPG"
        if not os.path.exists(jmeno):
            os.rename(file, path+jmeno)
            print("Změna: "+file+" -> "+path+jmeno)
        else:
            print("Přeskok: "+jmeno)

        if not os.path.exists(path+"Compress/C"+jmeno):
            compressMe(jmeno, True)
            print("C"+jmeno+" -> "+path+"Compress/"+"C"+jmeno)
            shutil.move(path+"/C"+jmeno, path+"Compress/"+"C"+jmeno)

        tf.add(path+"Compress/"+"C"+jmeno, jmeno)
print("Hotovo! (Stikni ENTER pro ukončení programu)")
input()
        #newfile = file.replace(" ", "-")
        #os.rename(newfile, newfile.replace("(", ""))
        #newfile = newfile.replace("(", "")
        #os.rename(newfile, newfile.replace(")", ""))
        #newfile = newfile.replace(")", "")
        #compressMe(newfile)
        #shutil.move("C"+newfile, "./Compress/"+"C"+newfile)
