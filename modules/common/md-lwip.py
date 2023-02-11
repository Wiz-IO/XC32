# Copyright 2023 WizIO ( Georgi Angelov )

# custom_module = %MODULES/common/md-lwip [ SRC(optional) ]

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO

# TODO

def init(env, params=''):
    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'lwip' )
    SRC_DIR = join( env.framework_dir, 'libraries', 'lwip')

    # PRJ_DIR = join( env.subst('$PROJECT_DIR'), 'include' )
    # if not exists( join(PRJ_DIR, '.h') ): copyfile()

    env.Append(
        CPPDEFINES = [ 'LWIP' ],
        CPPPATH = [ 
            join(SRC_DIR, 'include'), 
            join(SRC_DIR, 'port'), 
        ]
    )

    filter = [
        '-<*>', 
        '+<core>',         
    ]

    if 'SRC' in params.upper():
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter ) 
    else:
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )

    PRINT_MODULE_INFO('LWIP')