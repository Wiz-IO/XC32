# Copyright 2023 (c) WizIO ( Georgi Angelov )

from os.path import join, dirname
from shutil import copyfile
from SCons.Script import Builder
from wiz import INFO, FRAMEWORK_NAME
import uploader

def dev_uploader(target, source, env):
    p = env.BoardConfig().get('upload.protocol', None) 
    if p == 'curiosity':
        from uploader.CURIOSITY import upload
        uploader.CURIOSITY.upload(target, source, env)
    elif p == 'GEN4':
        from uploader.GEN4 import upload
        uploader.GEN4.upload(target, source, env)

def dev_ini_add(env, txt):
    f = open( join( env.subst('$PROJECT_DIR'), 'platformio.ini' ), 'a+' )
    f.write(txt) 
    f.close()

def dev_get_value(env, name, default):
    return env.GetProjectOption('custom_%s' % name, # ini user config  
           env.BoardConfig().get('build.%s' % name, default) ) # default from board

def dev_init_compiler(env):
    env['PLATFORM_DIR' ] = env.platform_dir  = dirname( env['PLATFORM_MANIFEST'] )
    env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir( FRAMEWORK_NAME )    
    env.Replace( 
        PROGNAME = env.GetProjectOption('custom_name', 'APPLICATION') # INIDOC 
    )

    INFO('XC32 : %s' % env.xc32_ver)
    if 'Arduino' in env['PIOFRAMEWORK']:
        INFO('CORE : %s' % env.BoardConfig().get('build.core') )
    env.category = env.BoardConfig().get('build.category')      
    env.mcu     = env.BoardConfig().get('build.mcu')           
    INFO('CHIP : %s' % env.mcu )
    heap = dev_get_value(env, 'heap', '32768') # INIDOC 
    INFO('HEAP : %s' % heap ) 

    env.Append(
        #ASFLAGS=[],
        CPPDEFINES = [
           'F_CPU=' + dev_get_value(env, 'f_cpu', '200000000L'),
        ],
        CPPPATH = [
            join('$PROJECT_DIR', 'src'),
            join('$PROJECT_DIR', 'lib'),
            join('$PROJECT_DIR', 'include'),
        ],
        CFLAGS = [
            #'-std=gnu99',
        ],
        CCFLAGS = [
            #'-O0', # LICENSED COMPILER
            '-mprocessor=' + env.mcu,            
            '-fdata-sections',
            '-ffunction-sections',            
            '-Wall',
            '-Wextra',
            '-Wfatal-errors',
            '-Wno-unused-parameter',
            '-Wno-unused-function',
            '-Wno-unused-variable',
            '-Wno-unused-value',
        ],
        CXXFLAGS = [
            #'-std=c++11',
            '-fno-rtti',
            '-fno-exceptions',
            '-fno-use-cxa-atexit',      # __cxa_atexit, __dso_handle
            "-fno-threadsafe-statics",  # __cxa_guard_acquire, __cxa_guard_release            
            '-fno-non-call-exceptions',
        ],
        LIBSOURCE_DIRS = [ 
            join('$PROJECT_DIR', 'lib'), 
        ],        
        LIBPATH = [ 
            join(env.xc32_dir, env.category, 'lib', 'proc', env.mcu),
            join('$PROJECT_DIR', 'lib'), 
        ],
        LIBS = [ 'm', 'c', ], 
        LINKFLAGS = [ 
            '-DXPRJ_default=default',          
            '-mprocessor=' + env.mcu, 
            '-Wl,--script="p' + env.mcu + '.ld"',
            '-Wl,--defsym=__MPLAB_BUILD=1',
            '-Wl,--defsym=_min_heap_size=%s' % heap,
            '-Wl,--no-code-in-dinit',
            '-Wl,--no-dinit-in-serial-mem',
            '-Wl,--gc-sections',
            '--entry=_reset',
        ],
        BUILDERS = dict(
            ELF2HEX = Builder(
                action = env.VerboseAction(' '.join([ '$ELFHEX', '$SOURCES', '-a']), 'Creating HEX $TARGET'),
                suffix = '.hex'
            )           
        ), 
        UPLOADCMD = dev_uploader,       
    )
    
###############################################################################
