#!/bin/bash

sudo add-apt-repository ppa:kivy-team/kivy
sudo apt update
sudo apt-get install python-kivy python3-kivy python3-pip
pip3 install pyserial
cd ~/cutter/src
chmod +x main.py
cd ~/
echo "cd ~/cutter/src" >> .bashrc
echo "./main.py" >> .bashrc
