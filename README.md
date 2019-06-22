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

./generate_powha.sh

#generate hashes for geodata
the generator script works with Python2, there is a problem with geohash library in Python3 (https://github.com/vinsci/geohash/issues/4)
