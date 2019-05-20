#!/bin/bash

x="$(hostnamectl)"
PACKAGE="apt install -y"


if [[ $x == *"Ubuntu"* ]]; then
        PACKAGE="apt install -y"
	apt update
	apt upgrade
	add-apt-repository ppa:kivy-team/kivy -y
	apt install python-kivy python3-kivy
elif [[ $x == *"Arch Linux"* ]]; then
        PACKAGE="pacman -S --noconfirm"
	pacman -Syu
	pacman -S python3-pip
	pip3 install kivy
elif [[ $x == *"Raspbian"* ]]; then
        PACKAGE="apt install -y"
	apt update   
        apt upgrade
	apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
	pkg-config libgl1-mesa-dev libgles2-mesa-dev \
	python-setuptools libgstreamer1.0-dev git-core \
	gstreamer1.0-plugins-{bad,base,good,ugly} \
	gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
	xclip xsel samba
else
        echo "UNKNOWN DISTRO"
	exit 1
fi

$PACKAGE python3-pip python3 python3-dev git
pip3 install -U Cython==0.28.2
pip3 install pygame netifaces pyserial

if [[ $x == *"Raspbian"* ]]; then
	git clone https://github.com/kivy/kivy
	cd kivy
	python3 setup.py build
	python3 setup.py install
fi

cd ~/
git clone https://github.com/Angoosh/EPP_cutter cutter
cd ~/cutter/src
mkdir gcodes
mkdir logs
chmod +x main.py
cd ~/
echo "cd ~/cutter/src" >> .bashrc
echo "./main.py" >> .bashrc
cd ~/cutter
mv powerbtn.py /usr/local/bin
mv IP.py /usr/local/bin
chmod +x /usr/local/bin/powerbtn.py
mv powerbtn.sh /etc/init.d
chmod +x /etc/init.d/powerbtn.sh
update-rc.d powerbtn.sh defaults
rm rpi_install.sh
rm ubuntu_install.sh
rm arch_install.sh
rm install.sh
rm README.md
rm -rf PCB

if [[ $x == *"Raspbian"* ]]; then
	echo "[gcodes]" >> /etc/samba/smb.conf
	echo "   comment = Gcode folder for cutter" >> /etc/samba/smb.conf
	echo "   path = /home/pi/cutter/src/gcodes" >> /etc/samba/smb.conf
	echo "   browsable = yes" >> /etc/samba/smb.conf
	echo "   read only = no" >> /etc/samba/smb.conf
	echo "[logs]" >> /etc/samba/smb.conf
        echo "   comment = Logs folder for cutter" >> /etc/samba/smb.conf
        echo "   path = /home/pi/cutter/src/logs" >> /etc/samba/smb.conf
        echo "   browsable = yes" >> /etc/samba/smb.conf
        echo "   read only = yes" >> /etc/samba/smb.conf
	service smbd restart
	smbpasswd -a pi
fi
sudo reboot
