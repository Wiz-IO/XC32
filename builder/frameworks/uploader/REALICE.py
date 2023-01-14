# Copyright 2023 (c) WizIO ( Georgi Angelov )
#   Reverse Engineering of PIC32MZ Curiosity PKOB

### COMMANDS
cmd_ME2_RUNTIMEWRITE = 1
cmd_GETVOLTAGES = 32
cmd_PRODTESTMODE = 33
cmd_PROGRS = 34
cmd_PROGAP = 35
cmd_PROGFPGA = 36
cmd_INITCOMM = 37
cmd_BIST = 38
cmd_SELF_TESTER = 39
cmd_INITCOMMICD3 = 41
cmd_INITCOMMPK3_2K = 45
cmd_ABORT = 62
cmd_GET_STATUS = 63
cmd_SETDDS = 64
cmd_GETVERSIONS = 65
cmd_SETJAM = 66
cmd_SETPROBES = 69
cmd_SETPMON = 72
cmd_GETVERSIONS2 = 73
cmd_SETOPDESC = 80
cmd_PROGRAMOPDESC = 81
cmd_VERIFYOPDESC = 82
cmd_ERASEOPDESC = 83
cmd_READOPDESC = 84
cmd_BLANKOPDESC = 85
cmd_SETOSCCALOVERRIDE = 87
cmd_GET_LASTERROR = 94
cmd_GET_FAILURES = 95
cmd_MEMOBJ_2_REALICE = 96
cmd_MEMOBJ_2_PC = 97
cmd_SETDMAREADDESC = 98
cmd_SETEMULATORPWR = 99
cmd_SENDDMAWRITE = 100
cmd_REQDMAREADS = 101
cmd_SENDAPPIN = 102
cmd_ONE_TIME_DMA_READ = 103
cmd_SETDYNAMICBPS = 104
cmd_CONNECT2DEVICE = 112
cmd_CONNECT2DEBUG = 113
cmd_RUN = 131
cmd_SINGLESTEP = 132
cmd_RESET = 133
cmd_GETPC = 134
cmd_SETPC = 135
cmd_PGM_SINGLE_INSTRUCTION = 137
cmd_PT_DMA_TEST = 144
cmd_SET_TRACEDESCRIPT = 145
cmd_SET_PERIPHERAL_FREEZE = 146
cmd_SET_DEBUG_OPTIONS = 147
cmd_PROGPMON = 149
cmd_STACK_SNAPSHOT_TAKE_HT = 153
cmd_SENDSINGLE_CFG = 158
cmd_SETBRACKET = 160
cmd_QUERY_PGM_2_GO = 161
cmd_SETUP_PGM_2_GO = 162
cmd_FINAL_PGM_2_GO = 163
cmd_CLEAR_PGM_2_GO = 164

