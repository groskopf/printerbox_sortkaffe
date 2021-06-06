# printerbox_sortkaffe
Python program for "Sort Kaffe" integration with Printerbox

# Installation on the RPI

Install Raspberion OS on the flash card

## Setup network headlessly on the RPI

Write an empty text file named "ssh" (no file extension) to the root of the directory of the card. 

Place a file in the root folder called wpa_supplicant.conf. This must contain following:

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}

#Change password for user pi to pi
 
sudo passwd pi

## Setup hostname and change passwor
sudo raspi-config 

# Save idle power
sudo apt-get install cpufrequtils &&
echo 'GOVERNOR="powersave"' | sudo tee /etc/default/cpufrequtils &&
sudo update-rc.d ondemand disable 

# Disable Wifi and Bluetooth
echo dtoverlay=pi3-disable-wifi >> /boot/config.txt &&
echo dtoverlay=pi3-disable-bt >> /boot/config.txt

# Disable HDMI
sudo sed -i 's/exit 0/# Diable HDMI\n\/opt\/vc\/bin\/tvservice -o\n\nexit 0/' /etc/rc.local

# Setup docker  and logout
sudo apt install docker docker-compose &&
sudo systemctl enable docker &&
sudo usermod -a -G docker pi &&
exit

# blink1 support
sudo apt install libhidapi-hidraw0

# Clone project
git clone git://github.com/groskopf/printerbox_sortkaffe.git --recurse-submodules &&
cd printerbox_sortkaffe

# Rename the printer ID
mkdir config &&
cp src/printerbox_config_example.json config/printerbox_config.json &&
vim.tiny config/printerbox_config.json 

# Power on printer and connect it
cd printerbox_cupsd/ && ./docker_build.sh && cd - &&
docker-compose build &&
sudo docker-compose up -d
