from binascii import unhexlify, hexlify
from pycose.messages import Enc0Message
from pycose.keys import SymmetricKey

# Create a COSE Encrypt0 Message
msg = Enc0Message(
    phdr={'ALG': 'A128GCM', 'IV': unhexlify(b'01010101010101010101010101010101')},
    uhdr={'KID': b'meriadoc.brandybuck@buckland.example'},
    payload='a secret message'.encode('utf-8')
)

# Create a COSE Symmetric Key
cose_key = SymmetricKey(unhexlify(b'000102030405060708090a0b0c0d0e0f'))
msg.key = cose_key

# Performs encryption and CBOR serialization
print(msg.encode())
print(hexlify(msg.encode()))
#----------------------------------------------------------------------------------
# expected response:
# b'\xd0\x83U\xa2\x01\x01\x05P\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\xa1\x04X$meriadoc.brandybuck@buckland.exampleX \xc4\xaf\x85\xacJQ4\x93\x19\x93\xec\n\x18c\xa6\xe8\xc6n\xf4\xc9\xac\x161^\xe6\xfe\xcd\x9b.\x1cy\xa1'
#----------------------------------------------------------------------------------