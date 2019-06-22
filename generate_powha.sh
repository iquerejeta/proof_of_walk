#!/bin/sh

python3 signature_generator/generate_proof_data.py -p "signature_generator/input_data/" -fn "first_try" -gh 2189963759073207093083509 4379927518137661037313142 4379927518137661037313142 547490939765545336952944 547490939765545336952944 273745469882637314117173 -mind 30 -maxd 500 -maxtc 40 -maxtw 1000 -st 0

zokrates compile -i powha_range.code 
cat signature_generator/input_data/first_try_walk_one | zokrates compute-witness
cat signature_generator/input_data/first_try_walk_two | zokrates compute-witness

zokrates compile -i powha_path_verification.code
cat signature_generator/input_data/first_try | zokrates compute-witness

zokrates setup

zokrates export-verifier

time zokrates generate-proof
