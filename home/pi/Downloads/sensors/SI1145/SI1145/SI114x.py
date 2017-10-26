#!/usr/bin/python
#
# by Khill NX7H


# based on the work of Joe Gutting
# With use of Adafruit SI1145 library for Arduino, Adafruit_GPIO.I2C & BMP Library by Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:




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
import si114x, time

class SI1145(si114x.SI114X):

        # Parameter register for the Gain setting for the channels
        channelD= { 'Vis' : si114x.PARAM_ALSVISADCGAIN,
                   'IR'  : si114x.PARAM_ALSIRADCGAIN,
                   'PS1' : si114x.PARAM_PSADCGAIN}

        def writeGain(self, chan, gain=0, rng= 0, rec_period = -1, align = 0):
                ''' sets gain (integration time), recovery time, sensitivity
                range and encoding alignment for selected channel

                (channel, gain, range, recovery time, alignment)
                
                defaults: gain 1x, range Normal Signal, Rec_period 511 clocks, align MSB
                recovery period is automatically set to 2 ** 1's complement of
                gain if not set explicitly. If range set for High signal rec is set
                to 1 clock
                returns (gain, range, recovery period, align) '''

                
                if chan == 'PS1': #TODO prox align values not encoded
                        align = self.writeParam(si114x.PARAM_PSENCODE, align) 
                elif chan == 'Vis':
                        x = self.readParam(si114x.PARAM_ALSENCODE) & 0b100000 # preserve IR align
                        align <<= 4
                        align |= x
                        align = (self.writeParam(si114x.PARAM_ALSENCODE, align)
                                & 0b10000) >> 4 # decode written value
                elif chan == 'IR':
                        x = self.readParam(si114x.PARAM_ALSENCODE) & 0b10000 # preserve Vis align
                        align <<= 5
                        align |= x
                        align = (self.writeParam(si114x.PARAM_ALSENCODE, align)
                                 & 0b100000) >> 5
                else: print("Gain for Channel %s cannot be set" % chan); return # error
                        
                chan = self.channelD[chan]
                # write 'gain' its actually setting the integration time by dividing
                # the clock by 2 ** gain
                gain = self.writeParam(chan, gain & 0b111)
                
                # recovery period
                if rng : rec_period = 0 # per data sheet if using  high signal range rec = 0
                else:
                        if rec_period < 0:
                                rec_period = 0b111 ^ gain # 1s compliment of gain
                # writing the 1's compliment to the ADC_Counter         
                rec_period = (self.writeParam(chan -1, (rec_period & 0b111) << 4) & 0x70) >> 4

                # bit 5  of  misc param. sets signal range.  0 is normal, 1 is High signal range, gain
                # is divided by 14.5 which is useful for high light operation like direct sunlight
                x = self.readParam(chan +1) # get current value
                x &=  ~si114x.PARAM_ADCMISC_RANGE_HI # sets the bits to zero
                # set or reset range bit
                rng = (self.writeParam(chan + 1, (rng << 5) | x ) & 0x20) >> 5 
                
                return gain, rng, rec_period, align 

        
        def readGain(self,chan):
                ''' read gain parameters

                returns a tuple (gain, rng, rec_period, align)
                the PS1 align is not decoded'''
                
                if chan=="PS1" :
                        align = self.readParam(si114x.PARAM_PSENCODE) #contains all 3 ps vals
                elif chan == "Vis" or chan == "IR":
                        align = self.readParam(si114x.PARAM_ALSENCODE)
                        if chan == 'Vis':
                                align = (align & 0x10) >> 4
                        else:
                                align = (align & 0x20) >> 5
                else: print("Gain for Channel %s not defined" % chan); return # error
                
                gain = self.readParam(self.channelD[chan]) & 0b111
                rec_period = (self.readParam(self.channelD[chan]-1) & 0x70) >> 4
                rng = (self.readParam(self.channelD[chan]+1) & 0x20) >> 5
                
                return gain, rng, rec_period, align

        def chan_sel_encode(self, *pargs):
                ''' encode channels for CHLIST'''
                
                channel = 0
                for i in pargs:
                        if i == 'Vis': channel|= si114x.PARAM_CHLIST_ENALSVIS
                        elif i == 'UV' : channel |= si114x.PARAM_CHLIST_ENUV
                        elif i == 'IR' : channel |= si114x.PARAM_CHLIST_ENALSIR
                        elif i == 'Aux' : channel |= si114x.PARAM_CHLIST_ENAUX
                        elif i == 'PS1' : channel |= si114x.PARAM_CHLIST_ENPS1
                        else : print ( "Channel %s not available \n" % i); return
                return channel
        
        # write to CHLIST
        def writeChan_enable(self, *pargs):
                '''Enables the desired channels for use.

                 Expects char values for desired channels.
                 Valid args are 'Vis', 'UV', 'IR', 'Aux' and 'PS1'.
                 Set all values at the same time.
                   
                 Sets default to UV, IR, Vis and PS1 if no parameters sent

                 Returns the value writen to the register'''
                
                if not pargs : return self.writeParam(si114x.PARAM_CHLIST, si114x.PARAM_CHLIST_ENUV |
                                si114x.PARAM_CHLIST_ENALSIR | si114x.PARAM_CHLIST_ENALSVIS
                                | si114x.PARAM_CHLIST_ENPS1)

                channel = self.chan_sel_encode(*pargs)
                if not channel : return # error
                       
                return self.writeParam(si114x.PARAM_CHLIST, channel)

        # read Chlist channels enabled not decoded
        def readChan_enable(self):return self.readParam(si114x.PARAM_CHLIST)

        def decodeCHLIST(self):
                '''decodeCHLIST()
                returns a list of the channels currently enabled'''
                
                _chan =  self.readChan_enable()
                chanlist = []
                if _chan & si114x.PARAM_CHLIST_ENALSVIS: chanlist.append('Vis')
                if _chan & si114x.PARAM_CHLIST_ENALSIR : chanlist.append('IR')
                if _chan & si114x.PARAM_CHLIST_ENUV: chanlist.append('UV')
                if _chan & si114x.PARAM_CHLIST_ENAUX : chanlist.append('Aux')
                if _chan & si114x.PARAM_CHLIST_ENPS1 : chanlist.append('PS1')
                if _chan & si114x.PARAM_CHLIST_ENPS2 : chanlist.append('PS2')
                if _chan & si114x.PARAM_CHLIST_ENPS3 : chanlist.append('PS3')
                return chanlist
        
                
        # Returns 8 bit unsigned value of the requested register
        def readReg(self, reg): return self._device.readU8(reg)

        def writeReg(self, reg, val) :
                '''writes 8 bit value to register

                (register, unsigned value)
                Verifies write and returns value writen to register'''
                
                ## print ("previous setting reg 0x%02x val 0x%02x " %
                ##      (reg, self._device.readU8(reg)))
                self._device.write8(reg, val)
                return self._device.readU8(reg)

        def writeMeasRate(self, rate = 0xff):
                '''set time for next measurement

                (rate)  sets measuring rate.
                Value is multilplied by 31.25 uS
                default to 0xff * 31.25 uS = 7.968 mS'''

                '''returns rate written'''
                
                self._device.write16(si114x.REG_MEASRATE0, rate)
                return self._device.readU16LE(si114x.REG_MEASRATE0)
        
        # read Measuring rate. Value * 31.25 uS = measuremnt interval
        def readMeasRate(self): return self._device.readU16LE(si114x.REG_MEASRATE0)
  
        def readResponse(self) : 
                '''Returns value in response register.

                This register is set in response to a write to the command
                register or an overflow error in measurements.  If bit 7 is set
                Error status is written in the lower nibble.  If it is not
                set, the lower nibble contains a count of the successfule commands.
                It is cleared by writting a NOOP or Reset command to Command register.'''

                return self.readReg(si114x.REG_RESPONSE)

        def writeCommand(self,command):
                '''Writes command to command register.

                (command)
                 
                User should check and clear response register  before
                sending a series of commands. 

                returns the value in the Response register.'''
                
