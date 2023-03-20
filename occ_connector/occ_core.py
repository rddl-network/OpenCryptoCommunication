#!/usr/bin/python3

import serial
import sys
import struct
import math
from time import sleep

# from occAES import *
# from occCRC32 import *


class OSCProcessor:
    def __init__(self):
        self.fDict = {"/i": self.doSingleton, "/iif": self.doStruct}

    def doSingleton(self, singletonLis):
        print(singletonLis[0])

    def doStruct(self, structLis):
        adcChid = structLis[0]
        timeStamp = structLis[1]
        value = round(structLis[2], 3)
        print(adcChid, timeStamp, value)

    def dispatchOSCList(self, oscLis):
        self.fDict[oscLis[0]](oscLis[2:])


def hexDump(bytes):
    """Useful utility; prints the string in hexadecimal"""
    for i in range(len(bytes)):
        sys.stdout.write("%2x " % (ord(bytes[i])))
        if (i + 1) % 8 == 0:
            print(repr(bytes[i - 7 : i + 1]))

    if len(bytes) % 8 != 0:
        str = ""
        print(str.rjust(14, " "), repr(bytes[i - len(bytes) % 8 : i + 1]))


class OSCMessage:
    """Builds typetagged OSC messages."""

    def __init__(self):
        self.address = ""
        self.typetags = ","
        self.message = ""

    def setAddress(self, address):
        self.address = address

    def setMessage(self, message):
        self.message = message

    def setTypetags(self, typetags):
        self.typetags = typetags

    def clear(self):
        self.address = ""
        self.clearData()

    def clearData(self):
        self.typetags = ","
        self.message = ""

    def append(self, argument, typehint=None):
        """Appends data to the message,
        updating the typetags based on
        the argument's type.
        If the argument is a blob (counted string)
        pass in 'b' as typehint."""

        if typehint == "b":
            binary = OSCBlob(argument)
        elif typehint == "a":
            binary = OSCAESArgument(argument)
        else:
            binary = OSCArgument(argument)
            # print(argument)
            # print(binary)

        self.typetags = self.typetags + binary[0]
        self.rawAppend(binary[1])

    def rawAppend(self, data):
        """Appends raw data to the message.  Use append()."""
        # print(type(data))
        self.message = self.message + str(data)

    def getBinary(self):
        """Returns the binary message (so far) with typetags."""
        address = OSCArgument(self.address)[1]
        typetags = OSCArgument(self.typetags)[1]
        return address + typetags + self.message

    def __repr__(self):
        return self.getBinary()


def readString(data):
    length = str.find(data.decode("utf_8"), "\x00")
    nextData = int(math.ceil((length + 1) / 4.0) * 4)
    return (data[0:length].decode("utf-8"), data[nextData:])


def readTimeTag(data):
    """Tries to interpret the next 8 bytes of the data
    as a TimeTag.
    """
    high, low = struct.unpack(">LL", data[0:8])
    if (high == 0) and (low <= 1):
        time = 0.0
    else:
        time = int(NTP_epoch + high) + float(low / NTP_units_per_second)
    rest = data[8:]
    return (time, rest)


def readBlob(data):
    length = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4 : length + 4], data[nextData:])


def readInt(data):
    if len(data) < 4:
        print("Error: too few bytes for int", data, len(data))
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest = data[4:]

    return (integer, rest)


def readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer."""
    high, low = struct.unpack(">ll", data[0:8])
    big = (long(high) << 32) + low
    rest = data[8:]
    return (big, rest)


def readDouble(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit double float."""
    floater = struct.unpack(">d", data[0:8])
    big = float(floater[0])
    rest = data[8:]
    return (big, rest)


def readFloat(data):
    if len(data) < 4:
        print("Error: too few bytes for float", data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest = data[4:]

    return (float, rest)


def readBlob(data):
    """Reads the next (numbered) block of data"""
    length = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4 : length + 4], data[nextData:])


def readTrue(data):
    bool = True
    rest = data[2:]
    return (bool, rest)


def readFalse(data):
    bool = False
    rest = data[2:]
    return (bool, rest)


def readAESCRC32(data):
    bool = False
    rest = data[2:]
    return (bool, rest)


def readAES(data):
    """cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    rest = data[2:]
    return (bool, rest)"""

    length = str.find(data.decode("utf-8"), "\x00")
    nextData = int(math.ceil((length + 1) / 4.0) * 4)
    return (data[0:length].decode("utf_8"), data[nextData:])


def readCRC32(data):
    bool = False
    rest = data[2:]
    return (bool, rest)


def readASN1(data):
    bool = False
    rest = data[2:]
    return (bool, rest)


