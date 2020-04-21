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
# This is an attempt on steganography investigation in the LSB of hashes of the bitcoin transactions.
# Run it with python3 LSB_HashesAnalysis.py
# Juha Partala seems to be the first to propose a (secure) steganography approach for the blockchain.
# This tool extracts LSB from hashes in output transactions sequentially.
# After extracted, a file carving tool can be used (like scalpel) to see if there is something hidden.
# Requirements: Must have the bitcoin blocks. Must have the bitcoin-parser library from: https://github.com/alecalve/python-bitcoin-blockchain-parser

import sys
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.script import CScriptInvalidError
import os
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.utils import btc_ripemd160, double_sha256
import hashlib
from datetime import datetime
from dateutil.relativedelta import relativedelta



def saveInFile(fileName, byte, chunk):
    arq = open('extracted/LSBitsFrom'+ fileName +'_SHA256Addresses_'+str(chunk)+'.data', 'ab')
#def saveInFile(fileName, byte):
#    arq = open('extracted/LSBitsFrom'+ fileName +'_SHA256Addresses_.data', 'ab')
    arq.write(byte.to_bytes(1, byteorder = 'little'))
    arq.close()
    return 0

#To save OP_Return or unknown transaction bytes, if needed
def saveAllBytes(fileName, data, chunk):
    arq = open('extracted/AllBytesFrom'+ fileName +""+str(chunk)+'.data', 'ab')
#def saveAllBytes(fileName, data):
#    arq = open('extracted/AllBytesFrom'+ fileName +'.data', 'ab')
    arq.write(data)
    arq.close()
    return 0


#Function that checks the output and accordingly:
#   sets the data that is hashed: if pubkey, hash it with sha256. And so on.
#   then, sets the file that where the bits must go on/in.
def check_output_type_setHash_and_setFile(address, output):
    #Beautiful checking
    if (str(output.type) == "pubkey"):
        hashed = hashlib.sha256(address.public_key).digest()
        arqName = "pubkey"
    else:
        if (str(output.type) == "pubkeyhash"):
            #No pubkey attribute
            #from utils.py it hashes 256 and then hash160. We hash it 256 only. (instead of using hash from the address.py which is hash160)
            hashed = hashlib.sha256(output.script.operations[2]).digest()
            arqName = "pubkeyhash"
        else:
            if (str(output.type) == "p2sh"):
                #Same thing but the position is different. 
                hashed = hashlib.sha256(output.script.operations[1]).digest()
                arqName = "p2sh"
            else:
                if (str(output.type) == "multisig"):
                    #Would give a list of sub addresses. We should search it.
                    hashed = "NOT_DONE_YET"        
                    arqName = "NOT_DONE_YET"
                else:
                    if (output.script.is_return()):
                        #OP_Return.    skip because all bytes will be saved
                        hashed = "SKIP"
                        arqName = "SKIP"
                    else:                
                        if ( str(output.type) == "unknown"):
                            hashed = "SKIP"
                            arqName = "SKIP"

    return hashed,arqName
    

#copy of the previous function but returns RIPEMD-160 hash instead of SHA-256
def check_output_type_setHash160_and_setFile(address, output):
#Beautiful checking
    if (str(output.type) == "pubkey"):
        hashed = address.hash
        arqName = "pubkey"
    else:
        if (str(output.type) == "pubkeyhash"):
            hashed = address.hash
            arqName = "pubkeyhash"
        else:
            if (str(output.type) == "p2sh"):
                hashed = address.hash
                arqName = "p2sh"
            else:
                if (str(output.type) == "multisig"):
                    #Would give a list of sub addresses. We should search it.
                    hashed = "NOT_DONE_YET"        
                    arqName = "NOT_DONE_YET"
                else:
                    if (output.script.is_return()):
                        #OP_Return.    skip because all bytes will be saved
                        hashed = "SKIP"
                        arqName = "SKIP"
                    else:                
                        if ( str(output.type) == "unknown"):
                            hashed = "SKIP"
                            arqName = "SKIP"

    return hashed,arqName


##################################################################################### START

blockchain = Blockchain(os.path.expanduser('~/snap/bitcoin-core/common/.bitcoin/blocks'))

count = -1
countBitsFromBlockHash = 0
countBitsFromPK = 0
countBitsFromPKH = 0
countBitsFromP2SH = 0
countBitsForCoinbaseOutput = 0
byteBlockHash = 0
byteCoibaseOutput = 0
bytePubKey = 0
bytePubKeyHash = 0 
byteP2SHash = 0
countChunks = 1
chunkSize = 0
blockNumber = -1

#default: data analyzed by semesters (6 months, except the first, which is 7). See variable t2.
chunkDivision = 6
chunkTimestamp = "03/01/2009 00:00:00" #first chunk
lastBlockTimestamp = "03/01/2009 00:00:00"
t2 = datetime.strptime(chunkTimestamp, "%d/%m/%Y %H:%M:%S") + relativedelta(months=+chunkDivision)

