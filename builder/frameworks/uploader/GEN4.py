# Copyright 2023 (c) WizIO ( Georgi Angelov )
#   Based of Reverse Engineering of Pickit4 protocol ( GEN4 )
#   Version:
#       PlatformIO mod
#   Python depend:
#       intelhex,
#       pyusb ( libusb-1.0.dll ) https://github.com/libusb/libusb/releases
#
#   NOTES: Tool must be in PIC mode
#

import sys, struct, time, inspect, json
from os.path import join, normpath, dirname

try:
    from platformio import proc
    IS_PLATFORMIO = True
except:
    IS_PLATFORMIO = False

###############################################################################

THIS_DIR                    = normpath( dirname(__file__) )

RESULT                      = 13
GET_FIRMWARE_INFO           = 0xE1
GET_FW_INFO_TYPE_APP        = 0xAF
SCRIPT_NO_DATA              = 0x0100
SCRIPT_WITH_DOWNLOAD        = 0xC0000101
SCRIPT_WITH_UPLOAD          = 0x80000102
SCRDONE                     = 259
COMMAND_GET_STATUS_FROM_KEY = 261
KEY_COMMANDS_GET_ERROR_STATUS = 'ERROR_STATUS_KEY'

PTG_MODE_CONTROL_COMMAND    = 94

# ICSPSel
ICSP_WIRE_2                 = 0
ICSP_WIRE_4                 = 1
ICSP_SWD                    = 2

# PGCPGDConfig
PULL_NONE                   = 0
PULL_UP                     = 1
PULL_DOWN                   = 2

###############################################################################

def FUNC(txt=''):
    return
    print( '%s(%s)' % ( inspect.stack()[1][3], str(txt) ) )

def ERROR(txt):
    print()
    try:
        import click
        click.secho( '[ERROR] %s' % txt, fg='red')
    except:
        print( '[ERROR] %s < %s() >' % (txt, inspect.stack()[1][3]) )
    print()
    time.sleep(.1)
    sys.exit(-1)

def INFO(txt):
    try:
        import click
        #click.secho( '   %s' % (txt), fg='blue') # BUG: Windows: 4 same chars
        print( '   %s' % (txt))
    except:
        print( '   %s' % (txt))

def DUMP(buf, txt=None, cnt=64, mod=16, print_chars=False, max=True):
    return
    i = 1
    s = '/t'
    if txt:
        print('( %s )' % txt)
    for d in buf:
        print(' %02X' % d, end='')
        c = chr(d)
        c = c if c.isalpha() or c.isdigit() else '.'
        s += c
        if i % mod == 0:
            if print_chars: print(s, end='')
            print()
            s = '/t'
        i += 1
        cnt -= 1
        if max and cnt==0: break
    print()

###############################################################################

try:
    import usb.core
    import usb.util
    from intelhex import IntelHex
except ImportError:
    if IS_PLATFORMIO:
        from platformio import proc
        PYTHON_EXE = proc.get_pythonexe_path()
        print('\nInstalling Python requirements...')
        args = [ PYTHON_EXE, '-m', 'pip', '-q', 'install', '-r', 'requirements.txt' ]
        result = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd=THIS_DIR )
        print(result)
        print('Requirements DONE')
        print('Download and Put libusb-1.0.dll in PIO Python folder:', dirname(PYTHON_EXE), '\n') # TODO add libs
        print('https://github.com/libusb/libusb/releases')
        print('and click [ Upload ] again\n')
        exit(0)
    else:
        ERROR('Python dependency not found')

###############################################################################

TIMEOUT_DEFAULT             = 1000
TIMEOUT_HI                  = 5000
END_POINT_SIZE              = 0x200
END_STREAM_SIZE             = 0x1000

