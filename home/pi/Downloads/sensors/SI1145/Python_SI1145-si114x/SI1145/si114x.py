#!/usr/bin/python


# Author: Joe Gutting
# With use of Adafruit SI1145 library for Arduino, Adafruit_GPIO.I2C & BMP Library by Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# Modified by Khill NX7H



# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import time

import Adafruit_GPIO.I2C as I2C

# COMMANDS
PARAM_QUERY                      = 0x80
PARAM_SET                        = 0xA0
NOP                              = 0x0
RESET                            = 0x01
BUSADDR                          = 0x02
PS_FORCE                         = 0x05
ALS_FORCE                        = 0x06
PSALS_FORCE                      = 0x07
PS_PAUSE                         = 0x09
ALS_PAUSE                        = 0x0A
PSALS_PAUSE                      = 0xB
PS_AUTO                          = 0x0D
ALS_AUTO                         = 0x0E
PSALS_AUTO                       = 0x0F
GET_CAL                          = 0x12

# Parameters
PARAM_I2CADDR                    = 0x00
PARAM_CHLIST                     = 0x01
PARAM_CHLIST_ENUV                = 0x80
PARAM_CHLIST_ENAUX               = 0x40
PARAM_CHLIST_ENALSIR             = 0x20
PARAM_CHLIST_ENALSVIS            = 0x10
PARAM_CHLIST_ENPS1               = 0x01
PARAM_CHLIST_ENPS2               = 0x02
PARAM_CHLIST_ENPS3               = 0x04

PARAM_PSLED12SEL                 = 0x02
PARAM_PSLED12SEL_PS2NONE         = 0x00
PARAM_PSLED12SEL_PS2LED1         = 0x10
PARAM_PSLED12SEL_PS2LED2         = 0x20
PARAM_PSLED12SEL_PS2LED3         = 0x40
PARAM_PSLED12SEL_PS1NONE         = 0x00
PARAM_PSLED12SEL_PS1LED1         = 0x01
PARAM_PSLED12SEL_PS1LED2         = 0x02
PARAM_PSLED12SEL_PS1LED3         = 0x04
PARAM_PSLED3SEL                  = 0x03

PARAM_PSENCODE                   = 0x05  #defaults to MSB=0
PARAM_ALSENCODE                  = 0x06  #defaults to MSB=0

PARAM_PS1ADCMUX                  = 0x07
PARAM_PS2ADCMUX                  = 0x08
PARAM_PS3ADCMUX                  = 0x09

PARAM_PSADCOUNTER                = 0x0A
PARAM_PSADCGAIN                  = 0x0B
PARAM_PSADCMISC                  = 0x0C

PARAM_PSADCMISC_PSMODE_PROX      = 0x04
PARAM_PSADCMISC_PSMODE_RAW       = 0x00


PARAM_ALSIRADCMUX                = 0x0E
PARAM_AUXADCMUX                  = 0x0F

PARAM_ALSVISADCOUNTER            = 0x10
PARAM_ALSVISADCGAIN              = 0x11
PARAM_ALSVISADCMISC              = 0x12

PARAM_ALSIRADCOUNTER             = 0x1D
PARAM_ALSIRADCGAIN               = 0x1E
PARAM_ALSIRADCMISC               = 0x1F

PARAM_ADCCOUNTER_511CLK          = 0x70

PARAM_ADCMUX_SMALLIR             = 0x00
PARAM_ADCMUX_VIS                 = 0x02
PARAM_ADCMUX_LARGEIR             = 0x03
PARAM_ADCMUX_NO_DIODE            = 0x06
PARAM_ADCMUX_GRD_VOLT            = 0x25
PARAM_ADCMUX_TEMP                = 0x65
PARAM_ADCMUX_VDD                 = 0x75
PARAM_CHLIST_ENUV
PARAM_ADCMISC_RANGE_NORM         = 0x00
PARAM_ADCMISC_RANGE_HI           = 0x20



