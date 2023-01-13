# Copyright 2023 (c) 2023 WizIO ( Georgi Angelov )
#   Reverse Engineering of PIC32MZ Curiosity PKOB
#   Version:
#       Reverse Engineering version ... NOT READY !!!
#
#   Python depend:
#       intelhex,
#       pyusb ( libusb-1.0.dll ) https://github.com/libusb/libusb/releases
#


import sys, struct, time, inspect
from os.path import join, normpath, dirname

THIS_DIR = normpath( dirname(__file__) )

END_POINT_SIZE = 64
DEBUG = True

def FUNC(txt=''):
    print( 'FUNCTION: %s( %s )' % ( inspect.stack()[1][3], str(txt) ) )

def ERROR(txt):
    print()
    print( 'FUNCTION: %s( %s )' % ( inspect.stack()[1][3], str(txt) ) )
    try:
        import click
        click.secho( '[ERROR] %s' % txt, fg='red')
    except:
        print( '[ERROR] %s' % txt)
    print()
    time.sleep(.1)
    sys.exit(-1)

def DUMP(buf, txt=None, cnt=END_POINT_SIZE, mod=16, print_chars=False, max=True):
    #return
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

try:
    import usb.core
    import usb.util
    from intelhex import IntelHex
except ImportError:
    ERROR('Python dependency')

### COMMANDS
cmd_ME2_RUNTIMEWRITE = 1
cmd_GETVOLTAGES = 32
cmd_PRODTESTMODE = 33
cmd_PROGRS = 34
cmd_PROGAP = 35
cmd_PROGFPGA = 36
cmd_INITCOMM = 37
cmd_BIST = 38
cmd_SELF_TESTER = 39
cmd_INITCOMMICD3 = 41
cmd_INITCOMMPK3_2K = 45
cmd_ABORT = 62
cmd_GET_STATUS = 63
cmd_SETDDS = 64
cmd_GETVERSIONS = 65
cmd_SETJAM = 66
cmd_SETPROBES = 69
cmd_SETPMON = 72
cmd_GETVERSIONS2 = 73
cmd_SETOPDESC = 80
cmd_PROGRAMOPDESC = 81
cmd_VERIFYOPDESC = 82
cmd_ERASEOPDESC = 83
cmd_READOPDESC = 84
cmd_BLANKOPDESC = 85
cmd_SETOSCCALOVERRIDE = 87
cmd_GET_LASTERROR = 94
cmd_GET_FAILURES = 95
cmd_MEMOBJ_2_REALICE = 96
cmd_MEMOBJ_2_PC = 97
cmd_SETDMAREADDESC = 98
cmd_SETEMULATORPWR = 99
cmd_SENDDMAWRITE = 100
cmd_REQDMAREADS = 101
cmd_SENDAPPIN = 102
cmd_ONE_TIME_DMA_READ = 103
cmd_SETDYNAMICBPS = 104
cmd_CONNECT2DEVICE = 112
cmd_CONNECT2DEBUG = 113
cmd_RUN = 131
cmd_SINGLESTEP = 132
cmd_RESET = 133
cmd_GETPC = 134
cmd_SETPC = 135
cmd_PGM_SINGLE_INSTRUCTION = 137
cmd_PT_DMA_TEST = 144
cmd_SET_TRACEDESCRIPT = 145
cmd_SET_PERIPHERAL_FREEZE = 146
cmd_SET_DEBUG_OPTIONS = 147
cmd_PROGPMON = 149
cmd_STACK_SNAPSHOT_TAKE_HT = 153
cmd_SENDSINGLE_CFG = 158
cmd_SETBRACKET = 160
cmd_QUERY_PGM_2_GO = 161
cmd_SETUP_PGM_2_GO = 162
cmd_FINAL_PGM_2_GO = 163
cmd_CLEAR_PGM_2_GO = 164

### POWER BITS
bitEMULATOR_POWER   = 1
bitPOWER_STAY_ON    = 2
bitMCLRHOLD         = 4
bitP24FHVEntry      = 8
bitLVP_TMOD         = 16  

### OBJ REGIONS
cregion_PgmMem = 1
cregion_DataMem = 2
cregion_Ids = 3
cregion_Cfgs = 4
cregion_Test = 5
cregion_DebugExec = 7
cregion_PgmExec = 8
cregion_OscCal = 9
cregion_RAM = 12
cregion_REG = 13
cregion_BtCfg = 15
cregion_FREEZE_RAM = 16
cregion_FREEZE_EMU = 17
cregion_NMMR = 31
cregion_AUX = 20
cregion_AltBootMemory = 21
cregion_Boot1Memory = 22
cregion_Boot2Memory = 23
cregion_AltConfigMemory = 24
cregion_Boot1ConfigMemory = 25
cregion_Boot1AltConfigMemory = 26
cregion_Boot2ConfigMemory = 27
cregion_Boot2AltConfigMemory = 28
cregion_LowerBootAliasLastPage = 29
cregion_Boot1LastPage = 30
cregion_Boot2LastPage = 33
cregion_FBOOT = 48

