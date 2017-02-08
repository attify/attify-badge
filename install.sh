#!/bin/bash

RED='\033[0:31m'


echo "[*] Updating apt"
apt-get update

echo "[*] Getting Pyserial"
sudo apt-get install python-serial

echo "[*] Getting PyQt "
sudo apt-get install python-qt4

echo "[*] Getting git"
sudo apt-get install git

echo "[*] Getting Unzip "
sudo apt-get install unzip

echo "[*] Cloning Adafruit's FT232H Libraries"
git clone https://www.github.com/adafruit/Adafruit_Python_GPIO

echo "[*] Installing Adafruit's FT232H Libraries "
cd Adafruit_Python_GPIO/
sudo python setup.py install

echo "[*] Getting LibFTDI "
echo "[*] Installing dependencies "
sudo apt-get install build-essential libusb-1.0-0-dev swig cmake python-dev libconfuse-dev libboost-all-dev

echo "[*] Downloading Libraries " 
wget http://www.intra2net.com/en/developer/libftdi/download/libftdi1-1.2.tar.bz2

echo "[*] Decompressing Libraries "
tar xvf libftdi1-1.2.tar.bz2
cd libftdi1-1.2
mkdir build
cd build

echo "[*] Installing Libraries "
cmake -DCMAKE_INSTALL_PREFIX="/usr/" ../
make
sudo make install

cd ../../

echo "[*] Removing Files "
sudo rm -r libftdi1-1.2.tar.bz2

echo "[*] Installation Complete "

echo "[*] To run the program run -> sudo python main.py "
echo "[*] May the force be with you"


