# PoWha Proof-of-Walk Human Attestation

This repositery contains zkSNARK implementation in ZoKrates to prove in ZK signed GPS locations


Follow the instruction below to setup ZoKrates and ZoKtrates pyCrypto library to generate signed GPS data hashes

## Install ZoKrates

check https://github.com/Zokrates/ZoKrates

be sure to have zokrates binary available in your $PATH
be sure to set $ZOKRATES_HOME properly

e.g. edit .bashrc ;)

## Install ZoKrates pyCrypto

Make sure you are running a python 3 runtime.

```bash
git clone https://github.com/Zokrates/pycrypto.git
pip install -r requirements.txt
```


End-to-end example

python3 generating_signature.py

you will get as an output powha_args

### remember to stay in the same directory ###

zokrates compile -i /path/to/powha_verification.com

#check output == 1
cat path/to/powha_args | zokrates compute-witness

zokrates setup

#this generates solidity smart contract to verify the proofs
zokrates export-verifier

#here you can estimate the prover time
time zokrates compute-proof
