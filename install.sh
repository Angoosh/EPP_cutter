#!bin/bash

sudo apt update
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python-setuptools libgstreamer1.0-dev git-core gstreamer1.0-plugins {bad,base,good,ugly} gstreamer1.0-{omx,alsa} python-dev libmtdev-dev xclip xsel python-pip
sudo pip install -U Cython==0.28.2
sudo pip install git+https://github.com/kivy/kivy.git@master
git clone https://github.com/kivy/kivy
cd kivy
make
echo "export PYTHONPATH=$(pwd):\$PYTHONPATH" >> ~/.profile
source ~/.profile

