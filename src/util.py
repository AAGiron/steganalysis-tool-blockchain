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

	def checkTags(self,clusterTag):
		for l in self.clusterLists:
			if clusterTag == int(l[0]):
				return self.clusterLists.index(l)
		return -1

	#primary function: populates a list of lists: self.clusterLists
	#each row is a cluster, each columns are tag+address
	# L = [ [tag1, address1], [tag2, address1,address2,address3], ...  ]
	def readBitiodineCSVAllClusters(self):
		countLines = 0		
		columntypes = {0:'str',1:'str'} #no header in bitiodine
		wholeData = pd.read_csv(self.fileName, header=0, low_memory=False)
		for (_, col1, col2) in wholeData.itertuples(name=None):
			innerList = []
			countLines = countLines + 1
			if countLines % 50000 == 0:
				print("\tCluster processing status:"+str(countLines))
			clusterTag = col2 			#cluster Tag position in CSV			
			address = str(col1)
			
			indexInner = self.checkTags(clusterTag)
			if indexInner == -1:
				innerList.append(clusterTag)
				innerList.append(address)
				self.clusterLists.append(innerList)
			else:
				#put into the list of lits
				retrieveInnerList = self.clusterLists.pop(indexInner)
				retrieveInnerList.append(address)
				self.clusterLists.append(retrieveInnerList)	

class EtherclustCSVReader(object):
	def __init__(self, fileName="None", clusterLists=[]):
		super(EtherclustCSVReader, self).__init__()
		self.fileName = fileName
		self.clusterLists = clusterLists
		
	#etherclust has 3 types of clusterings: deposit, depositToken, airdrops
	#However it seems that this is applicable only to token networks (over eth)
	#CSV is user,deposit,exchange,blockDiff
	def readEtherclustCSVDepositAllClusters(self):
		#wholeData = pd.read_csv(self.fileName, header=0, low_memory=False)
		columntypes = {'user':'str','deposit':'str'}#'exchange':'str','blockDiff':'str'} 
		cols = ['user','deposit']
		
		#wholeData = pd.read_csv(self.fileName, usecols=cols, low_memory=False)
		countLines = 0
		#for row in wholeData.itertuples():
		for df_chunk in tqdm(pd.read_csv(self.fileName, usecols=cols, dtype=columntypes, chunksize=100000)):			
			innerList = []
			for i in df_chunk.index:
				clusterTag = df_chunk.at[i, 'deposit']
				address = df_chunk.at[i, 'user'] 

				#create a inner list= 	  [ClusterTag,Address]
				#or retrieve and update=  [ClusterTag,Address_1,Adress_2...]
				indexInner = self.checkTags(clusterTag)
				if indexInner == -1:
					innerList.append(clusterTag)
					innerList.append(address)
					self.clusterLists.append(innerList)
				else:
					#put into the list of lits
					retrieveInnerList = self.clusterLists.pop(indexInner)
					retrieveInnerList.append(address)
					self.clusterLists.append(retrieveInnerList)

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
		arq = open("extracted/"+fileName, 'ab')
		for b in range(len(byteData)):
			arq.write(bytes((byteData[b]),'UTF-8'));
		arq.close()

	def saveBytes(self,fileName, data):
		arq = open("extracted/"+fileName, 'ab')
		for item in data:
			try:
				arq.write(item.to_bytes(1, byteorder = 'little'))
			except (AttributeError):
				arq.write(item)
			
		arq.close()

	def saveByte(self,fileName, data):
		arq = open("extracted/"+fileName, 'ab')
		arq.write(data.to_bytes(1, byteorder = 'little'))			
		arq.close()

	#opens and returns a byte list
	def openByteFile(self,fileName):
		with open("extracted/"+fileName, "rb") as arq:
			data = bytearray(arq.read())
		return data

	def deleteFile(self,fileName):
		if os.path.exists("extracted/"+fileName):
			os.remove("extracted/"+fileName)

	#for sequential analysis: reads columns from file
	def sequentialCSVReader(self,fileName,listCols):			
		#for df_chunk in tqdm(pd.read_csv(self.fileName, usecols=cols, dtype=columntypes, chunksize=chunksize)):		
		countLines = 0
		wholeData = pd.read_csv(fileName, dtype=str, low_memory=False)
		countLines = 0
		retdata = []
		for index,row in wholeData.iterrows():

			countLines = countLines + 1
			if countLines % 100000 == 0:
				print(fileName +" loading status:"+str(countLines))
			
			#mostly it is only one column
			for i in listCols:
				if str(row[i]).startswith('nan'): #empty outputs
					continue
				retdata.append(str(row[i]))

		return retdata


