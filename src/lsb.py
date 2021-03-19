from stegSelector import StegSelector
from util import UtilFileManager
from statistics import Statistics

MIN_EXTRACTED_DATA_SIZE = 50 #in bytes, for scalpel

#LSB Analyzer
class LSB(StegSelector):
	"""docstring for ClassName"""
	def __init__(self, data="None", clusterType="None",choosenStatistics="AM,Entropy,Monobit"):
		super(StegSelector, self).__init__()
		self.data = data
		self.clusterType = clusterType
		self.choosenStatistics = choosenStatistics		

	#get the LSBit
	def extractLSBfromAddress(self,address):
		LSB = address[-1] & 1
		return LSB

	#auxiliary control function: we are interested in maintaining small files? No	
	def keepExtractedData(self,fileName,data,fileUtilManager):
		if len(data) < MIN_EXTRACTED_DATA_SIZE:
			fileUtilManager.deleteFile(fileName)			
	
	#Blocksci cluster analysis
	#reads the addresses of a cluster, saves the extracted LSB data
	def analyzeBlockSciCluster(self,data,ctag):
		filem = UtilFileManager()
		arqName = "ClusterLSBAddressOutput_"+self.clusterType+"_"+ctag
		countBits = 0
		byteStr = ""
		byteOutput = 0
		addressesIterator = data.addresses
		for ad in addressesIterator.with_type(blocksci.address_type.pubkey):
			address = ad.address_string
			countBits = countBits + 1
			if (self.extractLSBfromAddress(address) == 1):
				byteOutput = (byteOutput << 1)+1
			else:
				byteOutput = (byteOutput << 1)

			if (countBits == 8):
				#save this in respective file
				filem.saveInFile(arqName,byteOutput)
				byteStr = byteStr + str(byteOutput)
				byteOutput = 0
				countBits = 0
		
		#compute statistics
		if len(byteStr) != 0:

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
	def analyzeSequentialAddresses(self):
		pass

	#Overrider: entry point
	def startAnalysis(self,data,ctag):
		if self.clusterType in 'blocksci':
			self.analyzeBlockSciCluster(data, ctag)
		else:
			self.analyzeSequentialAddresses()


