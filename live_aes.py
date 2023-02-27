# {128, "000102030405060708090a0b0c0d0e0f", "00112233445566778899aabbccddeeff", "69c4e0d86a7b0430d8cdb78070b4c55a"},
# {key, plain, cipher, ciphered}

from util import *
import binascii
import os
import hmac
import hashlib

ENCRYPT, DECRYPT = 1, 2

case = ([ 16, "000102030405060708090a0b0c0d0e0f",
              "00112233445566778899aabbccddeeff",
              "69c4e0d86a7b0430d8cdb78070b4c55a" ])

print( make_cbuffer(case[1]))
key, plain, cypher = [make_cbuffer(s)[0] for s in case[1:]]
key_bytes = 16
print(plain)

out_buf, out_len = make_cbuffer('00' * key_bytes)

resp = wally_aes(key, 16, plain, 16, ENCRYPT, out_buf, out_len)

print(resp)
print(h(out_buf))

