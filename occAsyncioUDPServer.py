import asyncio
import datetime
import binascii

from aioudp import UDPServer

from occAsyncioServer import *
from occSlip import *


class OccUDPServer:
    def __init__(self, server, loop):
        self.server = server
        self.loop = loop
        self.occMsg = ""
        # Subscribe for incoming udp packet event
        self.server.subscribe(self.on_datagram_received)
        #asyncio.ensure_future(self.do_occSend(), loop=self.loop)

    async def on_datagram_received(self, data, addr):
        # Override virtual method and process incoming data
        print(datetime.datetime.now(), addr, data)
        self.occMsg = data
        

async def do_occSendReceive():
    while True:
        # Any payload
        time.sleep(0.3)
        msg = OSCMessage()
        msg.setAddress("/IHW/trnd")
        msg.append(64, 'i')
        slipEncoder = OccSlip()
        payload = slipEncoder.encodeToSLIP(msg.getBinary())
        payload = ''.join(map(str, payload))
        payload = payload.encode('utf-8')
        payload = payload.replace(b'192', b'\xc0')

        transport, protocol = await serial_asyncio.create_serial_connection(loop, SLIPProtocol, '/dev/ttyUSB0', baudrate=115200)
        while True:
            await asyncio.sleep(0.3)
            transport.serial.write(payload)
            time.sleep(0.3)
        buf = binascii.unhexlify(protocol.occ_response[3])   


        

        """loop.run_forever()
        loop.close()"""

        # Delay for prevent tasks concurency
        #await asyncio.sleep(0.001)
        #await asyncio.wait(self.do_occSend())
        #await do_occSendReceive()

async def main(loop):
    # Bandwidth speed is 100 bytes per second
    udp = UDPServer(download_speed=100, upload_speed=100)
    udp.run("127.0.0.1", 9006, loop=loop)
    server = OccUDPServer(server=udp, loop=loop)

   

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(loop))
    asyncio.ensure_future(do_occSendReceive)

    loop.run_until_complete()
    
    # loop.run_until_complete(main(loop))
    loop.run_forever()