class USBHID:
    def __init__(self):
        self.usb = None
        self.timeout = TIMEOUT_DEFAULT

        try:
            self.usb = usb.core.find(idVendor=0x04D8, idProduct=0x9012)
            if self.usb: 
                INFO('Tool              : PicKit4')
                self.tool = 'PK4'
        except:
            ERROR('libusb-1.0.dll not found')

        if None == self.usb:
            self.usb = usb.core.find(idVendor=0x04D8, idProduct=0x9018)
            if self.usb: 
                INFO('Tool              : SNAP')
                self.tool = 'SNAP'

        if None == self.usb:
            ERROR('Tool not found')

        try:
            usb.util.claim_interface(self.usb, 0)
            self.usb.reset()
        except:
            ERROR('Tool driver is busy')

    def write(self, buf, ep=0x02):
        try:
            res = self.usb.write(ep, buf, self.timeout)
            DUMP(buf, 'W')
        except:
            ERROR('USB WRITE TIMEOUT')
        return res

    def write_stream(self, buf, ep=0x04):
        size = len(buf)
        i = 0;
        while size > 0:
            size -= self.write( buf[ i : i + END_STREAM_SIZE ], ep )
            i += END_STREAM_SIZE

    def read(self, size=END_POINT_SIZE, ep=0x81):
        rx = b''
        try:
            rx = self.usb.read(ep, size + 1, self.timeout)
        except:
            ERROR('USB READ TIMEOUT')
        DUMP(rx, 'R [%d]' % len(rx))
        return rx

    def read_stream(self, size, ep=0x83): # TODO buffer
        rx = b''
        while size > 0:
            buf = self.read(END_STREAM_SIZE, ep)
            rx += buf
            size -= len(buf)
        return rx

    def set_timeout(self, val=TIMEOUT_DEFAULT):
        self.timeout = val        

###############################################################################

PICS = {
    'PIC32MZ2048EFM100': {
        'device_id'  : 0x0723B053,
        'flash'      : 0x1D000000,
        'flash_size' : 0x200000,
        'boot'       : 0x1FC00000,
        'boot_size'  : 0xFF00,
        'config'     : 0x1FC0FFC0,
        'config_size': 0x40,
    },
}

###############################################################################

class GEN4:
    def __init__(self, hex, device='PIC32MZ2048EFM100', DI=None, PE=None, start=True):
        self.rx = b''
        self.status = 0    
        self.enter = False    
        self.connected = False
        self.start_time = time.time()
        INFO('Programing %s' % device)
        self.setup_device_info(device, DI)
        self.USB = USBHID()

        try:
            with open( join(THIS_DIR, device + '.json')) as json_file:
                self.SCR = json.load(json_file)
        except: 
            ERROR('Load Script file')

        try:
            if PE == None: 
                PE = join(THIS_DIR, 'RIPE_15_000502.hex')
            pe = IntelHex()
            pe.fromfile(PE, format='hex')
            for s in pe.segments(): 
                pass
            self.PE_START = s[0]
            self.PE_BIN = pe.tobinarray(start = s[0], end = s[1] - 1)
        except: 
            ERROR('Load PExecutable file')

        try:
            self.HEX = IntelHex()
            self.HEX.fromfile(hex, format='hex')
        except: 
            ERROR('Load HEX file')

        if start:
            self.connect()
            self.setup()

    def is_blank(self, buf):
        for b in buf:
            if b !=0xFF:
                return buf
        return []

    def get_bin(self, key):
        LAST = START = self.DI[key]
        END = self.DI[key] + self.DI[key + '_size']
        for s in self.HEX.segments():
            if s[1] > LAST and s[1] < END:
                LAST = s[1]
        LAST += self.DI['row'] - ( LAST % self.DI['row'] )
        if LAST > END: 
            LAST = END
        return self.is_blank( self.HEX.tobinarray(start = START, end = LAST-1) )

    def setup_device_info(self, device, info):
        if info:
            for k in info: # convert to int
                if type(info[k]) == str:
                    info[k] = int(info[k], 0)
            self.DI = info
        else:
            if device not in PICS:
                ERROR('Not supported device: ' + device)
            self.DI = PICS[device]

        if 'power' not in self.DI:
            self.DI['power'] = 0 
        if 'reset' not in self.DI:
            self.DI['reset'] = 0 
        if 'row' not in self.DI:
            self.DI['row'] = 2048

    def connect(self):
        self.USB.write( [ GET_FIRMWARE_INFO ] )
        rx = self.USB.read()
        if END_POINT_SIZE != len(rx):
            ERROR('BOOT ANSWER SIZE')
        if GET_FIRMWARE_INFO != rx[0] or GET_FW_INFO_TYPE_APP != rx[1]:
            ERROR('BOOT APP')
        res = str( rx[32:47], 'utf-8').replace('\0','' )
        INFO('Serial            : %s' % res)
        return res # BURxxx

    def receive(self, size=END_POINT_SIZE, ep=0x81):
        self.rx = self.USB.read(size, ep)
        if RESULT != self.rx[0]:
            ERROR('RECEIVE ANSWER <> 13')
        self.status = struct.unpack('<I', self.rx[16:20])[0]
        return struct.unpack('<I', self.rx[8:12])[0] # packet size

    def transmit(self, cmd, transferSize=0, payload=None, ep=0x02):
        a = struct.pack('<I', cmd)              # COMMAND
        a += struct.pack('<I', 0)               # SEQUENSE
        size = 16
        if payload:
            size += len(payload)
        a += struct.pack('<I', size)            # PACKET SIZE
        a += struct.pack('<I', transferSize)    # TRANSFER SIZE
        if payload:
            a += bytearray(payload)             # PAYLOAD
        self.USB.write(a, ep)

    def script(self, cmd=SCRIPT_NO_DATA, transferSize=0, prm=None, scr=None):
        #FUNC()
        payload = b''
        if prm:
            payload += struct.pack('<I', len(prm))
        else:
            payload += struct.pack('<I', 0)
        if scr:
            payload += struct.pack('<I', len(scr))
        else:
            payload += struct.pack('<I', 0)
        if prm:
            payload += bytearray(prm)
        if scr:
            payload += bytearray(scr)
        self.transmit(cmd, transferSize, payload)
        self.receive()

    def releaseFromReset(self):
        FUNC()
        self.script(scr = [0x42, 0xB0])
        time.sleep(.1)

    def holdInReset(self):
        FUNC()
        self.script(scr = [0xB1])
        time.sleep(.1)

    def selectPowerSource(self, fromTool=0):
        FUNC()
        self.script(scr = [0x46, fromTool & 1, 0, 0, 0 ])
        time.sleep(.1)

    def shutDownPowerSystem(self):
        FUNC()
        self.script(scr = [0x44])
        time.sleep(.1)

    def closeRelay(self, closeIt=0):
        FUNC()
        self.script(scr = [0xEF, closeIt & 1])

    def setPowerInfo(self, Vdd=3250, VppOperation=3250, Vpp_op=3250):
        FUNC()
        self.script(scr = [ 0x40,
                (Vdd & 0xFF), (Vdd >> 8 & 0xFF), 0, 0,
                (VppOperation & 0xFF), (VppOperation >> 8 & 0xFF), 0, 0,
                (Vpp_op & 0xFF), (Vpp_op >> 8 & 0xFF), 0, 0,
                66, 67 ] )
        time.sleep(.1)

    def getVoltagesInfo(self):
        FUNC()
        self.script(scr = [0x47])
        return struct.unpack('<IIIIIIII', self.rx[24:24+32])

    def applySelICSP(self, mode=0):
        # BootFlash = 0, FlashData = 1
        FUNC()
        self.script(SCRIPT_NO_DATA, scr = [0x27, mode & 1])

    def setSpeed(self, nanoseconds=100):
        FUNC()
        self.script(scr = [0xEC, (nanoseconds & 0xFF), (nanoseconds >> 8 & 0xFF), 0, 0 ])

    def getSpeed(self):
        FUNC()
        self.script(scr = [0xED])
        return struct.unpack('<I', self.rx[24:28])[0]

    def applySelJTAGSpeed(self, speed_level=1):
        FUNC()
        self.script(scr = [0xD4, (speed_level & 0xFF), (speed_level >> 8 & 0xFF), 0, 0 ])

    def applySelPullUpDown(self, dir, pullChannel, pullState, resistance=4700):
        FUNC()
        pullDirCmd = 205 + ( dir & 1 )
        self.script(scr = [ pullDirCmd, pullChannel, (resistance & 0xFF), (resistance >> 8 & 0xFF), 0, 0, pullState ])

