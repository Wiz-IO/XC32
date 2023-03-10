# https://github.com/microsoft/uf2/blob/master/utils/uf2conv.py
#!/usr/bin/env python3
import sys
import struct
import subprocess
import re
import os
import os.path
import time
from os.path import join
from platform import system

UF2_MAGIC_START0 = 0x0A324655 # "UF2\n"
UF2_MAGIC_START1 = 0x9E5D5157 # Randomly selected
UF2_MAGIC_END    = 0x0AB16F30 # Ditto

familyid         = 0xAABBCCDD # PIC32
appstartaddr     = 0x1D000000

INFO_FILE = "/INFO_UF2.TXT"

def is_uf2(buf):
    w = struct.unpack("<II", buf[0:8])
    return w[0] == UF2_MAGIC_START0 and w[1] == UF2_MAGIC_START1

def is_hex(buf):
    try:
        w = buf[0:30].decode("utf-8")
    except UnicodeDecodeError:
        return False
    if w[0] == ':' and re.match(b"^[:0-9a-fA-F\r\n]+$", buf):
        return True
    return False

def convert_from_uf2(buf):
    global appstartaddr
    numblocks = len(buf) // 512
    curraddr = None
    outp = []
    for blockno in range(numblocks):
        ptr = blockno * 512
        block = buf[ptr:ptr + 512]
        hd = struct.unpack(b"<IIIIIIII", block[0:32])
        if hd[0] != UF2_MAGIC_START0 or hd[1] != UF2_MAGIC_START1:
            print("Skipping block at " + ptr + "; bad magic")
            continue
        if hd[2] & 1:
            # NO-flash flag set; skip block
            continue
        datalen = hd[4]
        if datalen > 476:
            assert False, "Invalid UF2 data size at " + ptr
        newaddr = hd[3]
        if curraddr == None:
            appstartaddr = newaddr
            curraddr = newaddr
        padding = newaddr - curraddr
        if padding < 0:
            assert False, "Block out of order at " + ptr
        if padding > 10*1024*1024:
            assert False, "More than 10M of padding needed at " + ptr
        if padding % 4 != 0:
            assert False, "Non-word padding size at " + ptr
        while padding > 0:
            padding -= 4
            outp += b"\x00\x00\x00\x00"
        outp.append(block[32 : 32 + datalen])
        curraddr = newaddr + datalen
    return b"".join(outp)

def convert_to_carray(file_content):
    outp = "const unsigned long bindata_len = %d;\n" % len(file_content)
    outp += "const unsigned char bindata[] __attribute__((aligned(16))) = {"
    for i in range(len(file_content)):
        if i % 16 == 0:
            outp += "\n"
        outp += "0x%02x, " % file_content[i]
    outp += "\n};\n"
    return bytes(outp, "utf-8")

def convert_to_uf2(file_content):
    global familyid
    #print("  FamilyID:", hex(familyid))
    datapadding = b""
    while len(datapadding) < 512 - 256 - 32 - 4:
        datapadding += b"\x00\x00\x00\x00"
    numblocks = (len(file_content) + 255) // 256
    outp = []
    for blockno in range(numblocks):
        ptr = 256 * blockno
        chunk = file_content[ptr:ptr + 256]
        flags = 0x0
        if familyid:
            flags |= 0x2000
        hd = struct.pack(b"<IIIIIIII",
            UF2_MAGIC_START0, UF2_MAGIC_START1,
            flags, ptr + appstartaddr, 256, blockno, numblocks, familyid)
        while len(chunk) < 256:
            chunk += b"\x00"
        block = hd + chunk + datapadding + struct.pack(b"<I", UF2_MAGIC_END)
        assert len(block) == 512
        outp.append(block)
    return b"".join(outp)

class Block:
    def __init__(self, addr):
        self.addr = addr
        self.bytes = bytearray(256)

    def encode(self, blockno, numblocks):
        global familyid
        flags = 0x0
        if familyid:
            flags |= 0x2000
        hd = struct.pack("<IIIIIIII",
            UF2_MAGIC_START0, UF2_MAGIC_START1,
            flags, self.addr, 256, blockno, numblocks, familyid)
        hd += self.bytes[0:256]
        while len(hd) < 512 - 4:
            hd += b"\x00"
        hd += struct.pack("<I", UF2_MAGIC_END)
        return hd

