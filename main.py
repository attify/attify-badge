#!/usr/bin/python


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from UI.Badge import Ui_MainWindow
from src.GpioInputMonitor import IPMonitor
from src.Threads import UART_ConsoleReadThread
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H
import serial,os,fnmatch,sys,subprocess


class BadgeMain(Ui_MainWindow):
        def __init__(self,dialog,parent=None):
                Ui_MainWindow.__init__(self)
		self.ser=serial.Serial()
                self.setupUi(dialog)
		self.UART_getports()
		self.pushButton_UartRefresh.clicked.connect(self.UART_getports)
                self.pushButton_UartConnect.clicked.connect(self.UART_connect)
		self.lineEdit_UartInput.returnPressed.connect(self.UART_send)
		self.pushButton_SpiRun.clicked.connect(self.SPI_run)
		self.SPI_process = QtCore.QProcess()
		self.SPI_process.readyRead.connect(self.SPI_dataReady)
		self.ft232h=0
 	        self.checkBox_d0.clicked.connect(lambda: self.GPIO_handler(0))
                self.checkBox_d1.clicked.connect(lambda: self.GPIO_handler(1))
                self.checkBox_d2.clicked.connect(lambda: self.GPIO_handler(2))
                self.checkBox_d3.clicked.connect(lambda: self.GPIO_handler(3))
                self.checkBox_d4.clicked.connect(lambda: self.GPIO_handler(4))
                self.checkBox_d5.clicked.connect(lambda: self.GPIO_handler(5))
                self.checkBox_d6.clicked.connect(lambda: self.GPIO_handler(6))
                self.checkBox_d7.clicked.connect(lambda: self.GPIO_handler(7))
		self.InputMonitor=None
                self.pushButton_GpioStartInputMonitor.clicked.connect(self.GPIO_startmonitor)


	def UART_getports(self):
		#Function checks for connected usb devices
        	print("[*] UART_getport invoked ")
        	path="/dev/"
        	pattern="ttyUSB*"
        	result=[]
        	for root, dirs, files in os.walk(path):
        	        for name in files:
        	                if fnmatch.fnmatch(name, pattern):
        	                        result.append(os.path.join(root, name))
        	self.comboBox_UartPort.clear()
		self.comboBox_UartPort.addItems(result)

	def UART_connect(self):
		#Connects to the device who's port address is given by ComboBox_Port, disconnects if already connected
		print("[*] UART_Connect invoked ")
		ser_port=str(self.comboBox_UartPort.currentText())
		baud_rate=int(str(self.comboBox_UartBaud.currentText()))
		self.ser.port=ser_port
		self.ser.baudrate=baud_rate
		try:
			if(str(self.ser.isOpen())=="False"):
				self.ser.open()
				self.lineEdit_UartInput.enabledChange(True)
				print("[*] UART_Connect executed Successfully ")
				self.pushButton_UartConnect.setText("Disconnect")
				print("[*] Serial port opened ")
				if(self.ser.isOpen()):
			                self.uartReadThread=UART_ConsoleReadThread(self.ser)
					QtCore.QObject.connect(self.uartReadThread,QtCore.SIGNAL("update_console(QString)"), self.UART_read)
					print("[*] Starting UARTConsoleReadThread ")
					self.uartReadThread.start()
			else:
				print("[*] Stopping UART_ConsoleReadThread ")
				self.uartReadThread.close()
				self.ser.close()
                                self.lineEdit_UartInput.enabledChange(False)
                                self.pushButton_UartConnect.setText("Connect")
				print("[*] Serial port closed ")
		except Exception as e:
			print("[*] UART_Connect Failed ->  "+str(e))
			self.textEdit_UartConsole.append("[*] Connection Failed ")
		return


	def UART_read(self, QString):
		if(len(str(QString))>0):
			self.textEdit_UartConsole.insertPlainText(str(QString))
		self.textEdit_UartConsole.moveCursor(QtGui.QTextCursor.End)

	def UART_send(self):
		#sends the contents of lineEdit_UartInput to the connected device
		print("[*] UART_txsend invoked ")
		terminator=""
		command=self.lineEdit_UartInput.text()
		if(command=="clear"):
			self.textEdit_UartConsole.clear()
			command=""
		elif(str(self.comboBox_UartTerminator.currentText())=="No line ending"):
			terminator=""
		elif(str(self.comboBox_UartTerminator.currentText())=="Carriage Return"):
			terminator="\r"
		elif(str(self.comboBox_UartTerminator.currentText())=="New Line"):
			terminator="\n"
		elif(str(self.comboBox_UartTerminator.currentText())=="Both CR + NL"):
			terminator="\r\n"
		self.ser.write(str((command+terminator)).encode())
		self.ser.write(terminator.encode())
		self.lineEdit_UartInput.setText("")

	def SPI_dataReady(self):
		cursor=self.textEdit_SpiConsole.textCursor()
		cursor.movePosition(cursor.End)
		cursor.insertText(str(self.SPI_process.readAll()))
		self.textEdit_SpiConsole.ensureCursorVisible()

	def SPI_run(self):
		print("[*] SPI_RunCmds Executing ")
		self.textEdit_SpiConsole.append("----------------------------------------------------------------\n")
		filepath=str(self.lineEdit_SpiFilePath.text())
		cmd=str(self.comboBox_SpiOperation.currentText()).strip()
		if cmd=="Find Chip":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H'])
		elif cmd=="Read":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H','-r',filepath])
		elif cmd=="Write":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H','-w',filepath])
		elif cmd=="Erase":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H','--erase',filepath])

	def GPIO_setup(self):
        	if(self.ft232h==0):
                	try:
				print("[*] Setting up GPIO ")
                        	FT232H.use_FT232H()
                        	self.ft232h = FT232H.FT232H()
				#setting everything as out
				#because leaving then un-
				#initialized confuses the
				#Input Monitor
	        		self.ft232h.setup(0, GPIO.OUT)
        			self.ft232h.setup(1, GPIO.OUT)
        			self.ft232h.setup(2, GPIO.OUT)
        			self.ft232h.setup(3, GPIO.OUT)
        			self.ft232h.setup(4, GPIO.OUT)
        			self.ft232h.setup(5, GPIO.OUT)
        			self.ft232h.setup(6, GPIO.OUT)
       			 	self.ft232h.setup(7, GPIO.OUT)

                	except Exception as e:
                        	print("[*] Error : "+str(e))
                        	exit()

	def GPIO_handler(self,pin):
		self.GPIO_setup()
		pin_combo={0:self.comboBox_d0,1:self.comboBox_d1,2:self.comboBox_d2,3:self.comboBox_d3,4:self.comboBox_d4,5:self.comboBox_d5,6:self.comboBox_d6,7:self.comboBox_d7}
		pin_check={0:self.checkBox_d0,1:self.checkBox_d1,2:self.checkBox_d2,3:self.checkBox_d3,4:self.checkBox_d4,5:self.checkBox_d5,6:self.checkBox_d6,7:self.checkBox_d7}
		mode=pin_check[pin].isChecked()
		if(str(pin_combo[pin].currentText())=="Input"):
			self.ft232h.setup(pin,GPIO.IN)
			print("[*] Pin "+str(pin)+" set as Input")
		elif(str(pin_combo[pin].currentText())=="Output"):
                        print("[*] Pin "+str(pin)+" set as Output")
			self.ft232h.setup(pin,GPIO.OUT)
			if(mode):
				print("[*] Pin "+str(pin)+" : HIGH ") 
				self.ft232h.output(pin, GPIO.HIGH)
			else:
				self.ft232h.output(pin, GPIO.LOW)
                                print("[*] Pin "+str(pin)+" : LOW ") 

	def GPIO_startmonitor(self):
		if self.InputMonitor is None:
			self.InputMonitor=IPMonitor(self.ft232h)
		self.InputMonitor.show()


if __name__=="__main__":
        app=QtGui.QApplication(sys.argv)
        dialog=QtGui.QMainWindow()
        prog=BadgeMain(dialog)
        dialog.show()
        sys.exit(app.exec_())

