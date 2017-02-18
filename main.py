#!/usr/bin/python

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import SIGNAL
from UI.Badge import Ui_MainWindow
from src.GpioInputMonitor import IPMonitor
from src.Threads import UART_ConsoleReadThread,I2CScanner,OpenOCDServerThread,JTAGTelnetThread,JTAGGdbThread,I2COperationThread
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
		self.gpio_init=0
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
		self.pushButton_I2cRun.clicked.connect(self.I2C_run)
		self.pushButton_JtagStartServer.clicked.connect(self.JTAG_startserver)
                self.JTAG_getcfg()
		self.pushButton_JtagConnect.clicked.connect(self.JTAG_telnetconnect)
		self.pushButton_JtagRunGdb.clicked.connect(self.JTAG_rungdb)


	def UART_getports(self):
		#Function checks for connected usb devices
        	print("[*] UART_getport invoked ")
		self.statusbar.showMessage("    UART  | Getting USB Devices ",2000)
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
                		self.statusbar.showMessage("    UART  | Connected to "+str(ser_port),2000)
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
				del(self.uartReadThread)
                                self.lineEdit_UartInput.enabledChange(False)
                                self.pushButton_UartConnect.setText("Connect")
                                self.statusbar.showMessage("    UART  | Disconnected from "+str(ser_port),2000)
				print("[*] Serial port closed ")
		except Exception as e:
			print("[*] UART_Connect Failed ->  "+str(e))
                        self.statusbar.showMessage("    UART  | Connection Failed ",2000)
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
                self.statusbar.showMessage("    UART  | Sending %d bytes "%(len(command)*2),1000)
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
                        self.statusbar.showMessage("   SPI  | Looking for devices ",1000)
		elif cmd=="Read":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H','-r',filepath])
                        self.statusbar.showMessage("   SPI  | Reading data from SPI device ",1000)
		elif cmd=="Write":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H','-w',filepath])
                        self.statusbar.showMessage("   SPI  | Writing to SPI device ",1000)
		elif cmd=="Erase":
			self.SPI_process.start('flashrom',['-p','ft2232_spi:type=232H','--erase',filepath])
                        self.statusbar.showMessage("   SPI  | Erasing data on SPI device ",1000)

	def FTDI_setup(self):
                	try:
				if(self.ft232h):
					print("[*] FTDI Drivers already enabled ")
				else:
                                	self.statusbar.showMessage("    Badge  | Setting up FTDI drivers ",1000)
					print("[*] Enabling Adafruit FTDI ")
                        		FT232H.use_FT232H()
                        		self.ft232h = FT232H.FT232H()

			except Exception as e:
                                self.statusbar.showMessage("    Badge  | FTDI driver setup failed ",1000)
                                print("[*] Error : "+str(e))

	def FTDI_destroy(self):
		try:
			self.ft232h.close()
		except:
			print("[*] FTDI Drivers already disabled" )


	def GPIO_setup(self):
		if(self.gpio_init==0):
			print("[*] Setting up GPIO pins")
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


	def GPIO_handler(self,pin):
		self.FTDI_setup()
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

	def I2C_run(self):
		operation=self.comboBox_I2cOperation.currentText()
		file=self.lineEdit_I2cFilePath.text()
		if(operation=="Find Chip"):
                	self.FTDI_setup()
                        self.textEdit_I2cConsole.append("")
                        self.statusbar.showMessage("    I2C   | Device scan initializing ",1000)
                	self.textEdit_I2cConsole.append("[*] Scanning all I2C addresses. ")
			self.I2CScanThread=I2CScanner(self.ft232h)
			self.I2CScanThread.start()
                	QtCore.QObject.connect(self.I2CScanThread,QtCore.SIGNAL("I2c_device_found(int)"), self.I2C_adddevice)



		elif(operation=="Read"):
			#Readop
                        self.textEdit_I2cConsole.append("")
			print("[*] Reading I2c EEPROM ")
                        self.textEdit_I2cConsole.append("[*] Dumping the contents of I2C EEPROM ")
			self.I2COpThread=I2COperationThread(file,operation,8000)
			self.I2COpThread.start()
			QtCore.QObject.connect(self.I2COpThread,QtCore.SIGNAL("I2c_operation_handler(int,int)"),self.I2C_operationhandler)

		elif(operation=="Erase"):
			#Writeop
			print("[*] Erasing I2C EEPROM ")
	                self.textEdit_I2cConsole.append("")
                        self.textEdit_I2cConsole.append("[*] Erasing the contents of I2C EEPROM ")
                        self.I2COpThread=I2COperationThread(file,operation,8000)
                        self.I2COpThread.start()
                        QtCore.QObject.connect(self.I2COpThread,QtCore.SIGNAL("I2c_operation_handler(int,int)"),self.I2C_operationhandler)


	def I2C_adddevice(self,address):
		if(address>=1000):
			count=address-1000
                	self.textEdit_I2cConsole.append("[*] Found "+str(count)+" I2C Devices ")
                       	self.statusbar.showMessage("    I2C   | Device scan complete ",500)
                        self.ft232h.close()
			del(self.I2CScanThread)
		else:
			self.textEdit_I2cConsole.append("[*] Found I2C device at address 0x{0:02X}".format(address))


	def I2C_operationhandler(self,status,op):
		if(status==0):
			self.textEdit_I2cConsole.append("[*] I2c Operation Failed ")
			print("[*] I2C Operation Failed ")
		else:
			if(op==1):
                                self.statusbar.showMessage("    I2C   | I2C Dump Successful ",500)
	                        self.textEdit_I2cConsole.append("[*] I2c Read Operation Successful ")
                        elif(op==2):
                                self.statusbar.showMessage("    I2C   | I2C Write Successful ",500)
                                self.textEdit_I2cConsole.append("[*] I2c Erase Operation Successful ")
                        elif(op==3):
                                self.statusbar.showMessage("    I2C   | I2C Write Successful ",500)
                                self.textEdit_I2cConsole.append("[*] I2c Erase Operation Successful ")
                self.textEdit_I2cConsole.append("")




        def JTAG_getcfg(self):
                #Function checks for .cfg files in the 'cfg/' directory
                print("[*] JTAG_getcfg invoked ")
                path="cfg/"
                pattern="*cfg"
                result=[]
                for root, dirs, files in os.walk(path):
                        for name in files:
                                if fnmatch.fnmatch(name, pattern):
                                        result.append(os.path.join(root, name))
		result.sort()
		cfg_list=[]
		for iterator in result:
			cfg_list.append(iterator.replace("cfg/",""))
                self.comboBox_JtagSelectDevice.addItems(cfg_list)

        def JTAG_startserver(self):
		if(self.pushButton_JtagStartServer.isChecked()):
                	print("[*] JTAG_StartServer Executing ")
                	self.textEdit_JtagConsole.append("\n[*] Initializing OpenOCD Server in the background")
			self.pushButton_JtagStartServer.setText("Stop OpenOCD Server")
                	filepath=str(self.comboBox_JtagSelectDevice.currentText())
			self.openocdthread=OpenOCDServerThread(filepath)
			self.openocdthread.start()
		else:
			print("[*] Stopping OpenOCD Server ")
                        self.textEdit_JtagConsole.append("[*] Stopping OpenOCD Server")
                        self.pushButton_JtagStartServer.setText("Start OpenOCD Server")
			self.openocdthread.close()
			del(self.openocdthread)

	def JTAG_telnetconnect(self):
		if(self.pushButton_JtagConnect.isChecked()):
			self.JtagTelnetThread=JTAGTelnetThread()
			self.JtagTelnetThread.start()
			self.pushButton_JtagConnect.setText(" Disconnect ")
		else:
                        self.pushButton_JtagConnect.setText("Connect to OpenOCD Server")
			self.JtagTelnetThread.close()
			del(self.JtagTelnetThread)

	def JTAG_rungdb(self):
		if(self.pushButton_JtagRunGdb.isChecked()):
			elf_path=str(self.lineEdit_JtagElfPath.text())
			self.gdbthread=JTAGGdbThread(elf_path)
			self.gdbthread.start()
			self.pushButton_JtagRunGdb.setText(" Stop GDB ")
		else:
                        self.pushButton_JtagRunGdb.setText(" Run GDB ")
                        self.gdbthread.close()
                        del(self.gdbthread)

if __name__=="__main__":
        app=QtGui.QApplication(sys.argv)
        dialog=QtGui.QMainWindow()
	app.setWindowIcon(QIcon("UI/icon.png"))
        prog=BadgeMain(dialog)
        dialog.show()
        sys.exit(app.exec_())
