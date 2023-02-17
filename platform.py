# Copyright 2023 WizIO ( Georgi Angelov )

from platformio.managers.platform import PlatformBase

class Xc32Platform(PlatformBase):
    def is_embedded(self):
        return True

###############################################################################
