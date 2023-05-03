import time
from typing import Tuple
import serial
import serial.tools.list_ports
from logic.occ_slip import SlipDecoder
from osc4py3.oscbuildparse import *
import wallycore as wally

ports = serial.tools.list_ports.comports()

# check 'serial' is 'pyserial' and not 'serial'
# ref. https://github.com/espressif/esptool/issues/269
try:
    if "serialization" in serial.__doc__ and "deserialization" in serial.__doc__:
        raise ImportError(
            "esptool.py depends on pyserial, but there is a conflict with a currently "
            "installed package named 'serial'.\n"
            "You may work around this by 'pip uninstall serial; pip install pyserial' "
            "but this may break other installed Python software "
            "that depends on 'serial'.\n"
            "There is no good fix for this right now, "
            "apart from configuring virtualenvs. "
            "See https://github.com/espressif/esptool/issues/269#issuecomment-385298196"
            " for discussion of the underlying issue(s)."
        )
except TypeError:
    pass  # __doc__ returns None for pyserial


def slip_reader(port):
    partial_packet = None
    in_escape = False
    successful_slip = False
    occ_slip = bytes([])
    while True:
        waiting = port.inWaiting()
        read_bytes = port.read(1 if waiting == 0 else waiting)
        occ_slip += read_bytes
        if read_bytes == b"":
            if partial_packet is None:  # fail due to no data
                msg = (
                    "Serial data stream stopped: Possible serial noise or corruption."
                    if successful_slip
                    else "No serial data received."
                )
            else:  # fail during packet transfer
                msg = "Packet content transfer stopped (received {} bytes)".format(len(partial_packet))
        if b"ESP-ROM:" in read_bytes:
            if b"ESP-ROM:esp32c3" not in read_bytes:
                print(f"Wrong hardware target. Only works with Risc-V based ESP32C3 chip series.")
                quit()
        if b"\xc0" in read_bytes:
            for b in read_bytes:
                b = bytes([b])
                if partial_packet is None:  # waiting for packet header
                    if b == b"\xc0":
                        occ_slip = b"\xc0"
                        partial_packet = b""
                    else:
                        remaining_data = port.read(port.inWaiting())
                elif b == b"\xc0":  # end of packet
                    partial_packet = None
                    global decoded_data
                    slipDecoder = SlipDecoder()
                    slip = slipDecoder.decode_from_slip(occ_slip)
                    decoded_data = decode_packet(bytes(slip))
                    successful_slip = True
                    occ_slip = bytes([])
                    yield decoded_data
                    return
                else:  # normal byte in packet
                    partial_packet += b


class OccSerial:
    def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.ser = None

    def connect(self):
        assert self.ser is None

        print("Connecting to {} at {}".format(self.port, self.baudrate))
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout, write_timeout=self.timeout)
        assert self.ser is not None

        if not self.ser.is_open:
            self.ser.open()
        # As learned from Blockstream's Jade hardware
        # Ensure RTS and DTR are not set (as this can cause the hw to reboot)
        self.ser.setRTS(False)
        self.ser.setDTR(False)

        print("Connected")

    def disconnect(self):
        assert self.ser is not None

        # Consider also here the peculiarities of Jade aka Espressif's ESP32
        # Ensure RTS and DTR are not set (as this can cause the hw to reboot)
        # and then close the connection
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.ser.close()

        # Reset state
        self.ser = None

    def write(self, bytes_):
        assert self.ser is not None
        return self.ser.write(bytes_)

    def read(self, n):
        assert self.ser is not None
        return self.ser.read(n)


