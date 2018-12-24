import socket

name = "zenggewifi"

TRUE                 = 0xF0
FALSE                = 0x0F
ON                   = 0x23
OFF                  = 0x24
COMMANDSETTIME       = 0x10
COMMANDSETTIME2      = 0x14
COMMANDGETTIME       = 0x11
COMMANDGETTIME2      = 0x1A
COMMANDGETTIME3      = 0x1B
COMMANDGETTIMERS     = 0x22
COMMANDGETTIMERS2    = 0x2A
COMMANDGETTIMERS3    = 0x2B
COMMANDSETCOLOR      = 0x31
COMMANDSETMUSICCOLOR = 0x41
COMMANDSETMODE       = 0x61
COMMANDSETPOWER      = 0x71
COMMANDGETSTATE      = 0x81
COMMANDGETSTATE2     = 0x8A
COMMANDGETSTATE3     = 0x8B

MODECOLOR    = 97
MODEMUSIC    = 98
MODECUSTOM   = 35
MODEPRESET1  = 37
MODEPRESET2  = 38
MODEPRESET3  = 39
MODEPRESET4  = 40
MODEPRESET5  = 41
MODEPRESET6  = 42
MODEPRESET7  = 43
MODEPRESET8  = 44
MODEPRESET9  = 45
MODEPRESET10 = 46
MODEPRESET11 = 47
MODEPRESET12 = 48
MODEPRESET13 = 49
MODEPRESET14 = 50
MODEPRESET15 = 51
MODEPRESET16 = 52
MODEPRESET17 = 53
MODEPRESET18 = 54
MODEPRESET19 = 55
MODEPRESET20 = 56

class ZenggeWifiBulb(object):
    def __init__(self, host):
        """Initialization"""
        self.host = host
        self.port = 5577
        self.timeout = 5

    def checksum(self, data):
        sum = 0
        for byte in data:
            sum += byte
        return sum % 256

    def get_status(self):
        """Get data from bulb"""
        self.connect()
        senddata = [COMMANDGETSTATE, COMMANDGETSTATE2, COMMANDGETSTATE3]
        senddata.append(self.checksum(senddata))
        try:
            if self.sendraw(senddata) is False:
                return False
            data = self.sock.recv(14)
        except OSError:
            return False
        self.state = state(data[1], data[2] == ON, data[3], data[5], color(data[6], data[7], data[8], data[9], data[12] == TRUE), data[10])
        return self.state

    def get_bulb_state(self):
        self.get_status()
        return self.state.isOn

    def connect(self):
        self.sock = socket.socket()
        try:
            self.sock.connect((self.host, self.port))
            return True
        except OSError:
            return False

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def send(self, msg):
        self.connect()
        msg.append(FALSE)
        msg.append(self.checksum(msg))
        try:
            self.sock.sendall(bytes(msg))
            return True
        except OSError:
            return False
    
    def sendraw(self, msg):
        self.connect()
        try:
            self.sock.sendall(bytes(msg))
            return True
        except OSError:
            return False
    
    def format_set_power(self, on):
        if on == True:
            return [COMMANDSETPOWER, ON]
        else:
            return [COMMANDSETPOWER, OFF]

    def format_set_color(self, color):
        buf = [COMMANDSETCOLOR, color.R, color.G, color.B, color.W]
        if color.IgnoreW:
            buf.append(TRUE)
        else:
            buf.append(FALSE)
        return buf

    def set_rgb(self, red, green, blue):
        return self.send(self.format_set_color(color(red, green, blue, 0, True)))

    def set_white(self, white):
        return self.send(self.format_set_color(color(0, 0, 0, white, False)))

    def on(self):
        return self.send(self.format_set_power(True))

    def off(self):
        return self.send(self.format_set_power(False))

class state:
    def __init__(self, deviceType, isOn, Mode, Slowness, Color, LedVersionNum):
        self.deviceType = int(deviceType)
        self.isOn = bool(isOn)
        self.Mode = int(Mode)
        self.Slowness = int(Slowness)
        self.Color = Color
        self.LedVersionNum = int(LedVersionNum)

class color:
    def __init__(self, R, G, B, W, IgnoreW):
        self.R = int(R)
        self.G = int(G)
        self.B = int(B)
        self.W = int(W)
        self.IgnoreW = bool(IgnoreW)