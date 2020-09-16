"""
Used with ble_uart_echo_test.py. Transmits "echo" to the UARTService and receives it back.
"""

import time

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
while True:
    print("Checking advertisements...")
    for advertisement in ble.start_scan(ProvideServicesAdvertisement):
        if UARTService in advertisement.services:
            connection = ble.connect(advertisement)
            print("connected")
            break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()

    uart = connection[UARTService]
    buf = bytearray(1)
    while connection.connected:
        buf[0] = (buf[0] + 1) % 256
        print("sent:", buf)
        uart.write(buf)
        # Returns b'' if nothing was read.
        echo = uart.read(1)
        if echo:
            print("rcvd", echo)

    print("disconnected, scanning")
    connection = None
