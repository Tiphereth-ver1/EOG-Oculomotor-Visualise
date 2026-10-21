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
        self.connection_status.emit("Trying to connect port (COM3)...")  # CONFIG: Connection progress message; update this text when changing the serial port.
        try: 
            self.ser = serial.Serial(
                port = "COM3",  # CONFIG: Device serial port; set this to the actual port.
                baudrate = 9600,  # CONFIG: Serial baud rate; must match the device.
                bytesize = EIGHTBITS,  # CONFIG: Eight data bits; configure according to the device protocol.
                stopbits = STOPBITS_ONE,  # CONFIG: One stop bit; configure according to the device protocol.
                xonxoff = False,
                rtscts = False,
                dsrdtr = False,
                parity = PARITY_NONE,  # CONFIG: No parity; configure according to the device protocol.
                timeout = 1  # CONFIG: Serial read timeout in seconds; no continuous read loop is implemented.
                )
            self.connection_established.emit()
            self.connection_status.emit("Connection successful.")  # CONFIG: Connection success message shown in the Debug log.
        except serial.SerialException as e:
            print(e)
            self.connection_status.emit(str(e))
    
    @property
    def connected(self):
        return self.ser is not None and self.ser.is_open

    @Slot()
    def marker_high(self):
        self.ser.write(b"111111")  # CONFIG: High marker bytes; currently not connected to experiment stimulus events.

    @Slot()
    def marker_low(self):
        self.ser.write(b"000000")  # CONFIG: Low marker bytes; currently not connected to experiment stimulus events.

    @Slot()
    def disconnect_port(self):
        self.ser.close()
