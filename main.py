#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import glob
import tarfile
import threading
import progressbar

from PIL import Image

THREADS = 12


def compressImage(path, file, verbose=False):
    filepath = path + file
    oldsize = os.stat(filepath).st_size
    picture = Image.open(filepath)
    picture.save(path + "Compress/C" + file, "JPEG", optimize=True, quality=85)

    newsize = os.stat(path + "Compress/C" + file).st_size
    percent = round((oldsize - newsize) / float(oldsize) * 100)
    avgList.append(percent)
    if verbose:
        print("Zmenšeno o {2}%".format(oldsize, newsize, percent))
    return percent


def process(den):
    while len(listOfFiles) != 0:
        file = listOfFiles.pop(0)
        cislovani = totalLenOfListOfFiles-len(listOfFiles)-1
        if file.endswith((".JPG", ".jpg")):
            cislovani += 1
            path = "./data/" + den + ".den/"
            jmeno = "LT2021-D" + den + "-" + format(cislovani, '03d') + ".JPG"
            if not os.path.exists(jmeno):
                os.rename(file, path + jmeno)
                # print("Změna: "+file+" -> "+path+jmeno)
            # else:
            # print("Přeskok: "+jmeno)

            if not os.path.exists(path + "Compress/C" + jmeno):
                compressImage(path, jmeno)
        bar.update(totalLenOfListOfFiles - len(listOfFiles))


def tar(den):
    path = "./data/" + day + ".den"
    with tarfile.open(path + ".tar.gz", mode="a") as tar:
        it = 0
        for file in filter(os.path.isfile, glob.glob("./data/" + day + ".den/Compress/*")):
            it = it+1
            tar.add(file, arcname=os.path.basename(path + "/Compress/" + file))
            bar.update(it)


def progressBarPrep(event, top):
    widgets = [event + ": ", progressbar.Bar('█', '|', '|', '░'), progressbar.Percentage()]
    bar = progressbar.ProgressBar(maxval=top, widgets=widgets)
    return bar


input = str(input("Zadejte den, nebo dny ke zpracování. (Dny oddělujte čárkou bez mezer): \n"))
days = []
if "," in input:
    days = input.split(",")
else:
    days.append(input)

for day in days:
    threads = []

    try:
        os.makedirs("./data/" + day + ".den/Compress")
    except FileExistsError:
        print("Složka již existuje")
    listOfFiles = filter(os.path.isfile, glob.glob("./data/" + day + ".den/*"))
    listOfFiles = sorted(listOfFiles, key=os.path.getmtime)
    totalLenOfListOfFiles = len(listOfFiles)
    if os.path.exists("./data/" + day + ".den.tar.gz"):
        os.remove("./data/" + day + ".den.tar.gz")
    avgList = list()

    # Progress bar
    bar = progressBarPrep("Komprese", totalLenOfListOfFiles)
    bar.start()
    barlen = 0

    for i in range(THREADS):
        t = threading.Thread(target=process, args=(day,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    bar.finish()
    
    # Print avg spave-save-percentage
    if len(avgList) > 0:
        print("Ušetřeno průměrně: {0}%".format(sum(avgList)/len(avgList)))
    else:
        print("Více už ušetřit nelze..")

    # Archiving
    bar = progressBarPrep("Archivace", totalLenOfListOfFiles)
    bar.start()
    barlen = 0
    tar(day)
    bar.finish()

print("Hotovo! (Stikni ENTER pro ukončení programu)")
