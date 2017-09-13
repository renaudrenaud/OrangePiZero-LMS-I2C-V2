# OrangePiZero-LMS-I2C-V2
Orange Pi Zero Pi One : Managing LCD I2C for Logitech Media Server 

The is the second version of the code:
- the first version was using PyLMS. PyLMS was containing few bugs and was unable to grab the bitrate
- this second version uses LMSTools. This version shows the bitrate on the LCD.

To use it: 
- download the LMSTools from my repo and put it for example in /home/sources/lms/LMSTools
- put the lms_lcd.py on /home/sources/lms
- enter python /home/sources/lms/lms_lcd.py -s myserveripadress -c

If you want to start it at boot then enter on the command line:
crontabt -e

then add the line at the bottom of the file
@reboot python /home/sources/lcdv2/lms_lcd.py -s 192.168.1.140 -c

Please note
- -s <ipserver> to indicate the LMS server IP Adress (something like 192.168.1.140
- -p <ipPlayer> to indicate the IP of the player. If no parameter, shows the current player info
- -w <lcd_width> default is 20 for 20x4. Use -w 16 to indicate 16x2 LCD
- -l <lcd_address> indicated by i2cdetect https://www.sites.google.com/site/orangepizero/logitech-media-server/lcd-i2c
- -c for clock mode to always have the time information on the screen
