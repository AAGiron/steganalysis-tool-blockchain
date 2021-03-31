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

####################################################################################################################################
import sys
import os
import importlib
import blocksci
import setup as sp
import src.graphExporter as ge
from src.stegSelector import StegSelector
from src.util import BitiodineCSVReader
from src.util import EtherclustCSVReader,UtilFileManager
from src.nonces import NonceAnalyzer
from src.lsb import LSB


#Class Manager: coordinate the analysis 
class steganalysisManager:
	"""docstring for ClassName"""
	def __init__(self,blockchainName, blockchainPath, clusteringName,clusteringPath,selectorType):
		#super(ClassName, self).__init__()
		self.blockchainName = blockchainName
		self.blockchainPath = blockchainPath
		self.clusteringName = clusteringName	
		self.clusteringPath = clusteringPath
		self.selectorType = selectorType


#load clusters
#compute list of addresses
#call the analyzer
def processBitiodineClusters(self):
	print("Loading Bitiodine clusters...")
	#no need to open the chain, but only returns a list of tags for later loading
	bitidioneUtilObject = BitiodineCSVReader(self.clusteringPath)
		
	#cluster Data in this case is actually a list of cluster tags in this object.
	bitidioneUtilObject.readBitiodineCSVAllClusters()

	countClusters = 0
	#for each cluster tag:	
	for clsWithAddr in bitidioneUtilObject.clusterLists:
		countClusters = countClusters +1

		#retrieve the tag
		ctag = clsWithAddr.pop(0)
	
		print("\tAnalyzing Cluster(ctag=" + str(ctag) + ":"+ str(countClusters)+" ...")
		#for each analyzer (currently only one: LSB)
		a = LSB("None", self.clusteringName)
		a.startAnalysis(clsWithAddr,ctag)

#load clusters
#compute list of addresses
#call the analyzer
#update to create cluster instead of open it
def processBlocksciClusters(self):

	#select cluster 
	chain = blocksci.Blockchain(self.clusteringPath+"blocksciConfFile")
	
	print("Starting the Blocksci Cluster Manager to create clusters...")
	cm = blocksci.cluster.ClusterManager.create_clustering(self.clusteringPath, chain, should_overwrite=True)	

	#for now it is all clusters 
	clsterData = cm.clusters()

	#run through available clusters
	for c in clsterData:	
		
		print("\tAnalyzing Cluster(ctag=" + c.index + ":"+ str(countAddr)+" ...")		
		countAddr = c.address_count()

		#for each analyzer (currently only LSB)
		a = LSB("None", self.clusteringName)
		a.startAnalysis(c.addresses,c.index)


#load cluster CSV file
#compute list of addresses
#call the analyzer
def processEtherClusters(self):
	etherDepositCluster = EtherclustCSVReader(self.clusteringPath)
		
	#cluster Data in this case is actually a list of cluster tags in this object.
	print("Start loading etherclust clusters...")
	etherDepositCluster.readEtherclustCSVDepositAllClusters()
	#for each cluster tag:	
	countClusters = 0
	for clusterAddresses in etherDepositCluster.clusterLists:
		countClusters = countClusters +1
			
		#retrieve the tag
		ctag = clsWithAddr.pop(0)
	
		print("\tAnalyzing Cluster(ctag=" + ctag + "):"+ str(countClusters)+" ...")
		#for each analyzer (currently only LSB)
		a = LSB("None", self.clusteringName)
		a.startAnalysis(clusterAddresses,ctag)

#load blockchain
#compute list of (sequential) addresses
#call the analyzer
def processBlockchainSequentially(self):
	
	if self.blockchainName == "bitcoin":
		pass	#for now, implemented separately in the sequential analysis folder. 
	elif self.blockchainName == "ethereum":
		filem = UtilFileManager()
		listCols = ['nonce']
		blocksCSV = self.blockchainPath + "blocks.csv"	
		#get nonces first
		blocksdata = filem.sequentialCSVReader(blocksCSV,listCols)
		blocksdata = []
		listLSByte = []
		listMSByte = []
		listNonces = []
		countChunks = 0
		countNonces = 0
		for nonce in blocksdata:
			countNonces = countNonces + 1			
			listLSByte.append(bytes.fromhex(nonce[2:])[0])
			listMSByte.append(bytes.fromhex(nonce[2:])[-1])
			listNonces.append(bytes.fromhex(nonce[2:]))
			
			if (countNonces % 100000 == 0):
				print("Writing chunk " + str(countChunks) + " of nonces...")
				NoncesLSBArqName = self.blockchainName + "_LSBytenonces"+"_"+str(countChunks)+".data"
				NoncesMSBArqName = self.blockchainName + "_MSBytenonces"+"_"+str(countChunks)+".data"
				NoncesArqName = self.blockchainName + "_nonces"+"_"+str(countChunks)+".data"
				filem.saveBytes(NoncesLSBArqName,listLSByte)
				filem.saveBytes(NoncesMSBArqName,listMSByte)
				filem.saveBytes(NoncesArqName,listNonces)

				#graph exporting
				ge.saveGraphAM(NoncesArqName,"Nonce Arithmetic Mean", countChunks)
				ge.saveGraph(NoncesLSBArqName,"LSByte Values",countChunks)
				ge.saveGraph(NoncesMSBArqName,"MSByte Values",countChunks)
				countChunks = countChunks + 1				

		#get transactions
		listCols = ['to_address']
		transactionsCSV = self.blockchainPath + "transactions.csv"	
		
		addressData = UtilFileManager().sequentialCSVReader(transactionsCSV,listCols)
		
		#start extraction
		a = LSB("None", "sequential")
		a.startAnalysis(addressData,"N/A")


#1.
#open blockchain for parsing
#but it can return a cluster manager (which also opens a blockchain)
def loadAndStart(self):

	if "blocksci" in self.clusteringName:
		processBlocksciClusters(self)
	elif self.clusteringName == 'bitiodine_csv':
		processBitiodineClusters(self)
	elif self.clusteringName == 'etherclust':
		processEtherClusters(self)
	else:
		# Do the default alle calve/ethereum-etl parsing.
		processBlockchainSequentially(self)


if __name__ == "__main__":
	print("Steganography investigation in blockchain.")
									#set in setup.py
	instanceSM = steganalysisManager(configBlockchainName,configBlockchainPath,configClustererName,configClusterPath, configAnalyzer)

	#1 Open things (blockchain, cluster)
	#2 Start Analysis
	#3 Save extracted data
	loadAndStart(instanceSM)

	print("Ended.")
