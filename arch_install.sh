#!/bin/bash

sudo pacman -Syu
sudo pacman -S git python3-pip python3 python3-dev
sudo pip3 install pygame kivy netifaces pyserial

cd ~/
git clone https://github.com/Angoosh/EPP_cutter cutter
cd ~/cutter/src
mkdir gcodes
chmod +x main.py
cd ~/
echo "cd ~/cutter/src" >> .bashrc
echo "./main.py" >> .bashrc
cd ~/cutter
sudo mv powerbtn.py /usr/local/bin
sudo mv IP.py /usr/local/bin
sudo chmod +x /usr/local/bin/powerbtn.py
sudo mv powerbtn.sh /etc/init.d
sudo chmod +x /etc/init.d/powerbtn.sh
sudo update-rc.d powerbtn.sh defaults
rm rpi_install.sh
rm ubuntu_install.sh
rm README.md
rm -rf PCB
sudo reboot
