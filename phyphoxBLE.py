import bluetooth
import struct
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

phyphoxBleDataServiceUUID = bluetooth.UUID('cddf1001-30f7-4671-8b43-5e40ba53514a')
phyphoxBleDataCharacteristicUUID = bluetooth.UUID('cddf1002-30f7-4671-8b43-5e40ba53514a')
phyphoxBleConfigCharacteristicUUID = bluetooth.UUID('cddf1003-30f7-4671-8b43-5e40ba53514a')

_experimentCharacteristic = (
    phyphoxBleExperimentCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_WRITE,
)
_experimentService = (
    phyphoxBleExperimentServiceUUID,
    (_experimentCharacteristic,),
)

_dataCharacteristic = (
    phyphoxBleDataCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
)
_configCharacteristic = (
    phyphoxBleConfigCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_WRITE,
)
_phyphoxDataService = (
    phyphoxBleDataServiceUUID,
    (_dataCharacteristic,_configCharacteristic,),
)

class PhyphoxBLE:
    def __init__(self, ble, name="phyphox"):
        print("Init Bluetooth server")
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_data, self._handle_config),) = self._ble.gatts_register_services((_phyphoxDataService,))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name="phyphox", services=[phyphoxBleExperimentServiceUUID])
        self._resp_data = advertising_payload(name=name)
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
            print("Write Event triggered")
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_config and self._write_callback:
                self._write_callback(value)
    
    """
    \brief Write multiple values to data characteristic
    use as write(value1, value2, value3, ...)
    phyphox experiment needs "formattedString" as input and with seperator "," 
    \param put in any value(s)
    """
    def write(self, *more_data):
        send_data=""
        
        for data_item in more_data:
            send_data = send_data + str(data_item) + ","
        
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_data, send_data)
            print("Writing to data characteristic:", send_data)
    """
    Reads config characteristic
    TODO: fix b'data'
    """
    def read(self):
        config = self._ble.gatts_read(self._handle_config)
        print("read:",config)
        return config
        

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload,resp_data=self._resp_data)
        print("Started advertising")


    def on_write(self, callback):
        self._write_callback = callback
