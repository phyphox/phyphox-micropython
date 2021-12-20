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

_phyphoxExperimentService = (
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
    def __init__(self, name="phyphox"):
        print("Init Bluetooth server")
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_data, self._handle_config), self._handle_experiment) = self._ble.gatts_register_services((_phyphoxDataService,_phyphoxExperimentService))
        self._connections = set()
        self._write_callback = None
        if(len(name)<9):
            self._payload = advertising_payload(name=name, services=[phyphoxBleExperimentServiceUUID])
        else:
            self._payload = advertising_payload(name="phyphox", services=[phyphoxBleExperimentServiceUUID])
        self._resp_data = advertising_payload(name=name)
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
            print("Connections:",self._connections)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            print("Config write was successful")
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_config and self._write_callback:
                self._write_callback(value)
    
    """
    \brief Write multiple float values to data characteristic
    use as write(value1, value2, value3, ...)
    \param put in any value(s)
    """
    def write(self, *more_data):
        list_data = list(more_data)
        send_data = struct.pack(f'{len(list_data)}f', *more_data)
        
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_data, send_data)
            print("Writing to data characteristic:", send_data)
    """
    Reads a float from config characteristic
    returns the float value if succesful
    """
    def read(self):
        packed_data = self._ble.gatts_read(self._handle_config)
        if packed_data != b'':
            try:
                config = struct.unpack('<f',packed_data)
                print("read:",config[0])
                return config[0]
            except:
                print("Error: value in config is not a 4-byte float")
        else:
            print("config is empty")
            return 0
    """
    Reads an array of floats from config characteristic
    returns a tuple of float values if succesful
    """
    
    def read_array(self, array_size):
        packed_data = self._ble.gatts_read(self._handle_config)
        if packed_data != b'':
            try:
                config = struct.unpack(f'{array_size}f',packed_data)
                print("read:",config)
                return config
            except:
                print("Error: value in config is not a float or array size is wrong")
        else:
            print("config is empty")
            return (0,)
        
    def add_experiment(self, phyphox_experiment):
        try:
            experiment_bytes = phyphox_experiment.get_bytes()
            for conn_handle in self._connections:
                self._ble.gatts_notify(conn_handle, self._handle_experiment, phyphox_experiment)
        except:
            print("Error in adding experiment")
            
    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload,resp_data=self._resp_data)
        print("Started advertising")


    def on_write(self, callback):
        self._write_callback = callback