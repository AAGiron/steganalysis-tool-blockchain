import sys
import os
import importlib
from pathlib import Path

class StegSelector(object):

    def __init__(self, name="None",clusterParam="None",extractPath=".",choosenStatistics="AM,Entropy,Monobit"):
        self.name = name #Statistical, None (just extract),
        self.clusterParam = clusterParam
        self.extractPath = extractPath


    def startAnalysis(data,ctag):
        print("Overriden Method")

    def getSelectorNameList(self):
        return ["LSB", "Subliminal", "AddressCombinatorics"]

    #Returns the list of available Analyzers implemented
    #not working
    def getSelectorNameListFromDir(self):
        nameList = []
        for filepath in Path.cwd().iterdir():
            if filepath.suffix == ".py":
                nameList.append(str(filepath).replace(".py",""))
        nameList.append("None")
        return nameList


