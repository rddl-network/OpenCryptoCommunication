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

#from .util import FatalError, NotImplementedInROMError, UnsupportedCommandError
#from .util import byte, hexify, mask_to_shift, pad_to

try:
    import serial
except ImportError:
    print(
        "Pyserial is not installed for %s. "
        "Check the README for installation instructions." % (sys.executable)
    )
    raise

def slip_reader(port, trace_function):
    """Generator to read SLIP packets from a serial port.
    Yields one full SLIP packet at a time, raises exception on timeout or invalid data.

    Designed to avoid too many calls to serial.read(1), which can bog
    down on slow systems.
    """
    partial_packet = None
    in_escape = False
    successful_slip = False
    while True:
        waiting = port.inWaiting()
        read_bytes = port.read(1 if waiting == 0 else waiting)
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
            #trace_function(msg)
            #raise FatalError(msg)
        #trace_function("Read %d bytes: %s", len(read_bytes), HexFormatter(read_bytes))
        for b in read_bytes:
            b = bytes([b])
            if partial_packet is None:  # waiting for packet header
                if b == b"\xc0":
                    partial_packet = b""
                else:
                    #trace_function("Read invalid data: %s", HexFormatter(read_bytes))
                    remaining_data = port.read(port.inWaiting())
                    #trace_function(
                    #    "Remaining data in serial buffer: %s",
                    #    HexFormatter(remaining_data),
                    #)
                    #detect_panic_handler(read_bytes + remaining_data)
                    #raise FatalError(
                    #    "Invalid head of packet (0x%s): "
                    #    "Possible serial noise or corruption." % hexify(b)
                    #)
            elif in_escape:  # part-way through escape sequence
                in_escape = False
                if b == b"\xdc":
                    partial_packet += b"\xc0"
                elif b == b"\xdd":
                    partial_packet += b"\xdb"
                else:
                    #trace_function("Read invalid data: %s", HexFormatter(read_bytes))
                    remaining_data = port.read(port.inWaiting())
                    #trace_function(
                    #    "Remaining data in serial buffer: %s",
                    #    HexFormatter(remaining_data),
                    #)
                    #detect_panic_handler(read_bytes + remaining_data)
                    #raise FatalError("Invalid SLIP escape (0xdb, 0x%s)" % (hexify(b)))
            elif b == b"\xdb":  # start of escape sequence
                in_escape = True
            elif b == b"\xc0":  # end of packet
                #trace_function("Received full packet: %s", HexFormatter(partial_packet))
                yield partial_packet
                partial_packet = None
                successful_slip = True
            else:  # normal byte in packet
                partial_packet += b