# REGISTERS
REG_PARTID                       = 0x00
REG_REVID                        = 0x01
REG_SEQID                        = 0x02

REG_INTCFG                       = 0x03
REG_INTCFG_INTOE                 = 0x01
REG_INTCFG_INTMODE               = 0x02

REG_IRQEN                        = 0x04
REG_IRQEN_ALSEVERYSAMPLE         = 0x01
REG_IRQEN_PS1EVERYSAMPLE         = 0x04
REG_IRQEN_PS2EVERYSAMPLE         = 0x08
REG_IRQEN_PS3EVERYSAMPLE         = 0x10


REG_IRQMODE1                     = 0x05  # not documented in data sheets
REG_IRQMODE2                     = 0x06  # not documented in data sheets

REG_HWKEY                        = 0x07
REG_MEASRATE0                    = 0x08
REG_MEASRATE1                    = 0x09
REG_PSRATE                       = 0x0A
REG_PSLED21                      = 0x0F
REG_PSLED3                       = 0x10
REG_UCOEFF0                      = 0x13
REG_UCOEFF1                      = 0x14
REG_UCOEFF2                      = 0x15
REG_UCOEFF3                      = 0x16
REG_PARAMWR                      = 0x17
REG_COMMAND                      = 0x18
REG_RESPONSE                     = 0x20
REG_IRQSTAT                      = 0x21
REG_IRQSTAT_ALS                  = 0x01

REG_ALSVISDATA0                  = 0x22
REG_ALSVISDATA1                  = 0x23
REG_ALSIRDATA0                   = 0x24
REG_ALSIRDATA1                   = 0x25
REG_PS1DATA0                     = 0x26
REG_PS1DATA1                     = 0x27
REG_PS2DATA0                     = 0x28
REG_PS2DATA1                     = 0x29
REG_PS3DATA0                     = 0x2A
REG_PS3DATA1                     = 0x2B
REG_UVINDEX0                     = 0x2C
REG_UVINDEX1                     = 0x2D
REG_PARAMRD                      = 0x2E
REG_CHIPSTAT                     = 0x30

# I2C Address
SI1145_ADDR                             = 0x60