class OccConnector:
    serial_interface = None
    private_key = None
    public_key = None
    mnemonic = None
    planet_mint_private_key = None

    def __init__(self, serial_interface, planet_mint_private_key, public_key):
        self.serial_interface = serial_interface
        self.planet_mint_private_key = planet_mint_private_key
        self.public_key = public_key
        self.private_key = None
        self.mnemonic = None
        self.seed = None

    def _connect_trusted_anker(self) -> OccSerial:
        occ_serial = OccSerial(
            self.serial_interface, 115200, serial.PARITY_NONE, serial.STOPBITS_ONE, serial.EIGHTBITS, 1
        )
        occ_serial.connect()
        return occ_serial

    def _send_osc_message(self, msg):
        raw = encode_packet(msg)

        raw = b"\xc0" + raw[:-1] + b"@\xc0"
        occ_serial = self._connect_trusted_anker()
        time.sleep(1)
        occ_serial.write(raw)
        f = slip_reader(occ_serial.ser)
        msg = next(f)
        time.sleep(1)
        occ_serial.disconnect()
        return msg

    def sign_hash_with_trusted_anchor(self, data_hash: str) -> Tuple[str, str, str]:
        """
        @brief: Signs a hash with the Trusted Anchor
        @param data_hash: raw hash of the data to be signed
        @return: the signed hash
        """
        msg = OSCMessage("/IHW/ecdsaSigFromBytes", ",sisis", [self.private_key, 32, data_hash, 32, ""])
        occ_message = self._send_osc_message(msg)
        return occ_message[2]

    def valise_seed_init(self) -> str:
        """
        @brief: Initializes with hardcoded seed of the Valise
        @return: mnemonic seed
        """
        msg = OSCMessage("/IHW/valiseMnemonicSeedInit", ",s", [""])
        occ_message = self._send_osc_message(msg)
        return occ_message[2][0]

    def create_mnemonic(self) -> str:
        """
        @brief: Creates a mnemonic seed
        @return: the mnemonic seed
        """
        # Change calls according to wallet implementation on te different ESP32 MCUs
        msg = OSCMessage("/IHW/bip39Mnemonic", ",s", [""])
        occ_message = self._send_osc_message(msg)
        mnemonic = occ_message[2][1]
        self.mnemonic = mnemonic
        return mnemonic

    def valise_mnemonic_set(self, mnemonic):
        """
        @brief: Sets the mnemonic seed
        @param mnemonic: string of the mnemonic seed
        @return: true if successful
        """
        msg = OSCMessage("/IHW/valiseMnemonicSet", ",ss", [mnemonic, ""])
        occ_message = self._send_osc_message(msg)
        return occ_message[2][0]

    def valise_get(self) -> str:
        """
        @brief: Gets the mnemonic seed
        @return: the mnemonic seed
        """
        msg = OSCMessage("/IHW/valiseMnemonicGet", ",s", [""])
        occ_message = self._send_osc_message(msg)
        self.mnemonic = occ_message[2][0]
        return self.mnemonic

    def mnemonic_to_private_key(self):
        """
        @brief: Derives the private key from the mnemonic seed
        """
        msg = OSCMessage("/IHW/bip39MnemonicToSeed", ",ss", [self.mnemonic, ""])
        occ_message = self._send_osc_message(msg)
        self.private_key = occ_message[2][0]

    def ecdsa_derive_pubkey(self, parent_key):
        """
        @brief: Derives the public key from the private key
        @param parent_key: contains private key to derive the public key from
        @return:
        """
        msg = OSCMessage("/IHW/ecdsaPubKey", ",sii", [parent_key, 32, 1])
        occ_message = self._send_osc_message(msg)
        return occ_message[2][0]

    def ecdsa_sig_verify_pub_key_hash(self, pubkey, data_hash):
        """
        @brief: Saves the public key and the data hash to the trusted anchor that you want to verify. This is because the OSC message is limited to 64 bytes so we need to split it up into two calls.
        @param pubkey: public key to verify
        @param data_hash: Original unsigned data hash
        @return: public key if successful
        """
        msg = OSCMessage("/IHW/ecdsaSigVerifyPubkeyHash", ",sisi", [pubkey, 33, data_hash, 32])
        occ_message = self._send_osc_message(msg)
        return occ_message[2][0]

    def ecdsa_sig_verify(self, signature) -> bool:
        """
        @brief: Verifies the signature of the data hash
        @param signature: signed hash
        @return: true if successful
        """
        msg = OSCMessage("/IHW/ecdsaSigVerify", ",si", [signature, 64])
        occ_message = self._send_osc_message(msg)
        return occ_message[2][6]


def get_usb_serial_ports() -> str | None:
    """
    Get a list of all serial ports on the system
    :return: A list of all serial ports on the system
    """
    for port in sorted(ports):
        if "usb" in port.device:
            return port.device
    return None
