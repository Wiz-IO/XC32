'''
Copyright 2023 WizIO ( Georgi Angelov )
'''

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO

def init(env, params=''):
    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'fatfs' )
    SRC_DIR = join( env.framework_dir, 'libraries', 'fatfs')
    
    PRJ_DIR = join( env.subst('$PROJECT_DIR'), 'include' )
    if not exists( join(PRJ_DIR, 'ffconf.h') ):
        copyfile( 
            join(env.framework_dir, 'libraries', 'fatfs', 'ffconf'), 
            join(PRJ_DIR, 'ffconf.h') 
        ) 

    env.Append(
        CPPDEFINES = [ 'FATFS' ],
        CPPPATH    = [ join(SRC_DIR) ],
    )

    filter = []

    if 'SRC' in params.upper():
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter )
    else:
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )

    PRINT_MODULE_INFO('FATFS')