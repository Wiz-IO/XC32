# Copyright 2023 WizIO ( Georgi Angelov )

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO, dev_module_load

def init(env, params=''):
    dev_module_load(env, '$MODULES/common/md-freertos.py')
    dev_module_load(env, '$MODULES/common/md-lwip.py', 'ARDUINO')
    dev_module_load(env, '$MODULES/common/md-mbedtls.py')

    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'wifi' )
    
    # Curiosity version ?
    SRC_DIR = join( env.framework_dir, 'libraries', 'mrf24wn', 'arduino', 'v1')

    env.Append(
        LIBS = [ 'wdrvext_mz_ef' ],
    )

    filter = []
    if 'SRC' in params.upper():
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter ) 
        PRINT_MODULE_INFO('MRF24WN (src)')
    else:
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )
        PRINT_MODULE_INFO('MRF24WN (lib)')