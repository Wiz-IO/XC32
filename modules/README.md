# Basic modules template

Adds uncompiled framework source codes

<br>Module script:
```py
from modules import PRINT_MODULE_INFO, dev_module_load

## Execute Function ###########################################################

def init(env, params=''):

    # OBJ_DIR = join( '$BUILD_DIR', 'modules', ... 'MODULE NAME' )
    # SRC_DIR = join( env.framework_dir, ... 'SOURCE PATH')

    env.Append(
        # CPPDEFINES = [  ], ## ADD FLAGS
        # CPPPATH    = [  ], ## INCLUDES
        # LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = [] ) ### COMPILE AS LIBRARY
    )
    
    # env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = [] ) ### COMPILE AS OBJECTS

    # dev_module_load(env, '$MODULES/md-xxx.py') # load other module
    
    PRINT_MODULE_INFO('MODULE TEMPLATE')

## End ########################################################################
```

<br>Project INI:
```ini
custom_module = 
    PATH/md-name.py
    PATH/FOLDER
    md-freertos.py
    md-lwip.py
```
