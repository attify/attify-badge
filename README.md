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


Run main.py ( with sudo )!

