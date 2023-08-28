#!/bin/bash

# Make sure C++ build is up to date
echo "Building matrix code"
cd rpi-rgb-led-matrix
make
cd ..

# Start python server
python3 ./main.py


#sudo python3 home/pi/BannerGenerator.py
#echo "Banner Generated"
#echo "Starting Up LED Matrix"
#sudo taskset 3 sudo /home/pi/Desktop/rpi-rgb-led-matrix/examples-api-use/demo --led-rows=32 --led-chain=10 --led-brightness=75 --led-gpio-mapping=adafruit-hat-pwm -m 10 -D 1 home/pi/banner.ppm
#echo "To change the banner edit the banner.txt file and reboot"