def convert_from_hex_to_uf2(buf):
    global appstartaddr
    appstartaddr = None
    upper = 0
    currblock = None
    blocks = []
    for line in buf.split('\n'):
        if line[0] != ":":
            continue
        i = 1
        rec = []
        while i < len(line) - 1:
            rec.append(int(line[i:i+2], 16))
            i += 2
        tp = rec[3]
        if tp == 4:
            upper = ((rec[4] << 8) | rec[5]) << 16
        elif tp == 2:
            upper = ((rec[4] << 8) | rec[5]) << 4
            assert (upper & 0xffff) == 0
        elif tp == 1:
            break
        elif tp == 0:
            addr = upper | (rec[1] << 8) | rec[2]
            if appstartaddr == None:
                appstartaddr = addr
            i = 4
            while i < len(rec) - 1:
                if not currblock or currblock.addr & ~0xff != addr & ~0xff:
                    currblock = Block(addr & ~0xff)
                    blocks.append(currblock)
                currblock.bytes[addr & 0xff] = rec[i]
                addr += 1
                i += 1
    numblocks = len(blocks)
    resfile = b""
    for i in range(0, numblocks):
        resfile += blocks[i].encode(i, numblocks)
    return resfile

def to_str(b):
    #return b.decode("utf-8")
    return b.decode("utf-8", errors='ignore')

def get_drives():
    drives = []
    if sys.platform == "win32":
        r = subprocess.check_output(["wmic", "PATH", "Win32_LogicalDisk", "get", "DeviceID,", "VolumeName,", "FileSystem,", "DriveType"])
        for line in to_str(r).split('\n'):
            words = re.split('\s+', line)
            if len(words) >= 3 and words[1] == "2" and words[2] == "FAT":
                drives.append(words[0])
    else:
        rootpath = "/media"
        if sys.platform == "darwin":
            rootpath = "/Volumes"
        elif sys.platform == "linux":
            tmp = rootpath + "/" + os.environ["USER"]
            if os.path.isdir(tmp):
                rootpath = tmp
        for d in os.listdir(rootpath):
            drives.append(os.path.join(rootpath, d))


    def has_info(d):
        try:
            return os.path.isfile(d + INFO_FILE)
        except:
            return False

    return list(filter(has_info, drives))

def board_id(path):
    with open(path + INFO_FILE, mode='r') as file:
        file_content = file.read()
    return re.search("Board-ID: ([^\r\n]*)", file_content).group(1)

def list_drives():
    for d in get_drives():
        print(d, board_id(d))

def write_file(name, buf):
    with open(name, "wb") as f:
        f.write(buf)
    print("  Wrote %d bytes to %s" % (len(buf), name))


# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/


def upload(target, source, env):
    global appstartaddr
    device_info = env.BoardConfig().get('upload.info', None)
    appstartaddr = int( device_info['flash'], 0 )

    hex_name = join(env.get("BUILD_DIR"), env.get("PROGNAME"))+'.hex'
    uf2_name = join(env.get("BUILD_DIR"), env.get("PROGNAME"))+'.uf2'

    print( "  Converting to UF2 ( 0x%x )" % (appstartaddr) )
    with open( hex_name, mode='rb' ) as f: inpbuf = f.read()
    outbuf = convert_from_hex_to_uf2(inpbuf.decode("utf-8"))

    time.sleep(.1)
    write_file(uf2_name, outbuf) # write uf2 to build folder
    drives = get_drives()
    if len(drives) == 0:
        print("\033[1;37;41m                               ")
        print("\033[1;37;41m   USB drive not found.        ")
        print("\033[1;37;41m                               ")
        return
    for d in drives:
        print("Flashing %s (%s)" % (d, board_id(d)))
        write_file(d +'/'+ env.get("PROGNAME")+'.uf2', outbuf)
    time.sleep(1.0) # usb-serial driver up