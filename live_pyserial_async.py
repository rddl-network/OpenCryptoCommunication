import asyncio
import serial_asyncio

from occAsyncioServer import *
from occSlip import *


class InputChunkProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('data received', repr(data))
        if b'\xc0' in data:
            self.transport.close()

        # stop callbacks again immediately
        self.pause_reading()

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()


async def reader():
    transport, protocol = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, '/dev/ttyUSB0', baudrate=115200)

    while True:
        await asyncio.sleep(0.3)


        msg = OSCMessage()
        msg.setAddress("/IHW/trnd")
        msg.append(64, 'i')
        print(msg)

        slipEncoder = OccSlip()
        payload = slipEncoder.encodeToSLIP(msg.getBinary())

        payload = ''.join(map(str, payload))
        payload = payload.encode('utf-8')
        payload = payload.replace(b'192', b'\xc0')

        print(payload)

        transport.write(payload)

        protocol.resume_reading()


loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()

