'''
Copyright 2023 WizIO ( Georgi Angelov )
'''

from modules import PRINT_MODULE_INFO

## Execute Function ###########################################################

def init(env, params=''):

    # OBJ_DIR = join( '$BUILD_DIR', 'modules', ... 'MODULE NAME' )
    # SRC_DIR = join( env.framework_dir, ... 'SOURCE PATH')

    env.Append(
        # CPPDEFINES = [  ], ## ADD FLAGS
        # CPPPATH    = [  ], ## INCLUDES
        # LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = [] ) ### COMPILE AS LIBRARY
    )
    
    #env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = [] ) ### COMPILE AS OBJECTS

    PRINT_MODULE_INFO('ARDUINO MODULE TEMPLATE')

## End ########################################################################