

import wallycore as wally
import binascii
import hmac
import hashlib
import os

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import base64

import unittest
import copy
from util import *

rpc_port = 18884
rpc_user = 'nestor'
rpc_password = 'nestor'

VER_MAIN_PUBLIC = 0x0488B21E
VER_MAIN_PRIVATE = 0x0488ADE4
VER_TEST_PUBLIC = 0x043587CF
VER_TEST_PRIVATE = 0x04358394

FLAG_KEY_PRIVATE, FLAG_KEY_PUBLIC, FLAG_SKIP_HASH, = 0x0, 0x1, 0x2
FLAG_KEY_TWEAK_SUM, FLAG_STR_WILDCARD, FLAG_STR_BARE = 0x4, 0x8, 0x10
ALL_DEFINED_FLAGS = FLAG_KEY_PRIVATE | FLAG_KEY_PUBLIC | FLAG_SKIP_HASH
BIP32_SERIALIZED_LEN = 78
BIP32_FLAG_SKIP_HASH = 0x2

# address_prefix = wally.WALLY_CA_PREFIX_LIQUID
address_prefix = wally.WALLY_CA_PREFIX_LIQUID_REGTEST
# network = wally.WALLY_NETWORK_LIQUID
# wif_prefix = wally.WALLY_ADDRESS_VERSION_WIF_MAINNET
network = wally.WALLY_NETWORK_LIQUID_REGTEST
wif_prefix = wally.WALLY_ADDRESS_VERSION_WIF_TESTNET

class Slip21Node:
            def __init__(self, seed = None):
                if seed is not None:
                    self.data = hmac.HMAC(b'Symmetric key seed', seed, hashlib.sha512).digest()
                else:
                    self.data = None

            def derive_path(self, path):
                for label in path:
                    h = hmac.HMAC(self.data[0:32], b'\x00', hashlib.sha512)
                    h.update(label)
                    self.data = h.digest()

            def key(self):
                return h(self.data[32:64])

def derive_eui():
    out = c_void_p()
    LEN = 16
    bip39_get_wordlist('english', byref(out))
    buf = os.urandom(32)
    _, mnemonic = bip39_mnemonic_from_bytes(out,buf,LEN)

    # start-create_p2pkh_address
    _, seed = wally.bip39_mnemonic_to_seed512 ( mnemonic, 'my password')


    seed, seed_len = make_cbuffer ( binascii.hexlify(seed))
    master = ext_key ()
    ret = bip32_key_from_seed ( seed, len(seed),
                          VER_TEST_PRIVATE, 0, byref ( master))


    _,wif = wally_wif_from_bytes ( master.priv_key, 32, 0xef, 0)

    derived_eui = [binascii.hexlify ( seed)[0:16], binascii.hexlify ( seed)[16:32]]

    return ( derived_eui)


if __name__ == '__main__':
    print ( derive_eui())