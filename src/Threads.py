import Adafruit_GPIO.FT232H as FT232H
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
import serial,os
import subprocess
from mpsse import *



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
		print("[*] Terminating I2C Scanner Thread ")
		self.terminate()

class OpenOCDServerThread(QtCore.QThread):
        def __init__(self,cfg):
                self.cfg_name=cfg
                print("[*] Initializing OpenOCD Server Thread ")
                super(OpenOCDServerThread,self).__init__()

        def __del__(self):
                self.wait()

        def close(self):
          	print("[*] Terminating OpenOCD Server Thread ")
		self.proc.kill()
                self.terminate()

        def run(self):
		self.proc=subprocess.Popen(['openocd','-c','telnet_port 4444','-f','cfg/badge.cfg','-f',"cfg/"+self.cfg_name],stdout=open(os.devnull, 'wb'))


class JTAGTelnetThread(QtCore.QThread):
        def __init__(self):
                print("[*] Initializing Jtag telnet Thread ")
                super(JTAGTelnetThread,self).__init__()

        def __del__(self):
                self.wait()

        def close(self):
                print("[*] Terminating Jtag Telnet Thread ")
                self.proc.kill()
                self.terminate()

        def run(self):
                self.proc=subprocess.Popen(['x-terminal-emulator','-e','telnet','localhost','4444']) 



class JTAGGdbThread(QtCore.QThread):
        def __init__(self,elf_path):
                self.elf_path=elf_path
                print("[*] Initializing JTAG GDB Thread ")
                super(JTAGGdbThread,self).__init__()

        def __del__(self):
                self.wait()

        def close(self):
                print("[*] Terminating JTAG GDB Thread ")
                self.proc.kill()
                self.terminate()

        def run(self):
                self.proc=subprocess.Popen(['x-terminal-emulator','-e','arm-none-eabi-gdb','--eval-command=\"target remote localhost:3333\"',self.elf_path])


class I2COperationThread(QtCore.QThread):
	def __init__(self,filepath,operation,size):
		print("[*] Initializing I2C Operation Thread ")
		self.filepath=filepath
		self.operation=operation
		super(I2COperationThread,self).__init__()

        def __del__(self):
                self.wait()

        def close(self):
                print("[*] Terminating I2C Operation Thread")
                self.terminate()

	def run(self):
		SIZE = 0x8000
		WCMD = "\xA0\x00\x00"
		RCMD = "\xA1"
		FOUT = self.filepath
		status=0
		op=0
		#Try to claim ftdi device 
		try:
			FT232H.enable_FTDI_driver()
			eeprom = MPSSE(I2C, FOUR_HUNDRED_KHZ)
		except Exception as e:
			print("[*] I2C Operation Thread Initialization Error :" + str(e))
			self.terminate()
			exit(1)

		#Perform Operations
		try:
			#FT232H.enable_FTDI_driver()
			if(self.operation=="Read"):
				op=1
				eeprom.Start()
				eeprom.Write(WCMD)
				if(eeprom.GetAck()==ACK):
					eeprom.Start()
					eeprom.Write(RCMD)
					if(eeprom.GetAck()==ACK):
						data=eeprom.Read(SIZE)
						eeprom.SendNacks()
						eeprom.Read(1)
				eeprom.Stop()
				open(FOUT,"wb").write(data)
				print("[*] I2C EEPROM Dump Successful ")

			elif(self.operation=="Erase"):
				op=2
				#Erase OP
				print("[*] Not implemented ")
                	elif(self.operation=="Write"):
				op=3
				#Write Op
				print("[*] Not Implemented ")

			eeprom.Close()
			status=1

		except Exception as e:
			eeprom.Close()
			print("[*] I2C Thread Operation Error :" +str(e))
			self.terminate()

                self.emit(SIGNAL('I2c_operation_handler(int,int)'),status,op)
		self.terminate()
