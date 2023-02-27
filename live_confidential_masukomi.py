"""

# Derived from Bip-0039 mnemotic phrase:
# all all all all all all all all all all all all with empty passphrase

S = b'c76c4ac4f4e4a00d6b274d5c39c700bb4a7ddc04fbc6f78e85ca75007b5b495f74a9043eeb77bdd53aa6fc3a0e31462270316fa04b8c19114c8798706cd02ac8'

m = HMAC-SHA512(key = b'Symmetric key seed", msg = S)

# label has to be unique for application, like 'SLIP-0021'
# or 'OEBB Railbox Credential ID"
ChildNode(N, label) = HMAC-SHA512(key = N[0:32], msg = b"\x00" + label)

Key(N) = N[32:64]

Key(m) = dbf12b44133eaab506a740f6565cc117228cbf1dd70635cfa8ddfdc9af734756
Key(m/"SLIP-0021") = 1d065e3ac1bbe5c7fad32cf2305f7d709dc070d672044a19e610c77cdf33de0d
Key(m/"SLIP-0021"/"Master encryption key") = ea163130e35bbafdf5ddee97a17b39cef2be4b4f390180d65b54cf05c6a82fde
Key(m/"SLIP-0021"/"Authentication key") = 47194e938ab24cc82bfa25f6486ed54bebe79c40ae2a5a32ea6db294d81861a6

# Compatible with all major symmetric-key algorithms in use today, such as AES-256, ChaCha20Poly1305 or HMAC.

# Requirement: https://github.com/ph4r05/py-chacha20poly1305

"""

from chacha20poly1305 import ChaCha20Poly1305
import binascii
import os
import hmac
import hashlib

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

key = b'dbf12b44133eaab506a740f6565cc117228cbf1dd70635cfa8ddfdc9af734756'
key = binascii.unhexlify(key)

print(key)
cip = ChaCha20Poly1305(key)

nonce = os.urandom(12)
#ciphertext = cip.encrypt(nonce, b'801 08 35 b9 44 1c 84 0f 1b 09')
ciphertext = cip.encrypt(nonce, b'Hi, thats a interplanetary message for all my co-evolutionists!')


plaintext = cip.decrypt(nonce, ciphertext)
print(F'PLAINTEXT HEX: {plaintext}')
print(F'PLAINTEXT: {binascii.hexlify(ciphertext)}')

slip21_key = Slip21Node(key)
print(F"Slip-21 key: {slip21_key.key()}")

slip21_key.derive_path(["SLIP-0021", "Masukommi Master Key"])
print(F"Slip-21 derived key 1: {slip21_key.key()}")

path = "SLIP-0021/Masukomi Master Key/Interplanetary Message"
path = path.split('/')
print(path)

slip21_key.derive_path(path)
print(F"Slip-21 derived key 1: {slip21_key.key()}")