##                x=self.readResponse()
##                if x : self.writeReg(si114x.REG_COMMAND, si114x.NOP)
                self.writeReg(si114x.REG_COMMAND, command)
                return self.readResponse()
        
        # returns contents of IntCFG and IRQENable register as a tuple
        def readInt_en(self):return self.readReg(si114x.REG_INTCFG), self.readReg(si114x.REG_IRQEN)

        # return Interupt status register
        def readInt_stat(self):return self.readReg(si114x.REG_IRQSTAT)

        def enableInt(self, int_cfg = si114x.REG_INTCFG_INTOE, int_en_ALS = si114x.REG_IRQEN_ALSEVERYSAMPLE,
                       int_en_PS1 = si114x.REG_IRQEN_PS1EVERYSAMPLE):
                '''enables interrupts.  Default: all interrupts.

                (enable interupt pin, enable individual channels)
                both must be set to enable interupt pin to go live

                Returns tuple (Infconfig, int_enable)'''
                
                self.writeReg(si114x.REG_INTCFG, int_cfg)
                self.writeReg(si114x.REG_IRQEN, int_en_ALS | int_en_PS1)
                return self.readInt_en()

        def readSensor(self, chan):
                '''returns the sensor assignment for configurable channels

                Sensor settings:  0x00 Small IR photodiode
                                  0x02 Visible photodiode
                                  0x03 Large IR photodiode
                                  0x06 no photodiode (reference for ambient IR
                                  or visble light)
                                  0x25 Gnd voltage (reference for voltage and temp)
                                  0x65 temperature need to subtract gnd voltage
                                  0x75 Vdd voltage need to subtract gnd voltage

                returns (channel, sensor selected, bool(enabled status))
                '''
                
                if chan == 'PS1' :
                        channel = si114x.PARAM_PS1ADCMUX 
                        mode_enable = (self.readParam(si114x.PARAM_PSADCMISC) & 0b100) and \
                                  (self.readParam(si114x.PARAM_CHLIST) & si114x.PARAM_CHLIST_ENPS1)
                elif chan == "Raw" :
                        channel = si114x.PARAM_PS1ADCMUX
                        mode_enable = not (self.readParam(si114x.PARAM_PSADCMISC) & 0b100) and \
                                  (self.readParam(si114x.PARAM_CHLIST) & si114x.PARAM_CHLIST_ENPS1)
                elif chan == 'Aux' :
                        channel = si114x.PARAM_AUXADCMUX
                        mode_enable = self.readParam(si114x.PARAM_CHLIST) & \
                                      si114x.PARAM_CHLIST_ENAUX  # is aux enabled?
                        
                elif chan == 'IR' :
                        channel = si114x.PARAM_ALSIRADCMUX
                        mode_enable = self.readParam(si114x.PARAM_CHLIST) & \
                                      si114x.PARAM_CHLIST_ENALSIR
                        
                else: print ('error channel %s not supported' % chan); return
                return chan, self.readParam(channel), mode_enable
                                
        # select sensor for the configurable channels
        def selectSensor (self, chan, sensor):
                '''Selects the sensor for the configurable channels.
                No error checking done.  Channel must be enabled seperately.

                (channel, sensor)
                
                Allowable channels: PS1 -- small and large IR                                         
                                    Raw -- all sensors
                                    Aux -- temp and Vdd
                                    IR  -- small and large IR
                                    Raw and PS1 are mutually exclusive

                Sensor settings:  0x00 Small IR photodiode
                                  0x02 Visible photodiode
                                  0x03 Large IR photodiode
                                  0x06 no photodiode (reference for ambient IR or visble light)
                                  0x25 Gnd voltage (reference for voltage and temp)
                                  0x65 temperature need to subtract gnd voltage
                                  0x75 Vdd voltage need to subtract gnd voltage

                returns (channel, sensor setting)'''
                
                if chan == 'PS1':
                        x = self.readParam(si114x.PARAM_PSADCMISC)
                        self.writeParam(si114x.PARAM_PSADCMISC, x |
                                   si114x.PARAM_PSADCMISC_PSMODE_PROX)
                        self.writeParam(si114x.PARAM_PS1ADCMUX, sensor)
                elif chan == 'Raw':
                        x = self.readParam(si114x.PARAM_PSADCMISC) & 0b11111011 # 0 mode bit
                        self.writeParam(si114x.PARAM_PSADCMISC, x)
                        self.writeParam(si114x.PARAM_PS1ADCMUX, sensor)
                elif chan == 'Aux': self.writeParam(si114x.PARAM_AUXADCMUX, sensor)
                elif chan == 'IR': self.writeParam(si114x.PARAM_ALSIRADCMUX, sensor)
                else:  print ('error channel %s not supported' % chan); return
                return self.readSensor(chan)
                
        def setup_led(self, led_current = 0x03, sensor= 3):
                '''sets up LED current and select which sensor to use for proximty
                measurements.  The 1145 only has 1 LED available.

                Defaults to ca. 22 mA.   0 = 0 mA to 0x0f = ca. 359 mA,
                !!!!!Use with caution!!!!!!!

                TODO generalize for 1146 and 47'''

                self._device.write8(si114x.REG_PSLED21, led_current) # 20mA for LED 1 only
                self.selectSensor('PS1', sensor) # large IR sensor
                # Prox sensor #1 uses LED #1
                self.writeParam(si114x.PARAM_PSLED12SEL, si114x.PARAM_PSLED12SEL_PS1LED1)

        # default dark adc count. This should probably be recalibrated with any gain change
        visdark, irdark = 260, 253

        def readDarkCnt(self):
                '''calibrates the dark count

                sets global variables
                returns (visible dark cnt, ir dark cnt)'''

                input ("Cover sensor with opaque cover. Hit any key")
                irdark = visdark = 0
                for i in range (1000):
                        visdark += self.readVisible()
                        irdark += self.readIR()
                        time.sleep(.001)
                SI1145.visdark = int(round(visdark/1000))
                SI1145.irdark = int(round(irdark/1000))
                print ("Visual dark -> %i IR dark %i" % (SI1145.visdark, SI1145.irdark))
                input ("Uncover sensor and hit any key")
                return SI1145.visdark, SI1145.irdark

        def calc_gaincorr(self):
                ''' Calculate gain correction factor based on the gain, range
                and align settings.

                Returns  a dictionary { channel: correctionfactor }
                '''
                
                gaincor = {}
                for chan in self.channelD.keys():
                        gain=self.readGain(chan)
                        gaincor[chan] = (14.25 if gain[1] else 1)/(2 ** gain[0]) / \
                                        (2 if gain[3] else 1)
                return gaincor

        def restart(self,*chans, meas_rate = 0xff, auto = True, int_enable = True):
                ''' restart ([ channel list, measuring rate, autonomous mode, enable interupts])
                defaults to all channels except aux, autonomous and enables interrupts

                Gain is set to normal signal and default gain.  Default sensor selection'''
                
                self._reset()
                if not chans : chans = ('Vis', 'IR', 'UV', 'PS1') # defaults
                while self.writeChan_enable(*chans) != self.chan_sel_encode(*chans): pass

                als_int = PS1_int = int_cfg = 0
                if int_enable :
                        int_cfg = si114x.REG_INTCFG_INTOE
                        if "Vis" in chans or "IR" in chans or "UV" in chans or "Aux" in chans:
                                als_int = si114x.REG_IRQEN_ALSEVERYSAMPLE
                        if "PS1" in chans : PS1_int = si114x.REG_IRQEN_PS1EVERYSAMPLE
                        
                self.enableInt(int_cfg, als_int, PS1_int)

                self.writeMeasRate(meas_rate)
                if "Vis" in chans: self.writeGain("Vis")
                if "IR" in chans: self.writeGain("IR")
                if "PS1" in chans:
                        self.writeGain("PS1")
                        self.setup_led()

                if auto: self.writeCommand(si114x.PSALS_AUTO)
                        
                        
        # coefficient for ALS lux and proximity calculations
        # (cover material : (Visible, IR, scaling prox_850 nm, scaling prox_950 nm, visible light)
        # see page 4 of Silicon labs AN523 Overlay Consideration for the SI114x Sensor
        # other material can be added to table
        lux_coef = {'Ref'       : (5.41, -0.08, 1.0, 1.0, 1.0), # reference no cover material     
                    'AcG'       : (6.33, -0.094, 0.96, 0,96, 0.957), # clear acrylic Glass
                    'PC2405'    : (5.86, -0.089, 0.94, 0.94, 0.935), # polycarbonate Marolon 2405 (clear)
                    'PC2407'    : (6.616, -.101, 0.93, 0.93, 0.914)} # polycarbonate Marolon 2407 (UV stabilized
        
  
        def readLux(self,  coef = lux_coef['Ref'][:2], readdark=False):
                """Returns Lux Calculation

                ( (visible_coefficient, IR_coefficient), read dark count )
                
                Uses first 2 entries from lux_coef dictionary.
                default is reference with no cover.
                Corrected for dark count, gain settings.  Does not check for
                overflow.  Set readdark to true to calculate an average dark count.
                """
                
                if readdark : self.readDarkCnt()  # get dark reading
                                               
