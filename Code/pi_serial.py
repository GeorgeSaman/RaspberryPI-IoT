import serial
import time

#-----Instantiating a serial write object
serial_Write_Object = serial.Serial(
            port='/dev/serial0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
       )

#-----Instantiating a serial Read object
serial_Read_Object = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
       )

#--------Declaring a new Class for serial comm.--------
class PiSerial(object):
   
    def serialWrite(self, text):
        serial_Write_Object.write(text)

    def serialRead(self):
       	readValue = serial_Read_Object.readline()
       	print readValue
        return readValue
