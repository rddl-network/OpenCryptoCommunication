Set serial port in occSlipConnect() to the one you are using
Example:
```python
occ_serial = OccSerial('/dev/cu.usbserial-210', 115200, serial.PARITY_NONE, serial.STOPBITS_ONE, serial.EIGHTBITS, 1)
```
serial port, run the following command in a terminal:
```shell
ls /dev/cu.*
```
to find the 