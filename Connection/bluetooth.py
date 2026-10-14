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
        self.connection_status.emit("Trying to connect port (COM3)...")  # 《《《《《《《《《《《连接中的提示语，修改串口时同步修改此文字
        try: 
            self.ser = serial.Serial(
                port = "COM3",  # 《《《《《《《《《《《设备串口名称，按实际端口修改
                baudrate = 9600,  # 《《《《《《《《《《《串口波特率，需与设备一致
                bytesize = EIGHTBITS,  # 《《《《《《《《《《《数据位8位，按设备协议设置
                stopbits = STOPBITS_ONE,  # 《《《《《《《《《《《停止位1位，按设备协议设置
                xonxoff = False,
                rtscts = False,
                dsrdtr = False,
                parity = PARITY_NONE,  # 《《《《《《《《《《《无校验，按设备协议设置
                timeout = 1  # 《《《《《《《《《《《串口读取超时秒数，目前没有持续读取数据循环
                )
            self.connection_established.emit()
            self.connection_status.emit("Connection successful.")  # 《《《《《《《《《《《连接成功提示语，显示在Debug框
        except serial.SerialException as e:
            print(e)
            self.connection_status.emit(str(e))
    
    @property
    def connected(self):
        return self.ser is not None and self.ser.is_open

    @Slot()
    def marker_high(self):
        self.ser.write(b"111111")  # 《《《《《《《《《《《高标记字节协议，目前未连接到实验刺激事件

    @Slot()
    def marker_low(self):
        self.ser.write(b"000000")  # 《《《《《《《《《《《低标记字节协议，目前未连接到实验刺激事件

    @Slot()
    def disconnect_port(self):
        self.ser.close()
