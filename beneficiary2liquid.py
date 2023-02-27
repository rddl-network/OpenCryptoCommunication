

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

PM_MAIN_PUBLIC = 0x02D41400
PM_MAIN_PRIVATE = 0x02D40FC0

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

out = c_void_p()
LEN = 16
bip39_get_wordlist('english', byref(out))
buf = os.urandom(32)
_, mnemonic = bip39_mnemonic_from_bytes(out,buf,LEN)


# mnemonic = "supreme layer police brand month october rather rack proud strike receive joy limit random hill inside brand depend giant success quarter brain butter mechanic"
# wallet RDDLtoken
mnemonic = "sad potato mad strategy ecology invite fossil answer kiwi juice joy borrow"
# Result cMcbt5FD4XQvaaRKoqGR1GrdDPqsUAwcpAsXAZt31ej5DQeNhXHK
# wallet WRAPPEDtoken
# mnemonic = "bacon sunset lecture left auction print unable main oxygen problem grace field"
# Result cMbi8gNnVsU4v6e7Sf8J5GzRJaQnrpA2hdKw3rE8RoDGfozFLwfg
print ( F'Mnemonic: {mnemonic}')

# start-create_p2pkh_address
_, seed = wally.bip39_mnemonic_to_seed512 ( mnemonic, 'my password')


seed, seed_len = make_cbuffer ( binascii.hexlify(seed))
master = ext_key ()
ret = bip32_key_from_seed ( seed, len(seed),
                          VER_TEST_PRIVATE, 0, byref ( master))

print ( F'Master Key as WIF: {wally_wif_from_bytes ( master.priv_key, 32, 0xef, 0)}')

_,wif = wally_wif_from_bytes ( master.priv_key, 32, 0xef, 0)
print(wif)
print ( F'Seed Raw HEX: {binascii.hexlify ( seed)}')

version = 0xC4
ret, new_addr = wally_bip32_key_to_address( master, 0x04, version)
print(new_addr)
print ( F'New Address: { new_addr}')

version = 0x6F
bech32_prefix = 'tb'
ret, new_addr = wally_bip32_key_to_addr_segwit(master, utf8(bech32_prefix), 0)
print(new_addr)
print ( F'New Address: { new_addr}')

pub, _ = make_cbuffer('00'*33)
ret = wally_ec_public_key_from_private_key(master.priv_key, 32, pub, len(pub))
print(binascii.hexlify(pub))

#seed = create_string_buffer(64)
# bip39_mnemonic_to_seed(b' '.join([b'all'] * 12), b'', seed, 64)
root = Slip21Node ( seed = seed)
root.derive_path ( [b'SLIP-0077'])
master_blinding_key_hex = root.key ( )

print ( F'Master Blinding Key HEX: {master_blinding_key_hex}')
print ( F'Master Key Base58 Serialized: {bip32_key_to_base58 ( master, FLAG_KEY_PRIVATE)}')

print ( F'Beneficiaries and Keys:')
for x in range ( 51):
    derive_key_out = ext_key ( )
    # ret = bip32_key_from_parent ( master, x, FLAG_KEY_PRIVATE, derive_key_out)
    ret = bip32_key_from_parent_path_str_n(master, 'm/0h/0h/'+str(x)+'h', len('m/0h/0h/'+str(x)+'h'), 0, FLAG_KEY_PRIVATE, derive_key_out)
    _,wif = wally_wif_from_bytes ( derive_key_out.priv_key, 32, 0xef, 0)
    print ( wif)

derive_key_out = ext_key ( )
# ret = bip32_key_from_parent ( master, x, FLAG_KEY_PRIVATE, derive_key_out)
ret = bip32_key_from_parent_path_str_n(master, 'm/0h/0h/'+str(359)+'h', len('m/0h/0h/'+str(359)+'h'), 0, FLAG_KEY_PRIVATE, derive_key_out)
_,wif = wally_wif_from_bytes ( derive_key_out.priv_key, 32, 0xef, 0)
print ( wif)

"""
try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    resp = rpc_connection.importprivkey ( wif, "RDDLmint2", False)
    print(resp)

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))
"""