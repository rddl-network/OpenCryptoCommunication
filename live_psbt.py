from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import binascii
import base64
import hashlib
import json
import time
import six
import sys
import os
import wallycore as wally

rpc_port = 18884
rpc_user = 'nestor'
rpc_password = 'nestor'

ASSET_A = "8eca97f4ed8c894905ae82eadf8b6e5ff10adfcea150250cf9889bc4eb8fac5c"
ASSET_B = "cb186efd4ed52a78204482787b98ee967d5940c7b369503fad30694363f99a48"

TXID_A  = "0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b"

try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    ADDRESS_INFO = rpc_connection.getaddressinfo("FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv")
        

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

ADRESS = ADDRESS_INFO['address']
SCRIPT_PUB_KEY = ADDRESS_INFO['scriptPubKey']

print(F"ADRESS INFO: {ADDRESS_INFO}")
print(ADDRESS_INFO['address'])
print(ADDRESS_INFO['scriptPubKey'])

try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    VOUT = rpc_connection.gettransaction("0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b")
        

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

# print(VOUT)
print(F'VOUT DETAILS: {VOUT["details"][0]}')
print(VOUT["details"][0]['vout'])

try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    #TXU = rpc_connection.createrawtransaction([{"txid":"0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b","vout":VOUT["details"][0]['vout'],"sequence":0}], [{"FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv":20,"asset":"cb186efd4ed52a78204482787b98ee967d5940c7b369503fad30694363f99a48"}], 0, True)
    TXU = rpc_connection.createrawtransaction([{"txid":"0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b","vout":VOUT["details"][0]['vout'],"sequence":0}], [{"FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv":20,"FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv":"cb186efd4ed52a78204482787b98ee967d5940c7b369503fad30694363f99a48"}], 0, True)
  

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

print(TXU)

# vtSKPPjnpyrAp7x7Q6uBbxLfZFioZYeJFiMedFmPhrEhZ7JudZn4Y2oYJkjZhYyMmFaFqxYSLyTR6TzP

try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    PRIVATEKEY = rpc_connection.dumpprivkey("vtSKPPjnpyrAp7x7Q6uBbxLfZFioZYeJFiMedFmPhrEhZ7JudZn4Y2oYJkjZhYyMmFaFqxYSLyTR6TzP")
    PRIVATEKEY2 = rpc_connection.dumpprivkey("vtSDUydsj7NfD744VCoeAntMKobEJ8pgSJqwcHKxV2fKv34ALbzT1oW4j8LY7kPyMoBWgzvGn8qLfM4L")
        

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

print(PRIVATEKEY)
print(PRIVATEKEY2)


try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    TXS = rpc_connection.signrawtransactionwithkey(TXU, [PRIVATEKEY], [{"txid":"0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b","vout":1,"scriptPubKey":"76a914726963e8c7c4ed114ff98ee43d28573fd226f3dc88ac"}], "SINGLE|ANYONECANPAY" )
except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

print(F'Partly signed bitcoin transaction by RDDLtoek wallet: {TXS}')

"""
try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    ADDRESS_TAKER = rpc_connection.getnewaddress("WRAPPEDtoken", "legacy")
except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

print(ADDRESS_TAKER)
"""

AMOUNT_B = 10

ADDRESS_TAKER = "vtSDUydsj7NfD744VCoeAntMKobEJ8pgSJqwcHKxV2fKv34ALbzT1oW4j8LY7kPyMoBWgzvGn8qLfM4L"
"""
try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    TXID_B = rpc_connection.sendtoaddress(ADDRESS_TAKER, AMOUNT_B, "", "", False, True, 1, "UNSET", False, ASSET_B)
except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

print(TXID_B)
"""

TXID_B = "efd063c4f9c56d3207723866305a99aecbc482146f72d0b82e026ac72d4e8fc3"

try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    VOUT = rpc_connection.gettransaction(TXID_B)
        

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))


VOUT_B = VOUT["details"][0]['vout']

