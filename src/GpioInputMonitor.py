from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from UI.Gpio import Ui_Form
from Threads import InputMonitorThread


class IPMonitor(QtGui.QWidget, Ui_Form):
	def __init__(self,ft232h):
		self.ft232h=ft232h
        	QtGui.QWidget.__init__(self)
        	self.setupUi(self)
                pin_set=[]
                PinStates=[]
	        self.PinMappings={0:self.D0_Status,1:self.D1_Status, 2:self.D2_Status, 3:self.D3_Status, 4:self.D4_Status, 5:self.D5_Status, 6:self.D6_Status, 7:self.D7_Status}
		print("[*] Input monitor Initialized ")
                self.CloseButton.clicked.connect(self.close)
                self.StartMonitor.clicked.connect(self.UpdatePinStates)
                self.CloseButton.clicked.connect(self.stopthread)
		self.CloseButton.clicked.connect(self.close_monitor)
                input_pins=ft232h.input_pins([0,1,2,3,4,5,6,7])
                for x in range(0,8):
                        if(input_pins[x]):
                                pin_set.append(x)
                print("[*] Pins Set as input "+str(pin_set))
                self.pin_set=pin_set

	def stopthread(self):
		self.thread.close()

	def UpdatePinStates(self):
		print("[*] Thread Starter ")
		self.thread=InputMonitorThread(self.pin_set,self.ft232h)
		self.connect(self.thread, SIGNAL("update_states(int,int)"), self.update_states)
		self.thread.start()

	def update_states(self,state,pin):
		if(state):
			self.PinMappings[pin].setText("State : HIGH ")
		else:
                        self.PinMappings[pin].setText("State : LOW ")

	def close_monitor(self):
		self.close()

