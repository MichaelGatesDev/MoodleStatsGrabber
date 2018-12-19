#!/usr/bin/env python3

import os

"""
Loads delim-separated list
    Returns list where each entry is an index
"""
def loadListFromFile(fileName, delim):
    list = []
    if not fileName:
        print("Could not find file with that name! (" + fileName + ")")
        return
    with open(fileName, 'r') as myfile:
        data = myfile.read()
        spl = data.split(delim)
        for s in spl:
            list.append(s.strip())
    return list
    
""" Saves delim-separated list to a file """
def saveListToFile(fileName, list, delim, allowEmpty, dir = None):
    if not allowEmpty and len(list) == 0:
        return
    if(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
    f = open(os.path.join(dir, fileName), "w")
    for item in list:
        f.write(item + delim)
    f.close()
    print("Saved list with " + str(len(list)) + " content(s) to file (" + fileName + ")")


""" Saves delim-separated dictionary to a file """
def saveDictToFile(fileName, dict, delim, allowEmpty, dir = None):
    if not allowEmpty and len(dict) == 0:
        return
    if(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
    f = open(os.path.join(dir, fileName), "w")
    for k in dict.keys():
        v = dict[k]
        f.write(str(v) + "\t" + k + delim)
    f.close()
    print("Saved dict with " + str(len(dict)) + " content(s) to file (" + fileName + ")")


def simplifyFileName(name):
    return name.replace('/','').replace('-','').replace('_','').replace(':','')
