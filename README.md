# EPP_cutter
Final exam project<br />
Contains controlling app and gcode sender.<br />
CAM is here: https://bitbucket.org/Zbynek_Dostal/cam-for-hot-wire <br />
<br />
## Installation:<br />
```
git clone https://github.com/Angoosh/EPP_cutter ~/cutter
cd ~/cutter
sudo sh install.sh
```

**Supported distros:** 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Ubuntu 16.04 and up<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Raspbian Stretch and up <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Arch Linux <br />
<br />
Connect your power button to GPIO 3 and GND <br />
Connect your power button light to GPIO 2 and GND <br />
Connect your Emergency button to GPIO 14 and GND <br />
Connect your Emergency button light to GPIO 4 and GND <br />
<br />
**IP LED display:** <br />
b7 = GPIO-5     = 128<br />
b6 = GPIO-6     = 64<br />
b5 = GPIO-13    = 32<br />
b4 = GPIO-19    = 16<br />
b3 = GPIO-26    = 8<br />
b2 = GPIO-16    = 4<br />
b1 = GPIO-20    = 2<br />
b0 = GPIO-21    = 1<br />
<br />
(all GPIOs are BCM named) <br />
```
sudo usermod -a -G dialout USER_NAME
```
When installation is finished pi will ask for new password. It is password for samba. <br />
Path to samba drive is: <br />
  On Windows: \\\RPI_IP_ADDRESS\ <br />
  On Linux: smb://RPI_IP_ADDRESS/ <br />
<br />
When selecting gcode the path is: gcodes/YOUR_GCODE.gcode <br />
<br />
Default username is: cutter and password is Pizza <br />

enjoy!

