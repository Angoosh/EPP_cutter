#!/bin/bash

sudo add-apt-repository ppa:kivy-team/kivy -y
sudo apt update
sudo apt install python-kivy python3-kivy
sudo apt upgrade
sudo apt-get install python3-pip -y
pip3 install pyserial
cd ~/cutter/src
chmod +x main.py
cd ~/
echo "cd ~/cutter/src" >> .bashrc
echo "./main.py" >> .bashrc
cd ~/cutter
rm rpi_install.sh
rm ubuntu_install.sh
rm README.md
sudo reboot
