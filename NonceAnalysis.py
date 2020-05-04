#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#####################################################################################################################################
# This is an attempt on steganography investigation in the nonces of the bitcoin blockchain.
# Run it with python3 NonceAnalysis.py
# It checks the nonce of a block, extracting bytes (like LSByte) of nonces
# For each chunk it creates a histogram for the nonce bytes.
# After extracted, a file carving tool can be used (like scalpel) to see if there is something hidden in nonces.
# Requirements: Must have the bitcoin blocks. Must have the bitcoin-parser library from: https://github.com/alecalve/python-bitcoin-blockchain-parser

import sys
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.script import CScriptInvalidError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from blockchain_parser.blockchain import Blockchain
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd   


#histogram for each chunk bytes
def saveGraph(fileName, xlabelName, countFileChunk):
    #could choose another from here: https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
    mpl.style.use('default')
    plt.rcParams["patch.force_edgecolor"] = True
    #styling:http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
    plt.figure(figsize=(12, 9))  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    plt.xticks(fontsize=14)
    plt.yticks( fontsize=14)  

    with open(fileName, "rb") as binary_file:
    # Read the whole file at once
        data = binary_file.read()    

    graphData = bytearray(data)

    #colors 003399, 3F5D7D
    freq, bins, patches = plt.hist(graphData, 256, color="#003399")
    plt.xlabel(xlabelName, fontsize=16) #, fontsize=25

    plt.ylabel("Frequency", fontsize=16)
    #plt.grid(False)
    #plt.show()
    plt.savefig("results/"+xlabelName.strip()+"_chunk"+str(countFileChunk)+".png", bbox_inches="tight");  

    plt.close()

#histogram but for the arithmetic mean values
def saveGraphAM(fileName, xlabelName, countFileChunk):
    mpl.style.use('default')
    plt.rcParams["patch.force_edgecolor"] = True
    #styling:http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
    plt.figure(figsize=(12, 9))  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
    #plt.xticks(fontsize=14)
    plt.xticks(range(0, 250, 50), fontsize=14)
    plt.yticks( fontsize=14)
    
    with open(fileName, 'r') as file1:
        for line in file1.readlines():
            f_list = [float(i) for i in line.split(",") if i.strip()]

    #colors 003399, 3F5D7D
    freq, bins, patches = plt.hist(f_list, 256, color="#003399")
    plt.xlabel(xlabelName, fontsize=16) #, fontsize=25

    plt.ylabel("Frequency", fontsize=16)
    plt.savefig("results/"+xlabelName.strip()+"_chunk"+str(countFileChunk)+".png", bbox_inches="tight")  

    plt.close()
    os.remove(fileName) #AM file may get big.


#the API filters orphan blocks
#                                       ##CHANGE HERE TO YOUR CONFIG
blockchain = Blockchain(os.path.expanduser('~/snap/bitcoin-core/common/.bitcoin/blocks'))
bitcoinlocalpath = '/home/aagiron/snap/bitcoin-core/common/.bitcoin/blocks'

#Initial file names
LSBytesFileName = "extracted/LSBytesFromEveryNonce_FullBlockchainChunk1.data"
Bytes1FileName = "extracted/Bytes1FromEveryNonce_FullBlockchainChunk1.data"
Bytes2FileName = "extracted/Bytes2FromEveryNonce_FullBlockchainChunk1.data"
MSBytesFileName = "extracted/MSBytesFromEveryNonce_FullBlockchainChunk1.data"
AM_fileName = "extracted/AM_Chunk1.txt"

#open files
arqLSBytes = open(LSBytesFileName, 'ab')
arqBytes1 = open(Bytes1FileName, 'ab')
arqBytes2 = open(Bytes2FileName, 'ab')
arqMSBytes = open(MSBytesFileName, 'ab')
arqArithmeticMean = open(AM_fileName, 'a')

blockNumber = -1
countChunks = 1
chunkSize = 0
byte = 0

#default: data analyzed by semesters (6 months). See variable t2.
chunkDivision = 6
chunkTimestamp = "03/01/2009 00:00:00" #first chunk
lastBlockTimestamp = "03/01/2009 00:00:00"
#start of the second chunk
t2 = datetime.strptime(chunkTimestamp, "%d/%m/%Y %H:%M:%S") + relativedelta(months=+chunkDivision)


