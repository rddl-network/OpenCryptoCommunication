import os
import binascii

from ecdsa import SECP256k1, SigningKey


seed = os.urandom ( 32)

class Base36 ( ):

    def base36encode ( number):
        if not isinstance ( number, ( int)):
            raise TypeError ( 'number must be an integer')
        is_negative = number < 0
        number = abs ( number)

        alphabet, base36 = [ '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

        while number:
            number, i = divmod ( number, 36)
            base36 = alphabet[i] + base36
        if is_negative:
            base36 = '-' + base36

        return base36 or alphabet[0]
    
    def base36decode ( number):
        return int ( number, 36)



sk = SigningKey.from_string ( seed, SECP256k1)
print ( sk.to_string ())
print ( int (binascii.hexlify ( sk.to_string ()), base=16)) 

# key = int ( 0x3ef1c8342eaa4fb5)
key = int (binascii.hexlify ( sk.to_string ()), base=16)
key_encoded = Base36.base36encode ( key)


print ( key)
print ( Base36.base36encode ( key))

did_serial = F'{key_encoded[0:3]}-{key_encoded[3:6]}-{key_encoded[6:9]}-{key_encoded[9:12]}'
print(did_serial)

did =binascii.hexlify(did_serial.encode('ascii')).decode() + "00"
print(did) 

did_page_1 = "hf 14a raw -s -c A2 06 " + did[:8]
did_page_2 = "hf 14a raw -s -c A2 06 " + did[8:16]
did_page_3 = "hf 14a raw -s -c A2 06 " + did[16:24]
did_page_4 = "hf 14a raw -s -c A2 06 " + did[24:]



