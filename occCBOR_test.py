
import base64
import hashlib
import itertools
import json
import os
import re
import string
import struct
import sys
import time
import serial

from occSlip import *
from occCore import *

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


try:
    import serial
except ImportError:
    print(
        "Pyserial is not installed for %s. "
        "Check the README for installation instructions." % (sys.executable)
    )
    raise

# check 'serial' is 'pyserial' and not 'serial'
# ref. https://github.com/espressif/esptool/issues/269
try:
    if "serialization" in serial.__doc__ and "deserialization" in serial.__doc__:
        raise ImportError(
            "esptool.py depends on pyserial, but there is a conflict with a currently "
            "installed package named 'serial'.\n"
            "You may work around this by 'pip uninstall serial; pip install pyserial' "
            "but this may break other installed Python software "
            "that depends on 'serial'.\n"
            "There is no good fix for this right now, "
            "apart from configuring virtualenvs. "
            "See https://github.com/espressif/esptool/issues/269#issuecomment-385298196"
            " for discussion of the underlying issue(s)."
        )
except TypeError:
    pass  # __doc__ returns None for pyserial

try:
    import serial.tools.list_ports as list_ports
except ImportError:
    print(
        "The installed version (%s) of pyserial appears to be too old for esptool.py "
        "(Python interpreter %s). Check the README for installation instructions."
        % (sys.VERSION, sys.executable)
    )
    raise
except Exception:
    if sys.platform == "darwin":
        # swallow the exception, this is a known issue in pyserial+macOS Big Sur preview
        # ref https://github.com/espressif/esptool/issues/540
        list_ports = None
    else:
        raise


for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

def slip_reader(port):
    partial_packet = None
    in_escape = False
    successful_slip = False
    occ_slip = bytes([])

    while True:
        waiting = port.inWaiting()
        read_bytes = port.read(1 if waiting == 0 else waiting)
        # print(F'READ BYTES: {read_bytes}')
        occ_slip += read_bytes
        # print(F"OCC SLIP: {occ_slip}")
        if read_bytes == b"":
            if partial_packet is None:  # fail due to no data
                msg = (
                    "Serial data stream stopped: Possible serial noise or corruption."
                    if successful_slip
                    else "No serial data received."
                )
            else:  # fail during packet transfer
                msg = "Packet content transfer stopped (received {} bytes)".format(
                    len(partial_packet)
                )    
        if b"ESP-ROM:" in read_bytes:
            #print(read_bytes)
            if b'ESP-ROM:esp32c3' not in read_bytes:
                print(F'Wrong hardware target. Only works with Risc-V based ESP32C3 chip series.')
                quit()
        if b"\xc0" in read_bytes:
            for b in read_bytes:
                b = bytes([b])
                if partial_packet is None:  # waiting for packet header
                    if b == b"\xc0":
                        occ_slip = b'\xc0'
                        partial_packet = b''
                    else:
                        remaining_data = port.read(port.inWaiting()) 
                        # print(F"REMAINING:DATA: {remaining_data}")   
                elif b == b"\xc0":  # end of packet
                    partial_packet = None
                    slipDecoder = SlipDecoder()
                    slip = slipDecoder.decodeFromSLIP(occ_slip)
                    slip_decoded = decodeOSC(bytes(slip))
                    successful_slip = True
                    occ_slip = bytes([])
                    yield slip_decoded
                    return
                else:  # normal byte in packet
                    partial_packet += b
                    
class OccSerial:
    def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.ser = None

    def connect(self):
        assert self.ser is None

        print('Connecting to {} at {}'.format(self.port, self.baudrate))
        self.ser = serial.Serial(self.port, self.baudrate,
                                 timeout=self.timeout,
                                 write_timeout=self.timeout)
        assert self.ser is not None

        if not self.ser.is_open:
            self.ser.open()
        # As learned from Blockstream's Jade hardware
        # Ensure RTS and DTR are not set (as this can cause the hw to reboot)
        self.ser.setRTS(False)
        self.ser.setDTR(False)

        print('Connected')

    def disconnect(self):
        assert self.ser is not None

        # Consider also here the peculiarities of Jade aka Espressif's ESP32
        # Ensure RTS and DTR are not set (as this can cause the hw to reboot)
        # and then close the connection
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.ser.close()

        # Reset state
        self.ser = None

    def write(self, bytes_):
        assert self.ser is not None
        return self.ser.write(bytes_)

    def read(self, n):
        assert self.ser is not None
        return self.ser.read(n)


occ_serial = OccSerial('/dev/ttyACM0', 115200, serial.PARITY_NONE, serial.STOPBITS_ONE, serial.EIGHTBITS, 1)
occ_serial.connect()


"""ser = serial.Serial(
    port = '/dev/ttyUSB1',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout=1 # add this
    )"""


time.sleep(0.5)
occ_serial.write(b'')

message = OSCMessage()
message.setAddress("/IHW/cbor")
message.append("36b6c616e642e6578616d706c655820c4af85ac4a5134931993ec0a1863a6e8c66ef4c9ac16315ee6fecd9b2e1c79a1",'s')
# d08355a20101055001010101010101010101010101010101a10458246d65726961646f632e6272616e64796275636b406275636b6c616e642e6578616d706c655820c4af85ac4a5134931993ec0a1863a6e8c66ef4c9ac16315ee6fecd9b2e1c79a1

slipEncoder = SlipEncoder()
occ_cmd = slipEncoder.encodeToSLIP(message.getBinary())
occ_cmd = ''.join(map(str, occ_cmd))
print("The SLIP encoded data %s" %(occ_cmd))

occ_cmd = occ_cmd.encode('utf-8')
occ_cmd = occ_cmd.replace(b'192', b'\xc0')
print(occ_cmd)

occ_serial.write(occ_cmd)
f = slip_reader(occ_serial.ser)

for i in f: 
    print(i)

message = OSCMessage()
message.setAddress("/IHW/cbor")
message.append("d08355a20101055001010101010101010101010101010101a10458246d65726961646f632e6272616e64796275636b4062756", 's')
slipEncoder = SlipEncoder()
occ_cmd = slipEncoder.encodeToSLIP(message.getBinary())
occ_cmd = ''.join(map(str, occ_cmd))
print("The SLIP encoded data %s" %(occ_cmd))

occ_cmd = occ_cmd.encode('utf-8')
occ_cmd = occ_cmd.replace(b'192', b'\xc0')
print(occ_cmd)

occ_serial.write(occ_cmd)
g = slip_reader(occ_serial.ser)

for i in g: 
    print(i)

occ_serial.disconnect()

"""
occ_serial.write(b'\xc0/IHW/trnd\x00\x00\x00,i\x00\x00\x00\x00\x00@\xc0')
slip_reader(occ_serial.ser)

occ_serial.write(b'\xc0/IHW/trnd\x00\x00\x00,i\x00\x00\x00\x00\x00@\xc0')
slip_reader(occ_serial.ser)


occ_serial.write(b'\xc0/IHW/trnd\x00\x00\x00,i\x00\x00\x00\x00\x00@\xc0')
f = slip_reader(occ_serial.ser)

for i in f: 
    print(i)



# ser.close()
occ_serial.disconnect()

"""
