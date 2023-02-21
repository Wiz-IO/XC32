# Copyright 2023 WizIO ( Georgi Angelov )

import sys
from os.path import join, dirname, exists
from SCons.Script import AlwaysBuild, DefaultEnvironment, Default
from frameworks.wiz import ERROR
from platformio import proc
PYTHON_PATH = dirname( proc.get_pythonexe_path() )

env = DefaultEnvironment()

XC32PATH = join(dirname( env['PLATFORM_MANIFEST'] ), 'XC32PATH')
p = 'C:\\Program Files\\Microchip\\xc32\\v4.21'
if exists( XC32PATH ):
    f = open(XC32PATH, 'r')
    p = f.read()
env.xc32_dir = env.GetProjectOption('custom_x32', p) 
env['ENV']['PATH'] = '' + join(env.xc32_dir, 'bin' + ';' + PYTHON_PATH)
if sys.platform == "win32":
    env['ENV']['PATH'] += ';C:\Windows\system32\WBEM' # need for UF2

env.xc32_ver = 2.10
x = env.xc32_dir.replace('/','').replace('\\','').split('xc32')
env.xc32_ver = float(x[1].replace('v',''))

env.Replace( 
    BUILD_DIR   = env.subst("$BUILD_DIR"),
    ARFLAGS     = ['rc'],        
    AR          = 'xc32-ar',
    ARCOM       = '$AR $ARFLAGS $TARGET.posix ${_long_sources_hook(__env__, SOURCES)}',
    AS          = 'xc32-as',
    CC          = 'xc32-gcc',
    CXX         = 'xc32-g++', 
    RANLIB      = 'xc32-ranlib',
    OBJCOPY     = 'xc32-objdump', 
    ELFHEX      = 'xc32-bin2hex',
    SIZETOOL    = 'xc32-size',
    PROGSUFFIX  = '.elf',   
)

prg = None

###############################################################################

if 'Baremetal' in env['PIOFRAMEWORK'] or 'Arduino' in env['PIOFRAMEWORK']: 
    elf = env.BuildProgram()
    hex = env.ELF2HEX( join('$BUILD_DIR', '${PROGNAME}'), elf )
    prg = env.Alias( 'buildprog', hex)
else: 
    ERROR('[MAIN] Wrong platform: %s' % env['PIOFRAMEWORK'][0])

AlwaysBuild( prg )

# DEBUG - Challenge, but in some other life...
Default( prg )

# UPLOAD
upload = env.Alias('upload', prg, env.VerboseAction('$UPLOADCMD', 'Uploading...'), ) 
AlwaysBuild( upload )

#print(env.Dump())

###############################################################################