print(VOUT["details"][0])
print(VOUT["details"][0]['vout'])

'''
TXID_FEE=$(ec sendtoaddress $ADDRESS_TAKER $(ec getbalance | jq .bitcoin) "" "" true)
VOUT_FEE=$(ec gettransaction $TXID_FEE | jq .details | jq .[0].vout)
'''

TXID_FEE = '726f08f46366da554a5bdba6012d4f3fadcc415a0fe7a3293ad304b5b5bbc44a'

'''
try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    TXID_FEE = rpc_connection.sendtoaddress(ADDRESS_TAKER, 0.005, "", "", True, True)
except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))

'''

print(F'TXID FEE: {TXID_FEE}')

try:
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
    VOUT = rpc_connection.gettransaction(TXID_FEE)
        

except JSONRPCException as json_exception:
    print("A JSON RPX exception occured: " + str(json_exception))
except Exception as general_exception:
    print("An exception occured: " + str(general_exception))


VOUT_FEE = VOUT["details"][0]['vout']
print(VOUT_FEE)



rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:%s"%(rpc_user, rpc_password, rpc_port))
VOUT = rpc_connection.gettransaction(TXID_FEE)

print(VOUT["details"][0]['vout'])   
print(VOUT["details"][0])

x = float(10)
y = float(10)

A = "8eca97f4ed8c894905ae82eadf8b6e5ff10adfcea150250cf9889bc4eb8fac5c"
B = "cb186efd4ed52a78204482787b98ee967d5940c7b369503fad30694363f99a48"

txidB = TXID_B
voutB = int(VOUT_B)
txidFEE = TXID_FEE

amountB = float(AMOUNT_B)
voutFEE = int(VOUT_FEE)

amountFEE = float(0.00050000)

FEE = '144c654344aa716d6f3abcc1ca90e5641e4e2a7f633bc09fe3baf64585819a49'

fixed_fee = 0.00005000

print(TXS)
tx = wally.tx_from_hex(TXS['hex'], 3)

address_taker = ADDRESS_TAKER
scriptpubkey = wally.address_to_scriptpubkey('FeNiDXGgNWPwtkQcXAURjyZtHAduePw2fx', wally.WALLY_NETWORK_LIQUID_TESTNET)
print(binascii.hexlify(scriptpubkey))

def h2b_rev(h):
    return wally.hex_to_bytes(h)[::-1]

def btc2sat(btc):
    return round(btc * 10**8)

def add_unblinded_output(tx_, script, asset, amount):
    wally.tx_add_elements_raw_output(
        tx_,
        script,
        b'\x01' + h2b_rev(asset),
        wally.tx_confidential_value_from_satoshi(btc2sat(amount)),
        None, # nonce
        None, # surjection proof
        None, # range proof
        0)

def add_unsigned_input(tx_, txid, vout):
    wally.tx_add_elements_raw_input(
        tx_,
        h2b_rev(txid),
        vout,
        0xffffffff,
        None, # scriptSig
        None, # witness
        None, # nonce
        None, # entropy
        None, # issuance amount
        None, # inflation keys
        None, # issuance amount rangeproof
        None, # inflation keys rangeproof
        None, # pegin witness
        0)

fixed_fee = 0.00005000

#add output A
add_unblinded_output(tx, scriptpubkey, A, x)
#add output change B
add_unblinded_output(tx, scriptpubkey, B, amountB - y)
#add output change FEE
add_unblinded_output(tx, scriptpubkey, FEE, amountFEE - fixed_fee)
#add output FEE
add_unblinded_output(tx, None, FEE, fixed_fee)
#add input B
add_unsigned_input(tx, txidB, voutB)
#add input FEE
add_unsigned_input(tx, txidFEE, voutFEE)
#print tx
print()

TX_TAKER_U = wally.tx_to_hex(tx, 3)

TX_TAKER = rpc_connection.signrawtransactionwithkey(TX_TAKER_U, [PRIVATEKEY2])

print(TX_TAKER)