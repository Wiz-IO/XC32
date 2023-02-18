# Copyright 2023 WizIO ( Georgi Angelov )

from os.path import join
from SCons.Script import DefaultEnvironment
from common import dev_init_compiler, dev_ini_add
from modules import dev_init_modules

def template(env):
    dir = join( env.subst('$PROJECT_DIR'), 'src' )
    open( join(dir, 'main.c'), 'w').write('''
/* Basic template: Curiosity Blink */

#include <xc.h>
#define LED 4

void Delay(unsigned int ticks)
{
    unsigned int start = _CP0_GET_COUNT();
    while ((unsigned int)(_CP0_GET_COUNT() - start) < ticks)
        continue;
}

int main(void)
{
    ANSELECLR = 1 << LED;
    TRISECLR = 1 << LED;
    while (1)
    {
        LATEINV = 1 << LED;
        Delay(10000000);
    }
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
dev_init_compiler(env, template)

env.Append(
    CPPPATH = [
        join(env.framework_dir, 'include'),
        join(env.framework_dir, 'src', 'SYS_Cache'),
    ],
)

env.BuildSources(
    join('$BUILD_DIR', 'SYS', 'Cache'),
    join(env.framework_dir, 'src', 'SYS_Cache')
)

dev_init_modules(env)

###############################################################################
