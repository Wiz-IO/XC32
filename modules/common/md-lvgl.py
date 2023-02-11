# Copyright 2023 WizIO ( Georgi Angelov )

# custom_module = %MODULES/common/md-lvgl [ SRC(optional) ]

from os.path import join, exists
from shutil import copyfile
from modules import PRINT_MODULE_INFO

# TODO

def init(env, params=''):
    OBJ_DIR = join( '$BUILD_DIR', 'modules', 'lvgl' )
    SRC_DIR = join( env.framework_dir, 'libraries', 'lvgl', 'src')

    env.Append(
        CPPDEFINES = [ 'LVGL', 'LV_CONF_INCLUDE_SIMPLE' ],
        CPPPATH    = [ SRC_DIR ],
    )

    filter = [
        '+<*>', 
        '-<draw/arm2d>', 
        '-<draw/gd32_ipa>',
        '-<draw/nxp>',
        '-<draw/sdl>',
        '-<draw/stm32_dma2d>',
        '-<draw/swm341_dma2d>',      
    ]

    if 'SRC' in params.upper():
        env.BuildSources( OBJ_DIR, SRC_DIR, src_filter = filter ) 
    else:
        env.Append( LIBS = env.BuildLibrary( OBJ_DIR, SRC_DIR, src_filter = filter ) )

    PRINT_MODULE_INFO('LVGL')