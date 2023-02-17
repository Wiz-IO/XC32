# Copyright 2023 WizIO ( Georgi Angelov )

import sys, time, click, inspect

PLATFORM_NAME  = 'XC32'
FRAMEWORK_NAME = 'framework-' + PLATFORM_NAME

MODE_INSTALL    = 0
MODE_INTEGRATE  = 1

def LOG(txt = ''):
    pass

def ERROR(txt = ''):
    txt = '%s() %s' % (inspect.stack()[1][3], txt)
    click.secho( '[ERROR] %s \n' % txt, fg='red') 
    time.sleep(.1)
    sys.exit(-1)

def INFO(txt): 
    click.secho( '   %s' % (txt), fg='blue') # BUG: Windows: 4 same chars
