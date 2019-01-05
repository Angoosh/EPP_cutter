#!/bin/bash

sudo apt update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel
sudo apt install -y python3-pip
sudo pip3 install -U Cython==0.28.2
git clone https://github.com/kivy/kivy
cd kivy
python3 setup.py build
sudo python3 setup.py install
cd ~/cutter/src
chmod +x main.py
cd ~/
echo "cd ~/cutter/src" >> .bashrc
echo "sudo ./main.py" >> .bashrc
cd ~/cutter
rm rpi_install.sh
rm ubuntu_install.sh
rm README.md
sudo reboot
