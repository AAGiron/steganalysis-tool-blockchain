#compute statistics from files
import math 
import numpy as np


class Statistics(object):
	def __init__(self, arg):
		super(Statistics, self).__init__()
		self.arg = arg

	def dataToBitstring(self,data):
		binstring = ""
		for x in data:
			bytestring = "{0:b}".format(x, 'b')
			#concat
			binstring = binstring + bytestring
		return binstring


	def computeAM(self,data):
		count = 0
		AMSum = 0
		for b in data:
			AMSum = AMSum + b
			count = count + 1
		AM = AMSum / count
		return AM

	def computeEntropy(self,data):
		frequencies, _ = np.histogram(data,  bins=np.arange(256+1))
		soma = np.sum(frequencies) 
		ratio = frequencies / soma

		positiveFrequencies = ratio[ratio > 0]
		entropy = np.abs(positiveFrequencies * np.log2(positiveFrequencies))
		totalEntropy = np.sum(entropy)

		return totalEntropy


	def monobitTest(self,data):
		#convert data first
		bitstring = Statistics().dataToBitstring(data)

		count = 0
		for c in bitstring:
			if c == '1':
				count = count+1
			else:				
				count = count-1
		#p value
		test = abs(count) / math.sqrt(len(bitstring))
		pvalue = math.erfc(test / math.sqrt(2))
		return pvalue
	
	def printStatistics(self,analysis, arqName,filem,byteStr="None"):
		savedData = filem.openByteFile(arqName)
		pvalue = self.monobitTest(savedData)

		print ("\t\t---- "+ analysis + " ----")
		if byteStr != "None":
			print ("\t\t\'Message\':"+ byteStr)
		print ("\t\tAM:"+str(self.computeAM(savedData)))
		print ("\t\tEntropy:"+str(self.computeEntropy(savedData)))		
		if pvalue < 0.01: 
			monobitresult = 1
		else:
			monobitresult = 0
		print ("\t\tMonobit test (p-value):"+str(pvalue) + ", PASS:" + str(monobitresult))
