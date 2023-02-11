# Copyright 2023 WizIO ( Georgi Angelov )

# custom_module = %MODULES/common/md-freertos [ SRC(optional) ]

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO

def init(env, params=''):
    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'freertos' )
    SRC_DIR = join( env.framework_dir, 'libraries', 'freertos')

    PRJ_DIR = join( env.subst('$PROJECT_DIR'), 'include' )
    if not exists( join(PRJ_DIR, 'FreeRTOSConfig.h') ): 
        copyfile(
            join(env.framework_dir, 'libraries', 'freertos', 'FreeRTOSConfig'),
            join(PRJ_DIR, 'FreeRTOSConfig.h')
        )

    env.Append(
        CPPDEFINES = [ 'FREERTOS' ],
        CPPPATH    = [
            join(SRC_DIR, 'include'),
            join(SRC_DIR, 'portable', 'MPLAB', 'PIC32MZ'),
        ],
    )

    filter = [
        '+<*>',
        '-<portable/Common>',
        '-<portable/MemMang>',
        '+<portable/MemMang/heap_4.c>',
    ]

    if 'SRC' in params.upper():
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter ) 
        PRINT_MODULE_INFO('FREERTOS (src)')
    else:
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )
        PRINT_MODULE_INFO('FREERTOS (lib)')