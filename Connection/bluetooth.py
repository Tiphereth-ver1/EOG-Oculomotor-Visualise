import serial
from serial import Serial, STOPBITS_ONE, PARITY_NONE, EIGHTBITS
import time
from PySide6.QtCore import QObject, Signal, Slot

class Serial_Worker(QObject):
    connection_established = Signal()
    connection_status = Signal(str)
    def __init__(self):
        super().__init__()
        self.ser : Serial = None
        self.on : bool = False
        pass

    @Slot()
    def connect_port(self):
        self.connection_status.emit("Trying to connect port (COM3)...")
        try: 
            self.ser = serial.Serial(
                port = "COM3",
                baudrate = 9600,
                bytesize = EIGHTBITS,
                stopbits = STOPBITS_ONE,
                xonxoff = False,
                rtscts = False,
                dsrdtr = False,
                parity = PARITY_NONE,
                timeout = 1
                )
            self.connection_established.emit()
            self.connection_status.emit("Connection successful.")
        except serial.SerialException as e:
            print(e)
            self.connection_status.emit(str(e))
    
    @property
    def connected(self):
        return self.ser is not None and self.ser.is_open

    @Slot()
    def marker_high(self):
        self.ser.write(b"111111")

    @Slot()
    def marker_low(self):
        self.ser.write(b"000000")

    @Slot()
    def disconnect_port(self):
        self.ser.close()