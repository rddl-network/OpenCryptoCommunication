import binascii

class OscCRC32():

    def __init__(self):
        self.data = None
        self.checksum = None

    def validateCRC32(self, data, checksum):
        self.data = data
        self.checksum = checksum
        
        crc = binascii.crc32(self.data) & 0xffffffff
        crc32 = hex(crc)

        if (crc32 == self.checksum):
            return(True)
        else:
            return(False)

    def generateCRC32(self, data):
        self.data = data
        
        crc = binascii.crc32(self.data) & 0xffffffff
        self.checksum = bytes(hex(crc), 'utf-8')

        return(self.checksum)

crc = OscCRC32()

data = b'GpvE85eRPk47o8t1tbtV6A=='

crc_gen = crc.generateCRC32(data)

print(crc_gen)