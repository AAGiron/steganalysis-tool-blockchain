import csv
import os
import pandas as pd 
from tqdm import tqdm

#util classes: BitiodineCSVReader, EtherclustCSVReader, UtilFileManager

class BitiodineCSVReader(object):
	def __init__(self, fileName="None", clusterLists=[]):
		super(BitiodineCSVReader, self).__init__()
		self.fileName = fileName
		self.clusterLists = clusterLists

	#primary function: populates a list of lists: self.clusterLists
	def readBitiodineCSVAllClusters(self):
		pass	

class EtherclustCSVReader(object):
	def __init__(self, fileName="None", clusterLists=[]):
		super(EtherclustCSVReader, self).__init__()
		self.fileName = fileName
		self.clusterLists = clusterLists
		
	#etherclust has 3 types of clusterings: deposit, depositToken, airdrops
	#CSV is user,deposit,exchange,blockDiff
	def readEtherclustCSVDepositAllClusters(self):
		pass

	#could be implemented although the paper said that 
	#the most efficient one is the deposit heuristic
	def readEtherclustCSVTokenAllClusters(self):
		pass

	def readEtherclustCSVAirdropAllClusters(self):
		pass

#for handling extracted data
class UtilFileManager(object):
	"""docstring for FileManager"""
	def __init__(self):
		super(UtilFileManager, self).__init__()

	def saveInFile(self,fileName, byteData):
		arq = open(fileName, 'wb')
		for b in range(len(byteData)):
			arq.write(bytes((byteData[b]),'UTF-8'));
			arq.close()

	#opens and returns a byte list
	def openByteFile(fileName):
		with open(fileName, "rb") as arq:
			data = bytearray(arq.read())
		return data

	def deleteFile(fileName):
		if os.path.exists(fileName):
			os.remove(fileName)


