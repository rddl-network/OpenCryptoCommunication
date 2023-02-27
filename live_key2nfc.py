import os
import string
import subprocess
import sys
import time
import random
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
did_page_2 = "hf 14a raw -s -c A2 07 " + did[8:16]
did_page_3 = "hf 14a raw -s -c A2 08 " + did[16:24]
did_page_4 = "hf 14a raw -s -c A2 09 " + did[24:]

print(did_page_1)
print(did_page_2)
print(did_page_3)
print(did_page_4)


serial_port = '/dev/ttyACM0'

# pm3_client = '/home/proxmark3'
pm3_client = '/home/nestor/proxmark3/pm3'

# For writing to tag we use the command A2h (h for hex)
# Beginning at an page address, eg.: 06h
# We write in pages, means 4 bytes per sequence, eg.: AAEEDDBB

"""write_hf_pm3 = subprocess.run(
    [pm3_client, '-c', 'help'], capture_output=True)"""

write_hf_pm3 = subprocess.run(
     [pm3_client, '-c', did_page_1], capture_output=True)
print ( write_hf_pm3.returncode)
if (write_hf_pm3.returncode == 0):
    print(write_hf_pm3.stdout.decode('ASCII'))
time.sleep(2)

write_hf_pm3 = subprocess.run(
     [pm3_client, '-c', did_page_2], capture_output=True)
print ( write_hf_pm3.returncode)
if (write_hf_pm3.returncode == 0):
    print(write_hf_pm3.stdout.decode('ASCII'))
time.sleep(2)

write_hf_pm3 = subprocess.run(
     [pm3_client, '-c', did_page_3], capture_output=True)
print ( write_hf_pm3.returncode)
if (write_hf_pm3.returncode == 0):
    print(write_hf_pm3.stdout.decode('ASCII'))
time.sleep(2)

write_hf_pm3 = subprocess.run(
     [pm3_client, '-c', did_page_4], capture_output=True)
print ( write_hf_pm3.returncode)
if (write_hf_pm3.returncode == 0):
    print(write_hf_pm3.stdout.decode('ASCII'))
time.sleep(2)


# For reading a tag we use the command 30h (h for hex)
# Beginning at an page address, eg.: 06h
# We read 4 pages, means 16 bytes per sequence

"""
read_hf_pm3 = subprocess.run([pm3_client, serial_port, '-c', 'hf 14a raw -sc 3006'], capture_output=True)


if (read_hf_pm3.returncode == 0):
    print(read_hf_pm3.stdout.decode('ASCII'))


# For reading a tag's UID we use the command A2h to rite data to page number 4 bytes long (h for hex)

apdu = 'hf 14a raw -s -c A2 06 ' + '68616C6C'
uid_hf_pm3 = subprocess.run([pm3_client, '-c', apdu], capture_output=True)
# uid_hf_pm3 = subprocess.run([pm3_client, serial_port, '-c', 'hf 14a help'], capture_output=True)


if (uid_hf_pm3.returncode == 0):
    print(uid_hf_pm3.stdout.decode('ASCII'))

#for line in iter(uid_hf_pm3.stdout.decode('ASCII').readline,''):
#   print(line.rstrip())

print(uid_hf_pm3.stdout.decode('ASCII').split('\n'))
print("")
#print(uid_hf_pm3.stdout.decode('ASCII').split('\n')[8])
"""
