# Copyright 2023 WizIO ( Georgi Angelov )

# custom_module = %MODULES/common/md-lwip [ SRC(optional) ]

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO

# TODO

def init(env, params=''):
    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'lwip' )
    SRC_DIR = join( env.framework_dir, 'libraries', 'lwip')

    PRJ_DIR = join( env.subst('$PROJECT_DIR'), 'include' )

    arduino = False
    for define in env.get('CPPDEFINES'):
        if 'ARDUINO' in define:
            arduino = True

    if not exists( join(PRJ_DIR, 'lwipopts.h') ): 
        template = 'b_lwipopts'
        if arduino: 
            template = 'a_lwipopts'
        copyfile(
            join(SRC_DIR, template),
            join(PRJ_DIR, 'lwipopts.h')
        )            
    env.Append(
        CPPDEFINES = [ 'LWIP' ],
        CPPPATH = [ 
            join(SRC_DIR, 'include'), 
        ]
    )

    filter = [
        '-<*>', 
        '+<core>',  
        '+<api>',
        '+<netif/ethernet.c>',       
    ]

    if 'SRC' in params.upper():
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter ) 
        PRINT_MODULE_INFO('LWIP (src)')
    else:
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )
        PRINT_MODULE_INFO('LWIP (lib)')