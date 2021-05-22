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

## Setup hostname, wifi countrycode, etc.
sudo raspi-config 

#Setup WIFI

wpa_passphrase "firkloevervej12" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null
# Enter password
sudo vim.tiny /etc/wpa_supplicant/wpa_supplicant.conf
# Remove password in clear test
 wpa_cli -i wlan0 reconfigure

sudo apt install docker docker-compose
sudo systemctl enable docker
sudo usermod -a -G docker pi

git clone git://github.com/groskopf/printerbox_sortkaffe.git --recurse-submodules

cd printerbox_sortkaffe

# Rename the printer ID
mkdir config
cp config/printerbox_config_example.json config/printerbox_config.json

# Power on printer and connect it
cd printerbox_cupsd/ && ./docker_build.sh && cd -
docker-compose build
sudo docker-compose up -d
