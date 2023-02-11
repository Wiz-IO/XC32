'''
Copyright 2023 WizIO ( Georgi Angelov )
'''
# Copyright 2023 WizIO ( Georgi Angelov )

# custom_module = %MODULES/common/md-tinyusb [ HOST(optional) SRC(optional) ]

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO

def init(env, params=''):
    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'tyusb' )
    SRC_DIR = join( env.framework_dir, 'libraries', 'tinyusb' )

    PRJ_DIR = join( env.subst('$PROJECT_DIR'), 'include' )
    if not exists( join(PRJ_DIR, 'tusb_config.h') ):
        copyfile( 
            join(env.framework_dir, 'libraries', 'tinyusb', 'tusb_config'), 
            join(PRJ_DIR, 'tusb_config.h') 
        ) 

    env.Append(       
        CPPDEFINES = [ 'TINYUSB', 'CFG_TUSB_MCU=OPT_MCU_PIC32MZ', 'CFG_TUSB_OS=OPT_OS_NONE' ], 
        CPPPATH    = [ SRC_DIR ]  
    )

    mode = 'DEVICE'
    if 'HOST' in params.upper():    
        filter =  [ '+<*>', '-<device>', '+<class>' ]
        mode = 'HOST'
    else:       
        filter = [ '+<*>', '-<host>', '+<class>' ]

    if 'SRC' in params.upper(): 
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter )   
        PRINT_MODULE_INFO('TINYUSB %s (src)' % mode)
    else: 
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )   
        PRINT_MODULE_INFO('TINYUSB %s (lib)' % mode)  