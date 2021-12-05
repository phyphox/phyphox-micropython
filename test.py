import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

phyphoxBleExperimentServiceUUID = bluetooth.UUID('cddf0001-30f7-4671-8b43-5e40ba53514a')
phyphoxBleExperimentCharacteristicUUID = bluetooth.UUID('cddf0002-30f7-4671-8b43-5e40ba53514a')
phyphoxBleExperimentControlCharacteristicUUID = bluetooth.UUID('cddf0003-30f7-4671-8b43-5e40ba53514a')

phyphoxBleDataServiceUUID = bluetooth.UUID('cddf1001-30f7-4671-8b43-5e40ba53514a')
phyphoxBleDataCharacteristicUUID = bluetooth.UUID('cddf1002-30f7-4671-8b43-5e40ba53514a')
phyphoxBleConfigCharacteristicUUID = bluetooth.UUID('cddf1003-30f7-4671-8b43-5e40ba53514a')

_myExperimentDescriptor = (

)
_experimentCharacteristic = (
    phyphoxBleExperimentCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY | bluetooth.FLAG_WRITE,
)
_experimentService = (
    phyphoxBleExperimentServiceUUID,
    (_experimentCharacteristic,),
)

_myDataDescriptor = (
)
_dataCharacteristic = (
    phyphoxBleDataCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY | bluetooth.FLAG_WRITE,
)
_myConfigDescriptor = (
)
_configCharacteristic = (
    phyphoxBleConfigCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY | bluetooth.FLAG_WRITE,
)
_phyphoxDataService = (
    phyphoxBleDataServiceUUID,
    (_dataCharacteristic,_configCharacteristic,),
)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLESimplePeripheral:
    def __init__(self, ble, name="phyphox"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),(self._handle_ex)) = self._ble.gatts_register_services((_phyphoxDataService,_experimentService))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[phyphoxBleExperimentServiceUUID])
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback


def demo():
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)

    def on_rx(v):
        print("RX", v)

    p.on_write(on_rx)

    i = 0
    while True:
        if p.is_connected():
            # Short burst of queued notifications.
            for _ in range(3):
                data = str(i) + "_"
                print("TX", data)
                p.send(data)
                i += 1
        time.sleep_ms(100)


if __name__ == "__main__":
    demo()


