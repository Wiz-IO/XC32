# Copyright 2023 (c) WizIO ( Georgi Angelov )
#   Reverse Engineering of PIC32MZ Curiosity PKOB
#   Version:
#       NOT READY !!!
#
#   Python depend:
#       intelhex,
#       pyusb ( libusb-1.0.dll ) https://github.com/libusb/libusb/releases
#

import sys, struct, time, inspect
from os.path import join, normpath, dirname
import REALICE as RI

THIS_DIR = normpath( dirname(__file__) )

END_POINT_SIZE = 64
FILL = 0x5A5A

def FUNC(txt=''):
    return
    print( '%s(%s)' % ( inspect.stack()[1][3], str(txt) ) )

def ERROR(txt):
    print()
    try:
        import click
        click.secho( '[ERROR] %s' % txt, fg='red')
    except:
        print( '[ERROR] %s in %s()' % (txt, inspect.stack()[1][3]) )
    print()
    time.sleep(.1)
    sys.exit(-1)

def INFO(txt):
    try:
        import click 
        click.secho( '\t%s' % (txt), fg='blue') # BUG: Windows: 4 same chars
    except:
        print( '\t%s' % (txt))

def DUMP(buf, txt=None, cnt=END_POINT_SIZE, mod=16, print_chars=False, max=True):
    return
    i = 1
    s = '/t'
    if txt:
        print('( %s )' % txt)
    return
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

try:
    import usb.core
    import usb.util
    from intelhex import IntelHex
except ImportError:
    ERROR('Python dependency')

###############################################################################

class USBHID:
    def __init__(self):
        self.usb = None
        self.timeout = 1000
        try:
            self.usb = usb.core.find(idVendor=0x04D8, idProduct=0x8107)
        except:
            ERROR('libusb-1.0.dll not found')
        if None == self.usb:
            ERROR('USB Tool not connected')
        usb.util.claim_interface(self.usb, 0)
        self.usb.reset()

    def write(self, buf, ep = 0x01):
        try:
            self.usb.write(ep, buf, self.timeout)
            DUMP(buf, 'SEND')
        except:
            ERROR('USB WRITE TIMEOUT')
        return buf

    def send(self, buf, ep = 0x01):
        for i in range(0, len(buf), END_POINT_SIZE ):
            part = buf[ i : i + END_POINT_SIZE ]
            if len(part) == END_POINT_SIZE:
                self.write( part, ep )

    def read(self, size=END_POINT_SIZE, ep=0x81, terminate=True):
        rx = b''
        try:
            rx = self.usb.read(ep, size + 1, self.timeout)
        except:
            if terminate:
                ERROR('USB READ TIMEOUT')
        DUMP(rx, 'READ')
        return rx

###############################################################################