###############################################################################

    def runScript(self, name):
        FUNC( name )
        self.script(scr = self.SCR[name])

    def pyload(self, script, address, size, cmd=SCRIPT_WITH_DOWNLOAD):
        self.script( 
            scr = self.SCR[script],
            cmd = SCRIPT_WITH_DOWNLOAD if cmd==SCRIPT_WITH_DOWNLOAD else SCRIPT_WITH_UPLOAD,
            prm = struct.pack('<I', address) + struct.pack('<I', size),
            transferSize = size
        )

    def ScriptDone(self):
        self.script(SCRDONE)

    def EnterTMOD_LV(self):
        if False == self.enter:
            self.runScript('EnterTMOD_LV')
            self.enter = True

    def ExitTMOD(self):
        if True == self.enter:
            self.runScript('ExitTMOD')
            self.enter = False

    def InitJTAG(self):
        self.runScript('InitJTAG')

    def GetDeviceID(self):
        self.runScript('GetDeviceID')
        self.id = struct.unpack('<I', self.rx[24:28])[0]
        return self.id

    def CheckCodeProtect(self):
        self.runScript('CheckCodeProtect')
        return 0

    def SetupSerialMode(self):
        self.runScript('SetupSerialMode')

    def LoadLoader(self):
        self.runScript('LoadLoader')

    def TestPEConnect(self):
        self.runScript('TestPEConnect')

    def EraseChip(self):
        self.runScript('EraseChip')

    def BlankProgmemRange(self, address, size):
        self.USB.set_timeout( TIMEOUT_HI )    
        self.script( 
            scr = self.SCR['BlankProgmemRange'],
            prm = struct.pack('<I', address) + struct.pack('<I', size)
        )
        if self.status == 258: 
            ERROR('Blank check failed. The device is not blank')
        self.USB.set_timeout()    

    def DownloadPE(self, address, size):
        self.pyload('DownloadPE', address, size)

    def ReadProgmemPE(self, address, size):
        self.pyload('ReadProgmemPE', address, size, cmd=SCRIPT_WITH_UPLOAD)

    def ProgramPE(self, address, size, aligned):
        if aligned:
            self.pyload('WriteProgmemPE', address, size)
        else:
            self.pyload('P32PE_ProgramCluster', address, size)

    def WriteConfigmemPE(self, address, size):
        self.pyload('WriteConfigmemPE', address, size)

