# steganalysis-tool-blockchain
A repository for an attempt to perform steganalysis on the blockchain, based on the nonces and in LSB of hashes.

If you want to cite this for academic purposes, please standby until June, 2020 (hopefully!). "Giron, A. A., Martina, J. E., Custódio, R. F.: Bitcoin Blockchain Steganographic Analysis, 2020."

Two experiments were performed to find evidence of the presence (or not) of steganographic messages in the blockchain (the experiments are explained with details in the paper). Both of the tools used are available here.

#Requirements
1. Bitcoin's blockchain, which can be obtained at https://bitcoin.org/en/download. 
2. The blockchain parser library (available at: https://github.com/alecalve/python-bitcoin-blockchain-parser)

# How can I use it?
Change the paths in the code where you download the blockchain. Run it with: python3 Name.py

Depending on the size of the blockchain, it may take a lot of hours to execute completely.

You can change the time interval that divides the data into chunks (variable chunkTimeDivision). By default, it divides the blockchain blocks with timestamp interval between 6 months each.

Suggestions are welcome!
