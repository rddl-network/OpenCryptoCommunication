import subprocess
import sys


def register(argv):

    ASSET_ID = str(argv[1])
    CONTRACT = str(argv[2])


    # register_request = ['curl', 'https://assets.blockstream.info/', '-H', 'Content-Type: application/json', '-d', F'{{"asset_id":"{ASSET_ID}","contract":{CONTRACT}}}']
    register_request = ['curl', 'https://assets-testnet.blockstream.info/', '-H', 'Content-Type: application/json', '-d', F'{{"asset_id":"{ASSET_ID}","contract":{CONTRACT}}}']

    # For registering the asset within Blockstream's asset registry
    register_response = subprocess.run(register_request, capture_output=True)


    if (register_response.returncode == 0):
        print ( register_response.stdout.decode ( 'ASCII'))
    else:
        print ( register_response.returncode)

    return ( register_response.stdout.decode ( 'ASCII'))



def show(argv):
    n0 = str(argv[1])
    n1 = str(argv[2])

    return ( [ n0, n1])


if __name__ == '__main__':
    print ( register(sys.argv))


"""

python3.10 '/home/nestor/libwally-core/src/test/live_register2liquid_testnet.py' 6fc8c3ff46af3ba1131e68dea482919ec4e56d735c3db34bf0c51b069e5c26cb '{"entity":{"domain":"lab.r3c.network"}, "issuer_pubkey":"0343ce8039395ec16676bf2e08911ed5ccdedc05033b3758a2ef37eb8bd7848a11", "name":"Transport Token", "precision":0, "ticker":"L-TRNS", "version":0}'

"""