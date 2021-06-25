# printerbox_sortkaffe
Python program for "Sort Kaffe" integration with Printerbox

## Installation on the RPI

Install Raspberion OS on the flash card

##Setup network headlessly on the RPI

Write an empty text file named "ssh" (no file extension) to the root of the directory of the card. 

Timezone
```
sudo timedatectl set-timezone Europe/Copenhagen &&
echo 'FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org' | sudo tee -a /etc/systemd/timesyncd.conf
```
Change password for user pi to pi
```
sudo passwd pi
```

Setup hostname, wait for network on boot
```
sudo raspi-config 
```

Update apt
```
sudo apt update && sudo apt upgrade
```

Save idle power
```
sudo apt-get install cpufrequtils &&
echo 'GOVERNOR="powersave"' | sudo tee /etc/default/cpufrequtils &&
sudo update-rc.d ondemand disable 
```

Disable Wifi and Bluetooth
```
echo dtoverlay=pi3-disable-wifi | sudo tee -a /boot/config.txt &&
echo dtoverlay=pi3-disable-bt | sudo tee -a /boot/config.txt
```
Disable HDMI
```
sudo sed -i 's/exit 0/# Diable HDMI\n\/opt\/vc\/bin\/tvservice -o\n\nexit 0/' /etc/rc.local
```

Setup docker  and logout
```
sudo apt install docker docker-compose &&
sudo systemctl enable docker &&
sudo usermod -a -G docker pi &&
exit
```

blink1 support
```
sudo apt install libhidapi-hidraw0
```

Clone project
```
git clone git://github.com/groskopf/printerbox_sortkaffe.git --recurse-submodules &&
cd printerbox_sortkaffe
```

Rename the printer ID
```
mkdir config &&
cp src/printerbox_config_example.json config/printerbox_config.json &&
vim.tiny config/printerbox_config.json 
```

Power on printer and connect it
```
cd printerbox_cupsd/ && ./docker_build.sh && cd - &&
docker-compose build &&
sudo docker-compose up -d
```


Reverse SSH setup

Generate SSH key

```
ssh-keygen && cat /home/pi/.ssh/id_rsa.pub  
```

Upload key to cloud.google.com

Change port and user name ti printerbox-n
```
echo -e '[Unit]\nDescription=Reverse SSH connection\nAfter=network.target\n\n[Service]\nType=simple\nExecStart=/usr/bin/ssh -vvv -g -N -T -o "ServerAliveInterval 10" -o "ExitOnForwardFailure yes" -R 6000:localhost:22 printerbox-1@35.234.110.50\nUser=pi\nGroup=pi\nRestart=always\nRestartSec=5s\n\n[Install]\nWantedBy=default.target\n' | sudo tee /etc/systemd/system/ssh-reverse.service && sudo vim.tiny /etc/systemd/system/ssh-reverse.service  

```
Test !

```
/usr/bin/ssh printerbox-2@35.234.110.50  
systemctl enable ssh-reverse.service && systemctl start ssh-reverse.service && systemctl status ssh-reverse.service
```



# Update
'blink1-tool.exe --gobootload'

Update via 'https://dfu.blink1.thingm.com/'

'blink1-tool --setstartup 1,1,2,255'


