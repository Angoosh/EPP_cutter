#!/bin/bash

sudo apt update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel samba
sudo apt install -y python3-pip
sudo pip3 install -U Cython==0.28.2
sudo pip3 install netifaces pyserial
git clone https://github.com/kivy/kivy
cd kivy
python3 setup.py build
sudo python3 setup.py install
cd ~/cutter/src
mkdir gcodes
sudo echo "[gcodes]" >> /etc/samba/smb.conf
sudo echo "   comment = Gcode folder for cutter" >> /etc/samba/smb.conf
sudo echo "   path = /home/pi/cutter/src/gcodes" >> /etc/samba/smb.conf
sudo echo "   browsable = yes" >> /etc/samba/smb.conf
sudo echo "   read only = no" >> /etc/samba/smb.conf
sudo service smbd restart
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
sudo smbpasswd -a pi
sudo reboot
