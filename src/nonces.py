import os
import setup as sp
from src.util import UtilFileManager
from src.statistics import Statistics
from blockchain_parser.blockchain import Blockchain #alle calve parser

#The objective is to analyze from a miner perspective

MIN_EXTRACTED_NONCE_DATASIZE = 40

class NonceAnalyzer(object):	
	def __init__(self,  clusterType="None", nonceList= []):
		super(NonceAnalyzer, self).__init__()
		self.clusterType = clusterType
		self.nonceList = nonceList

	#retrieve the nonces if an address is found in coinbase
	#For each block, get coinbase transaction
	#For each output in that transaction, search if one of the cluster addresses is present
	#then save the nonce
	def noncesRelatedToBlocksciAddresses(self,addresses,ctag):
		filem = UtilFileManager()
		arqName = "ClusterNoncesOutput_"+self.clusterType+"_"+ctag
		addressesIterator = data.addresses
		countFindings = 0
		blockNumber = 0
		blockchain = Blockchain(os.path.expanduser(sp.configBlockchainPath+'blocks'))
		for block in blockchain.get_ordered_blocks(os.path.expanduser(sp.configBlockchainPath+"blocks/index"), start=0):
			blockNumber = blockNumber + 1
			nonce  = block.header.nonce

			transaction = block.transactions[0]
			#Get outputs from coinbase transaction
			for output in transaction.outputs:
				#Get addresses
				for outAddr in output.addresses:

					for ad in addressesIterator.with_type(blocksci.address_type.pubkey):					
						if outAddr._address == ad.address_string:
							#save that nonce
							filem.saveInFile(arqName,nonce)
							self.append(nonce)
							countFindings = countFindings + 1
		if countFindings > 0:
			scalc = Statistics()
			scalc.printStatistics("Nonces", arqName,filem)

		return countFindings


	#same for bitiodine and etherclust csv
	def noncesRelatedToBitiodineAddresses(self,caddresses,ctag):
		filem = UtilFileManager()
		arqName = "ClusterNoncesOutput_"+self.clusterType+"_"+str(ctag)		
		countFindings = 0
		blockNumber = 0
		blockchain = Blockchain(os.path.expanduser(sp.configBlockchainPath+'blocks'))
		for block in blockchain.get_ordered_blocks(os.path.expanduser(sp.configBlockchainPath+"blocks/index"), start=0):
			blockNumber = blockNumber + 1
			nonce  = block.header.nonce

			transaction = block.transactions[0]
			#Get outputs from coinbase transaction
			for output in transaction.outputs:
				#Get addresses
				for outAddr in output.addresses:

					for strAddr in caddresses:					
						if outAddr._address == strAddr:
							#save that nonce
							filem.saveInFile(arqName,nonce)
							self.append(nonce)
							countFindings = countFindings + 1

		if countFindings > 0:
			scalc = Statistics()
			scalc.printStatistics("Nonces", arqName,filem)
		return countFindings

	#auxiliary control function: we are interested in maintaining small files? No	
	def keepExtractedData(self,fileName,data,fileUtilManager):
		if len(data) < MIN_EXTRACTED_NONCE_DATASIZE:
			fileUtilManager.deleteFile(fileName)