def OSCBlob(next):
    """Convert a string into an OSC Blob,
    returning a (typetag, data) tuple."""
    if type(next) == type(""):
        length = len(next)
        padded = math.ceil((len(next)) / 4.0) * 4
        binary = struct.pack(">i%ds" % (padded), length, next)
        binary = binary.decode("utf-8", "replace")
        tag = "b"
    else:
        tag = ""
        binary = ""

    return (tag, binary)


def OSCArgument(next):
    """Convert some Python types to their
    OSC binary representations, returning a
    (typetag, data) tuple."""

    if type(next) == type(""):
        # next = hex(192) + next + hex(192)
        OSCstringLength = math.ceil((len(next) + 1) / 4.0) * 4
        next = next.encode("utf-8")
        binary = struct.pack(">%ds" % (OSCstringLength), next)
        binary = binary.decode("utf-8", "replace")
        tag = "s"
    elif type(next) == type(42.5):
        binary = struct.pack(">f", next)
        binary = binary.decode("utf-8", "replace")
        tag = "f"
    elif type(next) == type(13):
        binary = struct.pack(">i", next)
        binary = binary.decode("utf-8", "replace")
        tag = "i"
    else:
        binary = ""
        tag = ""

    return (tag, binary)


def OSCAESArgument(next):
    aes256 = OscAES()

    if type(next) == type(""):
        next = next.encode("utf-8")
        aesRespTuple = aes256.encodeToAES(next)
        aesResp = aesRespTuple[0] + aesRespTuple[1]
        print(aesRespTuple[0])
        print(aesRespTuple[1])
        OSCstringLength = math.ceil((len(aesResp) + 1) / 4.0) * 4
        aesResp = aesResp.encode("utf-8")

        binary = struct.pack(">%ds" % (OSCstringLength), aesResp)
        binary = binary.decode("utf-8", "replace")
        tag = "a"

    return (tag, binary)


def OSCAESCRC32Argument(next):
    pass


def OSCCRC32Argument(next):
    pass


def OSCASN1Argument(next):
    pass


def parseArgs(args):
    """Given a list of strings, produces a list
    where those strings have been parsed (where
    possible) as floats or integers."""
    parsed = []
    for arg in args:
        # print( arg)
        arg = arg.strip()
        interpretation = None
        try:
            interpretation = float(arg)
            if string.find(arg, ".") == -1:
                interpretation = int(interpretation)
        except:
            # Oh - it was a string.
            interpretation = arg
            pass
        parsed.append(interpretation)
    return parsed


class BundleNotSupported(Exception):
    pass


def decodeOSC(data):
    """Converts a typetagged OSC message to a Python list."""
    table = {
        "i": readInt,
        "f": readFloat,
        "s": readString,
        "b": readBlob,
        "d": readDouble,
        "F": readFalse,
        "T": readTrue,
        "A": readAESCRC32,
        "a": readAES,
        "r": readCRC32,
        "n": readASN1,
    }
    decoded = []
    address, rest = readString(data)
    typetags = ""

    if address == "#bundle":
        print("BUNDLE not Supported!")
        raise BundleNotSupported
        time, rest = readLong(rest)
        #       decoded.append(address)
        #       decoded.append(time)
        while len(rest) > 0:
            length, rest = readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest) > 0:
        typetags, rest = readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if typetags[0] == ",":
            for tag in typetags[1:]:
                value, rest = table[tag](rest)
                decoded.append(value)
        else:
            print("Oops, typetag lacks the magic ,")

    return decoded


class CallbackManager:
    """This utility class maps OSC addresses to callables.

    The CallbackManager calls its callbacks with a list
    of decoded OSC arguments, including the address and
    the typetags as the first two arguments."""

    def __init__(self):
        self.callbacks = {}
        self.add(self.unbundler, "#bundle")

    def handle(self, data, source=None):
        """Given OSC data, tries to call the callback with the
        right address."""
        decoded = decodeOSC(data)
        self.dispatch(decoded, source)

    def dispatch(self, message, source=None):
        """Sends decoded OSC data to an appropriate calback"""
        try:
            if type(message[0]) == str:
                # got a single message
                address = message[0]
                self.callbacks[address](message, source)

            elif type(message[0]) == list:
                # smells like nested messages
                for msg in message:
                    self.dispatch(msg, source)

        except KeyError as e:
            # address not found
            print("address %s not found " % address)
            pprint.pprint(message)
        except IndexError as e:
            print("got malformed OSC message")
            pass
        except None as e:
            print("Exception in", address, "callback :", e)

        return

    def add(self, callback, name):
        """Adds a callback to our set of callbacks,
        or removes the callback with name if callback
        is None."""
        if callback == None:
            del self.callbacks[name]
        else:
            self.callbacks[name] = callback

    def unbundler(self, messages):
        """Dispatch the messages in a decoded bundle."""
        # first two elements are #bundle and the time tag, rest are messages.
        for message in messages[2:]:
            self.dispatch(message)
