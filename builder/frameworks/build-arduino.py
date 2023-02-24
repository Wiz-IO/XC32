# Copyright 2023 WizIO ( Georgi Angelov )

from os.path import join
from SCons.Script import DefaultEnvironment
from common import dev_init_compiler, dev_ini_add
from modules import dev_init_modules

def template(env):
    dir = join( env.subst('$PROJECT_DIR'), 'src' )
    open( join(dir, 'main.cpp'), 'w').write('''#include <Arduino.h>

void setup()
{
    pinMode(LED, OUTPUT);
}

void loop()
{
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
}
''')
    dev_ini_add(env, '''
;custom_xc32 = C:/Program Files/Microchip/xc32/vX.XX
;custom_heap = 10000
;custom_stack = 1000
;monitor_port = COM26
;monitor_speed = 115200
;build_flags =
;custom_module = $MODULES/common/md-freertos.py
''' )

env = DefaultEnvironment()
core = env.BoardConfig().get('build.core')
variant = env.BoardConfig().get('build.variant')
dev_init_compiler(env, template)

env.Append(
    CPPDEFINES = [ 'ARDUINO=200' ],
    CPPPATH = [
        join(env.framework_dir, 'arduino', 'api'),
        join(env.framework_dir, 'arduino', 'cores', core),
        join(env.framework_dir, 'arduino', 'variants', variant),
        join(env.framework_dir, 'include'),
        join(env.framework_dir, 'src', 'SYS_Cache'),
        join(env.framework_dir, 'src', 'SYS_Timers'),
    ],
    LIBSOURCE_DIRS = [ join(env.framework_dir, 'arduino', "libraries", core) ],
    LIBPATH        = [ join(env.framework_dir, 'arduino', "libraries", core) ],
)

env.BuildSources(
    join('$BUILD_DIR', 'arduino', 'api'),
    join(env.framework_dir, 'arduino', 'api'),
)

env.BuildSources(
    join('$BUILD_DIR', 'arduino', 'core'),
    join(env.framework_dir, 'arduino', 'cores', core),
)

env.BuildSources(
    join('$BUILD_DIR', 'arduino', 'variant'),
    join(env.framework_dir, 'arduino', 'variants', variant),
)

env.BuildSources(
    join('$BUILD_DIR', 'SYS'),
    join(env.framework_dir, 'src'),
    [ '-<*>', '+<SYS_Cache>', '+<SYS_Timers>' ]
)

dev_init_modules(env)

###############################################################################
