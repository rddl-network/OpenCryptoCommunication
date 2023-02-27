from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class OscAES():

    def __init__(self):
        # self.key = get_random_bytes(32)
        # pre provisioned key
        self.key = b'c6ad69d30213251ed206e11024ff0a8d'
        #print(self.key)
        self.data = None

    def encodeToAES(self, data):
        self.data = data
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')

        #print(ct)

        '''
        print(result)
        print("")
        print(b64encode(data).decode('utf-8'))
        print(b64encode(key).decode('utf-8'))
        '''

        return(iv, ct)

    def decodeFromAES(self, iv, ct):
        iv = b64decode(iv)
        ciphertext = b64decode(ct)
        # iv = b64decode(b64['iv'])
        # ct = b64decode(b64['ciphertext'])
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return(pt)

aes = OscAES()
aes_enc = aes.encodeToAES(b"hello tom how is the da today with you daughters. they are cute and smart girls.hello tom how is the da today with you daughters. they are cute and smart girls.hello tom how is the da today with you daughters. they are cute and smart girls.")
aes_dec = aes.decodeFromAES(aes_enc[0], aes_enc[1])

print(F'AES encoded data: {aes_enc}')
print(F'AES decoded data: {aes_dec}')
print(F'AES msg length: {len(aes_dec)}')
