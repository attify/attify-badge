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
- JTAG - OpenOCD Server

###Not Implemented :
- I2C
- JTAG  ( New window which allows direct firmware dumping )


###Bugs :

- In the GPIO monitor window, the floating states are detected as high.
  this is a hardware issue which will be resolved in the next version of
  the badge

- Messed up install.sh, should be fixed by tomorrow! 


###Install

- chmod +x install.sh
- ./install.sh

###Manual Install ( in case of weird errors ): 

- Installing Git
`sudo apt-get install git`

- Getting libftdi

`sudo apt-get update`

`sudo apt-get install build-essential libusb-1.0-0-dev swig cmake python-dev libconfuse-dev libboost-all-dev`

`wget http://www.intra2net.com/en/developer/libftdi/download/libftdi1-1.2.tar.bz2`

`tar xvf libftdi1-1.2.tar.bz2`

`cd libftdi1-1.2`

`mkdir build`

`cd build`

`cmake -DCMAKE_INSTALL_PREFIX="/usr/" ../`

`make`

`sudo make install`

- Getting Adafruit libraries

Clone from 
`https://github.com/adafruit/Adafruit_Python_GPIO`

or

`wget https://codeload.github.com/adafruit/Adafruit_Python_GPIO/zip/master`

`cd Adafruit_Python_GPIO-master/
sudo python setup.py`

- Getting pyserial

`sudo apt-get install python-serial`

- Get PyQt

`sudo apt-get install python-qt4`


- Run 
Run main.py from the attify-badge directory ( with sudo )!
`sudo python main.py'
