# Microchip XC32 PlatformIO
_( The project is a work in progress, there may be bugs... )_

>If you want to help / support or treat me to Coffee  [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)

![pic32mz](https://raw.githubusercontent.com/Wiz-IO/LIB/master/microchip/Arduino-PIC32MZ.jpg)

## [Framework Source Codes](https://github.com/Wiz-IO/framework-XC32)

## Compiler<br>
The Platform use installed Microchip XC32 compiler ( must work on Windows / Linux / Mac )
<br>
* Install XC32 from the Microchip website
* Uploader use **libusb-1.0** https://github.com/libusb/libusb/releases <br>
Put DLL/LIB in PlatformIO Python folder ( .platformio/penv/Scripts )<br>
* Install Platform:<br> **ARDUINO BUILDER IS NOT READY YET**<br>
PlatformIO Home > Platforms > Advanced Installation: paste https://github.com/Wiz-IO/XC32<br>
_Note: be sure [**git**](https://git-scm.com/downloads) is installed_
```ini
custom_xc32 = PATH/Microchip/xc32/vX.XX ; change compiller path
```
* Uploader use "libusb-1.0.dll" https://github.com/libusb/libusb/releases
* * Put DLL in PlatformIO Python folder ( .platformio/penv/Scripts )

**[and read WiKI](https://github.com/Wiz-IO/XC32/wiki)**

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
* etc
* TODO ... CAN, Ethernet, lwip, mbedtls ... etc

## Upload
* ICD 4 / Snap ( integrated, very fast )
* Curiosity PKOB ( integrated )
* "Plan B" - use MPLAB X IPE

## Debug
* stdio printf() or Serial.printf()
* ICD / JTAG - Challenge, but in some other life...


## TODO...
[![DEMO](https://img.youtube.com/vi/salZwXYZfkg/0.jpg)](https://www.youtube.com/watch?v=salZwXYZfkg "DEMO")
![curiosity](https://microchipdeveloper.com/local--files/boards-i:curiosity-pic32mz/PIC32MZ-CURIOSITY.png)

>If you want to help / support or treat me to Coffee  [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
