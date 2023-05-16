import bluetooth
import struct
import phyphoxBLE.experiment
import time
import _thread
from io import StringIO
from io import BytesIO
from phyphoxBLE.ble_advertising import advertising_payload
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTC_NOTIFY = const(18)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

PhyphoxBLEExperimentServiceUUID = bluetooth.UUID('cddf0001-30f7-4671-8b43-5e40ba53514a')
PhyphoxBLEExperimentCharacteristicUUID = bluetooth.UUID('cddf0002-30f7-4671-8b43-5e40ba53514a')

phyphoxBleDataServiceUUID = bluetooth.UUID('cddf1001-30f7-4671-8b43-5e40ba53514a')
phyphoxBleDataCharacteristicUUID = bluetooth.UUID('cddf1002-30f7-4671-8b43-5e40ba53514a')
phyphoxBleConfigCharacteristicUUID = bluetooth.UUID('cddf1003-30f7-4671-8b43-5e40ba53514a')
PhyphoxBLEExperimentControlCharacteristicUUID = bluetooth.UUID('cddf0003-30f7-4671-8b43-5e40ba53514a')

_experimentCharacteristic = (
    PhyphoxBLEExperimentCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_WRITE | bluetooth.FLAG_NOTIFY,
)

_experimentControlCharacteristic = (
    PhyphoxBLEExperimentControlCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_WRITE,
)

