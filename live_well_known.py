import paramiko
import sys


def well_known(argv):

    privk = paramiko.Ed25519Key.from_private_key_file('/home/nestor/.ssh/id_ed25519')

    Client = paramiko.SSHClient()
    Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    Client.connect(hostname='lab.r3c.network',username='ubuntu', pkey=privk)

    ssh_stdin, ssh_stdout, ssh_stderr = Client.exec_command('ls /var/www/html/.well-known/')
    response = ssh_stdout.readlines()

    ASSET_ID = str(argv[1])
    #ASSET_ID = 'ddf8c4c47b19b4cc99f421d4ac826a41a3f8de153f78ae43a6bd1e26df0d6f94'
    ASSET_ID_STRING = "Authorize linking the domain name lab.r3c.network to the Liquid asset " + ASSET_ID

    #create_file = 'touch /var/www/html/.well-known/liquid-asset-proof-' + ASSET_ID
    print(F'touch /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    ssh_stdin, ssh_stdout, ssh_stderr = Client.exec_command(F'touch /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    response = ssh_stdout.readlines()

    print(F'echo {ASSET_ID_STRING} | sudo tee -a /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    ssh_stdin, ssh_stdout, ssh_stderr = Client.exec_command(F'echo {ASSET_ID_STRING} | sudo tee -a /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    response = ssh_stdout.readlines()

    Client.close()
    ssh_stdin.close()

    return ( response)

def show(argv):
    n0 = str(argv[1])

    return ( [ n0])


if __name__ == '__main__':
    print ( well_known(sys.argv))


"""

/home/nestor/libwally-core/src/test/live_well_known.py 'ddf8c4c47b19b4cc99f421d4ac826a41a3f8de153f78ae43a6bd1e26df0d6f94'

"""