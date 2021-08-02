#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import glob
import tarfile

from PIL import Image

def compressMe(path, file, verbose=False):
    filepath = path+file
    oldsize = os.stat(filepath).st_size
    picture = Image.open(filepath)
    picture.save(path+"Compress/C"+file,"JPEG",optimize=True,quality=85)
    
    newsize = os.stat(path+"Compress/C"+file).st_size
    percent = round((oldsize-newsize)/float(oldsize)*100)
    if verbose:
        print("Zmenšeno o {2}%".format(oldsize,newsize,percent))
    return percent

def main(den):
    cislovani = 0
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
                compressMe(path, jmeno, True)

            tf.add(path+"Compress/"+"C"+jmeno, jmeno)


input = str(input("Zadejte den, nebo dny ke zpracování. (Dny oddělujte čárkou bez mezer): \n"))
if "," in input:
    parsedInput = input.split(",")
    for den in parsedInput:
        main(den)

else:
    main(input)


print("Hotovo! (Stikni ENTER pro ukončení programu)")