### OP REGION MASK
RegionProgramMemory = 1
RegionDataMemory = 2
RegionIDMemory = 4
RegionCfgMemory = 8
RegionTestMemory = 16
RegionCalMemory = 32
RegionPgmExecutive = 64
RegionDbgExecutive = 128
RegionBootConfig = 256
RegionAuxMemory = 512
RegionAltBootMemory = 1024
RegionBoot1Memory = 2048
RegionBoot2Memory = 4096
RegionAltConfigMemory = 8192
RegionBoot1ConfigMemory = 16384
RegionBoot1AltConfigMemory = 32768
RegionBoot2ConfigMemory = 65536
RegionBoot2AltConfigMemory = 131072
RegionFBOOT = 262144
RegionProgramMemory2 = 16777216
RegionCfgMemory2 = 8388608
RegionLowerBootAliasLastPage = 524288
RegionAltBootMemoryLastPage = 4194304
RegionBoot1MemoryLastPage = 1048576
RegionBoot2MemoryLastPage = 2097152;

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
        print('Tool ready')

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

class DeviceInfo:
    PE_FILE = join(THIS_DIR, 'RIPE_15_000510.hex')
    ProgramMemory = 0x1D000000, 0x200000
    ConfigMemory  = 0x1FC0FFC0, 0x40

    def get(self): return self.dds

    def __init__(self):
        a  = struct.pack('<HH', 0x036C, 0x0002) # ProcId OperationMode
        a += struct.pack('<III', 0xFFFFFFFF, 0x0FFFFFFF,0x0723B053)  # DeviceId.Address Mask Value
        a += struct.pack('<IIIIIIII', 0,0,0,0,0,0,0,0)  # VersionIds[8]
        a += struct.pack('<HHHHHHH', 0,0,0,0,0,0,0) # PGMWAIT LVPGMWAIT EEDATAWAIT CFGWAIT IDWAIT ERASEWAIT LVERASEWAIT
        a += struct.pack('<H', 0) # EraseAlg
        a += struct.pack('<BBBBB', 0, 0, 0, 0, 0)    # Latches[5] PgmMem DataMem CfgMem Userid RowErase
        a += struct.pack('<BBB', 0x14, 0x1C, 0x1A)   # VDD[3] min, VDD.max, VDD.def
        a += struct.pack('<BBB', 0x14, 0x1C, 0x1A)   # VPP[3] min, VPP.max, VPP.def
        a += struct.pack('<BBB', 0x14, 0x1C, 0x00)   # [3] VddMinDef, VddMaxDef, LvThresh
        a += struct.pack('<II', self.ProgramMemory[0], self.ProgramMemory[1]) # ProgramMemory     00 00 00 1D - 00 00 20 00
        a += struct.pack('<II', 0x00000000, 0x00000000) # DataMemory        00 00 00 00 - 00 00 00 00
        a += struct.pack('<II', 0x00000000, 0x00000000) # IDMemory          00 00 00 00 - 00 00 00 00
        a += struct.pack('<II', 0x00000000, 0x00000000) # ConfigMemory      C0 FF C0 1F - 40 00 00 00
        a += struct.pack('<II', 0x00000000, 0x00000000) # TestMemory        00 40 C7 1F - 00 40 00 00
        a += struct.pack('<II', 0x00000000, 0x00000000) # TestAppMemory     00 00 00 00 - 00 00 00 00
        a += struct.pack('<HH', 1, 0) # PanelNumber PanelSize
        a += struct.pack('<HHHHHHHHHH', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) # RequiredBitsMask[10 * H]
        a += struct.pack('<HHHHHHHHHH', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) # BlankValue[10 * H]
        a += struct.pack('<I', 0) # CalibrationAddress [I]
        a += struct.pack('<III', 0, 0, 0) # BKBugBit [III]
        a += struct.pack('<H', 0) # MinorAlg [H]
        a += struct.pack('<II', 0, 0) # ConfigBootMemory [II]
        a += struct.pack('<H', 0) # DebugAlg [H]
        a += struct.pack('<HIIIIII', 0,   0, 0, 0, 0, 0, 0) # devHdr [H + 6*I]
        a += struct.pack('<H', 0) # EraseAlg
        a += struct.pack('<I', 0) # DevSpecificFlags [I]
        a += struct.pack('<II', 0, 0) # AuxMemory [II]
        a += struct.pack('<II', 0, 0) # CalibrationMemory [II]
        a += struct.pack('<BBBBBB', 0, 0, 0, 0, 0, 0) # LatchesHighByte [6*B]
        a += struct.pack('<II', 0, 0) # UpperBootAliasMemory MemoryDescriptors[10 * II]
        a += struct.pack('<II', 0, 0) # BootFlash1Memory
        a += struct.pack('<II', 0, 0) # BootFlash2Memory
        a += struct.pack('<II', 0, 0) # LowerBootCfgAltMemory
        a += struct.pack('<II', 0, 0) # BootFlash1CfgMemory
        a += struct.pack('<II', 0, 0) # BootFlash1CfgAltMemory
        a += struct.pack('<II', 0, 0) # BootFlash2Cfgmemory
        a += struct.pack('<II', 0, 0) # BootFlash2CfgAltmemory
        a += struct.pack('<II', 0, 0) # LowerBootAliasMemoryLastPage
        a += struct.pack('<II', 0, 1) # BootFlash1MemoryLastPage

        a += struct.pack('<H', 0) # ??!??
        self.dds = a
        #DUMP(a, "DeviceInfo", cnt=len(a))
        pass

