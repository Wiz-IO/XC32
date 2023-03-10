# Copyright 2023 WizIO ( Georgi Angelov )

from os.path import join, dirname
from os import listdir
from shutil import copyfile
from SCons.Script import Builder
from wiz import INFO, FRAMEWORK_NAME
import uploader

def dev_uploader(target, source, env):
    p = env.BoardConfig().get('upload.protocol', None)
    p = env.subst("$UPLOAD_PROTOCOL") or env.BoardConfig().get('upload.protocol', None)
    if p == 'CURIOSITY':
        from uploader.CURIOSITY import upload
        uploader.CURIOSITY.upload(target, source, env)
    elif p == 'GEN4':
        from uploader.GEN4 import upload
        uploader.GEN4.upload(target, source, env)
    elif p == 'UF2':
        from uploader.UF2 import upload
        uploader.UF2.upload(target, source, env)        

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
        open( join(env.subst('$PROJECT_DIR'), 'include', 'user_config.h'), 'w').write('''#pragma once
#ifdef __cplusplus
extern "C"
{
#endif



#ifdef __cplusplus
}
#endif
''')

def dev_get_value(env, name, default):
    return env.GetProjectOption('custom_%s' % name, # ini user config
           env.BoardConfig().get('build.%s' % name, default) ) # default from board

def dev_init_compiler(env, Template=None):
    env['PLATFORM_DIR' ] = env.platform_dir  = dirname( env['PLATFORM_MANIFEST'] )
    env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir( FRAMEWORK_NAME )
    create_template(env, Template)

    INFO('XC32   : %s' % env.xc32_ver)
    if 'Arduino' in env['PIOFRAMEWORK']:
        INFO('CORE   : %s' % env.BoardConfig().get('build.core') )

    env.category = env.BoardConfig().get('build.category')
    env.mcu     = env.BoardConfig().get('build.mcu')
    INFO('CHIP   : PIC%s' % env.mcu )
    stack = dev_get_value(env, 'stack', '1024') # INIDOC
    INFO('STACK  : %s' % stack )
    heap = dev_get_value(env, 'heap', '65536') # INIDOC
    INFO('HEAP   : %s' % heap )
    linker = dev_get_value(env, 'linker', 'p' + env.mcu + '.ld') # INIDOC
    INFO('LINK   : %s' % linker )    
    opti = dev_get_value(env, 'opt', '-O1') # INIDOC
    INFO('OPTI   : %s' % opti )
    generate_map_file = ''
    if dev_get_value(env, 'mapfile', False): # INIDOC
        generate_map_file = '-Wl,-Map="mapfile.map"'

    env.Replace(
        PROGNAME = env.GetProjectOption('custom_name', 'APPLICATION') # INIDOC
    )
    env.Append(
        ASFLAGS=[  '-mhard-float' ],
        CPPDEFINES = [
           'F_CPU=' + dev_get_value(env, 'f_cpu', '200000000ul'),
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
            '-Wno-comment',
        ],
        CXXFLAGS = [
            #'-std=c++14',
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
        LIBS = [ 'm' ], # 'lega-c'
        LINKFLAGS = [
            '-DXPRJ_default=default',
            '-mprocessor=' + env.mcu,
            '--entry=_reset',
            '-Wl,--script="%s"' % linker,
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

###############################################################################
