import sys
import string
import random
import codecs
import binascii
import subprocess

from hashlib import sha256
from ecdsa import SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain

from escpos.printer import Usb
from encodings import CodecRegistryError

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_dotcode_mark(argv):

    dotcode_str = id_generator()


    print(dotcode_str)
    print(F'{dotcode_str[0:3]}-{dotcode_str[3:6]}-{dotcode_str[6:9]}-{dotcode_str[9:12]}')

    dotcode_mark = F'{dotcode_str[0:3]}-{dotcode_str[3:6]}-{dotcode_str[6:9]}-{dotcode_str[9:12]}'

    dotcode_hash = sha256(dotcode_str.encode(encoding='UTF-8',errors='strict'))
    print(dotcode_hash.hexdigest())

    print(dotcode_hash.hexdigest()[0:32])

    binary_a = dotcode_hash.hexdigest()[0:32]
    binary_b = dotcode_hash.hexdigest()[32:64]

    print(type(binary_a))
    print((binary_a))
    print((binary_b))

    def xor_strings(xs, ys):
        return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

    xored = xor_strings(binary_a, binary_b).encode('utf-8').hex()

    print(codecs.encode(xored))
    print("That is the typof xored: {type(xored)}")

    xored2 = hex(int(binary_a,16) ^ int(binary_b,16))

    print(hex(int(binary_a,16) ^ int(binary_b,16)))
    print(type(xored2))
    print(codecs.encode(xored2))

    print(xored2[2:])

    seed = codecs.encode(xored2[2:])

    '''
    def make_key(seed):
        secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
        return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

    sk = SigningKey.from_string(xored.decode('hex'), SECP256k1)
    '''

    sk = SigningKey.from_string(seed, SECP256k1)
    print(sk.to_string())

    process = subprocess.Popen(['zint', '-o', '/home/nestor/libwally-core/src/test/dotcode.png', '-d', str (dotcode_str), '-b', '115', '--cols', '7', '--mask', '2', '--rotate', '270', '--scale', '3.50', '-w', '10', '--vwhitesp', '10', '--dotsize', '1.00'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break

    # p = Usb ( 0x0483, 0xa319)
    p = Usb ( 0x04b8, 0x0202)

    p.text ( '\n')
    p.text ( '   ' + dotcode_mark)
    p.text ( '\n')
    p.image ( 'dotcode.png')
    p.text ( '\n')
    pk = '   ' + xored2[2:]
    p.text ( pk)
    p.cut ()

if __name__ == '__main__':
    print ( create_dotcode_mark ( sys.argv))


'''    
def base36encode(number):
    if not isinstance(number, (int)):
        raise TypeError('number must be an integer')
    is_negative = number < 0
    number = abs(number)

    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36
    if is_negative:
        base36 = '-' + base36

    return base36 or alphabet[0]


def base36decode(number):
    return int(number, 36)

print(base36encode(1412823931503067241))
print(base36decode('AQF8AA0006EH'))

'''