class CURIOSITY:
    def getHex(self, hex, START, END):
        bin = hex.tobinarray(start = START, end = END - 1)
        for b in bin: # skip if blank
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
        self.rx = b''
        self.USB = USBHID()
        self.DI = DeviceInfo()

        PE = IntelHex()
        PE.fromfile(self.DI.PE_FILE, format='hex')
        for s in PE.segments(): pass # print('%X [ %d ]' %( s[0], s[1]-s[0]))
        self.PE_BIN = PE.tobinarray(start = s[0], end = s[1] - 1)
        #DUMP('D', self.PE_BIN, cnt=4204, mod=16)

        self.HEX = IntelHex()
        self.HEX.fromfile(hex_file, format='hex')

    def align(self, buf):
        size = len( buf )
        mod = size % END_POINT_SIZE
        if mod > 0:
            for i in range(0, END_POINT_SIZE - mod): 
                buf += b'\x5A'
        return buf

    def wait_command(self, cmd):
        self.rx = self.USB.read()
        CMD = struct.unpack('<H', self.rx[0:2])[0]
        if CMD != cmd:
            ERROR('Receive Command: %02X, Read: %02X' % (cmd, CMD))

    def wait_status(self):
        for i in range(20):
            rx = self.USB.read()
            if len(rx) > 0:
                if rx[0] == 255: # res_FAIL:
                    ERROR('STATUS FAIL')
                if rx[0] == 0: # res_SUCCESS:
                    return rx # done
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
        FUNC( cmd )
        a  = struct.pack('<H', cmd)
        a += struct.pack('<H', 0x5A5A)
        return self.send(a, None, read, status )

    def CMD_SET_DEBUG_OPTIONS(self, Options1=0, Options2=0):
        FUNC()
        a = struct.pack('<H', cmd_SET_DEBUG_OPTIONS)
        a += struct.pack('<I', 8)
        a += struct.pack('<I', Options1)
        a += struct.pack('<I', Options2)
        return self.send(a, None, True, False)

    def CMD_SETBRACKET(self, bool):
        FUNC( bool )
        a  = struct.pack('<H', cmd_SETBRACKET)
        a += struct.pack('<H', bool & 1)
        a += struct.pack('<H', 0x5A5A)
        self.send(a, None, True, True )

    def CMD_MEMOBJ_2_REALICE(self, MemRegion, StartAddr, Size, payload):
        FUNC()
        a  = struct.pack('<H', cmd_MEMOBJ_2_REALICE)
        a += struct.pack('<H', MemRegion)
        a += struct.pack('<I', StartAddr)
        a += struct.pack('<I', Size)
        a += struct.pack('<H', 0x5A5A)
        return self.send(a, payload, True, True)

    def CMD_SETOPDESC(self, Regions=0, Options=0, Pgm=0, Data=0, Id=0, Cfg=0, Test=0, BootCfg=0, Aux=0, FBoot=0):
        FUNC()
        a  = struct.pack('<H', cmd_SETOPDESC)
        a += struct.pack('<H', 72)
        a += struct.pack('<I', Regions)
        a += struct.pack('<I', Options)
        a += struct.pack('<Q', Pgm)
        a += struct.pack('<Q', Data)
        a += struct.pack('<Q', Id)
        a += struct.pack('<Q', Cfg)
        a += struct.pack('<Q', Test)
        a += struct.pack('<Q', BootCfg)
        a += struct.pack('<Q', Aux)
        a += struct.pack('<Q', FBoot)
        a += struct.pack('<H', 0x5A5A)
        self.send(a, None, True, False)

    def CMD_READOPDESC(self):
        FUNC()
        self.COMMAND(cmd_READOPDESC, True, True)

    def CMD_PROGRAMOPDESC(self):
        FUNC()
        self.COMMAND(cmd_PROGRAMOPDESC, True, True)

    def CMD_ERASEOPDESC(self):
        FUNC()
        self.COMMAND(cmd_ERASEOPDESC, True, True)

    def CMD_SETDDS(self):
        FUNC()
        b = self.DI.get()
        a  = struct.pack('<H', cmd_SETDDS)
        a += struct.pack('<H', len(b))
        a += struct.pack('<H', 0x5A5A)
        self.send(a, b, True, True)

    def CMD_SETEMULATORPWR(self, Power, Voltage):
        FUNC()
        a  = struct.pack('<H', cmd_SETEMULATORPWR)
        a += struct.pack('<H', 4)  
        a += struct.pack('<H', Power)
        a += struct.pack('<H', Voltage)  
        a += self.fill(52)   
        a += struct.pack('<I', 4 + 4) 
        self.send(a, None, True, True)

    def get_device_id(self):
        FUNC()
        self.CMD_SETBRACKET(1)
        rx = self.COMMAND(cmd_CONNECT2DEVICE, True, True) # 00 00 | 53 B0 23 17 = PIC32MZ2048EFM100 DevID: 0x0723B053 Rev?=1
        self.device_id = struct.unpack('<HI', rx[0:6])[1] & 0x0FFFFFFF
        self.CMD_SETBRACKET(0)
        if self.device_id == 0: ERROR('Device ID = 0')
        return self.device_id

    def end(self):
        FUNC()
        self.CMD_SETEMULATORPWR(bitPOWER_STAY_ON | bitEMULATOR_POWER, 26) 

    def begin(self):
        FUNC()
        self.COMMAND(cmd_INITCOMMPK3_2K, False, False)
        self.COMMAND(cmd_GET_STATUS)
        self.COMMAND(cmd_GETVERSIONS)
        self.COMMAND(cmd_GETVERSIONS2)
        self.CMD_SETDDS()
        self.CMD_SETEMULATORPWR(bitMCLRHOLD | bitPOWER_STAY_ON | bitEMULATOR_POWER, 26)
        self.program_pe()
        return self.get_device_id()

    def ping_read(self, bracket=True):
        FUNC()
        if bracket: self.CMD_SETBRACKET(bracket)
        self.CMD_SETOPDESC()
        self.CMD_READOPDESC()

    def program_pe(self, address=0):
        FUNC()
        print('Uploading PE')
        self.CMD_SET_DEBUG_OPTIONS()
        self.CMD_SETBRACKET(1)
        self.CMD_MEMOBJ_2_REALICE(cregion_PgmExec, address, len(self.PE_BIN), bytearray(self.PE_BIN))
        self.CMD_SETOPDESC(Options=1)
        self.CMD_PROGRAMOPDESC()
        self.CMD_SETBRACKET(0)
        print('Uploaded PE\n')

    def program_pgm(self):
        FUNC()
        print('Programing PGM: 0x%X [%d]' % (self.DI.ProgramMemory))
        STEP = 2048
        for ADDRESS in range(self.DI.ProgramMemory[0], self.DI.ProgramMemory[0]+self.DI.ProgramMemory[1], STEP):
            buf = self.getHex(self.HEX, ADDRESS, ADDRESS + STEP)
            if len(buf) > 0:
                A = ADDRESS - self.DI.ProgramMemory[0]
                print('\taddress: 0x%X [%X]' % (ADDRESS, A))
                self.CMD_MEMOBJ_2_REALICE(cregion_PgmMem, A, STEP, bytearray(buf) )
                self.CMD_SETOPDESC(Regions = RegionProgramMemory, Pgm = ( A + STEP - 1) << 32 | A) # end | start
                self.CMD_PROGRAMOPDESC()
        print('PGM DONE')
        pass


print('--- BEGIN ---')
c = CURIOSITY( join(THIS_DIR, 'APPLICATION.hex') )
print('Device ID: 0x%08X\n' % c.begin() )
c.ping_read()
c.program_pgm()
# TODO OTHER
c.end()
print('---- END ----')