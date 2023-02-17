# Basic modules template

Compile & Link uncompiled framework source codes ( existing ones, third-party )

<br>**Project INI**
```ini
custom_module = 
    PATH/md-name.py                 ; stand alone
    PATH/FOLDER                     ; all from folder, module names must begin with 'md-'
    $PROJECT_DIR/PATH               ; userware
    $MODULES/common/md-name.py      ; predefined ( common )
    $MODULES/Arduino/md-name.py     ; predefined
    $MODULES/Baremetal/md-name.py   ; predefined
    md-freertos.py                  ; platform ( Arduino / Baremetal ) predefined
    md-lwip.py                      ; platform ( Arduino / Baremetal ) predefined
    md-tinyusb.py = HOST            ; support params, separated by a space
    
; by default, predefined modules are compiled as static libraries, md-name.py = SRC or LIB
```

<br>**Basic module script** ( it's actually a normal Python script for PlatformIO support ( as extra script ) )
```py
from modules import PRINT_MODULE_INFO, dev_module_load

def init(env, params=''): # entry point

    OBJ_DIR = join( '$BUILD_DIR', 'modules', ... 'MODULE NAME' )
    SRC_DIR = join( env.framework_dir, ... 'SOURCE PATH')

    env.Append(
        CPPDEFINES = [ 'ANY FLAGS' ], 
        CPPPATH    = [ 'INCLUDE PATH' ], 
        LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = [ '+<*>', '-<code>' ] ) ### COMPILE AS LIBRARY
    )
    
    # env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = [ ??? ] ) ### COMPILE AS OBJECTS

    # dev_module_load(env, '$MODULES/md-xxx.py') ### load other module
    
    PRINT_MODULE_INFO('MODULE NAME')

```
as examples: see [here](https://github.com/Wiz-IO/XC32/tree/main/modules)

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
