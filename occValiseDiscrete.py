
from util import *
import wallycore as wally

import os
import binascii
import hmac
import hashlib

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


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

class OscAES:

    def __init__(self,key):
        self.key = key[0:16]
        self.data = None

    def encodeToAES(self, data):
        self.data = data
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')

        #print(ct)

        '''
        print(result)
        print("")
        print(b64encode(data).decode('utf-8'))
        print(b64encode(key).decode('utf-8'))
        '''

        return(iv, ct)

    def decodeFromAES(self, iv, ct):
        iv = b64decode(iv)
        ciphertext = b64decode(ct)
        # iv = b64decode(b64['iv'])
        # ct = b64decode(b64['ciphertext'])
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return(pt)


class Slip21Node:
            def __init__(self, seed = None):
                if seed is not None:
                    self.data = hmac.HMAC(b'Symmetric key seed', seed, hashlib.sha512).digest()
                else:
                    self.data = None

            def derive_path(self, path):
                for label in path:
                    h = hmac.HMAC(self.data[0:32], b'\x00', hashlib.sha512)
                    h.update(label.encode())
                    self.data = h.digest()

            def key(self):
                return binascii.hexlify(self.data[32:64])

def create_mnemonic():
    out = c_void_p()
    LEN = 16
    bip39_get_wordlist('english', byref(out))

    buf = os.urandom(32)
    # buf = occ.trnd(32)

    print(F"buf: {buf}")

    _, mnemonic = bip39_mnemonic_from_bytes(out,buf,LEN)
    
    print(F"buf: {buf}")
    print(F"out: {out}")

    out2 = c_void_p()
    buf2 = create_string_buffer(LEN)

    ret, written = bip39_mnemonic_to_bytes(out2, mnemonic, buf2, LEN)

    print(ret)
    print(written)
    print(F"buf2: {buf2}")
    print(F"out: {out2}")

    _, mnemonic2 = bip39_mnemonic_from_bytes(out2,buf2,LEN)
    print(f"mnemonic2: {mnemonic2}")

    buf3 = create_string_buffer(LEN)
    ret, written = bip39_mnemonic_to_seed(mnemonic, "", buf3, LEN )

    print(F"buf3: {buf3}")

    # start-create_p2pkh_address
    _, seed = wally.bip39_mnemonic_to_seed512 ( mnemonic, 'my password')

    print(F"seed: {seed}")

    seed, seed_len = make_cbuffer ( binascii.hexlify(seed))
    master = ext_key ()
    ret = bip32_key_from_seed ( seed, len(seed),VER_TEST_PRIVATE, 0, byref ( master))

    _,wif = wally_wif_from_bytes ( master.priv_key, 32, 0xef, 0)
    print(F"wif: {wif}")

    # derive symetric key according to SLIP-0021 for AES ciphers

    print(seed)
    #print(binascii.unhexlify(seed))
    print(binascii.hexlify(seed))


    key = b'dbf12b44133eaab506a740f6565cc117228cbf1dd70635cfa8ddfdc9af734756'
    key = binascii.unhexlify(key)

     #slip21_key = Slip21Node(key)
    slip21_key = Slip21Node(seed)
    print(F"Slip-21 key: {slip21_key.key()}")
    
    
    slip21_key.derive_path(["SLIP-0021", "Masukommi Master Key"])
    print(F"Slip-21 derived key 1: {slip21_key.key()}")
    
    path = "SLIP-0021/Masukomi Master Key/Interplanetary Message"
    path = path.split('/')
    print(path)

    slip21_key.derive_path(path)
    print(F"Slip-21 derived key 1: {slip21_key.key()}")
    
    aes = OscAES(slip21_key.key())
    aes_enc = aes.encodeToAES(b"hello tom how is the da today with you daughters. they are cute and smart girls.hello tom how is the da today with you daughters. they are cute and smart girls.hello tom how is the da today with you daughters. they are cute and smart girls.")
    aes_dec = aes.decodeFromAES(aes_enc[0], aes_enc[1])

    print(F'AES encoded data: {aes_enc}')
    print(F'AES decoded data: {aes_dec}')
    print(F'AES msg length: {len(aes_dec)}')


    return (mnemonic)


mnemo = create_mnemonic()
print(mnemo)

