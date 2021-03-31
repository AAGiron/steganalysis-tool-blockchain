#Configurations:

configBlockchainName = "bitcoin" #ethereum
configBlockchainPath = "~/.bitcoin/" #ethereum
configClustererName = "blocksci_all" 
configClusterPath = "pathToClustererOutput" 
configAnalyzerList = ["LSB", "None"] 


#Examples:
#Bitiodine (clustering)
#configBlockchainName = "bitcoin"
#configBlockchainPath = "~/.bitcoin/" 
#configClustererName = "bitiodine_csv"
#configClusterPath = "/home/user/path/BitiodineOutput.csv"
#configAnalyzerList = ["LSB"] 

#Blocksci (clustering)
#configBlockchainName = "bitcoin" 
#configBlockchainPath = "~/.bitcoin/" 
#configClustererName = "blocksci_all" #bitiodine_csv,etherclust
#configClusterPath = "/home/user/path/BlocksciOutputParsePath/" #path where a file named 'blocksciConfFile' resides
#configAnalyzerList = ["LSB"]

#Ethereum-etl (sequential)
#configBlockchainName = "ethereum" 
#configBlockchainPath = "/home/user/path/" #where blocks.csv and transactions.csv reside
#configClustererName = "None" 
#configClusterPath = "unused"
#configAnalyzerList = ["LSB"] #nonces are extracted too.

#Bitcoin sequential currently runs separately

#list of available clusterers (Bitcoin and Ethereum): currently for registering purposes only
availableClusterers = ["blocksci_all", "blocksci_oneCluster", "bitiodine_csv", "etherclust", "None"]
