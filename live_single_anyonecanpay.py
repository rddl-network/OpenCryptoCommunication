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

ADR_UNCONF = rpc_connection.getnewaddress("RDDLtoken")
print(F'New confidential address: {ADR_UNCONF}')

ADR_UNCONF_INFO = rpc_connection.getaddressinfo(ADR_UNCONF)
print(F'Unconfidential address info: {ADR_UNCONF_INFO["unconfidential"]}')
print(F'Unconfidential address info: {ADR_UNCONF_INFO}')

TX_UNCONF = rpc_connection.sendtoaddress(ADR_UNCONF_INFO["unconfidential"], 0.0123, "", "", False, True, 1, "UNSET", False, '8eca97f4ed8c894905ae82eadf8b6e5ff10adfcea150250cf9889bc4eb8fac5c' )
print(F'Unconfidential tx info: {TX_UNCONF}')
# the 5th argument concerning fees has to be false. Otherwise it would be tried to pay the transaction with non-L-BTC
# which is not possible

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
    TXU = rpc_connection.createrawtransaction([{"txid":"0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b","vout":VOUT["details"][0]['vout'],"sequence":'0xffffffff'}], [{"FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv":9.0}], 0, True)
    #  TXU = rpc_connection.createrawtransaction([{"txid":"0bac58023274dee4f157dc5ccc67a0a71d57ff0a3d4ec49031b70c8f2e33876b","vout":VOUT["details"][0]['vout'],"sequence":0}], [{"FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv":20,"FfbfjRVGrD7FkVLwzRwsQefAz7jLvvuinv":"cb186efd4ed52a78204482787b98ee967d5940c7b369503fad30694363f99a48"}], 0, True)
  

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

print(F'Partly signed bitcoin transaction by RDDLtoek wallet: {TXS["hex"]}')

MEMPOOL = rpc_connection.testmempoolaccept([TXS["hex"]])
print(F'MEMPOOL ACCEPT: {MEMPOOL}')

