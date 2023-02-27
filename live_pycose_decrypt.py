from binascii import unhexlify
from pycose.messages import Enc0Message
from pycose.keys import SymmetricKey

# message bytes (CBOR encoded)
msg =  b'\xd0\x83U\xa2\x01\x01\x05P\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\xa1\x04X$meriadoc.brandybuck@buckland.exampleX \xc4\xaf\x85\xacJQ4\x93\x19\x93\xec\n\x18c\xa6\xe8\xc6n\xf4\xc9\xac\x161^\xe6\xfe\xcd\x9b.\x1cy\xa1'

cose_msg = Enc0Message.decode(msg)

# Create a COSE Symmetric Key
cose_key = SymmetricKey(unhexlify(b'000102030405060708090a0b0c0d0e0f'))
cose_msg.key = cose_key

print(cose_msg.decrypt())