##                print(coef)
                vis_coef, ir_coef = coef # unpack coefficients
                corr= self.calc_gaincorr() # get gain correction
                vis_corr, ir_corr = corr['Vis'], corr['IR']
                
        
                lux = vis_coef*(self.readVisible()-self.visdark) * vis_corr +\
                      ir_coef*(self.readIR()-self.irdark) * ir_corr

                return lux

if __name__ == '__main__':
        s=SI1145()
        print('Lux = %.2f' % s.readLux(readdark=True))
        print('UV = %i UV index = %.2f' % (s.readUV(), s.readUV()/100.0))
        print('Channels enabled: %s' % s.decodeCHLIST())
        for i in s.decodeCHLIST(): print('Gain of %s is %s' % (i, s.readGain(i)))
        print('Visible reading = %i' % s.readVisible())
        print('IR = %i' % s.readIR())
        
        print('*------------------------------*')
        print('Changing gain ')
        s.restart('Vis', "IR")
        print('Channels enabled: %s' % s.decodeCHLIST())
        s.writeGain('Vis', gain=4)
        s.writeGain('IR', gain=3)
        s.readDarkCnt()
        print('Lux = %.2f' % s.readLux())
        for i in s.decodeCHLIST(): print('Gain of %s is %s' % (i, s.readGain(i)))
        print('Visible reading = %i' % s.readVisible())
        print('IR = %i' % s.readIR())

##        print('Read Proximity')
##        input("Place hand 5 cm from sensor, then hit any key")              
##        s.writeChan_enable("PS1")
##        print("Channels enanbled: %s" % s.decodeCHLIST())
##        print("Gain of %s is %s" % ("PS1", s.readGain("PS1")))
