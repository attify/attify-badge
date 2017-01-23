# attify-badge
Attify Badge GUI tool to interact over UART, SPI, JTAG, GPIO etc.

Requirements :
Adafruit's FT232H libraries
libftdi1-1.2
pyserial
PyQt4

I'll make a installer for the tool soon.

Implemented :
- UART
- GPIO - output, input

Not Implemented :
- SPI
- I2C
- JTAG


Bugs :

- In the GPIO monitor window, the floating states are detected as high.
  this is a hardware issue which will be resolved in the next version of
  the badge


Run main.py ( with sudo )!