CMD_TEXT = {
    cmd_ME2_RUNTIMEWRITE            : 'ME2_RUNTIMEWRITE',
    cmd_GETVOLTAGES                 : 'GETVOLTAGES',
    cmd_PRODTESTMODE                : 'PRODTESTMODE',
    cmd_PROGRS                      : 'PROGRS',
    cmd_PROGAP                      : 'PROGAP',
    cmd_PROGFPGA                    : 'PROGFPGA',
    cmd_INITCOMM                    : 'INITCOMM',
    cmd_BIST                        : 'BIST',
    cmd_SELF_TESTER                 : 'SELF_TESTER',
    cmd_INITCOMMICD3                : 'INITCOMMICD3',
    cmd_INITCOMMPK3_2K              : 'INITCOMMPK3_2K',
    cmd_ABORT                       : 'ABORT',
    cmd_GET_STATUS                  : 'GET_STATUS',
    cmd_SETDDS                      : 'SETDDS',
    cmd_GETVERSIONS                 : 'GETVERSIONS',
    cmd_SETJAM                      : 'SETJAM',
    cmd_SETPROBES                   : 'SETPROBES',
    cmd_SETPMON                     : 'SETPMON',
    cmd_GETVERSIONS2                : 'GETVERSIONS2',
    cmd_SETOPDESC                   : 'SETOPDESC',
    cmd_PROGRAMOPDESC               : 'PROGRAMOPDESC',
    cmd_VERIFYOPDESC                : 'VERIFYOPDESC',
    cmd_ERASEOPDESC                 : 'ERASEOPDESC',
    cmd_READOPDESC                  : 'READOPDESC',
    cmd_BLANKOPDESC                 : 'BLANKOPDESC',
    cmd_SETOSCCALOVERRIDE           : 'SETOSCCALOVERRIDE',
    cmd_GET_LASTERROR               : 'GET_LASTERROR',
    cmd_GET_FAILURES                : 'GET_FAILURES',
    cmd_MEMOBJ_2_REALICE            : 'MEMOBJ_2_REALICE',
    cmd_MEMOBJ_2_PC                 : 'MEMOBJ_2_PC',
    cmd_SETDMAREADDESC              : 'SETDMAREADDESC',
    cmd_SETEMULATORPWR              : 'SETEMULATORPWR',
    cmd_SENDDMAWRITE                : 'SENDDMAWRITE',
    cmd_REQDMAREADS                 : 'REQDMAREADS',
    cmd_SENDAPPIN                   : 'SENDAPPIN',
    cmd_ONE_TIME_DMA_READ           : 'ONE_TIME_DMA_READ',
    cmd_SETDYNAMICBPS               : 'SETDYNAMICBPS',
    cmd_CONNECT2DEVICE              : 'CONNECT2DEVICE',
    cmd_CONNECT2DEBUG               : 'CONNECT2DEBUG',
    cmd_RUN                         : 'RUN',
    cmd_SINGLESTEP                  : 'SINGLESTEP',
    cmd_RESET                       : 'RESET',
    cmd_GETPC                       : 'GETPC',
    cmd_SETPC                       : 'SETPC',
    cmd_PGM_SINGLE_INSTRUCTION      : 'PGM_SINGLE_INSTRUCTION',
    cmd_PT_DMA_TEST                 : 'PT_DMA_TEST',
    cmd_SET_TRACEDESCRIPT           : 'SET_TRACEDESCRIPT',
    cmd_SET_PERIPHERAL_FREEZE       : 'SET_PERIPHERAL_FREEZE',
    cmd_SET_DEBUG_OPTIONS           : 'SET_DEBUG_OPTIONS',
    cmd_PROGPMON                    : 'PROGPMON',
    cmd_STACK_SNAPSHOT_TAKE_HT      : 'STACK_SNAPSHOT_TAKE_HT',
    cmd_SENDSINGLE_CFG              : 'SENDSINGLE_CFG',
    cmd_SETBRACKET                  : 'SETBRACKET',
    cmd_QUERY_PGM_2_GO              : 'QUERY_PGM_2_GO',
    cmd_SETUP_PGM_2_GO              : 'SETUP_PGM_2_GO',
    cmd_FINAL_PGM_2_GO              : 'FINAL_PGM_2_GO',
    cmd_CLEAR_PGM_2_GO              : 'CLEAR_PGM_2_GO',    
}

def get_cmd_txt(cmd): 
    return CMD_TEXT[cmd]

### POWER BITS
bitEMULATOR_POWER   = 1
bitPOWER_STAY_ON    = 2
bitMCLRHOLD         = 4
bitP24FHVEntry      = 8
bitLVP_TMOD         = 16

### REGIONS
cregion_PgmMem = 1
cregion_DataMem = 2
cregion_Ids = 3
cregion_Cfgs = 4
cregion_Test = 5
cregion_DebugExec = 7
cregion_PgmExec = 8
cregion_OscCal = 9
cregion_RAM = 12
cregion_REG = 13
cregion_BtCfg = 15
cregion_FREEZE_RAM = 16
cregion_FREEZE_EMU = 17
cregion_NMMR = 31
cregion_AUX = 20
cregion_AltBootMemory = 21
cregion_Boot1Memory = 22
cregion_Boot2Memory = 23
cregion_AltConfigMemory = 24
cregion_Boot1ConfigMemory = 25
cregion_Boot1AltConfigMemory = 26
cregion_Boot2ConfigMemory = 27
cregion_Boot2AltConfigMemory = 28
cregion_LowerBootAliasLastPage = 29
cregion_Boot1LastPage = 30
cregion_Boot2LastPage = 33
cregion_FBOOT = 48

### OP REGION MASK
RegionProgramMemory = 1
RegionDataMemory = 2
RegionIDMemory = 4
RegionCfgMemory = 8
RegionTestMemory = 16
RegionCalMemory = 32
RegionPgmExecutive = 64
RegionDbgExecutive = 128
RegionBootConfig = 256
RegionAuxMemory = 512
RegionAltBootMemory = 1024
RegionBoot1Memory = 2048
RegionBoot2Memory = 4096
RegionAltConfigMemory = 8192
RegionBoot1ConfigMemory = 16384
RegionBoot1AltConfigMemory = 32768
RegionBoot2ConfigMemory = 65536
RegionBoot2AltConfigMemory = 131072
RegionFBOOT = 262144
RegionProgramMemory2 = 16777216
RegionCfgMemory2 = 8388608
RegionLowerBootAliasLastPage = 524288
RegionAltBootMemoryLastPage = 4194304
RegionBoot1MemoryLastPage = 1048576
RegionBoot2MemoryLastPage = 2097152