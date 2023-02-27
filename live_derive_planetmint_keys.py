import planetmint_wallet.keymanagement as wallet
import binascii
import sys

def derive_keys ( argv):
    seed = wallet.mnemonic_to_seed ( argv[1])
    master_key, _ = wallet.seed_to_extended_key ( seed)

    '''
     derv_key = wallet.derive_from_path ( master_key, 'm/44h/8630h/1h/0/')
    '''

    return binascii.hexlify( master_key).decode()

def show_argv ( argv):
    return ( binascii.hexlify( argv[1]).decode())

if __name__ == '__main__':
    print ( derive_keys ( sys.argv))

"""

python3.10 /home/nestor/libwally-core/src/test/live_derive_planetmint_keys.py 'planet art art art art art alert'

"""