_phyphoxExperimentService = (
    PhyphoxBLEExperimentServiceUUID,
    (_experimentCharacteristic,_experimentControlCharacteristic),
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
        self._device_name = "phyphox-mpy"
        self._p_exp = BytesIO()
        self._exp_len = 0
        self._ble = None
        self._connections = ()
        self._write_callback = None
        self._payload = None
        self._resp_data = None
        self.debug = False
        
    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            if self.debug: print("New connection", conn_handle)
            self._connections.add(conn_handle)
            if self.debug: print("Connections:",self._connections)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if self.debug: print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            if self.debug: print("Config write was successful")
            conn_handle, value_handle = data            
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_config and self._write_callback:
                self._write_callback()
            elif value_handle == self._handle_experiment_control:        
                control_data = self._ble.gatts_read(self._handle_experiment_control)
                if self.debug: print(control_data)
                if control_data == b'\x01':
                    _thread.start_new_thread(self.when_subscription_received, (conn_handle,))
                    if self.debug: print("Sending experiment")
    
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
            if self.debug: print("Writing to data characteristic:", send_data)
    """
    Reads a float from config characteristic
    returns the float value if succesful
    """
    def read(self):
        packed_data = self._ble.gatts_read(self._handle_config)
        if int.from_bytes(packed_data,"big") != 0:
            try:
                config = struct.unpack('<f',packed_data)
                if self.debug: print("read:",config[0])
                return config[0]
            except:
                print("Error: value in config is not a 4-byte float") # TODO Change to error code
        else:
            if self.debug: print("config is empty")
            return float('nan')
    """
    Reads an array of floats from config characteristic
    returns a tuple of float values if succesful
    """
    
    def read_array(self, array_size):
        packed_data = self._ble.gatts_read(self._handle_config)
        if packed_data != b'':
            try:
                config = struct.unpack(f'{array_size}f',packed_data)
                if self.debug: print("read:",config)
                return config
            except:
                print("Error: value in config is not a float or array size is wrong") # TODO Change to error code
        else:
            if self.debug: print("config is empty")
            return (float('nan'),)
            
    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload,resp_data=self._resp_data)
        if self.debug: print("Started advertising")
        
    def _stop_advertise(self):
        self._ble.gap_advertise(interval_us=None)
        if self.debug: print("stopped advertising")


    def on_write(self, callback):
        self._write_callback = callback
        
    
    def crc32_generate_table(self,table):
        polynomial = 0xEDB88320
        for i in range(256):
            c = i
            for j in range(8):
                if c&1:
                    c = polynomial ^ (c >> 1)
                else:
                    c = c >> 1
            table[i] = c
        
        
    def crc32_update(self, table, initial, buf, e_len):
        c = initial ^ 0xFFFFFFFF
        i = 0
        while i <= e_len-1:
            buf.seek(i)
            u = buf.readline()
            i = buf.tell()
            for ch in range(len(u)):
                c = table[(c^u[ch]) & 0xFF] ^ (c >> 8)
        return c ^ 0xFFFFFFFF
        
        
    def when_subscription_received(self, conn_handle):
        if self.debug: print("subscription received")

        self._stop_advertise()
        
        exp = self._p_exp
        exp_len = self._exp_len

        table = [0] * 256
        self.crc32_generate_table(table)
        checksum = self.crc32_update(table, 0, exp, exp_len)
        arrayLength = self._exp_len
        header = "phyphox".encode() + struct.pack('>I',arrayLength) + struct.pack('>I',checksum) + b'\x00' + b'\x00' + b'\x00' + b'\x00' + b'\x00'    
        time.sleep_ms(30)

        self._ble.gatts_notify(conn_handle, self._handle_experiment, header)
        time.sleep_ms(30)
        
        for i in range(int(self._exp_len/20)):
            exp.seek(i*20)
            byteSlice = exp.read(20)
            self._ble.gatts_notify(conn_handle, self._handle_experiment, byteSlice)
            time.sleep_ms(30)
        if(self._exp_len%20 != 0):
            rest = self._exp_len%20
            exp.seek(self._exp_len-rest)
            byteSlice = exp.read(rest)
            self._ble.gatts_notify(conn_handle, self._handle_experiment, byteSlice)
            time.sleep_ms(10)
            self._subscribed = True
        self._advertise()

    def addExperiment(self, exp):
        buf = StringIO()
        exp.getFirstBytes(buf, self._device_name)
        for vi in range(phyphoxBLE.phyphoxBleNViews):
            for el in range(phyphoxBLE.phyphoxBleNElements):
                exp.getViewBytes(buf,vi,el)
        exp.getLastBytes(buf)
        buf.seek(0)
        str_data = buf.read().encode('utf8')
        self._p_exp = BytesIO(str_data)    
        self._p_exp.seek(0)
        self._p_exp.read()
        lastPos = self._p_exp.tell()
        self._exp_len = lastPos
        buf.close()
        if self.debug: print("Experiment added")
        
    def start(self, device_name="phyphox", exp_pointer=None, exp_len=None):
        self._device_name = device_name
        if exp_pointer:
            #self._p_exp = exp_pointer
            #self.addExperiment(exp_pointer)
            if not exp_len:
                if self.debug: print("Please enter length of the experiment")
            else:
                self._exp_len = exp_len
        if self.debug: print("starting server")
        self._p_exp.seek(0)
        self._p_exp.read()
        if self._p_exp.tell() == 0:
            if self.debug: print("Create default experiment")
            defaultExperiment = phyphoxBLE.Experiment()
            firstView = phyphoxBLE.Experiment.View()
            firstView.setLabel("View")
            firstGraph = phyphoxBLE.Experiment.Graph()
            firstGraph.setChannel(0,1)
            firstView.addElement(firstGraph)
            defaultExperiment.addView(firstView)
            self.addExperiment(defaultExperiment)
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_data, self._handle_config), (self._handle_experiment, self._handle_experiment_control)) = self._ble.gatts_register_services((_phyphoxDataService,_phyphoxExperimentService))
        self._connections = set()
        self._write_callback = None
        
        if(len(self._device_name)>26):
            self._payload = advertising_payload(name="phyphox", services=[PhyphoxBLEExperimentServiceUUID])
        self._payload = advertising_payload(services=[PhyphoxBLEExperimentServiceUUID])

        self._resp_data = advertising_payload(name=self._device_name)
        self._advertise()
        



