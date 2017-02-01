# attify-badge
Attify Badge GUI tool to interact over UART, SPI, JTAG, GPIO etc.

Requirements :
Adafruit's FT232H libraries
libftdi1-1.2
pyserial
PyQt4

I'll make a installer for the tool soon.

###Implemented :
- UART
- GPIO - output, input
- SPI  - preset commands ( read,write,erase,find )

###Not Implemented :
- SPI  - custon commands ( allow user to write his own flashrom commands )
- I2C
- JTAG


###Bugs :

- In the GPIO monitor window, the floating states are detected as high.
  this is a hardware issue which will be resolved in the next version of
  the badge

- The SPI tab shows output only after the process has completed, which might
  take too long, should get fixed by changing the os.popen() with a
  subprocess.popen and using communicate() to display the output
  This Should get fixed by today ^.

- The UART thread hangs some times due to a fcntl bug, working on it.

#### Updating the code
	Till now the code has been written in a pretty sequential manner, I kept
	adding stuff as I went. I plan to take a break before starting working on
	I2C and JTAG and restructuring the code to make it more modular.
	I'm planning to add seperate classes for each of the protocols, which would
	make the code easier to read, and also solve a couple of problems related to 
	intializing the interfaces. The problems are caused because when main.py runs
	Each interface tries to intialize itself and obviously not all of them are 
	able to claim the FTDI devices, I solved this problem with a hacked-up
	sollution, but there might be more problems while trying to write the code 
	for JTAG and I2C. This is kinda important.

###Install: 
chmod +x install.sh
./install.sh
Run main.py ( with sudo )!

