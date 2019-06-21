from generating_signature import multiple_sig
import argparse

parser = argparse.ArgumentParser(description='Generates the files to be used as input for the zokrates proofs. '
                                             'The evaluation of this script generates three files where you have the'
                                             'proof of walk one, proof of walk two and finally the last proof of walk'
                                             'linking the previous waks.')

parser.add_argument(
    "-p", "--path",
    help="path to store the files which will be used as input for the proofs.",
    default="signature_generator/input_data/"
)

parser.add_argument(
    "-fn", "--file-name",
    help="name of the file to store the generated data."
)

parser.add_argument(
    "-gh", "--geo-hashes",
    help="include the geo hashes corresponding to the different walks. Current version needs 6 of them (for three paths).",
    nargs='+',
    type=int
)

parser.add_argument(
    "-mind", "--min-distance",
    help="minimal distance between points to consider it a path.",
    type=int
)

parser.add_argument(
    "-maxd", "--max-distance",
    help="maximum distance between the three paths.",
    type=int
)

parser.add_argument(
    "-maxtc", "--max-time-cert",
    help="maximum time difference accepted between time of proof and time of certified geohash location",
    type=int
)

parser.add_argument(
    "-maxtw", "--max-time-walks",
    help="maximum time difference accepted between to points to be considered a path",
    type=int
)

parser.add_argument(
    "-st", "--simulated-time",
    help="simulated time difference between walks. time.sleep() is used here to separate to certification of points",
    type=int,
    default=10
)
args = parser.parse_args()

if len(args.geo_hashes) != 6:
    raise ValueError("Expected 6 geohashes.")

hashes_path_1 = args.geo_hashes[0], args.geo_hashes[1]
hashes_path_2 = args.geo_hashes[2], args.geo_hashes[3]
hashes_path_3 = args.geo_hashes[4], args.geo_hashes[5]

times_path_1, hash_path_1 = multiple_sig(hashes_path_1[0], hashes_path_1[1],
                            distance=args.min_distance,
                            time_distance=args.max_time_walks,
                            path=args.path + args.file_name + "_walk_one",
                            time_walks=args.simulated_time)

times_path_2, hash_path_2 = multiple_sig(hashes_path_2[0], hashes_path_2[1],
                             distance=args.min_distance,
                             time_distance=args.max_time_walks,
                             path=args.path + args.file_name + "_walk_two",
                             time_walks=args.simulated_time)

times_path_3, hash_path_3 = multiple_sig(hashes_path_3[0], hashes_path_3[1],
                             distance=args.min_distance,
                             time_distance=args.max_time_walks,
                             path=args.path + args.file_name + "_walk_three",
                             time_walks=args.simulated_time)

with open(args.path + args.file_name + "_walk_three", "r") as file:
    walk_three_args = [list(map(int, line.strip().split(' '))) for line in file]


full_proof_input = [hash_path_1[0], hash_path_2[0], walk_three_args[0], args.max_distance,
                    hashes_path_1[0], times_path_1[0], hashes_path_2[0], times_path_2[0], args.max_time_walks]
full_proof_input_flat = []
for a in full_proof_input:
    try:
        full_proof_input_flat.extend(a)
    except:
        full_proof_input_flat.extend([a])

proof_data = " ".join(map(str, full_proof_input_flat))

with open(args.path + args.file_name, "w+") as file:
        for write_in in proof_data:
            file.write(write_in)

