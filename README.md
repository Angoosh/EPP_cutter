# EPP_cutter
Final exam project<br />
Contains controlling app and gcode sender.<br />
CAM is here: https://bitbucket.org/Zbynek_Dostal/cam-for-hot-wire <br />
<br />
## Installation:<br />
```
git clone https://github.com/Angoosh/EPP_cutter ~/cutter
cd ~/cutter
```
for system running ubuntu:
```
chmod +x ubuntu_install.sh
sudo ./ubuntu_install.sh
```
for RPi:
```
chmod +x rpi_install.sh
sudo ./rpi_install.sh
```
Connect your power button to GPIO 3 and GND <br />
Connect your power button light to GPIO 2 and GND <br />
Connect your Emergency button to GPIO 14 and GND <br />
Connect your Emergency button light to GPIO 4 and GND <br />
<br />
(all GPIOs are BCM named) <br />
```
sudo usermod -a -G dialout USER_NAME
```
When installation is finished pi will ask for new password. It is password for samba. <br />
Path to samba drive is: <br />
  On Windows: \\RPI_IP_ADDRESS\gcodes <br />
  On Linux: smb://RPI_IP_ADDRESS/gcodes <br />
<br />
When selecting gcode the path is: gcodes/YOUR_GCODE.gcode <br />
<br />
Default username is: cutter and password is Pizza <br />

enjoy!