#START
for block in blockchain.get_ordered_blocks(bitcoinlocalpath + '/index', start=0):
    blockNumber = blockNumber + 1

    #work nicely on timestamps
    t1 = datetime.strptime(str(block.header.timestamp), "%Y-%m-%d %H:%M:%S")        
    
    #if block timestamp greater than chunk start, save that chunk and change the filenames for the next.
    if (t1 >= t2):
        print("Last block of the chunk(",countChunks,"):", blockNumber-1, "; Timestamp:", lastBlockTimestamp, "; Size:", chunkSize)
        
        t2 = t2 + relativedelta(months=+chunkDivision)
        print("New chunk is from:", block.header.timestamp, " to:", t2)

        #close chunk files
        arqLSBytes.close()
        arqBytes1.close()
        arqBytes2.close()
        arqMSBytes.close()
        arqArithmeticMean.close()
        
        #save graphs        
        saveGraph(LSBytesFileName, "LSByte Values", countChunks)
        saveGraph(Bytes1FileName, "Byte 1 Values", countChunks)
        saveGraph(Bytes2FileName, "Byte 2 Values", countChunks)
        saveGraph(MSBytesFileName, "MSByte Values", countChunks)
        saveGraphAM(AM_fileName, "Nonce Arithmetic Mean", countChunks)   

        countChunks = countChunks + 1
        chunkSize = 0
        #Change file names for next chunk
        LSBytesFileName = "extracted/LSBytesFromEveryNonce_FullBlockchainChunk"+str(countChunks) +".data"
        Bytes1FileName = "extracted/Bytes1FromEveryNonce_FullBlockchainChunk"+str(countChunks) +".data"
        Bytes2FileName = "extracted/Bytes2FromEveryNonce_FullBlockchainChunk"+str(countChunks) +".data"
        MSBytesFileName = "extracted/MSBytesFromEveryNonce_FullBlockchainChunk"+str(countChunks) +".data"
        AM_fileName = "extracted/AM_Chunk"+str(countChunks)+".txt"

        #open new chunks
        arqLSBytes = open(LSBytesFileName, 'ab')
        arqBytes1 = open(Bytes1FileName, 'ab')
        arqBytes2 = open(Bytes2FileName, 'ab')
        arqMSBytes = open(MSBytesFileName, 'ab')
        arqArithmeticMean = open(AM_fileName, 'a')

    #Get the Nonce from the Header
    nonce  = block.header.nonce
    
    #extranonce is not fixed; is dependent on the mining software. Skip.

    byte0 = nonce & 0xFF                #LSByte
    byte1 = (nonce >> 8) & 0xFF 
    byte2 = (nonce >> 16) & 0xFF
    byte3 = (nonce >> 24) & 0xFF        

    #A.M.
    Arithmetic_Mean = (byte0+byte1+byte2+byte3)/4.0
    arqArithmeticMean.write(str(Arithmetic_Mean) +",")
    
    LSByte = byte0.to_bytes(1, byteorder = 'little')
    MSByte = byte3.to_bytes(1, byteorder = 'little')

    arqLSBytes.write(LSByte)
    arqBytes1.write(byte1.to_bytes(1, byteorder = 'little'))
    arqBytes2.write(byte2.to_bytes(1, byteorder = 'little'))
    arqMSBytes.write(MSByte)

    lastBlockTimestamp = block.header.timestamp
    chunkSize = chunkSize + block.size


#save the remaining chunk data
#close chunk files
arqLSBytes.close()
arqBytes1.close()
arqBytes2.close()
arqMSBytes.close()
arqArithmeticMean.close()
        
#save graphs        
saveGraph(LSBytesFileName, "LSByte Values", countChunks)
saveGraph(Bytes1FileName, "Byte 1 Values", countChunks)
saveGraph(Bytes2FileName, "Byte 2 Values", countChunks)
saveGraph(MSBytesFileName, "MSByte Values", countChunks)
saveGraphAM(AM_fileName, "Nonce Arithmetic Mean", countChunks)  

#end
print("End of processing Nonces. Last chunk:", countChunks, ", Size:", chunkSize ,". Last block:", blockNumber, ", Timestamp:",lastBlockTimestamp)


