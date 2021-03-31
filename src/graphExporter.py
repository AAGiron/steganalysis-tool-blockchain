# graph class
import sys
import os
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd   


#histogram for each chunk bytes
def saveGraph(fileName, xlabelName, countFileChunk):
    mpl.style.use('default')
    plt.rcParams["patch.force_edgecolor"] = True
    plt.figure(figsize=(12, 9))  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    plt.xticks(fontsize=14)
    plt.yticks( fontsize=14)  

    with open("extracted/"+fileName, "rb") as binary_file:
    # Read the whole file at once
        data = binary_file.read()    

    graphData = bytearray(data)

    #colors 003399, 3F5D7D
    freq, bins, patches = plt.hist(graphData, 256, color="#003399")
    plt.xlabel(xlabelName, fontsize=16) #, fontsize=25
    plt.ylabel("Frequency", fontsize=16)
    plt.savefig("results/"+xlabelName.strip()+"_chunk"+str(countFileChunk)+".png", bbox_inches="tight");  
    plt.close()

#histogram but for the arithmetic mean values
def saveGraphAM(fileName, xlabelName, countFileChunk):
    mpl.style.use('default')
    plt.rcParams["patch.force_edgecolor"] = True
    plt.figure(figsize=(12, 9))  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    plt.xticks(range(0, 250, 50), fontsize=14)
    plt.yticks( fontsize=14)
    
    #compute AMs
    AMList = []
    with open("extracted/"+fileName, "rb") as binary_file:
        sumup = 0
        countByte = 0
        byte = binary_file.read(1)
        while byte:
            sumup = sumup + int.from_bytes(byte, "little")
            countByte = countByte + 1
            if countByte == 8: #nonce size
                AMList.append(sumup/8.0)
                sumup = 0
                countByte = 0
            byte = binary_file.read(1)

    #colors 003399, 3F5D7D
    freq, bins, patches = plt.hist(AMList, 256, color="#003399")
    plt.xlabel(xlabelName, fontsize=16) #, fontsize=25
    plt.ylabel("Frequency", fontsize=16)
    plt.savefig("results/"+fileName+"_AM_chunk"+str(countFileChunk)+".png", bbox_inches="tight")  
    plt.close()
#   os.remove(fileName) #AM file may get big.