###############################################################################

    def setup(self):
        self.selectPowerSource( self.DI['power'] ) # from board
        self.shutDownPowerSystem()
        self.closeRelay()
        self.setPowerInfo()
        self.applySelICSP()
        self.setSpeed()

    def begin(self, check=True):
        self.EnterTMOD_LV()
        #self.InitJTAG()
        res = self.GetDeviceID() & 0x0FFFFFFF
        if check and res != self.DI['device_id']:
            ERROR('Wrong Device ID: 0x%08X, Must be: 0x%08X' % (res, self.DI['device_id']))
        INFO( 'Device ID         : 0x%08X' % res )
        self.CheckCodeProtect() # TODO 258
        return res

    def end(self):
        self.ExitTMOD()
        self.holdInReset()
        time.sleep(.1)
        if 0 == self.DI['reset']:
            self.releaseFromReset()
            time.sleep(.1)
        if self.USB.tool == 'SNAP':
            self.setPowerInfo(0,0,0)
            self.shutDownPowerSystem()
        self.closeRelay(1)
        INFO('Elapsed %d seconds\n' % ( ( time.time() - self.start_time ) ) )

    def stream(self, bin):
        self.USB.write_stream(bin)
        self.ScriptDone()

    def read_pe(self, address, size):
        self.ReadProgmemPE(address, size)
        buf = self.USB.read_stream(size)
        self.ScriptDone()
        return buf

    def prepare(self, address=None):
        self.EnterTMOD_LV()
        if self.connected: 
            return
        self.SetupSerialMode()
        self.LoadLoader() 
        if address == None: 
            address = self.PE_START       
        self.DownloadPE(address, len(self.PE_BIN))
        self.stream(self.PE_BIN)
        self.TestPEConnect() # status?
        self.connected = True
        #self.read_pe(0x1FC54020, 8)
        pass

    def check_blank(self):
        self.prepare()
        INFO('Blank Checking...')
        self.BlankProgmemRange(self.DI['flash'], self.DI['flash_size'])
        #INFO('The device is blank')
        # 1F06C000
        pass

    def erase(self, check=True):
        INFO('Erasing...')
        self.prepare()
        self.EraseChip()
        self.ScriptDone()
        #INFO('Erase successful')
        self.ExitTMOD()
        self.connected = False
        if check: 
            self.check_blank()

    def program(self):
        self.prepare()

        bin = self.get_bin('flash')
        size = len(bin)
        if size > 0:
            INFO('Programing Flash  : 0x%08X [ %d ]' % (self.DI['flash'], size))
            self.ProgramPE(self.DI['flash'], size, True)
            self.stream(bin)

        bin = self.get_bin('boot')
        size = len(bin)
        if size > 0:
            INFO('Programing Boot   : 0x%08X [ %d ]' % (self.DI['boot'], size))
            self.ProgramPE(self.DI['boot'], size, False)
            self.stream(bin)

        bin = self.get_bin('config')
        size = len(bin)
        if size > 0:
            INFO('Programing Config : 0x%08X [ %d ]' % (self.DI['config'], size))
            self.WriteConfigmemPE(self.DI['config'], size)
            self.stream(bin)

###############################################################################

def upload(target, source, env):
    c = GEN4( 
        join(env.get('BUILD_DIR'), env.get('PROGNAME')) + '.hex',
        DI = env.BoardConfig().get('upload.info', None)
    )
    c.begin()
    c.erase(False)
    c.program()
    c.end()

if __name__ == "__main__":
    c = GEN4( join(THIS_DIR, 'APPLICATION.hex') )
    c.begin()
    #c.erase(False)
    c.program()
    c.end()
