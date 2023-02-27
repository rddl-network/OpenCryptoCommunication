import termios
import serial
import struct
from collections import deque


class SlipEncoder():

    def __init__(self):
        # declared in octal  
        self.SLIP_END     = 0xC0 #0o300 
        self.SLIP_ESC     = 0xDB #0o333
        self.SLIP_ESC_END = 0xDC #0o334
        self.SLIP_ESC_ESC = 0xDD #0o335
        self.DEBUG_MAKER  = 0o015
        self.MAX_MTU      = 200
        self.readBufferQueue = deque([])
        self.tempSLIPBuffer = []

    # This function takes a byte list, encode it in SLIP protocol and return the encoded byte list  
    def encodeToSLIP(self, byteList):
        
        self.tempSLIPBuffer.append(self.SLIP_END)
        for i in byteList:
            if i == self.SLIP_END:
                self.tempSLIPBuffer.append(self.DEBUG_MAKERSLIP_ESC)
                self.tempSLIPBuffer.append(self.SLIP_ESC_END)
            elif i == self.SLIP_ESC:
                self.tempSLIPBuffer.append(self.SLIP_ESC)
                self.tempSLIPBuffer.append(self.SLIP_ESC_ESC)
            else:
                self.tempSLIPBuffer.append(i)
                
        self.tempSLIPBuffer.append(self.SLIP_END)
        return self.tempSLIPBuffer

class ProtocolError(Exception):
    pass

class SlipDecoder():
    SLIP_END     = 0o300   # 192 0xC0
    SLIP_ESC     = 0o333   # 219 0xDB
    SLIP_ESC_END = 0o334   # 220 0xDC
    SLIP_ESC_ESC = 0o335   # 221 0xDD
    
    def __init__(self):
        self.dataBuffer = []
        self.carry      = bytes([])
        self.carryBytes = bytes([])
        self.reset      = False
        
    def resetForNewBuffer(self):
        self.dataBuffer = []
        self.carry = bytes([])
        self.reset = False

    def decodeFromSLIP(self,bytesIn): 
        """
        arguments are bytes to decode
        return decode values as list or None if not available,
        carry over values are accumulated so partial messages work ok
        """
        if self.reset:
            self.resetForNewBuffer()

        serialFD=iter(self.carry + self.carryBytes + bytesIn)
        try:        
            while True:
                serialByte = next(serialFD)           ## could raise StopIteration, so carry better be right!
                if serialByte == SlipDecoder.SLIP_END:
                    if len(self.dataBuffer) > 0:       ## true if this is not a 'start byte'
                        self.carryBytes=bytes(serialFD)
                        self.reset = True
                        return self.dataBuffer         ## exit the while loop HERE only!
                elif serialByte == SlipDecoder.SLIP_ESC:
                    self.carry = bytes([SlipDecoder.SLIP_ESC])
                    serialByte = next(serialFD)        ## could raise  StopIteration, with new carry
                    if serialByte == SlipDecoder.SLIP_ESC_END:
                        self.dataBuffer.append(SlipDecoder.SLIP_END)
                    elif serialByte == SlipDecoder.SLIP_ESC_ESC:
                        self.dataBuffer.append(SlipDecoder.SLIP_ESC)
                    else:
                        raise ProtocolError
                else:
                    self.carry=bytes([])    ## in case of  StopIteration exception at top of loop
                    self.dataBuffer.append(serialByte)
        except StopIteration:
            self.carryBytes = bytes(serialFD)
            return None  # here reset is false