import Adafruit_GPIO.FT232H as FT232H
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
import serial




class UART_ConsoleReadThread(QtCore.QThread):
        def __init__(self,ser):
		self.ser=ser
                super(UART_ConsoleReadThread,self).__init__()
                string=""
		print("[*] Initializing ConsoleReadThread ")

        def __del__(self):
                self.wait()

        def close(self):
                self.terminate()

        def run(self):
                try:
                        while 1:
                                if(self.ser.in_waiting):
                                        self.string=self.ser.read_all()
                                        self.emit(SIGNAL('update_console(QString)'), QtCore.QString(self.string))
                except Exception as e:
                        print("[*] Exception : "+str(e))



class InputMonitorThread(QtCore.QThread):
        def __init__(self, pin_set,ft232h):
		self.ft232h=ft232h
                self.pin_set=pin_set
                super(InputMonitorThread,self).__init__()

        def __del__(self):
                self.wait()

        def close(self):
                self.terminate()

        def run(self):
                print("[*] InputMonitorThread -> run executing ")
                while 1:
                        for pin in self.pin_set:
                                state=self.ft232h.input(pin)
                                self.emit(SIGNAL('update_states(int,int)'), state, pin)


class I2CScanner(QtCore.QThread):
	def __init__(self,ft232h):
		self.ft232h=ft232h
		self.count=0
		print("[*] Inititalizing I2C Scanner Thread ")
		super(I2CScanner,self).__init__()

        def __del__(self):
                self.wait()

        def close(self):
                self.terminate()

	def run(self):
		for address in range(127):
	        	if address <= 7 or address >= 120:
	        	        continue
		        i2c = FT232H.I2CDevice(self.ft232h, address)
		        if i2c.ping():
				self.count=self.count+1
       		        	self.emit(SIGNAL('I2c_device_found(int)'),address)
                self.emit(SIGNAL('I2c_device_found(int)'),self.count+1000)
		print("[*] terminating ")
		self.terminate()

