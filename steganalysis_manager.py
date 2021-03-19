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
# Steganography investigation after clustering of bitcoin addresses.


import sys
import os
import importlib
import blocksci
import setup
from stegSelector import StegSelector
from src.util import BitiodineCSVReader
from src.util import EtherclustCSVReader



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
	pass

#load clusters
#compute list of addresses
#call the analyzer
#update to create cluster instead of open it
def processBlocksciClusters(self):

	#select cluster 
	clusterConfig = input("Inform the absolute path with the name of the " + self.clusteringName + " config file:")	
	chain = blocksci.Blockchain(clusterConfig)
	#cm = blocksci.cluster.ClusterManager(self.clusteringPath, chain)
	print("Starting the Blocksci Cluster Manager to create clusters...")
	cm = blocksci.cluster.ClusterManager.create_clustering(self.clusteringPath, chain, should_overwrite=True)
	

	#for now it is all clusters 
	if "all" in self.clusteringName:		
		clsterData = cm.clusters()
	else:									#it should not be a string I think
		clsterData = cm.cluster_with_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

	#run through available clusters
	for c in clsterData:	
		#print("Hello Cluster c:" + str(c.address_count()))
		print("\tAnalyzing Cluster(ctag=" + ctag + ":"+ str(countClusters)+" ...")
		#for each analyzer (currently only one! LSB)
		for a in getAnalyzer(self):
			a.dataType = self.clusteringName
			a.startAnalysis(c.addresses,c.index)

#load cluster CSV file
#compute list of addresses
#call the analyzer
def processEtherClusters(self):
	pass

#load blockchain
#compute list of (sequential) addresses
#call the analyzer
def processAlleCalveParser(self):
	pass

#instantiate objects for analysis: returns a list
def getAnalyzer(self):	
	analyzer = []
			#set in setup.py
	for a in configAnalyzerList:
		if self.selectorType == a:			
			desiredClass = getattr(importlib.import_module(a.lower()), a) #check case sensitive (module name vs class name)
			analyzer.append(desiredClass())
	#beware: it instantiates an objects from a string name.
	return analyzer

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
		# Do the default alle calve parsing.
		processAlleCalveParser(self)


if __name__ == "__main__":
	print("Steganography investigation in blockchain.")
									#set in setup.py
	instanceSM = steganalysisManager(configBlockchainName,configBlockchainPath,configClustererName,configClusterPath, configAnalyzer)

	#1 Open things (blockchain, cluster)
	#2 Start Analysis
	#3 Save extracted data
	loadAndStart(instanceSM)

	print("Ended.")
