import time
import asyncio
import serial_asyncio


class Reader(asyncio.Protocol):
    def connection_made(self, transport):
        """Store the serial transport and prepare to receive data.
        """
        self.transport = transport
        self.buf = bytes()
        self.msgs_recvd = 0
        print('Reader connection created')

    def data_received(self, data):
        """Store characters until a newline is received.
        """
        self.buf += data
        if b'\n' in self.buf:
            lines = self.buf.split(b'\n')
            self.buf = lines[-1]  # whatever was left over
            for line in lines[:-1]:
                print(f'Reader received: {line.decode()}')
                self.msgs_recvd += 1
        if self.msgs_recvd == 4:
            self.transport.close()

    def connection_lost(self, exc):
        print('Reader closed')


class SLIP(asyncio.Protocol):
    def connection_made(self, transport):
        """Store the serial transport and schedule the task to send data.
        """
        time.sleep(0.3)
        self.transport = transport
        self.buf = bytes()
        self.msgs_recvd = 0
        print('Reader connection created')
        print('Writer connection created')
        asyncio.ensure_future(self.send())
        print('Writer.send() scheduled')
        time.sleep(0.5)
        transport.serial.write(b'\xc0/IHW/trnd\x00\x00\x00,i\x00\x00\x00\x00\x00@\xc0')
        time.sleep(0.3)

    def connection_lost(self, exc):
        print('Writer closed')

    def data_received(self, data):
        """Store characters until a newline is received.
        """
        self.buf += data
        if b'\n' in self.buf:
            lines = self.buf.split(b'\n')
            self.buf = lines[-1]  # whatever was left over
            for line in lines[:-1]:
                print(f'Reader received: {line.decode()}')
                self.msgs_recvd += 1
        #if self.msgs_recvd == 4:
        self.transport.close()

    async def send(self):
        """Send four newline-terminated messages, one byte at a time.
        """
        message = b'foo\nbar\nbaz\nqux\nfoo\nbar\nbaz\nqux\n'
        """for b in message:
            await asyncio.sleep(0.5)
            self.transport.serial.write(bytes([b]))
            print(f'Writer sent: {bytes([b])}')"""
        
        #time.sleep(0.5)
        self.transport.serial.write(b'\xc0/IHW/trnd\x00\x00\x00,i\x00\x00\x00\x00\x00@\xc0')
        #time.sleep(0.3)
        self.transport.close()


loop = asyncio.get_event_loop()
#reader = serial_asyncio.create_serial_connection(loop, Reader, '/dev/ttyUSB0', baudrate=115200)
writer = serial_asyncio.create_serial_connection(loop, SLIP, '/dev/ttyACM0', baudrate=115200)
#asyncio.ensure_future(reader)
print('Reader scheduled')
asyncio.ensure_future(writer)
print('Writer scheduled')
loop.call_later(10, loop.stop)
loop.run_forever()
print('Done')
