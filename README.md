# OpenCryptoCommunication

This Python library allows you to connect to a hardware device called Trusted-Anker via OSC (Open Sound Control) with the OccConnector (Open Crypto Control Connector) class.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating an instance of OccConnector](#creating-an-instance-of-occconnector)
  - [Methods](#methods)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.6 or higher
- pyserial
- osc4py3
- wallycore

## Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation) if you haven't already.

2. Create a new directory for your project and navigate to it:

\```bash
mkdir my_project
cd my_project
\```

3. Initialize a new Poetry project:

\```bash
poetry init
\```

4. Add the required packages as dependencies:

\```bash
poetry add pyserial osc4py3 wallycore-python
\```

5. Download the `occ_connector.py` file and place it in your project directory.

## Usage

### Creating an instance of OccConnector

To create an instance of the `OccConnector` class, you will need to provide the following parameters:

- `serial_interface`: The serial interface for the Trusted-Anker device.
- `planet_mint_private_key`: The private key for Planet Mint.
- `public_key`: The public key for Trusted-Anker.

Example:

```python
from occ_connector import OccConnector, get_usb_serial_ports

serial_interface = get_usb_serial_ports()
planet_mint_private_key = "your_planet_mint_private_key"
public_key = "your_public_key"

occ_connector = OccConnector(serial_interface, planet_mint_private_key, public_key)
```

Note: The `get_usb_serial_ports()` function auto-detects a connected Trusted-Anker device. If more than one serial device is connected, you may need to adapt the function to select the correct device.

### Methods

The `OccConnector` class provides the following methods:

- `sign_hash_with_trusted_anchor(data_hash: str)`: Sign a hash with Trusted-Anker.
- `valise_seed_init()`: Initialize with hardcoded seed of the Valise.
- `create_mnemonic()`: Create a mnemonic seed.
- `valise_mnemonic_set(mnemonic)`: Set the mnemonic seed.
- `valise_get()`: Get the mnemonic seed.
- `mnemonic_to_private_key()`: Derive the private key from the mnemonic seed.
- `ecdsa_derive_pubkey(parent_key)`: Derive the public key from the private key.
- `ecdsa_sig_verify_pub_key_hash(pubkey, data_hash)`: Save the public key and the data hash to the trusted anchor that you want to verify.
- `ecdsa_sig_verify(signature)`: Verify the signature of the data hash.


## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

This library is licensed under the GNU Affero General Public License v3.0 (AGPLv3). See the [LICENSE](LICENSE) file for details.
