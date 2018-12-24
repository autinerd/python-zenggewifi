import socket

name = "zenggewifi"

TRUE = 0XF0
FALSE = 0X0F
ON = 0X23
OFF = 0X24
COMMANDSETTIME       = (0X10)
COMMANDSETTIME2      = (0X14)
COMMANDGETTIME       = (0X11)
COMMANDGETTIME2      = (0X1A)
COMMANDGETTIME3      = (0X1B)
COMMANDGETTIMERS     = (0X22)
COMMANDGETTIMERS2    = (0X2A)
COMMANDGETTIMERS3    = (0X2B)
COMMANDSETCOLOR      = (0X31)
COMMANDSETMUSICCOLOR = (0X41)
COMMANDSETMODE       = (0X61)
COMMANDSETPOWER      = (0X71)
COMMANDGETSTATE      = (0X81)
COMMANDGETSTATE2     = (0X8A)
COMMANDGETSTATE3     = (0X8B)

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
        self.sendraw(senddata)
        data = self.sock.recv(14)
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

    @staticmethod
    def rgb2hsv(color_data):
        R = color_data.R / 255
        G = color_data.G / 255
        B = color_data.B / 255
        max_value = max([R, G, B])
        min_value = min([R, G, B])
        h = 0
        if max_value == min_value:
            h = 0
        elif max_value == color_data.R:
            h = 60 * ((color_data.G - color_data.B) / (max_value - min_value))
        elif max_value == color_data.G:
            h = 60 * (2 + ((color_data.B - color_data.R) / (max_value - min_value)))
        elif max_value == color_data.B:
            h = 60 * (4 + ((color_data.R - color_data.G) / (max_value - min_value)))
        if h < 0:
            h += 360
        s = 0
        if max_value > 0:
            s = (max_value - min_value) / max_value
        v = max_value
        return h, s * 100, v * 100

    @staticmethod
    def hsv2rgb(h, s, v):
        import math
        s = s / 100
        v = v / 100
        hi = math.floor(h / 60)
        f = ((h / 60) - hi)
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        switch = {
            0: color(v * 255, t * 255, p * 255, 0, True),
            1: color(q * 255, v * 255, p * 255, 0, True),
            2: color(p * 255, v * 255, t * 255, 0, True),
            3: color(p * 255, q * 255, v * 255, 0, True),
            4: color(t * 255, p * 255, v * 255, 0, True),
            5: color(v * 255, p * 255, q * 255, 0, True),
            6: color(v * 255, t * 255, p * 255, 0, True)
        }
        return switch.get(hi)