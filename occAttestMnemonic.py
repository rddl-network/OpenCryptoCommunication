import asyncio
#from concurrent.futures import ThreadPoolExecutor as Executor

import datetime
import time
import binascii

from occAsyncioServer import *
from occSlip import *


async def slip(loop):
    await asyncio.sleep(0.001)
    serial_instance = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200)
    transport, protocol = await serial_asyncio.connection_for_serial(loop, SLIPProtocol, serial_instance)

    time.sleep(0.8)

    msg = OSCMessage()
    msg.setAddress("/IHW/trnd")
    msg.append(64, 'i')
    #msg.setAddress("/IHW/bip32_key_from_seed")
    #msg.append("f55ece858b0ddd5263f96810fe14437cd3b5e1fbd7c6a2ec1e031f05e86d8bd5", 's')
    #msg.setAddress("/IHW/mnemonic")
    #msg.append(64, 'i')

    print(msg)

    slipEncoder = SlipEncoder()
    payload = slipEncoder.encodeToSLIP(msg.getBinary())

    payload = ''.join(map(str, payload))
    payload = payload.encode('utf-8')
    payload = payload.replace(b'192', b'\xc0')

    print(payload)

    transport.serial.write(payload)
    time.sleep(1)

    return transport, protocol


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    occ_slip = loop.create_task(slip(loop))
    transport, protocol = loop.run_until_complete(occ_slip)

    pending = asyncio.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
    
    #group = asyncio.gather(*pending, return_exceptions=True)
    loop.run_until_complete(occ_slip)
    #loop.run_forever()
    loop.close()

    print(F"OCC message: {protocol.occ_response}")
    resp = protocol.occ_response
    print(F"\n\n{resp}")
    