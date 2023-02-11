# Basic modules template

Adds uncompiled framework source codes ( existing ones, third-party )

<br>Project INI:
```ini
custom_module = 
    PATH/md-name.py
    PATH/FOLDER
    md-freertos.py
    md-lwip.py
```

<br>Module script:
```py
from modules import PRINT_MODULE_INFO, dev_module_load

## Execute Function ###########################################################

def init(env, params=''):

    OBJ_DIR = join( '$BUILD_DIR', 'modules', ... 'MODULE NAME' )
    SRC_DIR = join( env.framework_dir, ... 'SOURCE PATH')

    env.Append(
        CPPDEFINES = [ 'ANY FLAGS' ], 
        CPPPATH    = [ 'INCLUDE PATH' ], 
        LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = [] ) ### COMPILE AS LIBRARY
    )
    
    # env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = [] ) ### COMPILE AS OBJECTS

    # dev_module_load(env, '$MODULES/md-xxx.py') ### load other module
    
    PRINT_MODULE_INFO('MODULE NAME')

## End ########################################################################
```

<br>LOG:
```
PLATFORM: PlatformIO - PIC32 (1.0.0) > WizIO-PIC32MZ
HARDWARE: 32MZ2048EFM100 200MHz, 512KB RAM, 2MB Flash
PACKAGES:
 - framework-XC32 @ 1.0.0
   XC32 : 2.1
   CORE   : PIC32MZ
   CHIP   : 32MZ2048EFM100
   STACK  : 1024
   HEAP   : 65536
   OPTI   : -O1
   PROJECT MODULES       <-------<
          : FREERTOS
          : LWIP
      
RAM:   [          ]   1.6% (used 8356 bytes from 524288 bytes)
Flash: [=         ]   6.3% (used 132352 bytes from 2097152 bytes)
====================== [SUCCESS] Took 1.52 seconds =================
```
