# Copyright 2019
# Antonio Nappa - Iñigo Querejeta Azurmendi 

import hashlib
import datetime as dt
from bitstring import BitArray
import time

from zokrates.eddsa import PrivateKey, PublicKey
from zokrates.field import FQ

# from zokrates.utils import write_signature_for_zokrates_cli


def write_signature_for_zokrates_cli(pk, sig, path, coordenadas):
    "Writes the input arguments for verifyEddsa in the ZoKrates stdlib to file."
    args = [0, 0, 0, coordenadas]
    sig_R, sig_S = sig
    args.extend([sig_R.x, sig_R.y, sig_S, pk.p.x.n, pk.p.y.n])
    args = " ".join(map(str, args))

    with open(path, "w+") as file:
        for l in args:
            file.write(l)


def write_double_sig(pk, sig_1, sig_2, coordinates_1, timestamp_1, coordinates_2, timestamp_2, distance, current_time, time_distance, path):
    args = [coordinates_1, timestamp_1, coordinates_2, timestamp_2]
    sig_R_1, sig_S_1 = sig_1
    sig_R_2, sig_S_2 = sig_2

    assert(current_time - timestamp_1 < time_distance)
    assert(current_time - timestamp_2 < time_distance)

    args.extend([sig_R_1.x, sig_R_1.y, sig_S_1, sig_R_2.x, sig_R_2.y, sig_S_2, pk.p.x.n, pk.p.y.n, distance, time_distance, current_time])

    args = " ".join(map(str, args))

    with open(path, "w+") as file:
        for l in args:
            file.write(l)

# coordinates = 23980240823
# timestamp = 1561039899
def telecom_signature(coordinates, write_sig_zokrates=False):
    """
    Hardcoded values. Just trust me.

    Example:
        >>> pk, sig, msg, ts, _ = telecom_signature(5)
        >>> pk.verify(sig, msg)
        True
        >>> msg_fake = hashlib.sha256("234".encode("utf-8")).digest()
        >>> pk.verify(sig, msg_fake)
        False
    """
    timestamp = int(dt.datetime.now().timestamp())
    # unbealievable that I have to do this manually
    pre_image_coords = "{0:b}".format(coordinates)
    pre_image_coords = "0" * (128 - len(pre_image_coords)) + pre_image_coords

    # We probably cannot do the timestamp proof with zokrates
    pre_image_ts = "{0:b}".format(timestamp)
    pre_image_ts = "0" * (128 - len(pre_image_ts)) + pre_image_ts

    pre_image = "0" * 256 + pre_image_ts + pre_image_coords # working with pre_image_coords = "0" * (512 - len(pre_image_coords)) + pre_image
    # pre_image = "0" * (512 - len(pre_image_coords)) + pre_image_coords
    pre_image_bytes = BitArray(bin=pre_image).bytes
    msg_bytes_short = hashlib.sha256(pre_image_bytes).digest()
    msg_bytes = msg_bytes_short + b"\0" * 32

    # args = " ".join(map(str, [timestamp, coordinates, Bn.from_hex(msg_bytes_short[:16].hex()), Bn.from_hex(msg_bytes_short[16:].hex())])) + "\n\n"
    #
    # with open("./computed_signatures", "a+") as file:
    #     for write_in in args:
    #         file.write(write_in)

    assert (len(msg_bytes) == 64)

    key = FQ(1997011358982923168928344992199991480689546837621580239342656433234255379025)
    sk = PrivateKey(key)
    pk = PublicKey.from_private(sk)
    sig = sk.sign(msg_bytes)

    if write_sig_zokrates:
        path = './zokrates_args'
        write_signature_for_zokrates_cli(pk, sig, path, coordinates)

    hash_pair = int(msg_bytes_short[:16].hex(), base=16), int(msg_bytes_short[16:].hex(), base=16)

    return pk, sig, msg_bytes, timestamp, hash_pair


def multiple_sig(coord_1, coord_2, distance=15, time_distance=300, path='./powha_args', time_walks=10):
    """
    Generate multiple signature

    Example:
        >>> _, _ = multiple_sig(2189963759064380391430512, 2189963759064397451712689)
    """
    sig_1 = telecom_signature(coord_1)
    time.sleep(time_walks)
    sig_2 = telecom_signature(coord_2)

    assert(sig_1[0] == sig_2[0])

    timestamp_1 = sig_1[3]
    timestamp_2 = sig_2[3]
    hash_pair_1 = sig_1[4]
    hash_pair_2 = sig_2[4]
    time.sleep(time_walks)
    current_time = int(dt.datetime.now().timestamp())

    write_double_sig(sig_1[0], sig_1[1], sig_2[1], coord_1, timestamp_1, coord_2, timestamp_2, distance, current_time, time_distance, path)

    return [timestamp_1, timestamp_2], [hash_pair_1, hash_pair_2]

if __name__ == '__main__':
    import doctest

    doctest.testmod()
