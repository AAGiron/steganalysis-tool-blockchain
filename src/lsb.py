import blocksci
from src.stegSelector import StegSelector
from src.util import UtilFileManager
from src.statistics import Statistics

MIN_EXTRACTED_DATA_SIZE = 50 #in bytes, for scalpel

#LSB Analyzer
class LSB(StegSelector):
	def __init__(self, data="None", clusterType="None",choosenStatistics="AM,Entropy,Monobit"):
		super(StegSelector, self).__init__()
		self.data = data
		self.clusterType = clusterType
		self.choosenStatistics = choosenStatistics		

	#get the LSBit
	def extractLSBfromAddress(self,address):
		#print("\t\tAddress:" + str(address))
		LSB = int(address[-1],base=16) & 1
		return LSB

	#get the LSBit (Bitidine CSV)
	def extractLSBfromBitiodineAddress(self,address):
		#print("\t\tAddress:" + str(address))
		LSB = bytearray(address.encode('utf-8'))[-1] & 1
		return LSB

	#auxiliary control function: we are interested in maintaining small files? No	
	def keepExtractedData(self,fileName,data,fileUtilManager):
		if len(data) < MIN_EXTRACTED_DATA_SIZE:
			fileUtilManager.deleteFile(fileName)			
	
	#Blocksci cluster analysis
	#reads the addresses of a cluster, saves the extracted LSB data
	def analyzeBlockSciCluster(self,data,ctag, addressType):
		filem = UtilFileManager()
		arqName = "ClusterLSBAddressOutput_"+self.clusterType+"_"+str(ctag) +addressType.name+".data"
		countBits = 0
		byteStr = ""
		byteOutput = 0
		addressesIterator = data.addresses
		for ad in addressesIterator.with_type(addressType):
			address = ad.address_string
			countBits = countBits + 1
			if (self.extractLSBfromAddress(address) == 1):
				byteOutput = (byteOutput << 1)+1
			else:
				byteOutput = (byteOutput << 1)

			if (countBits == 8):
				#save this in respective file
				filem.saveByte(arqName,byteOutput)
				byteStr = byteStr + char(byteOutput)
				byteOutput = 0
				countBits = 0
				
		
		#compute statistics
		if len(byteStr) != 0:
			scalc = Statistics()
			scalc.printStatistics("LSB Analyzer", arqName+"pubkey.data",filem,byteStr)
			self.keepExtractedData(arqName,byteStr,filem)


	#CSV (Bitiodine or Etherclust) analysis and extractor
	#reads the addresses of a cluster
	#saves the extracted LSB data
	def analyzeBitIodineOrEtherclustCluster(self,data,ctag):
		filem = UtilFileManager()
		arqName = "ClusterLSBAddressOutput_"+self.clusterType+"_"+str(ctag)
		countBits = 0
		byteStr = ""
		byteOutput = 0
		#compute data bytes
		for address in data:
			
			countBits = countBits + 1
			if (self.extractLSBfromBitiodineAddress(address) == 1):
				byteOutput = (byteOutput << 1)+1
			else:
				byteOutput = (byteOutput << 1)

			if (countBits == 8):
				#save this in respective file
				filem.saveByte(arqName,byteOutput)
				byteStr = byteStr + chr(byteOutput) #or .decode("utf-8")
				byteOutput = 0
				countBits = 0

		if len(byteStr) != 0:
			#compute statistics
			savedData = filem.openByteFile(arqName)
			scalc = Statistics()
			pvalue = scalc.monobitTest(savedData)

			print ("\t\t\'Message\':"+ byteStr)
			print ("\t\tAM:"+str(scalc.computeAM(savedData)))
			print ("\t\tEntropy:"+str(scalc.computeEntropy(savedData)))		
			if pvalue < 0.01: 
				monobitresult = 1
			else:
				monobitresult = 0
			print ("\t\tMonobit test (p-value):"+str(pvalue) + ", PASS:" + str(monobitresult))

			self.keepExtractedData(arqName,byteStr,filem)



	#no cluster: sequential Addresses
	def analyzeSequentialAddresses(self,data,ctag):
		filem = UtilFileManager()
		print("Analyzing Addresses...")
		arqName = "SequentialLSBAddressOutput_0.data"
		countBits = 0
		byteOutput = 0
		countAddresses = 0
		countChunk = 0
		#compute data bytes
		for address in data:
			countBits = countBits + 1
			if (self.extractLSBfromAddress(address) == 1):
				byteOutput = (byteOutput << 1)+1
			else:
				byteOutput = (byteOutput << 1)

			if (countBits == 8):
				#save this in respective file
				filem.saveByte(arqName,byteOutput)
				byteOutput = 0
				countBits = 0

			countAddresses = countAddresses + 1
			if countAddresses % 100000 == 0:
				#compute statistics
				savedData = filem.openByteFile(arqName)
				scalc = Statistics()
				pvalue = scalc.monobitTest(savedData)

				print ("\t\tAM:"+str(scalc.computeAM(savedData)))
				print ("\t\tEntropy:"+str(scalc.computeEntropy(savedData)))		
				if pvalue < 0.01: 
					monobitresult = 1
				else:
					monobitresult = 0
				print ("\t\tMonobit test (p-value):"+str(pvalue) + ", PASS:" + str(monobitresult))
				countChunk = countChunk + 1
				arqName = "SequentialLSBAddressOutput_"+str(countChunk)+".data"
	#Overrider: entry point
	def startAnalysis(self,data,ctag):
		if self.clusterType in 'blocksci':
			self.analyzeBlockSciCluster(data, ctag,blocksci.address_type.pubkey)
			self.analyzeBlockSciCluster(data, ctag,blocksci.address_type.pubkeyhash)
			self.analyzeBlockSciCluster(data, ctag,blocksci.address_type.scripthash)
			self.analyzeBlockSciCluster(data, ctag,blocksci.address_type.nonstandard)
		elif self.clusterType == 'bitiodine_csv' or self.clusterType == 'etherclust':
			self.analyzeBitIodineOrEtherclustCluster(data, ctag)		
		elif self.clusterType == "sequential":
			self.analyzeSequentialAddresses(data,ctag)


