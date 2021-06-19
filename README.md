# steganalysis-tool-blockchain
A repository for an attempt to perform steganalysis on blockchains, based on the nonces and in LSB of hashes.

If you want to use this for academic purposes, please check the publications section.

We provide a compilation of statistical results in `extracted` and `sequentialAnalysis` folders. When executed, the application extracts data from the blockchain accordingly to the analyzer specified in `setup` (currently LSB of addresses), in addition to nonce statistics. The objective is to find evidence of the presence (or not) of steganographic messages in the blockchain. Please check the publications for further details.

## Requirements

Depending on the configuration specified in `setup.py`, you'll need:
1. The blockchain data (currently, ethereum or bitcoin), or
2. The clustering API or output data;

Currently suported clusters: Bitiodine and Blocksci API (Etherclust support is given but not fully tested).

For the sequential analysis, a blockchain parser library is required. Here this one is used: https://github.com/alecalve/python-bitcoin-blockchain-parser).

## How can I use it?
Change the paths in `setup.py`. Examples are given. Run it with: `python3 steganalysis_manager.py`

Depending on the size of the blockchain/cluster set, it may take a lot of hours to execute completely.

This code is currently under development and revision, not fully tested. Suggestions are welcome.


## Publications

Giron A.A., Martina J.E., Custódio R. (2020) Bitcoin Blockchain Steganographic Analysis. In: Zhou J. et al. (eds) Applied Cryptography and Network Security Workshops. ACNS 2020. Lecture Notes in Computer Science, vol 12418. Springer, Cham. https://doi.org/10.1007/978-3-030-61638-0_3 

Giron, A.A.; Martina, J.E.; Custódio, R. Steganographic Analysis of Blockchains. Sensors 2021, 21, 4078. https://doi.org/10.3390/s21124078
