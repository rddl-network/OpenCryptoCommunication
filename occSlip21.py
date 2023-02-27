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
import time

from util import *

from occSlipConnect import slip_reader, OccSerial

from tkinter import *

import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

class Slip21Node:
            def __init__(self, seed = None):
                if seed is not None:
                    self.data = hmac.digest(b'Symmetric key seed', seed, hashlib.sha512)
                else:
                    self.data = None

            def derive_path(self, path):
                for label in path:
                    h = hmac.HMAC(self.data[0:32], b'\x00', hashlib.sha512)
                    h.update(label.encode())
                    self.data = h.digest()

            def key(self):
                return binascii.hexlify(self.data[32:64])

"""
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
"""

# Create object
root = Tk()

# Adjust size
root.geometry( "400x200" )

# Change the label text
# ToDo replace global accordingly with a useful class
global selected_port
def show():
    global selected_port
    label.config( text = clicked.get() )
    selected_port = clicked.get()
    root.destroy()

# Dropdown menu options
options = []
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
    options.append(port)

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set( options[0] )

# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()

# Create button, it will change label text
button = Button( root , text = "Connect" , command = show ).pack()

# Create Label
label = Label( root , text = " " )
label.pack()

# Execute tkinter
root.mainloop()


occ_serial = OccSerial(selected_port, 115200, serial.PARITY_NONE, serial.STOPBITS_ONE, serial.EIGHTBITS, 1)
occ_serial.connect()

print("after the connect attempt")

time.sleep(0.5)
occ_serial.write(b'')

print("after the initial write attempt")

occ_serial.write(b'\xc0/IHW/trnd\x00\x00\x00,i\x00\x00\x00\x00\x00@\xc0')

print("after the request random number  attempt")
f = slip_reader(occ_serial.ser)


global rnd_num
for i in f: 
    global rnd_num
    rnd_num = i[3]
    

print(rnd_num)
print(type(rnd_num))



occ_serial.disconnect()
time.sleep(0.1)


key = bytearray(rnd_num, 'utf-8')
key = binascii.unhexlify(key)

print(key)
cip = ChaCha20Poly1305(key)

nonce = os.urandom(12)
#ciphertext = cip.encrypt(nonce, b'801 08 35 b9 44 1c 84 0f 1b 09')
ciphertext = cip.encrypt(nonce, b'Hi, thats a interplanetary message for all my co-evolutionists!')
print(F"CIPHERTEXT: {ciphertext}")


plaintext = cip.decrypt(nonce, ciphertext)
print(F'PLAINTEXT HEX: {plaintext}')
print(F'PLAINTEXT: {binascii.hexlify(ciphertext)}')

slip21_key = Slip21Node(key)
print(F"Slip-21 key: {slip21_key.key()}")

slip21_key.derive_path(["SLIP-0021", "Masukommi Master Key"])
print(F"Slip-21 derived key 1: {slip21_key.key()}")

path = "m/SLIP-0021/Masukomi Master Key/Interplanetary Message"
path = path.split('/')
print(path)

slip21_key.derive_path(path)
print(F"Slip-21 derived key 1: {slip21_key.key()}")

print("\r\r\r\n")
seed = b'c76c4ac4f4e4a00d6b274d5c39c700bb4a7ddc04fbc6f78e85ca75007b5b495f74a9043eeb77bdd53aa6fc3a0e31462270316fa04b8c19114c8798706cd02ac8'
slip21_key = Slip21Node(binascii.unhexlify(seed.strip()))
path = "m"
#slip21_key.derive_path(path)
print(F"m: {slip21_key.key()}")
print(F"DATA: {binascii.hexlify(slip21_key.data)[32:]}")

path = ["SLIP-0021", "Master encryption key"]
slip21_key.derive_path(path)
print(F"Slip-21 derived key m/SLIP-0021: {slip21_key.key()}")

slip21_key = Slip21Node(binascii.unhexlify(seed.strip()))

path = ["SLIP-0021", "Authentication key"]
slip21_key.derive_path(path)
print(F"Slip-21 derived key m/SLIP-0021/Authentication key: {slip21_key.key()}")


seed2 = create_string_buffer(64)
bip39_mnemonic_to_seed(b' '.join([b'all'] * 12), b'', seed2, 64)
root = Slip21Node(seed2)