class DeviceInfo:
    Name                = 'Curiosity'
    Device              = 'PIC32MZ2048EFM100'    
    RowSize             = 2048
    DeviceId            = 0x0723B053
    DeviceIdMask        = 0x0FFFFFFF
    DeviceIdAddress     = 0xFFFFFFFF
    ProgramMemory       = 0x1D000000,   0x200000
    ConfigBootMemory    = 0x1FC00000,   0x14000,    0xFF00 # fix
    ConfigMemory        = 0x1FC0FFC0,   0x40
    PE_FILE = join(THIS_DIR, 'RIPE_15_000510.hex')

    def get(self): return self.di

    def __init__(self):
        a  = struct.pack('<HHIII', 0x036C, 0x0002, self.DeviceIdAddress, self.DeviceIdMask, self.DeviceId) # ProcId / OperationMode # DeviceId Address / Mask / Value
        a += struct.pack('<IIIIIIII', 0,0,0,0,0,0,0,0)      # VersionIds[8]
        a += struct.pack('<HHHHHHH',  0,0,0,0,0,0,0)        # PGMWAIT / LVPGMWAIT / EEDATAWAIT / CFGWAIT / IDWAIT / ERASEWAIT / LVERASEWAIT
        a += struct.pack('<H', 0)                           # EraseAlg
        a += struct.pack('<BBBBB', 0, 0, 0, 0, 0)           # Latches[5] PgmMem / DataMem / CfgMem / Userid / RowErase
        a += struct.pack('<BBB', 20, 28, 26)                # VDD[3] min, max, def
        a += struct.pack('<BBB', 20, 28, 26)                # VPP[3] min, max, def
        a += struct.pack('<BBB', 20, 28,  0)                # VddMinDef, VddMaxDef, LvThresh
        a += struct.pack('<II', self.ProgramMemory[0], self.ProgramMemory[1]) # ProgramMemory   00 00 00 1D - 00 00 20 00
        a += struct.pack('<II', 0, 0)                       # DataMemory                        00 00 00 00 - 00 00 00 00
        a += struct.pack('<II', 0, 0)                       # IDMemory                          00 00 00 00 - 00 00 00 00
        a += struct.pack('<II', self.ConfigMemory[0], self.ConfigMemory[1]) # ConfigMemory      C0 FF C0 1F - 40 00 00 00
        a += struct.pack('<II', 0x1FC74000, 0x4000)         # TestMemory                        00 40 C7 1F - 00 40 00 00
        a += struct.pack('<II', 0, 0)                       # TestAppMemory                     00 00 00 00 - 00 00 00 00
        a += struct.pack('<HH', 1, 0)                       # PanelNumber / PanelSize
        a += struct.pack('<HHHHHHHHHH', 0x0000, 0x7B00, 0x7FF7, 0x4007, 0xC7FF, 0xFFFF, 0xF77F, 0x403F, 0x0000, 0x0000) # RequiredBitsMask[10 * H]  0000 007B F77F 0740 FFC7 FFFF 7FF7 3F40 0000 0000
        a += struct.pack('<HHHHHHHHHH', 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF, 0xF7FF, 0xFFFF, 0xFFFF, 0xFFFF) # BlankValue[10 * H]        FFFF FFFF FFFF FFFF FFFF FFFF FFF7 FFFF FFFF FFFF
        a += struct.pack('<I', 0x1FC54020)                  # CalibrationAddress [I]            20 40 C5 1F
        a += struct.pack('<III', 12, 3, 1)                  # BKBugBit [III]                    0C 00 00 00 / 03 00 00 00 / 01 00 00 00
        a += struct.pack('<H', 2)                           # MinorAlg [H]                      02 00
        a += struct.pack('<II', self.ConfigBootMemory[0], self.ConfigBootMemory[1]) # ConfigBootMemory 00 00 C0 1F - 00 40 01 00
        a += struct.pack('<H', 1)                           # DebugAlg [H]                      01 00
        a += struct.pack('<HIIIIII', 0, 0, 0, 0, 0, 0, 0)   # devHdr [H + 6 * I]
        a += struct.pack('<H', 0)                           # EraseAlg [H]                      00 00
        a += struct.pack('<I', 0)                           # DevSpecificFlags [I]              00 00 00 00
        a += struct.pack('<II', 0x1FC70000, 0x4000)         # AuxMemory [II]                    00 00 C7 1F - 00 40 00 00
        a += struct.pack('<II', 0x1FC54020, 8)              # CalibrationMemory [II]            20 40 C5 1F - 08 00 00 00
        a += struct.pack('<BBBBBB', 0, 0, 0, 0, 0, 0)       # LatchesHighByte [6 * B]
        a += struct.pack('<II', 0x1FC20000, 0x14000)        # UpperBootAliasMemory              00 00 C2 1F - 00 40 01 00
        a += struct.pack('<II', 0x1FC40000, 0x14000)        # BootFlash1Memory                  00 00 C4 1F - 00 40 01 00
        a += struct.pack('<II', 0x1FC60000, 0x14000)        # BootFlash2Memory                  00 00 C6 1F - 00 40 01 00
        a += struct.pack('<II', 0x1FC0FF40, 0x40)           # LowerBootCfgAltMemory             40 FF C0 1F - 40 00 00 00
        a += struct.pack('<II', 0x1FC4FFC0, 0x40)           # BootFlash1CfgMemory               C0 FF C4 1F - 40 00 00 00
        a += struct.pack('<II', 0x1FC4FF40, 0x40)           # BootFlash1CfgAltMemory            40 FF C4 1F - 40 00 00 00
        a += struct.pack('<II', 0x1FC6FFC0, 0x40)           # BootFlash2Cfgmemory               C0 FF C6 1F - 40 00 00 00
        a += struct.pack('<II', 0x1FC6FF40, 0x40)           # BootFlash2CfgAltmemory            40 FF C6 1F - 40 00 00 00
        a += struct.pack('<II', 0x1FC10000, 0x4000)         # LowerBootAliasMemoryLastPage      00 00 C1 1F - 00 40 00 00
        a += struct.pack('<II', 0x1FC50000, 0x4000)         # BootFlash1MemoryLastPage          00 00 C5 1F - 00 40 00 00
        a += struct.pack('<H', 0)                           # ??!??
        self.di = a
        #DUMP(a, "DeviceInfo", cnt=len(a))
        #exit(0)
        pass

