from collections import deque


class SlipEncoder:
    def __init__(self):
        # declared in octal
        self.SLIP_END = 0xC0  # 0o300
        self.SLIP_ESC = 0xDB  # 0o333
        self.SLIP_ESC_END = 0xDC  # 0o334
        self.SLIP_ESC_ESC = 0xDD  # 0o335
        self.DEBUG_MAKER = 0o015
        self.MAX_MTU = 200
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


class SlipDecoder:
    SLIP_END = 0o300  # 192 0xC0
    SLIP_ESC = 0o333  # 219 0xDB
    SLIP_ESC_END = 0o334  # 220 0xDC
    SLIP_ESC_ESC = 0o335  # 221 0xDD

    def __init__(self):
        self.dataBuffer = []
        self.carry = bytes([])
        self.carryBytes = bytes([])
        self.reset = False

    def reset_for_new_buffer(self):
        self.dataBuffer = []
        self.carry = bytes([])
        self.reset = False

    def decode_from_slip(self, bytes_in):
        """
        arguments are bytes to decode
        return decode values as list or None if not available,
        carry over values are accumulated so partial messages work ok
        """
        if self.reset:
            self.reset_for_new_buffer()

        serial_fd = iter(self.carry + self.carryBytes + bytes_in)
        try:
            while True:
                serial_byte = next(serial_fd)  # could raise StopIteration, so carry better be right!
                if serial_byte == SlipDecoder.SLIP_END:
                    if len(self.dataBuffer) > 0:  # true if this is not a 'start byte'
                        self.carryBytes = bytes(serial_fd)
                        self.reset = True
                        return self.dataBuffer  # exit the while loop HERE only!
                elif serial_byte == SlipDecoder.SLIP_ESC:
                    self.carry = bytes([SlipDecoder.SLIP_ESC])
                    serial_byte = next(serial_fd)  # could raise  StopIteration, with new carry
                    if serial_byte == SlipDecoder.SLIP_ESC_END:
                        self.dataBuffer.append(SlipDecoder.SLIP_END)
                    elif serial_byte == SlipDecoder.SLIP_ESC_ESC:
                        self.dataBuffer.append(SlipDecoder.SLIP_ESC)
                    else:
                        raise ProtocolError
                else:
                    self.carry = bytes([])  # in case of  StopIteration exception at top of loop
                    self.dataBuffer.append(serial_byte)
        except StopIteration:
            self.carryBytes = bytes(serial_fd)
            return None  # here reset is false
