from LMSTools import LMSServer
from LMSTools import LMSTags as tags
from time import sleep
import smbus
import time
import sys, getopt

myLCD = None
lcd_w = None


class LCDLCD:
    """Pseudo LCD Class for printingon console, not on the LCD"""
    def __init__(self, lcd_address, lcd_width):
		# Define some device parameters
       
        self.I2C_ADDR  = lcd_address # 0x3f I2C device address 
                                     # To detect use sudo i2cdetect -y 0
                                     # or for RPi 2  sudo i2cdetect -y 1
        self.LCD_WIDTH = lcd_width   # 16 or 20 Maximum characters per line
        print ("class LCD " + str(lcd_width))    
        #LCD_WIDTH = 20 OR 16   # Maximum characters per line

        # Define some device constants
        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
        self.LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

        self.LCD_BACKLIGHT  = 0x08  # On
        #LCD_BACKLIGHT = 0x00  # Off

        self.ENABLE = 0b00000100 # Enable bit

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        #Open I2C interface
        # self.bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        #bus = smbus.SMBus(1) # Rev 2 Pi uses 1

        #def lcd_init():
        # Initialise display
        
    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command
        

        self.bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        self.bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

        # High bits
        try:
            self.bus.write_byte(self.I2C_ADDR, self.bits_high)
        except:
            print ("------------------------------------------")
            print ("ERROR - Cannot write on the LCD @ Address " + self.I2C_ADDR )
            print ("------------------------------------------")
            printhelp()
            quit()
        self.bus.write_byte(self.I2C_ADDR, self.bits_high)
        self.lcd_toggle_enable(self.bits_high)

        # Low bits
        self.bus.write_byte(self.I2C_ADDR, self.bits_low)
        self.lcd_toggle_enable(self.bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.ljust(self.LCD_WIDTH," ")
        # if line == 1:
        #     self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
        # elif line == 2:
        #     self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
        # elif line == 3:
        #     self.lcd_byte(self.LCD_LINE_3, self.LCD_CMD)
        # elif line == 4:
        #     self.lcd_byte(self.LCD_LINE_4, self.LCD_CMD)    
        # for i in range(self.LCD_WIDTH):
        #     self.lcd_byte(ord(message[i]),self.LCD_CHR)
        print(str(line) + " - " + message)





class LCD:
    """LCD Class build from the work of Math Hawkins"""
    def __init__(self, lcd_address, lcd_width):
		# Define some device parameters
       
        self.I2C_ADDR  = lcd_address # 0x3f I2C device address 
                                     # To detect use sudo i2cdetect -y 0
                                     # or for RPi 2  sudo i2cdetect -y 1
        self.LCD_WIDTH = lcd_width   # 16 or 20 Maximum characters per line
        print ("class LCD " + str(lcd_width))    
        #LCD_WIDTH = 20 OR 16   # Maximum characters per line

        # Define some device constants
        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
        self.LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

        self.LCD_BACKLIGHT  = 0x08  # On
        #LCD_BACKLIGHT = 0x00  # Off

        self.ENABLE = 0b00000100 # Enable bit

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        #Open I2C interface
        self.bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        #bus = smbus.SMBus(1) # Rev 2 Pi uses 1

        #def lcd_init():
        # Initialise display
        self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
        self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command
        

        self.bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        self.bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

        # High bits
        try:
            self.bus.write_byte(self.I2C_ADDR, self.bits_high)
        except:
            print ("------------------------------------------")
            print ("ERROR - Cannot write on the LCD @ Address " + self.I2C_ADDR )
            print ("------------------------------------------")
            printhelp()
            quit()
        self.bus.write_byte(self.I2C_ADDR, self.bits_high)
        self.lcd_toggle_enable(self.bits_high)

        # Low bits
        self.bus.write_byte(self.I2C_ADDR, self.bits_low)
        self.lcd_toggle_enable(self.bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.ljust(self.LCD_WIDTH," ")
        if line == 1:
            self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
        elif line == 2:
            self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
        elif line == 3:
            self.lcd_byte(self.LCD_LINE_3, self.LCD_CMD)
        elif line == 4:
            self.lcd_byte(self.LCD_LINE_4, self.LCD_CMD)    
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)
        #print(str(line) + " - " + message)



def lms_time_to_string(lms_time ):
    """convert a time from LMS into a mm:ss time"""
    seconds = int(lms_time)
    minutes = int(seconds / 60)
    seconds = seconds - minutes * 60
    if seconds < 10 :
            seconds = "0" + str(seconds)
    if minutes < 10 :
        minutes = "0" + str(minutes)
    return "%s:%s" %(minutes, seconds)


def printhelp():
    """Print help to explain parameters"""
    print ("------------ USAGE ---------------------------------------------")
    print ("lms_testcom.py ")
    print ("-s <ipserver>")
    print ("-p <ipPlayer>")
    print ("-w <lcd_width>")
    print ("-l <lcd_address>")
    print ("-c for clock mode on line 4")

    print ("ipserver like 192.168.1.102")
    print ("player like 192.168.1.115 / default = auto detect") 
    print ("lcd with is 16 or 20 / 16 means 16x2, 20 means 20x4 / default = 20")
    print ("lcd_address is the i2C LCD address like 0x3f (default). Use sudo i2cdetect -y 0") 
    print ("----------------------------------------------------------------")
    return

def LCDTime(myLCD, lcd_w):
    """PRINT Clock on LCD"""
    if lcd_w ==16:
        myLCD.lcd_string(" **  Clock **",1)
        myLCD.lcd_string(time.strftime('%Y-%m-%d %H:%M'),2)
        sleep(5)
    else:
        myLCD.lcd_string("     ** Clock **",1)
        myLCD.lcd_string(" ",2)
        myLCD.lcd_string(" " + time.strftime('%Y-%m-%d  %H:%M'),3)
        myLCD.lcd_string(" ",4) #sq.rescanprogress(),4)
        
        sleep(5)
    return

def playerAutodetect(sc, myLCD):
    """Discover the player in PLAY mode"""
    print ("autodetect")
    
    while True:
        while sc.get_player_count() == 0:
            LCDTime(myLCD, lcd_w) 
            sleep(1)
        players = sc.get_players()   
        for sq in players:
            modePlayer = sq.mode
            if modePlayer == "play":
                return sq
        LCDTime(myLCD, lcd_w)
        sleep(1)

def main(argv):
    """LCD MANAGER APP FOR LMS"""
    lmsserver = "192.168.1.140"
    lmsplayer = ""
    lcd_address = "0x3f"
    lcd_w = 20
    verbose = True
    clock_mode = True #False
    print 'server=' + lmsserver
    try:
        opts, args = getopt.getopt(argv,"hs:p:w:l:c",["server=","player=","lcd_width=","lcd_address=","clock"])
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            printhelp()
            sys.exit()
        elif opt in ("-s", "--server"):
            lmsserver = arg
        elif opt in ("-p", "--player"):
            lmsplayer = arg
        elif opt in("-w","--lcd_width"):
            lcd_w = int(arg)
        elif opt in("-l","--lcd_address"):
            lcd_address = arg    
        elif opt in("-c","--clock"):
            clock_mode = True    
    myLCD = LCD(int(lcd_address,16), lcd_w)
    #myLCD.lcd_string"1234567890123456",1)
    myLCD.lcd_string("   TVC Audio    ",1)
    myLCD.lcd_string("  LMS LCD INFO  ",2)
    sleep(2)
    myLCD.lcd_string("(C)2017 Renaud  ",1)
    myLCD.lcd_string("Coustellier     ",2)
    sleep(1)
    
    #sc = Server(hostname=lmsserver, port=9090, username="user", password="password")
    sc = LMSServer(lmsserver)
    # Server connection
    # Clock mode waiting connection
    connected = False
    waitconn = 1
    while sc.ping() <> True:
        LCDTime(myLCD, lcd_w) 
        waitconn = waitconn + 1
        if waitconn > 120:
            sys.exit(0)
        
    myLCD.lcd_string("LMS SERVER",1)
    myLCD.lcd_string("LMS v.: %s" % sc.version,2)
    sleep(2)
    
    
    while sc.get_player_count() == 0:
        LCDTime(myLCD, lcd_w)
        sleep(2)
    
    if lmsplayer <> "":
        while True:
            LCDTime(myLCD, lcd_w)
            sq = playerAutodetect(sc, myLCD)
            ipPlayer = str(sq.get_ip_address())
            ipPlayer = ipPlayer[0:ipPlayer.find(":")]
            if ipPlayer == lmsplayer:
                break
            sleep(3)
    else:
        myLCD.lcd_string("autodetect player",3)
        myLCD.lcd_string("in play mode",3)
        sq = playerAutodetect(sc, myLCD)
    
    if lcd_w == 20:
        myLCD.lcd_string(sq.name,3)
        myLCD.lcd_string(sq.model,4)
    sleep(2)
    
    if lcd_w == 16:
        # 16x2 LCD Code
        while True:
            try:
                modePlayer = sq.mode
                if modePlayer == "pause":
                    myLCD.lcd_string("mode = pause",1)
                    myLCD.lcd_string(time.strftime('%Y-%m-%d %H:%M:%S'),2)
                    sleep(2)
                elif modePlayer == "stop":
                    LCDTime(myLCD, lcd_w)
                    sleep(2)
                    # when "stop", looking for a running player except if player defined by user...  
                    if lmsplayer == "":
                        sq = playerAutodetect(sc, myLCD)
                        
                elif modePlayer == "play":
                   
                    try:
                        trackAlbum = sq.track_album
                    except:
                        trackAlbum = "--"
                
                    currentTrack = sq.track_title
                    trackArtist = sq.track_artist
                    currentVolume = sq.volume
                    
                    # print ("")
                    # print ("album:" + trackAlbum)
                    # print ("artist:" + trackArtist)
                    # print ("title:" + currentTrack)
                    try:
                        myLCD.lcd_string("Alb." + trackAlbum,1)
                    except:
                        myLCD.lcd_string("--" ,1)
                    myLCD.lcd_string("Art." + trackArtist,2)
                    sleep(4)
                    try:
                        myLCD.lcd_string(trackAlbum,1)
                    except:
                         myLCD.lcd_string('--',1)   
                    myLCD.lcd_string(trackArtist,2)
                    sleep(6)
                    td =  "/" + lms_time_to_string(sq.track_duration)          
                    ptc = str(sq.track_count) 
                    linestatus = 0
                    charOffset = 0
                    while True:
                        linestatus = linestatus + 1
                        volume = (" - Volume %" + str(sq.volume) )
                        #te =  "time " + lms_time_to_string(sq.get_time_elapsed())
                        te = lms_time_to_string(sq.time_elapsed) 
                        te = te + td
                        cti = str(sq.playlist_position +1)
                        
                        if len(cti) > 1 and len(ptc) > 1:
                            if linestatus % 4 == 0:
                                te = te + "  /" + ptc
                            else:
                                te = te + "  " + cti + "/"
                        else:
                            te = te + " " + cti + "/" + ptc
                        
                        while currentVolume != sq.volume:
                            # Volume
                            currentVolume = sq.volume
                            myLCD.lcd_string("Volume %" + str(currentVolume), 1)    
                            sleep(0.3)
                        if linestatus < 2:
                            myLCD.lcd_string("tle:" + currentTrack, 1)
                            if clock_mode != True:      
                                myLCD.lcd_string(te, 2)
                            else:
                                 myLCD.lcd_string(time.strftime('   %H:%M:%S'),2) 
                        else: 
                            # Track Name
                            if len(currentTrack) <= lcd_w:
                                # LENGHT is < LCD LCD_WIDTH
                                myLCD.lcd_string(currentTrack, 1)
                            else:
                                # LENGHT is > LCD_WIDTH
                                charOffset = linestatus - 2
                                myLCD.lcd_string(currentTrack[charOffset:], 1) 
                                if linestatus + lcd_w > len(currentTrack):
                                    linestatus = 0 
                            if clock_mode != True:      
                                myLCD.lcd_string(te, 2)
                            else:
                                 myLCD.lcd_string(time.strftime('   %H:%M:%S'),2)        
                        if sq.track_title != currentTrack or sq.mode !="play" :
                            # change detected
                            myLCD.lcd_string("Track/mode chang", 1)
                            myLCD.lcd_string("pls wait...     ", 2)
                            linestatus = 0
                            break
                        sleep(0.65)
            except:
                sq = playerAutodetect(sc, myLCD)
                sleep(2)
               
    else:
        # 20x4 LCD Code
        while True:
            try:
            #if True == True:
                modePlayer = sq.mode
                print modePlayer
                if modePlayer == "pause":
                    myLCD.lcd_string(sq.name,1)
                    myLCD.lcd_string("Mode = Pause",2)
                    line3 = "RJ45"
                    ipPlayer = sq._ip
                    ipPlayer = ipPlayer[0:ipPlayer.find(":")]
                    if sq.wifi_signal_strength > 1:
                        line3 = "wifi" + str(sq.wifi_signal_strength)
                    line3 = line3 + " " + ipPlayer
                    myLCD.lcd_string(line3,3)
                    myLCD.lcd_string(time.strftime('%Y-%m-%d %H:%M:%S'),4)
                    sleep(0.5)
                elif modePlayer == "stop":
                    LCDTime(myLCD, lcd_w)
                    sleep(2)
                    
                    if lmsplayer == "":
                        # when player mode is stop, looking for another running player except if...
                        sq = playerAutodetect(sc, myLCD)
                          
                elif modePlayer == "play" and lmsplayer == "":
                    trackAlbum = sq.track_album
                    currentTrack = sq.track_title
                    trackArtist = sq.track_artist
                    currentVolume = sq.volume

                    # td =  "/" + lms_time_to_string(sq.track_duration)                          
                    linestatus = 0
                    charOffset = 0
                    
                    while True:
                        if modePlayer <> "play":
                            break
                        linestatus = linestatus + 1
                        volume = (" - Volume %" + str(sq.volume))
                        td =  "/" + lms_time_to_string(sq.track_duration) 
                        if sq.time_elapsed < 8:
                            linestatus = linestatus
                            details = sq.playlist_get_detail(start=0,amount=1,taglist=[tags.BITRATE])
                            for detail in details:
                                print '' #(str(details))
                            te = (detail['bitrate'])

                        else:
                            te = lms_time_to_string(sq.time_elapsed) 
                            te = te + td
                            te = te + "   " + str(sq.playlist_position +1) + "/" + str(sq.track_count)
                        

                        while currentVolume != sq.volume:
                            # Volume
                            currentVolume = sq.volume
                            myLCD.lcd_string("Volume %" + str(currentVolume), 1)    
                            sleep(.25)
                        if sq.track_title != currentTrack or sq.mode !="play" :
                            # change detected
                            myLCD.lcd_string("Track/mode chang", 1)
                            #myLCD.lcd_string("pls wait...     ", 2)
                            break    
                        
                        # Track Name
                        myLCD.lcd_string(trackArtist, 1)
                        try:
                            myLCD.lcd_string(trackAlbum, 2)
                        except:
                            myLCD.lcd_string('no track', 2)
                        
                        if len(currentTrack) <= lcd_w:
                            # LENGHT is < LCD LCD_WIDTH
                            myLCD.lcd_string(currentTrack, 3)
                        else:
                            # LENGHT is > LCD_WIDTH
                            charOffset = linestatus - 1
                            myLCD.lcd_string(currentTrack[charOffset:], 3) 
                            if linestatus + lcd_w > len(currentTrack):
                                linestatus = 0       
                        #myLCD.lcd_string(currentTrack, 3)
                        if clock_mode != True:    
                            myLCD.lcd_string(te, 4)
                            sleep(0.5)
                        else:
                            if sq.time_elapsed < 8:
                                myLCD.lcd_string(te, 4)
                            else:
                                myLCD.lcd_string(time.strftime('%Y-%m-%d %H:%M:%S'),4)
                            sleep(0.5)
            except: #Exception as e:
            #else:
                #myLCD.lcd_string(str(e), 3)
                sq = playerAutodetect(sc, myLCD)
                sleep(2)
               

if __name__ == "__main__":
    
    main(sys.argv[1:])        
