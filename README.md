# Microchip XC32 PlatformIO
_( The project is a work in progress, there may be bugs... )_

>If you want to help / support or treat me to Coffee  [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)

![pic32mz](https://raw.githubusercontent.com/Wiz-IO/LIB/master/microchip/Arduino-PIC32MZ.jpg)

## Compiler<br>
The Platform use **installed Microchip XC32 compiler** ( must work on Windows / Linux / Mac )
<br>
* [Install XC32](https://github.com/Wiz-IO/XC32/wiki#compiler) from the Microchip website
* Uploader use [libusb-1.0](https://github.com/libusb/libusb/releases)<br>
Download & Put DLL/LIB in PlatformIO Python folder ( .platformio/penv/Scripts )<br>
* **Install Platform**<br> **ARDUINO BUILDER IS NOT READY YET**<br>
PlatformIO Home > Platforms > Advanced Installation: paste https://github.com/Wiz-IO/XC32<br>
_Note: be sure [**git**](https://git-scm.com/downloads) is installed_

## [and Read Wiki](https://github.com/Wiz-IO/XC32/wiki)

## Boards
* Curiosity v1.0
* **Looking for Hardware cooperation**

## Baremetal
* XC32 - NO Harmony !!!

## Arduino
* Arduino API
* Digital & EINT [ all ]
* Analog - ADC & PWM [ board defined ]
* HardwareSerials [ all ]
* SoftwareSerial [ 4 ]
* USBSerial [ 1 ]
* SPI [ all ]
* I2C [ all ] / Wire
* FreeRTOS mode
* TODO ... CAN, Ethernet, lwip, mbedtls ... etc

## Upload
* [ICD 4 / Snap ( integrated, very fast )](https://github.com/Wiz-IO/XC32/wiki#uploader)
* Curiosity PKOB ( integrated )
* [Microsoft UF2 ( USB MSD )](https://github.com/Wiz-IO/examples-XC32/tree/main/PIC32MZ-EFM-UF2)
* "Plan B" - use MPLAB X IPE


## Debug
* printf() or Serial.printf()
* ICD / JTAG - Challenge, but in some other life...

## [Examples](https://github.com/Wiz-IO/examples-XC32)
## [Framework Source Codes](https://github.com/Wiz-IO/framework-XC32)

[![DEMO](https://img.youtube.com/vi/salZwXYZfkg/0.jpg)](https://www.youtube.com/watch?v=salZwXYZfkg "DEMO")

## Licensing, Credits, Information used

* [PlatformIO - Apache License 2.0](https://github.com/platformio/platformio-vscode-ide/blob/develop/LICENSE)
* [Microchip XC32](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers/licenses)
* [Arduino Core API - GNU](https://github.com/arduino/ArduinoCore-API)
* [SbySpasov PLIB MZ - GNU](https://github.com/SbySpasov/PLIB_MZ/blob/master/license.txt)
* [FreeRTOS - MIT](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/LICENSE.md)
* [lwIP - BSD](https://github.com/lwip-tcpip/lwip/blob/master/COPYING)
* [lvgl - MIT](https://github.com/lvgl/lvgl/blob/master/LICENCE.txt)
* [PIC32 for the hobbyist](https://aidanmocke.com/about/)

![curiosity](https://microchipdeveloper.com/local--files/boards-i:curiosity-pic32mz/PIC32MZ-CURIOSITY.png)

>If you want to help / support or treat me to Coffee  [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
