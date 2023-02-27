import subprocess

import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor


import datetime
import time
import binascii

from aioudp import UDPServer

from occAsyncioServer import *
from occSlip import *

class OccUDPServer:
    def __init__(self, server, loop, transport, protocol):
        self.server = server
        self.loop = loop
        self.transport = transport
        self.protocol = protocol
        # Subscribe for incoming udp packet event
        self.server.subscribe(self.on_datagram_received)

    async def on_datagram_received(self, data, addr):
        # Override virtual method and process incoming data
        #print(datetime.datetime.now(), addr, data)
        asyncio.ensure_future(slip(self.loop))
        time.sleep(0.3)
        msg = OSCMessage()
        msg.setAddress("/IHW/mnemonic")
        msg.append(64, 'i')
        slipEncoder = OccSlip()
        payload = slipEncoder.encodeToSLIP(msg.getBinary())
        payload = ''.join(map(str, payload))
        payload = payload.encode('utf-8')
        payload = payload.replace(b'192', b'\xc0')
        self.transport.serial.write(payload)
        time.sleep(0.5)
        #asyncio.sleep(0.3)

async def main(transport, protocol):
    while True:
        udp = UDPServer(download_speed=100, upload_speed=100)
        udp.run("127.0.0.1", 9006, loop=loop)
        server = OccUDPServer(server=udp, loop=loop, transport=transport, protocol=protocol)
        print("the app is running")
        await asyncio.sleep(1)

async def slip(loop):
    await asyncio.sleep(1.0)
    serial_instance = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200)
    transport, protocol = await serial_asyncio.connection_for_serial(loop, SLIPProtocol, serial_instance)
    return transport, protocol


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    occ_slip = loop.create_task(slip(loop))
    transport, protocol = loop.run_until_complete(occ_slip)

    occ_udp = loop.create_task(main(transport, protocol))
    loop.run_until_complete(occ_udp) # Server starts listening

    loop.run_forever()
    loop.close()

    #print(F"OCC message: {protocol.occ_response}")
    #buf = unhexlify(protocol.occ_response[3])


    #loop.run_until_complete(write_messages()) # Start writing messages (or running tests)
    loop.run_forever()