###############################################################################

class CURIOSITY:
    def getHex(self, START, END):
        bin = self.HEX.tobinarray(start = START, end = END - 1)
        for b in bin: # skip blank
            if b != 0xFF: return bin
        return []

    def checksum(self, buf):
        L = len(buf)
        if L % 2 != 0: buf.append(0)
        CS = 0
        for i in range(0, L, 2):
            Val = struct.unpack('>H', buf[i:i+2])[0] & 0xFFFF
            CS = (CS + Val) & 0xFFFF
        return ((CS ^ 0xFFFFFFFF) + 1)  & 0xFFFF

    def __init__(self, hex_file):
        self.start_time = time.time()
        self.rx = b''
        self.USB = USBHID()
        self.DI = DeviceInfo()
        INFO('%s %s' % ( self.DI.Name, self.DI.Device) )

        PE = IntelHex()
        PE.fromfile(self.DI.PE_FILE, format='hex')
        for s in PE.segments(): pass
        self.PE_BIN = PE.tobinarray(start = s[0], end = s[1] - 1)

        self.HEX = IntelHex()
        self.HEX.fromfile(hex_file, format='hex')

        self.bracket = 0

    def align(self, buf):
        size = len( buf )
        mod = size % END_POINT_SIZE
        if mod > 0:
            for i in range(0, END_POINT_SIZE - mod):
                buf += b'\x5A'
        return buf

    def wait_command(self, cmd):
        self.rx = self.USB.read()
        c = struct.unpack('<H', self.rx[0:2])[0]
        if c != cmd:
            ERROR('Receive Command: %02X, Read: %02X' % (cmd, c))

    def wait_status(self):
        for i in range(20):
            rx = self.USB.read()
            if len(rx) > 0:
                if rx[0] == 0: return rx # done     
                if rx[0] == 255:           
                    ERROR('STATUS FAIL')
        ERROR('STATUS TIMEOUT')

    def send(self, header, payload=None, wait_command=True, wait_status=False):
        size = len(header)
        header = self.align(header)
        self.USB.send( header[ 0 : END_POINT_SIZE-4 ] + struct.pack('<I', size-2) + header[ END_POINT_SIZE-4 : ] )
        if wait_command:
            self.wait_command(header[0])
        if payload:
            payload += struct.pack('<H', self.checksum(payload))
            size = len(payload)
            payload = self.align(payload)
            self.USB.send( payload[ 0 : END_POINT_SIZE-4 ] + struct.pack('<I', size) + payload[ END_POINT_SIZE-4 : ] )
        if wait_status:
            return self.wait_status()
        return self.rx

    def COMMAND(self, cmd, read=True, status=False):
        FUNC( RI.get_cmd_txt(cmd) )
        a  = struct.pack('<H', cmd)
        a += struct.pack('<H', FILL)
        return self.send(a, None, read, status )

    def CMD_SET_DEBUG_OPTIONS(self, Options1=0, Options2=0):
        FUNC()
        a  = struct.pack('<H', RI.cmd_SET_DEBUG_OPTIONS)
        a += struct.pack('<I', 8)
        a += struct.pack('<I', Options1)
        a += struct.pack('<I', Options2)
        return self.send(a, None, True, False)

    def CMD_SETBRACKET(self, val=1):
        #FUNC( bool )
        a  = struct.pack('<H', RI.cmd_SETBRACKET)
        a += struct.pack('<H', val & 1)
        a += struct.pack('<H', FILL)
        self.send(a, None, True, True )
        self.bracket = val

    def CMD_MEMOBJ_2_REALICE(self, MemRegion, StartAddr, Size, payload):
        #FUNC( '%d, 0x%X, %d' % (MemRegion, StartAddr, Size) )
        a  = struct.pack('<H', RI.cmd_MEMOBJ_2_REALICE)
        a += struct.pack('<H', MemRegion)
        a += struct.pack('<I', StartAddr)
        a += struct.pack('<I', Size)
        a += struct.pack('<H', FILL)
        return self.send(a, payload, True, True)

    def CMD_SETOPDESC(self, RegionMask=0, Options=0, Pgm=0, Data=0, Id=0, Cfg=0, Test=0, BootCfg=0, Aux=0, FBoot=0):
        #FUNC( '0x%X' % RegionMask)
        a  = struct.pack('<H', RI.cmd_SETOPDESC)
        a += struct.pack('<H', 72)
        a += struct.pack('<I', RegionMask)
        a += struct.pack('<I', Options)
        a += struct.pack('<Q', Pgm)
        a += struct.pack('<Q', Data)
        a += struct.pack('<Q', Id)
        a += struct.pack('<Q', Cfg)
        a += struct.pack('<Q', Test)
        a += struct.pack('<Q', BootCfg)
        a += struct.pack('<Q', Aux)
        a += struct.pack('<Q', FBoot)
        a += struct.pack('<H', FILL)
        self.send(a, None, True, False)

    def CMD_READOPDESC(self):
        #FUNC()
        self.COMMAND(RI.cmd_READOPDESC, True, True)

    def CMD_PROGRAMOPDESC(self):
        #FUNC()
        self.COMMAND(RI.cmd_PROGRAMOPDESC, True, True)

    def CMD_ERASEOPDESC(self):
        #FUNC()
        self.COMMAND(RI.cmd_ERASEOPDESC, True, True)

    def CMD_SETDDS(self):
        #FUNC()
        b  = self.DI.get()
        a  = struct.pack('<H', RI.cmd_SETDDS)
        a += struct.pack('<H', len(b))
        a += struct.pack('<H', FILL)
        self.send(a, b, True, True)

    def CMD_SETEMULATORPWR(self, Power, Voltage):
        FUNC()
        a  = struct.pack('<H', RI.cmd_SETEMULATORPWR)
        a += struct.pack('<H', 4)
        a += struct.pack('<H', Power)
        a += struct.pack('<H', Voltage)
        a += struct.pack('<H', FILL)
        self.send(a, None, True, True)

