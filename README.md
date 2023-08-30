# fedc-led-sign
The code to make the FEDC first floor LED sign work.

## Setup:
```
sudo apt install build-essential python3-pip -y
sudo python3 -m pip install flask atexit pillow subprocess -y
git clone --recurse-submodules https://github.com/Zindswini/fedc-led-sign
cd fedc-led-sign/rpi-rgb-led-matrix
make
cd ../
chmod +x src/BannerDisplay.bash
```

## Running:
To run the script, run [BannerDisplay.bash](src/BannerDisplay.bash) **as root** from within the src folder. Root is needed for the library to access the gpio.
After the server is up, the web interface should be available from port 5000
