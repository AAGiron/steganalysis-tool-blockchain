# steganalysis-tool-blockchain
A repository for an attempt to perform steganalysis on the blockchain (of bitcoin), based on the nonces and in LSB of hashes.

If you want to use this for academic purposes, please check: Giron A.A., Martina J.E., Custódio R. (2020) Bitcoin Blockchain Steganographic Analysis. In: Zhou J. et al. (eds) Applied Cryptography and Network Security Workshops. ACNS 2020. Lecture Notes in Computer Science, vol 12418. Springer, Cham. https://doi.org/10.1007/978-3-030-61638-0_3 

Two experiments were performed to find evidence of the presence (or not) of steganographic messages in the blockchain (the experiments are explained with details in the paper). Both of the tools used are available here.

## Requirements

Depending on the configuration specified in `setup.py`, you'll need:
1. The blockchain data (of ethereum or bitcoin), or
2. The clustering output data (possibly, with the clusterer API installed);

Currently suported clusters: Blocksci API (Bitiodine and Etherclust are planned).

For sequential analysis, a blockchain parser library is required. Available at: https://github.com/alecalve/python-bitcoin-blockchain-parser)

## How can I use it?
Change the paths in `setup.py`. Run it with: python3 steganalysis_manager.py

Depending on the size of the blockchain/cluster set, it may take a lot of hours to execute completely.

This code is currently under development and revision, not fully tested. Suggestions are welcome.