###############################################################################

    def connect(self):
        FUNC()
        rx = self.COMMAND(RI.cmd_CONNECT2DEVICE, True, True) # PIC32MZ2048EFM100 DevID: 0x0723B053 Rev?=1
        self.device_id = struct.unpack('<HI', rx[0:6])[1] & self.DI.DeviceIdMask
        if self.device_id == 0: 
            ERROR('Device ID = 0')
        return self.device_id

    def upload_executable(self):
        FUNC()
        self.CMD_MEMOBJ_2_REALICE(RI.cregion_PgmExec, 0, len(self.PE_BIN), bytearray(self.PE_BIN))
        self.CMD_SETBRACKET()
        self.CMD_SETOPDESC( Options=1 ) # EraseAllB4Pgming
        self.CMD_PROGRAMOPDESC()
        self.CMD_SETBRACKET(0)
        #exit(0)
        pass        

    def ping_read(self):
        FUNC()
        self.CMD_SETBRACKET()
        self.CMD_SETOPDESC()
        self.CMD_READOPDESC()
        #self.CMD_SETBRACKET(0)
        pass

    def begin(self):
        FUNC()
        self.COMMAND(RI.cmd_INITCOMMPK3_2K, False, False)
        self.COMMAND(RI.cmd_GET_STATUS)
        self.COMMAND(RI.cmd_GETVERSIONS)
        self.COMMAND(RI.cmd_GETVERSIONS2)
        self.CMD_SETDDS()
        self.CMD_SETEMULATORPWR( RI.bitMCLRHOLD | RI.bitPOWER_STAY_ON | RI.bitEMULATOR_POWER, 26 )  
        #self.CMD_SET_DEBUG_OPTIONS()
        self.upload_executable()
        res = self.connect()
        self.ping_read()
        return res

    def end(self):
        FUNC()
        self.CMD_SETEMULATORPWR( RI.bitPOWER_STAY_ON | RI.bitEMULATOR_POWER, 26 )
        print('Elapsed: %d seconds\n' % ( ( time.time() - self.start_time ) ) )

    def erase(self, mask=None):
        FUNC()
        if mask == None:
            mask = RI.RegionProgramMemory | RI.RegionBootConfig | RI.RegionCfgMemory
        #mask = 0x007BFD09 
        if 0 == self.bracket: 
            self.CMD_SETBRACKET()            
        self.CMD_SETOPDESC(mask, Cfg=0x3F, Test=0x3FFF, BootCfg=0xFEFF)
        self.CMD_ERASEOPDESC()
        #self.CMD_SETBRACKET(0)
        pass

    def program(self, Region, Address=None, Size=None):
        FUNC()
        cnt = 0
        if 0 == self.bracket: 
            self.CMD_SETBRACKET()
        if Address == None:
            if   Region == RI.cregion_PgmMem: Address = self.DI.ProgramMemory[0]
            elif Region == RI.cregion_BtCfg:  Address = self.DI.ConfigBootMemory[0]
            elif Region == RI.cregion_Cfgs:   Address = self.DI.ConfigMemory[0]
        if Size == None:
            if   Region == RI.cregion_PgmMem: Size = self.DI.ProgramMemory[1]
            elif Region == RI.cregion_BtCfg:  Size = self.DI.ConfigBootMemory[2] # fix
            elif Region == RI.cregion_Cfgs:   Size = self.DI.ConfigMemory[1]
        A = Address
        End = Address + Size
        Inc = min(self.DI.RowSize, Size)
        while( A < End ):
            Size = Inc  
            Remain = End - A          
            if Remain < Inc: 
                Size = Remain
            Addr = A - Address
            Memory = ( Addr + Size - 1) << 32 | Addr
            buffer = self.getHex(A, A + Size)
            if len( buffer ) > 0:
                #print('#', end='')
                self.CMD_MEMOBJ_2_REALICE(Region, Addr, Size, bytearray(buffer) )
                if   Region == RI.cregion_PgmMem:  self.CMD_SETOPDESC(RI.RegionProgramMemory, Pgm = Memory)
                elif Region == RI.cregion_BtCfg:   self.CMD_SETOPDESC(RI.RegionBootConfig, BootCfg = Memory)
                elif Region == RI.cregion_Cfgs:    self.CMD_SETOPDESC(RI.RegionCfgMemory, Cfg = Memory)
                else: ERROR('Not supported region')
                self.CMD_PROGRAMOPDESC()
                cnt += Size
            A += Inc
        return cnt

###############################################################################

c = CURIOSITY( join(THIS_DIR, 'APPLICATION.hex') )
INFO('Device ID: 0x%08X' % c.begin() )   
if True:
    INFO('Programing...')
    n = c.program( RI.cregion_PgmMem )
    INFO('  Program Memory : %d' % n)
    n = c.program( RI.cregion_BtCfg )
    INFO('  Boot Config    : %d' % n)
    n = c.program( RI.cregion_Cfgs )
    INFO('  Configuration  : %d' % n)
    pass
c.end()
