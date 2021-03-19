#Configurations:

configBlockchainName = "bitcoin" #ethereum
configBlockchainPath = "~/.bitcoin/" #ethereum
configClustererName = "blocksci_all" #bitiodine_csv,etherclust
configClusterPath = "pathToClustererOutput" #in case of blocksci, it is the path+name of the config file
configAnalyzerList = ["LSB", "None"] 

#list of available clusterers (Bitcoin and Ethereum): currently for registering purposes only
availableClusterers = ["blocksci_all", "blocksci_oneCluster", "bitiodine_csv", "etherclust", "None"]