# Class creates SI114X instance
class SI114X(object):
        def __init__(self, address=SI1145_ADDR, busnum=I2C.get_default_bus()):
                ''' (default [I2C address of SI1145=0x60], [I2C bus number])
                intitalizes to default mode (UV,Vis,IR and Prox 1)
                enables all interupts and starts in autonomous mode'''

                self._logger = logging.getLogger('SI1145')

                # Create I2C device.
                self._device = I2C.Device(address, busnum)

                #reset device
                self._reset()

                # Load calibration values, default settings, enables interupts
                # and starts in autonomous mode.
                self._load_setup()

        # device reset
        def _reset(self):
                ''' zeros measurement rate, turns off interupts, sends
                 SI114x software reset command and writes hardware key'''
                
                self._device.write8(REG_MEASRATE0, 0)
                self._device.write8(REG_MEASRATE1, 0)
                self._device.write8(REG_IRQEN, 0)
                self._device.write8(REG_IRQMODE1, 0) #not documented in data sheet
                self._device.write8(REG_IRQMODE2, 0) #not documented in data sheet
                self._device.write8(REG_INTCFG, 0)
                self._device.write8(REG_IRQSTAT, 0xFF)

                self._device.write8(REG_COMMAND, RESET)
                time.sleep(.01)
                self._device.write8(REG_HWKEY, 0x17)
                time.sleep(.01)

        # write Param
        def writeParam(self, p, v):
                '''writes value to the parameter memory and verifies value is written

                (parameter, value)
                '''

                ''' Returns Parameter written '''
                
                self._device.write8(REG_PARAMWR, v)
                self._device.write8(REG_COMMAND, p | PARAM_SET)
                paramVal = self._device.readU8(REG_PARAMRD)
                return paramVal

        # read Param
        def readParam(self,p):
                '''(parameter) returns value of parameter, no decoding'''
                
                self._device.write8(REG_COMMAND, p | PARAM_QUERY)
                paramVal = self._device.readU8(REG_PARAMRD)
                return paramVal

        def _load_setup(self):
                '''# loads UV calibration coeficients, enables all interupts,
                sets default measurement parameters and start in autonomous mode'''
                
                # /***********************************/
                # Enable UVindex measurement coefficients!
                self._device.write8(REG_UCOEFF0, 0x29)
                self._device.write8(REG_UCOEFF1, 0x89)
                self._device.write8(REG_UCOEFF2, 0x02)
                self._device.write8(REG_UCOEFF3, 0x00)

                # Enable all sensors including UV sensor
                self.writeParam(PARAM_CHLIST, PARAM_CHLIST_ENUV |
                                PARAM_CHLIST_ENALSIR | PARAM_CHLIST_ENALSVIS
                                | PARAM_CHLIST_ENPS1)

                # Enable interrupt on every sample
                self._device.write8(REG_INTCFG, REG_INTCFG_INTOE)
                self._device.write8(REG_IRQEN, REG_IRQEN_ALSEVERYSAMPLE)

                # /****************************** Prox Sensor 1 */

                # Program LED current
                self._device.write8(REG_PSLED21, 0x03) # 20mA for LED 1 only for SI1145
                self.writeParam(PARAM_PS1ADCMUX, PARAM_ADCMUX_LARGEIR)

                # Prox sensor #1 uses LED #1
                self.writeParam(PARAM_PSLED12SEL, PARAM_PSLED12SEL_PS1LED1)

                # Fastest clocks, clock div 1 (integraton time)
                self.writeParam(PARAM_PSADCGAIN, 0)

                # Take 511 clocks to recover
                self.writeParam(PARAM_PSADCOUNTER, PARAM_ADCCOUNTER_511CLK)

                # in prox mode, high range
                self.writeParam(PARAM_PSADCMISC, PARAM_ADCMISC_RANGE_HI |
                                PARAM_PSADCMISC_PSMODE_PROX)
                
                # /****************************** IR Sensor */
                self.writeParam(PARAM_ALSIRADCMUX, PARAM_ADCMUX_SMALLIR)

                # Fastest clocks, clock div 1 (integration time)
                self.writeParam(PARAM_ALSIRADCGAIN, 0)

                # Take 511 clocks to recover 
                self.writeParam(PARAM_ALSIRADCOUNTER, PARAM_ADCCOUNTER_511CLK)

                # in high range mode
                self.writeParam(PARAM_ALSIRADCMISC, PARAM_ADCMISC_RANGE_HI)

                # /****************************** Visible Sensor */

                # fastest clocks, clock div 1 (integration time)
                self.writeParam(PARAM_ALSVISADCGAIN, 0)

                # Take 511 clocks to recover
                self.writeParam(PARAM_ALSVISADCOUNTER, PARAM_ADCCOUNTER_511CLK)

                # in high signal range mode divides gain by 14.5
                self.writeParam(PARAM_ALSVISADCMISC, PARAM_ADCMISC_RANGE_HI)


                # measurement rate for auto
                self._device.write8(REG_MEASRATE0, 0xFF) # 255 * 31.25 uS = 7.9 ms

                # auto run
                self._device.write8(REG_COMMAND, PSALS_AUTO)

        # returns the UV index * 100 (divide by 100 to get the index)
        def readUV(self):
                return self._device.readU16LE(0x2C)

        #returns visible + IR light levels
        def readVisible(self): # 256 added to counts to prevent - counts
                return self._device.readU16LE(0x22)

        #returns IR light levels
        def readIR(self): # 256 added to counts to prevent - counts
                return self._device.readU16LE(0x24)

        # Returns "Proximity" - assumes an IR LED is attached to LED
        def readProx(self):
                return self._device.readU16LE(0x26)

