from PyQt4 import QtCore, QtGui
from Badge import Ui_MainWindow
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H
from subprocess import call
import serial,time,os,fnmatch
from time import sleep
import sys

FT232H.use_FT232H()
ft232h = FT232H.FT232H()

#Function to get a list of USB ports connected to the computer
def UART_getport():
	print("[*] UART_getport invoked ")
	path="/dev/"
	pattern="ttyUSB*"
	result=[]
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(os.path.join(root, name))
	return result

#Function to toggle GPIO pins
def GPIO_PinSwitch(pin_number, state):
	ft232h.setup(pin_number, GPIO.OUT)
	if(state):
		ft232h.output(pin_number, GPIO.HIGH)
                print "[*] GPIO_PinSWitch invoked -> Pin number "+str(pin_number)+" changed to HIGH "
	else:
                print "[*] GPIO_PinSWitch invoked -> Pin number "+str(pin_number)+" changed to LOW "
		ft232h.output(pin_number, GPIO.LOW)

ser=serial.Serial()
connection_flag=0
class Myclass(Ui_MainWindow):
	def __init__(self,dialog):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
		#-----------------------UART--------------------------------
		result=[]
		#ser=serial.Serial()
		global ser
	        self.textEdit_UartConsole.append("[*] Looking for USB devices")
		result=UART_getport()
		self.comboBox_Port.addItems(result)
		self.pushButton_Connect.clicked.connect(self.UART_Connect)
		self.lineEdit_UartInput.returnPressed.connect(self.UART_txsend)
		self.pushButton_AutoDetect.clicked.connect(self.UART_BaudRate_py)
		#-----------------------GPIO--------------------------------
		self.checkBox_d0.clicked.connect(self.GPIO_d0_Handler)
		self.checkBox_d1.clicked.connect(self.GPIO_d1_Handler)
		self.checkBox_d2.clicked.connect(self.GPIO_d2_Handler)
		self.checkBox_d3.clicked.connect(self.GPIO_d3_Handler)
		self.checkBox_d4.clicked.connect(self.GPIO_d4_Handler)
		self.checkBox_d5.clicked.connect(self.GPIO_d5_Handler)
		self.checkBox_d6.clicked.connect(self.GPIO_d6_Handler)
		self.checkBox_d7.clicked.connect(self.GPIO_d7_Handler)


	def UART_Connect(self):
		#Connects to the device who's port address is given by ComboBox_Port, disconnects if already connected
		print("[*] UART_Connect invoked ")
		global ser
		ser_port=str(self.comboBox_Port.currentText())
		baud_rate=int(str(self.comboBox_BaudRate.currentText()))
		ser.port=ser_port
		ser.baudrate=baud_rate
		try:
			if(str(ser.isOpen())=="False"):
				ser.open()
				self.lineEdit_UartInput.enabledChange(True)
				print("[*] UART_Connect executed Successfully ")
				self.textEdit_UartConsole.append("[*] Connected to device on port <b>"+ser_port+"</b>")
				self.textEdit_UartConsole.append("[*] -----------------------------------------------------------------------------------------------------------")
				self.pushButton_Connect.setText("Disconnect")
				print("[*] Serial port opened ")
			else:
				ser.close()
                                self.lineEdit_UartInput.enabledChange(False)
                                self.pushButton_Connect.setText("Connect")
                                self.textEdit_UartConsole.append("[*] Disconnected from device on port <b>"+ser_port+"</b>")
				print("[*] Serial port closed ")
		except:
			print("[*] UART_Connect Failed ")
			self.textEdit_UartConsole.append("[*] Connection Failed ")
		return

	def UART_txsend(self):
		#sends the contents of lineEdit_UartInput to the connected device
		print("[*] UART_txsend invoked ")
		global ser
		terminator=""
		command=self.lineEdit_UartInput.text()
		if(str(self.comboBox_Ender.currentText())=="No line ending"):
			terminator=""
		elif(str(self.comboBox_Ender.currentText())=="Carriage Return"):
			terminator="\r"
		elif(str(self.comboBox_Ender.currentText())=="New Line"):
			terminator="\n"
		elif(str(self.comboBox_Ender.currentText())=="Both CR + NL"):
			terminator="\r\n"
		if(len(command)>0):
			self.textEdit_UartConsole.append(command)
		ser.write(str((command+terminator)).encode())
		sleep(0.5)
		ser.write(terminator.encode())
		self.lineEdit_UartInput.setText("")
                output=""
                while ser.inWaiting() > 0:
                        output += ser.read(1)
		if(len(output)>0):
			self.textEdit_UartConsole.append(output)


	def UART_BaudRate_py(self):
		#Runs baudrate.py and autodetects the baudrate, sets the value in ComboBox_BaudRate
		print("[*] UART_BaudRate_py invoked")
		return

	def GPIO_d0_Handler(self, state):
		#Toggles GPIO pin D0
		print("[*] GPIO_d0_Handler invoked ")
		GPIO_PinSwitch(0,state)

	def GPIO_d1_Handler(self, state):
		#Toggles GPIO pin D1
		print("[*] GPIO_d1_Handler invoked ")
		GPIO_PinSwitch(1,state)

	def GPIO_d2_Handler(self, state):
		#Toggles GPIO pin D2
		print("[*] GPIO_d2_Handler invoked ")
		GPIO_PinSwitch(2,state)

	def GPIO_d3_Handler(self, state):
		#Toggles GPIO pin D3
		print("[*] GPIO_d3_Handler invoked ")
		GPIO_PinSwitch(3,state)

	def GPIO_d4_Handler(self, state):
		#Toggles GPIO pin D4
		print("[*] GPIO_d4_Handler invoked ")
		GPIO_PinSwitch(4,state)

	def GPIO_d5_Handler(self, state):
		#Toggles GPIO pin D5
		print("[*] GPIO_d5_Handler invoked ")
		GPIO_PinSwitch(5,state)

	def GPIO_d6_Handler(self, state):
		#Toggles GPIO pin D6
		print("[*] GPIO_d6_Handler invoked ")
		GPIO_PinSwitch(6,state)

	def GPIO_d7_Handler(self, state):
		#Toggles GPIO pin D7
		print("[*] GPIO_d7_Handler invoked ")
		GPIO_PinSwitch(7,state)

if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	dialog=QtGui.QMainWindow()
	prog=Myclass(dialog)
	dialog.show()
	sys.exit(app.exec_())
