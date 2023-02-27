
import json

import base58
from hashlib import sha3_256 as sha3

from cryptoconditions import Ed25519Sha256, ZenroomSha256

from zenroom import zenroom_exec, zencode_exec


from bigchaindb_driver import BigchainDB
# bdb_root_url = 'https://ipdb3.riddleandcode.com'
bdb_root_url = 'http://localhost:9984/'
bdb = BigchainDB(bdb_root_url)

# generate the keypairs/wallets for producer and the buyer
# the pacemaker will only e represented by its public key address
# derived from the attached RFID tag's EPC code

from bigchaindb_driver.crypto import generate_keypair, CryptoKeypair

producer, buyer = generate_keypair(), generate_keypair()

# producer = CryptoKeypair(private_key='2KF5Qx4ksFWQ7j7DgTj1jYhQ6eoP38WoyFVMjTR5hDgK', public_key='2KF5Qx4ksFWQ7j7DgTj1jYhQ6eoP38WoyFVMjTR5hDgK')
print(producer.private_key)
print(producer.public_key)
print(buyer.private_key)
print(buyer.public_key)

# producer = CryptoKeypair(private_key='2KF5Qx4ksFWQ7j7DgTj1jYhQ6eoP38WoyFVMjTR5hDgK', public_key='2KF5Qx4ksFWQ7j7DgTj1jYhQ6eoP38WoyFVMjTR5hDgK')
# print(producer.private_key)

# buyer = CryptoKeypair(private_key='ASHwLY9zG43rNkCZgRFBV6K9j9oHM1joxYMxHRiNyPja', public_key='A7fpfDpaGkJubquXbj3cssMhx5GQ1599Sxc7MxR9SWa8')

# a dummy private key is used for the pacemaker, as it is of no importance
# the public key address is the one from the initial rfid_producer.py code

elements = CryptoKeypair(private_key='00000000000000000000000000000000000000000000', public_key='5bxnttfSNScCL2YtKWXKfya1uMq1TEg9nznX7cnKFiPR')
print(elements.public_key)

# create a digital asset for producer
# for readability we turn the original EPC code into capital hex chars

asset = {
    'data': {
        "Certificate": {
        "A03": "0000001",
        "A01": {
            "CompanyName": "voestalpine Krems GmbH",
            "AddressLine": "Schmidhüttenstrasse 5",
            "ZipCode": "3500",
            "City": "Krems",
            "Country": "AT",
            "VAT_Id": "U36909609"
        },
        "B01": "EN10025",
        "B02": "S275J2H",
        "B07": "175508",
        "B13": "24000",
        "Z02": "2019-05-30T09:30:10-01:00"   
        }
    }
}

metadata = {
    "Production_output": {
            "Unit": 'tonnes',
            "Amount": 30
    },
    "Carbon_Offset_Certificate": {
            "Unit": 'tonnes',
            "Amount": 2.7
    },
}

version = '2.0'

script = """Scenario 'certificate': "Attest chemical composition and carbon credit "
    Given 
        that the signal is 'BO_ 292 SteelToBeneficiary 8 RNCSTEEL  SG_ SteelToBeneficiaryApdu : 47|16@0+ (1,0) [0|0] "tonnes" RNCSTEEL'
        and that the hash is given
        and that the threshold is given
        and that the output is given
        and the machine signature is given
        and the machine publicKey is given
        and the receiverAddress is given
        and the amountToIssue is given
    When 
        the hash equals '0xa9bd136f9df549e1e3807ffa39ca5e135556d48fe8cc30e61fc41355d04210ff'
        and the output isBiggerThan threshold
        and the signature equals '0x3044022002748547ba97e986d26b48dc2093c21f04334aea4694470328d605c15971a8f302207501b30f114d1c27e5d8fa903635d9485dca60c705dbdf2a12daf795239d5e5e'
        and the signature validates with publicKey and hash
    Then 
        issue amountToIssue to receiverAddress
        and print all data
"""

# CRYPTO-CONDITIONS: instantiate an Ed25519 crypto-condition for buyer
### ed25519 = Ed25519Sha256(public_key=base58.b58decode(buyer.public_key))

ed25519 = ZenroomSha256(script="")


# CRYPTO-CONDITIONS: generate the condition uri
condition_uri = ed25519.condition.serialize_uri()

# CRYPTO-CONDITIONS: construct an unsigned fulfillment dictionary
unsigned_fulfillment_dict = {
    'type': ed25519.TYPE_NAME,
    ### 'public_key': base58.b58encode(ed25519.public_key).decode(),
    'script': "",
}

output = {
    'amount': '2400',
    'composite_amount': {
        "carbon_offset": "300",
        "C71": "1500", # "0.1500",
        "C72": "50", # "0.0050",
        "C73": "10000", # "1.0000",
        "C74": "18", # "0.0018",
        "C75": "2086", # "0.2086",
        "C76": "389", # "0.0389",
        "C77": "122", # "0.0122",
        "C78": "226", # "0.0226",
        "C79": "81", # "0.0081",
        "C80": "29", # "0.0029",
        "C81": "403", # "0.0403",
        "C82": "31", # "0.0031",
        "C83": "24", # "0.0024",
        "C86": "17", # "0.017",
        "C93": "3361", # "0.3361",
    }
    'condition': {
        'details': unsigned_fulfillment_dict,
        'uri': condition_uri,
    },
    'script': script,
    'keys': '',
    'data': '',
    'conf': '',
    'public_keys': (buyer.public_key,),
}

input_ = {
    'fulfillment': None,
    'fulfills': None,
    'owners_before': (producer.public_key,)
}

token_creation_tx = {
    'operation': 'CREATE_COMPOSE',
    'asset': asset,
    'metadata': None,
    'outputs': (output,),
    'inputs': (input_,),
    'version': version,
    'id': None,
}

# JSON: serialize the transaction-without-id to a json formatted string
message = json.dumps(
    token_creation_tx,
    sort_keys=True,
    separators=(',', ':'),
    ensure_ascii=False,
)

message = sha3.sha3_256(message.encode())

# CRYPTO-CONDITIONS: sign the serialized transaction-without-id
### ed25519.sign(message.digest(), base58.b58decode(producer.private_key))

# CRYPTO-CONDITIONS: generate the fulfillment uri
fulfillment_uri = ed25519.serialize_uri()

# add the fulfillment uri (signature)
token_creation_tx['inputs'][0]['fulfillment'] = fulfillment_uri
print(token_creation_tx)

# JSON: serialize the id-less transaction to a json formatted string
json_str_tx = json.dumps(
    token_creation_tx,
    sort_keys=True,
    separators=(',', ':'),
    ensure_ascii=False,
)

# SHA3: hash the serialized id-less transaction to generate the id
shared_creation_txid = sha3.sha3_256(json_str_tx.encode()).hexdigest()

# add the id
token_creation_tx['id'] = shared_creation_txid

# send CREATE tx into the bdb network
##returned_creation_tx = bdb.transactions.send_async(token_creation_tx)

##print(returned_creation_tx)