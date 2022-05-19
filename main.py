#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import glob
import tarfile
import threading

from PIL import Image

THREADS = 16

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

def process(den):

    while len(listOfFiles) != 0:
        file = listOfFiles.pop(0)
        cislovani = totalLenOfListOfFiles-len(listOfFiles)-1
        if file.endswith((".JPG", ".jpg")):
            cislovani += 1
            path = "./data/"+den+".den/"
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
days = []
if "," in input:
    days = input.split(",")
else:
    days.append(input)

for day in days:
    threads = []

    try:
        os.makedirs("./data/"+ day +".den/Compress")
    except FileExistsError:
        print("Složka již existuje")
    listOfFiles = filter(os.path.isfile, glob.glob("./data/"+ day +".den/*"))
    listOfFiles = sorted(listOfFiles, key=os.path.getmtime)
    totalLenOfListOfFiles = len(listOfFiles)
    if os.path.exists("./data/"+ day +".den.tar.gz"):
        os.remove("./data/"+ day +".den.tar.gz")
    tf = tarfile.open("./data/"+ day +".den.tar.gz", mode="a")

    for i in range(THREADS):
        t = threading.Thread(target=process, args=(day,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


print("Hotovo! (Stikni ENTER pro ukončení programu)")


