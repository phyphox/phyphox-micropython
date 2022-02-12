import bluetooth
import struct
import phyphoxBleExperiment
import io
import time
from io import StringIO
from io import BytesIO
from ble_advertising import advertising_payload
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTC_NOTIFY = const(18)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

phyphoxBleExperimentServiceUUID = bluetooth.UUID('cddf0001-30f7-4671-8b43-5e40ba53514a')
phyphoxBleExperimentCharacteristicUUID = bluetooth.UUID('cddf0002-30f7-4671-8b43-5e40ba53514a')

phyphoxBleDataServiceUUID = bluetooth.UUID('cddf1001-30f7-4671-8b43-5e40ba53514a')
phyphoxBleDataCharacteristicUUID = bluetooth.UUID('cddf1002-30f7-4671-8b43-5e40ba53514a')
phyphoxBleConfigCharacteristicUUID = bluetooth.UUID('cddf1003-30f7-4671-8b43-5e40ba53514a')
phyphoxBleExperimentControlCharacteristicUUID = bluetooth.UUID('cddf0003-30f7-4671-8b43-5e40ba53514a')

_experimentCharacteristic = (
    phyphoxBleExperimentCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_WRITE | bluetooth.FLAG_NOTIFY,
)

_experimentControlCharacteristic = (
    phyphoxBleExperimentControlCharacteristicUUID,
    bluetooth.FLAG_READ | bluetooth.FLAG_WRITE,
)

_phyphoxExperimentService = (
    phyphoxBleExperimentServiceUUID,
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
        self._connections = None
        self._write_callback = None
        self._payload = None
        self._resp_data = None
        
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
                
            control_data = self._ble.gatts_read(self._handle_experiment_control)
            if control_data == b'\x01':
                #self.when_subscription_received()
                print("Sending experiment")
    
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
            
    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload,resp_data=self._resp_data)
        print("Started advertising")
        
    def _stop_advertise(self):
        self._ble.gap_advertise(interval_us=None)
        print("stopped advertising")


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
        
        
    def when_subscription_received(self):
        print("subscription received")

        self._stop_advertise()
        print("adverdising stopped")
        
        exp = self._p_exp
        exp_len = self._exp_len
        
        header = [0] * 20
        phyphox = ['p','h','y','p','h','o','x']
        table = [0] * 256
        self.crc32_generate_table(table)
        checksum = self.crc32_update(table, 0, exp, exp_len)
        arrayLength = self._exp_len
        
        experimentSizeArray = [0] * 4
        experimentSizeArray[0] = (arrayLength >> 24)
        experimentSizeArray[1] = (arrayLength >> 16)
        experimentSizeArray[2] = (arrayLength >> 8)
        experimentSizeArray[3] = arrayLength
        
        checksumArray = [0] * 4
        checksumArray[0] = (checksum >> 24) & 0xFF
        checksumArray[1] = (checksum >> 16) & 0xFF
        checksumArray[2] = (checksum >> 8) & 0xFF
        checksumArray[3] = checksum & 0xFF
        
        header[0:7] = phyphox[0:7]
        header[7:11] = experimentSizeArray[0:4]
        header[11:15] = checksumArray[:]
        
        #TODO: Check below
        #experimentCharacteristic->setValue(header,sizeof(header));
        #experimentCharacteristic->notify();
        
        #header wrong type. Cast to Byte
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_experiment, header)
            
        for i in range(int(self._exp_len/20)):
            exp.seek(i*20)
            byteSlice = exp.read(20)
            for j in range(20):
                header[j] = byteSlice[j]
            for conn_handle in self._connections:
                self._ble.gatts_notify(conn_handle, self._handle_experiment, header)
            print(header)
            time.sleep_ms(10)
        if(self._exp_len%20 != 0):
            rest = self._exp_len%20
            sliceRest = [0] * rest
            exp.seek(self._exp_len-rest)
            byteSlice = exp.read(rest)
            for j in range(rest):
                sliceRest[j] = byteSlice[j]
            for conn_handle in self._connections:
                self._ble.gatts_notify(conn_handle, self._handle_experiment, sliceRest)
            print(sliceRest)
            time.sleep_ms(1)
            
        self._advertise()
        print("advertising started")
        
    def addExperiment(self, exp):
        buf = StringIO()
        exp.getFirstBytes(buf, self._device_name)
        for vi in range(phyphoxBleExperiment.phyphoxBleNViews):
            for el in range(phyphoxBleExperiment.phyphoxBleNElements):
                exp.getViewBytes(buf,vi,el)
        exp.getLastBytes(buf)
        
        buf.seek(0)
        str_data = buf.read().encode('utf8')
        self._p_exp = io.BytesIO(str_data)    
        self._p_exp.seek(0)
        self._p_exp.read()
        lastPos = self._p_exp.tell()
        self._exp_len = lastPos
        buf.close()
        print("Experiment added")
        
    def start(self, device_name="phyphox", exp_pointer=None, exp_len=None):
        if exp_pointer:
            #self._p_exp = exp_pointer
            self.addExperiment(exp_pointer)
            if not exp_len:
                print("Please enter length of the experiment")
            else:
                self._exp_len = exp_len
                
        self._device_name = device_name
        print("starting server")
        self._p_exp.seek(0)
        self._p_exp.read()
        if self._p_exp.tell() == 0:
            print("Create default experiment")
            defaultExperiment = phyphoxBleExperiment.PhyphoxBleExperiment()
            firstView = phyphoxBleExperiment.PhyphoxBleExperiment.View()
            firstGraph = phyphoxBleExperiment.PhyphoxBleExperiment.Graph()
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
            self._payload = advertising_payload(name="phyphox", services=[phyphoxBleExperimentServiceUUID])
        self._payload = advertising_payload(services=[phyphoxBleExperimentServiceUUID])

        self._resp_data = advertising_payload(name=self._device_name)
        self._advertise()
        

