# steganalysis-tool-blockchain
A repository for an attempt to perform steganalysis on the blockchain (of bitcoin), based on the nonces and in LSB of hashes.

If you want to use this for academic purposes, please check: Giron A.A., Martina J.E., Custódio R. (2020) Bitcoin Blockchain Steganographic Analysis. In: Zhou J. et al. (eds) Applied Cryptography and Network Security Workshops. ACNS 2020. Lecture Notes in Computer Science, vol 12418. Springer, Cham. https://doi.org/10.1007/978-3-030-61638-0_3 

Two experiments were performed to find evidence of the presence (or not) of steganographic messages in the blockchain (the experiments are explained with details in the paper). Both of the tools used are available here.

## Requirements
1. Bitcoin's blockchain, which can be obtained at https://bitcoin.org/en/download. 
2. The blockchain parser library (available at: https://github.com/alecalve/python-bitcoin-blockchain-parser)
3. The Blocksci parser library (for the clustering branch - under development), at https://github.com/citp/BlockSci

## How can I use it?
Change the paths in the code where you download the blockchain. Run it with: python3 Name.py

Depending on the size of the blockchain, it may take a lot of hours to execute completely.

You can change the time interval that divides the data into chunks (variable chunkTimeDivision). By default, it divides the blockchain blocks with timestamp interval between 6 months each.

Suggestions are welcome.
