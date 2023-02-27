
import json

import base58
import sha3
from cryptoconditions import Ed25519Sha256

from bigchaindb_driver import BigchainDB
# bdb_root_url = 'https://ipdb3.riddleandcode.com'
bdb_root_url = 'http://localhost:9984/'
bdb = BigchainDB(bdb_root_url)

# first draft of replacing the condition mechanism inside of bigchaindb with a 
# a policy engine

# generate the keypairs/wallets for producer and the buyer
# the pacemaker will only e represented by its public key address
# derived from the attached RFID tag's EPC code

from bigchaindb_driver.crypto import generate_keypair, CryptoKeypair

# producer, buyer = generate_keypair(), generate_keypair()



producer = CryptoKeypair(private_key='6AFRuHAwt7WoAEPjrxh6xxCM2mXmpzWgiiXcXqH39bG9', public_key='H5oz16Nc26EwfsJuPMzuMjecXmE1BnhVEyPzBHoq3TV3')
buyer = CryptoKeypair(private_key='CkLMXXNZS2idkMThiT6sZNKK6hRMdc8dC4a7Q2RoR2C', public_key='7xtmRqYjv1VrkuKZ81e5pLVTCTVJpvCqbFgWRtrDdiDC')


print(producer.private_key)
print(producer.public_key)
print(buyer.private_key)
print(buyer.public_key)

version = '2.0'

# CRYPTO-CONDITIONS: instantiate an Ed25519 crypto-condition for producer
producer_ed25519 = Ed25519Sha256(public_key=base58.b58decode(producer.public_key))

# CRYPTO-CONDITIONS: instantiate an Ed25519 crypto-condition for buyer
buyer_ed25519 = Ed25519Sha256(public_key=base58.b58decode(buyer.public_key))

# CRYPTO-CONDITIONS: generate the condition uris
producer_condition_uri = producer_ed25519.condition.serialize_uri()
buyer_condition_uri = buyer_ed25519.condition.serialize_uri()

# CRYPTO-CONDITIONS: get the unsigned fulfillment dictionary (details)
producer_unsigned_fulfillment_dict = {
    'type': producer_ed25519.TYPE_NAME,
    'public_key': base58.b58encode(producer_ed25519.public_key).decode(),
}

buyer_unsigned_fulfillment_dict = {
    'type': buyer_ed25519.TYPE_NAME,
    'public_key': base58.b58encode(buyer_ed25519.public_key).decode(),
}

producer_output = {
    'amount': '2000',
    'composite_amount': {
        "carbon_offset": "250",
        "C71": "1000",
        "C72": "40",
        "C73": "7000",
        "C74": "14",
        "C75": "1800",
        "C76": "300",
        "C77": "100",
        "C78": "200",
        "C79": "70",
        "C80": "20",
        "C81": "300",
        "C82": "20",
        "C83": "20",
        "C86": "10",
        "C93": "3000"
    }
    'condition': {
        'details': producer_unsigned_fulfillment_dict,
        'uri': producer_condition_uri,
    },
    'script': '',
    'keys': '',
    'data': '',
    'conf': '',
    'verbosity': '0',
    'public_keys': (producer.public_key,),
}

buyer_output = {
    'amount': '400',
    'composite_amount': {
        "carbon_offset": "50"
        "C71": "500", 
        "C72": "10",
        "C73": "3000",
        "C74": "4",
        "C75": "286",
        "C76": "89",
        "C77": "22",
        "C78": "26",
        "C79": "11",
        "C80": "9",
        "C81": "103",
        "C82": "11",
        "C83": "4",
        "C86": "7",
        "C93": "361",
    }
    'condition': {
        'details': buyer_unsigned_fulfillment_dict,
        'uri': buyer_condition_uri,
    },
    'script': '',
    'keys': '',
    'data': '',
    'conf': '',
    'verbosity': '0',
    'public_keys': (buyer.public_key,),
}

input_ = {
    'fulfillment': None,
    'fulfills': {
        # 'transaction_id': token_creation_tx['id'],
        'transaction_id': 'f1cc4d66ac892cdeb2f3cc82f3513d6d18267984dd1505c6a6b7a986050a378a',
        'output_index': 0,
    },
    'owners_before': (buyer.public_key,)
}

token_transfer_tx = {
    'operation': 'TRANSFER_COMPOSE',
    # 'asset': {'id': token_creation_tx['id']},
    'asset': {'id': 'f1cc4d66ac892cdeb2f3cc82f3513d6d18267984dd1505c6a6b7a986050a378a'},
    'metadata': None,
    'outputs': (producer_output, buyer_output),
    'inputs': (input_,),
    'version': version,
    'id': None,
}

# JSON: serialize the transaction-without-id to a json formatted string
message = json.dumps(
    token_transfer_tx,
    sort_keys=True,
    separators=(',', ':'),
    ensure_ascii=False,
)

message = sha3.sha3_256(message.encode())

message.update('{}{}'.format(
    token_transfer_tx['inputs'][0]['fulfills']['transaction_id'],
    token_transfer_tx['inputs'][0]['fulfills']['output_index']).encode()
)

# CRYPTO-CONDITIONS: sign the serialized transaction-without-id for buyer
buyer_ed25519.sign(message.digest(), base58.b58decode(buyer.private_key))

# CRYPTO-CONDITIONS: generate producer' fulfillment uri
fulfillment_uri = buyer_ed25519.serialize_uri()

# add producer' fulfillment uri (signature)
token_transfer_tx['inputs'][0]['fulfillment'] = fulfillment_uri

# JSON: serialize the id-less transaction to a json formatted string
json_str_tx = json.dumps(
    token_transfer_tx,
    sort_keys=True,
    separators=(',', ':'),
    ensure_ascii=False,
)

# SHA3: hash the serialized id-less transaction to generate the id
shared_transfer_txid = sha3.sha3_256(json_str_tx.encode()).hexdigest()

# add the id
token_transfer_tx['id'] = shared_transfer_txid

# send CREATE tx into the bdb network
returned_transfer_tx = bdb.transactions.send_async(token_transfer_tx)

print(returned_transfer_tx)