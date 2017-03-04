#!/bin/bash
echo
echo "      ___  _   _   _  __            "
echo "     / _ \| | | | (_)/ _|           "
echo "    / /_\ \ |_| |_ _| |_ _   _      "
echo "    |  _  | __| __| |  _| | | |     "
echo "    | | | | |_| |_| | | | |_| |     "
echo "    \_| |_/\__|\__|_|_|  \__, |     "
echo "                          __/ |     "
echo "                         |___/      "
echo
echo "[*] Attify Badge Tool v1.0 Installer" 

path="$(pwd)"
cd ${path}

sleep 1
echo
echo "[*] Updating apt"
echo
sudo apt-get update
echo
echo "[*] Getting Pyserial"
echo
sudo apt-get install python-serial
echo
echo "[*] Installing Flashrom "
echo
sudo apt-get install flashrom
echo
echo "[*] Installing arm tool chain "
echo
sudo apt install gdb-arm-none-eabi
echo
echo "[*] Installing OpenOCD "
echo
sudo apt-get install openocd
echo
echo "[*] Getting PyQt "
echo
sudo apt-get install python-qt4
echo
echo "[*] Getting git"
echo
sudo apt-get install git
echo
echo "[*] Getting Unzip "
echo
sudo apt-get install unzip
echo
echo "[*] Getting LibFTDI "
echo "[*] Installing dependencies "
sudo apt-get install build-essential libusb-1.0-0-dev swig cmake python-dev libconfuse-dev libboost-all-dev
echo
cd ${path}
echo "[*] Downloading Libraries "
wget http://www.intra2net.com/en/developer/libftdi/download/libftdi1-1.2.tar.bz2
echo
echo "[*] Decompressing Libraries "
tar xvf libftdi1-1.2.tar.bz2
sudo mv src/modcmakefile libftdi1-1.2/python/CMakeLists.txt
cd libftdi1-1.2
mkdir build
cd build
echo
echo "[*] Installing Libraries "
cmake -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python -DCMAKE_INSTALL_PREFIX="/usr/" ../
make
sudo make install

cd ../../
cd ${path}
echo "[*] Cloning devttys0's libmpsse repository"
echo
git clone https://github.com/devttys0/libmpsse
sudo cp src/mpsse.h libmpsse/src/
cd libmpsse/src
sudo ./configure
sudo make
sudo make install
cd ../../
echo
echo
cd ${path}
echo "[*] Cloning Adafruit's FT232H repository"
git clone https://www.github.com/adafruit/Adafruit_Python_GPIO
echo
echo "[*] Installing Adafruit's FT232H Libraries "
cd Adafruit_Python_GPIO/
sudo python setup.py install
echo
cd ..
sudo rm -r Adafruit_Python_GPIO/
sudo rm -r libmpsse
sudo rm -r libftdi1-1.2.tar.bz2
echo
echo
echo "[*] Installation Complete "
echo
echo "[*] To run the program run -> sudo python main.py "
echo
echo 
echo  " < Happy Hacking !  >              "
echo  "   ----------------             "
echo  "        o   ^__^                "
echo  "         o  (oo)\_______        "
echo  "            (__)\       )\/\    "
echo  "                ||----w |       "
echo  "                ||     ||       "
echo
echo