#listRepeatedAddresses = [] #unused in the moment
#########################################################
#Start iterating blocks. 
#Initially it divides the whole blockchain in chunks
#First, save LSBit from block hashes, sequentially
#Then go to the addresses in transactions of each block
#The LSB of the outputs are extracted sequentially
for block in blockchain.get_ordered_blocks('/home/aagiron/snap/bitcoin-core/common/.bitcoin/blocks' + '/index', start=0):
    blockNumber = blockNumber + 1

    #Initially divide in chunks by datetime
    t1 = datetime.strptime(str(block.header.timestamp), "%Y-%m-%d %H:%M:%S")

    #if block timestamp greater than chunk start, save that chunk and change the filenames for the next.
    if (t1 >= t2):
        print("Last block of the chunk(",countChunks,"):", blockNumber-1, "; Timestamp:", lastBlockTimestamp, "; Size:", chunkSize)
        
        t2 = t2 + relativedelta(months=+chunkDivision)
        print("New chunk is from:", block.header.timestamp, " to:", t2)

        countChunks = countChunks + 1
        chunkSize = 0

	
    lastBlockTimestamp = block.header.timestamp
    chunkSize = chunkSize + block.size   

    #End of division. Go for LSBits
    #LSBit from the block hash
    LSB_blockhash = int(block.hash[31],16)  & 1

    countBitsFromBlockHash = countBitsFromBlockHash + 1
    if (LSB_blockhash == 1):
        byteBlockHash = (byteBlockHash << 1)+1
    else:
        byteBlockHash = (byteBlockHash << 1)
                  
    if (countBitsFromBlockHash == 8):
    #save this in respective file
        saveInFile("BLOCK_Hash",byteBlockHash,countChunks)
        byteBlockHash = 0
        countBitsFromBlockHash = 0
    
    countTransaction = 0
    #Retrieve transactions
    for transaction in block.transactions:

        #Get outputs
        for output in transaction.outputs:

            try:
                script_op = output.script.operations
            except CScriptInvalidError:
                saveAllBytes("InvalidCoinbaseScripts",output.script.hex,countChunks)
                #print("CSCriptInvalidError:", str(coinbase.script.hex))
                continue

            if output.script.is_return():
                #we might want it all (all bytes) to save in a file
                saveAllBytes("Coinbase_OP_ReturnBytes", output.script.hex, countChunks);
                continue
            
            if output.script.is_unknown():
                #we might want it all (all bytes) to save in a file
                saveAllBytes("Coinbase_UnknownScriptFormat", output.script.hex, countChunks);
                continue

            #Get addresses
            for address in output.addresses:
                #public key specs from here : https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses

                #two options: get SHA256 or RIPEMD-160                
                #ret = check_output_type_setHash160_and_setFile(address,output)
                ret = check_output_type_setHash_and_setFile(address,output)  
                hashed = ret[0]
                fileName = ret[1] 
                
                #multisig is not done yet
                if (fileName == "NOT_DONE_YET" or fileName == "SKIP"):
                    continue

                #get the LSBit.    
                #pos (often) of the LSB.            
                pos = 31 
                #pos2 = 19 #for RIPEMD-160
                LSB = hashed[pos] & 1

                #LSBits in the output of Coinbase transaction will be extracted separately
                #But this transaction also counts for the sequential process
                if countTransaction == 0:
                    countBitsForCoinbaseOutput = countBitsForCoinbaseOutput + 1
                    if (LSB == 1):
                        byteCoibaseOutput = (byteCoibaseOutput << 1)+1
                    else:
                        byteCoibaseOutput = (byteCoibaseOutput << 1)
                    
                    if (countBitsForCoinbaseOutput == 8):
                        #save this in respective file
                        saveInFile("CoinbaseOutput",byteCoibaseOutput,countChunks)
                        byteCoibaseOutput = 0
                        countBitsForCoinbaseOutput = 0
                
                #check where to place the LSB into
                #                                1. If it is PUBKEY (hashed 256)
                if (fileName == "pubkey"):
                    countBitsFromPK = countBitsFromPK + 1
                    if (LSB == 1):
                        bytePubKey = (bytePubKey << 1)+1
                    else:
                        bytePubKey = (bytePubKey << 1)
                    
                    if (countBitsFromPK == 8):
                        #save this in respective file
                        saveInFile(fileName,bytePubKey,countChunks)
                        bytePubKey = 0
                        countBitsFromPK = 0

                else:#                            2. If it is PUBKEYHASH
                    if (fileName == "pubkeyhash"):
                        countBitsFromPKH = countBitsFromPKH + 1
                        if (LSB == 1):                    
                            bytePubKeyHash = (bytePubKeyHash << 1)+1
                        else:
                            bytePubKeyHash = (bytePubKeyHash << 1)

                        if (countBitsFromPKH == 8):
                            #save this in respective file
                            saveInFile(fileName,bytePubKeyHash,countChunks)
                            bytePubKeyHash = 0
                            countBitsFromPKH = 0    
                    else:#                                    3. If it is PAY-TO-SCRIPT-HASH                    
                        if (fileName == "p2sh"):
                            countBitsFromP2SH = countBitsFromP2SH + 1
                            if (LSB == 1):                    
                                byteP2SHash = (byteP2SHash << 1)+1
                            else:
                                byteP2SHash = (byteP2SHash << 1)

                            if (countBitsFromP2SH == 8):
                                #save this in respective file
                                saveInFile(fileName,byteP2SHash,countChunks)
                                byteP2SHash = 0
                                countBitsFromP2SH = 0
        countTransaction = countTransaction + 1
#compute the meansss.

print("End of extracting LSBits. Last chunk:", countChunks, ", Size:", chunkSize ,". Last block:", blockNumber, ", Timestamp:",lastBlockTimestamp)
