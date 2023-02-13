# Copyright 2023 (c) WizIO ( Georgi Angelov )

from os.path import join, dirname, exists
from os import listdir
from shutil import copyfile
from SCons.Script import Builder
from wiz import INFO, FRAMEWORK_NAME
from modules import dev_init_modules
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

def create_template(env, Template):
    dir = join( env.subst('$PROJECT_DIR'), 'src' )
    if not listdir( dir ):
        copyfile( join(env.platform_dir, 'boards', env.BoardConfig().id), join(dir, 'fuses.c') )    
        if Template: 
            Template(env)
        open( join(env.subst('$PROJECT_DIR'), 'include', 'user_config.h'), 'w').write('''#ifndef _USER_CONFIG_H_
#define _USER_CONFIG_H_
#ifdef __cplusplus
extern "C"
{
#endif

#include <stdint.h>

#ifdef __cplusplus
}
#endif
#endif /* _USER_CONFIG_H_ */
''')

def dev_get_value(env, name, default):
    return env.GetProjectOption('custom_%s' % name, # ini user config
           env.BoardConfig().get('build.%s' % name, default) ) # default from board

def dev_init_compiler(env, Template=None):
    env['PLATFORM_DIR' ] = env.platform_dir  = dirname( env['PLATFORM_MANIFEST'] )
    env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir( FRAMEWORK_NAME )
    create_template(env, Template)

    INFO('XC32 : %s' % env.xc32_ver)
    if 'Arduino' in env['PIOFRAMEWORK']:
        INFO('CORE   : %s' % env.BoardConfig().get('build.core') )

    env.EVB = env.BoardConfig().get('build.EVB')
    env.category = env.BoardConfig().get('build.category')
    env.mcu     = env.BoardConfig().get('build.mcu')
    INFO('CHIP   : %s' % env.mcu )
    stack = dev_get_value(env, 'stack', '1024') # INIDOC
    INFO('STACK  : %s' % stack ) 
    heap = dev_get_value(env, 'heap', '65536') # INIDOC
    INFO('HEAP   : %s' % heap )
    opti = dev_get_value(env, 'opt', '-O1') # INIDOC
    INFO('OPTI   : %s' % opti )
    generate_map_file = ''
    if dev_get_value(env, 'mapfile', False): # INIDOC   
        generate_map_file = '-Wl,-Map="mapfile.map"'

    env.Replace(
        PROGNAME = env.GetProjectOption('custom_name', 'APPLICATION') # INIDOC
    )
    env.Append(
        #ASFLAGS=[],
        CPPDEFINES = [
           'F_CPU=' + dev_get_value(env, 'f_cpu', '200000000ul'),
           'EVB=' + env.EVB,
        ],
        CPPPATH = [
            join('$PROJECT_DIR', 'src'),
            join('$PROJECT_DIR', 'include'),
        ],
        CFLAGS = [
            '-std=gnu99',
        ],
        CCFLAGS = [
            opti, # LICENSED COMPILER
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
            '-Wno-unused-but-set-variable',
            '-Wno-missing-field-initializers',
            '-Wno-missing-braces',
            '-Wno-sign-compare',
            '-Wno-comment'
        ],
        CXXFLAGS = [
            #'-std=c++11',
            '-fno-rtti',
            '-fno-exceptions',
            '-fno-use-cxa-atexit',      # __cxa_atexit, __dso_handle
            '-fno-threadsafe-statics',  # __cxa_guard_acquire, __cxa_guard_release
            '-fno-non-call-exceptions',
        ],
        LIBSOURCE_DIRS = [
            join('$PROJECT_DIR', 'lib'),
        ],
        LIBPATH = [
            join(env.xc32_dir, env.category, 'lib', 'proc', env.mcu),
            join('$PROJECT_DIR', 'lib'),
            join(env.framework_dir, 'lib'),
        ],
        LIBS = [ 'm', 'c' ], # 'lega-c'
        LINKFLAGS = [
            '-DXPRJ_default=default',
            '-mprocessor=' + env.mcu,
            '--entry=_reset',            
            '-Wl,--script="p' + env.mcu + '.ld"',
            '-Wl,--defsym=__MPLAB_BUILD=1',
            '-Wl,--defsym=_min_heap_size=%s' % heap,
            '-Wl,--defsym=_min_stack_size=%s' % stack,
            '-Wl,--no-code-in-dinit',
            '-Wl,--no-dinit-in-serial-mem',
            '-Wl,--gc-sections',
            generate_map_file
        ],
        BUILDERS = dict(
            ELF2HEX = Builder(
                action = env.VerboseAction(' '.join([ '$ELFHEX', '$SOURCES', '-a']), 'Creating HEX $TARGET'),
                suffix = '.hex'
            )
        ),
        UPLOADCMD = dev_uploader,
    )

    dev_init_modules(env)

###############################################################################
