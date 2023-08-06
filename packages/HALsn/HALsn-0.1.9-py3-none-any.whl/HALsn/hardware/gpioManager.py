#!/usr/bin/env python3

'''
MIT License

Copyright (c) 2021 Mikhail Hyde & Cole Crescas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import RPi.GPIO as iO
import time

class gpioManager():

    def __init__(self, ledPins, buttonPins):
        
        iO.setmode(iO.BOARD)
        iO.setwarnings(False)

        self.ledPins    = ledPins
        self.buttonPins = buttonPins

        self._set_outputs()
        self._set_inputs()
        
        for pin in self.ledPins:
            iO.output(pin, iO.LOW)

    def _set_outputs(self):
        '''
        Configures list of pins as outputs
        '''
        for pin in self.ledPins:
            iO.setup(pin, iO.OUT)

    def _set_inputs(self):
        '''
        Configures list of pins as inputs
        '''
        for pin in self.buttonPins:
            iO.setup(pin, iO.IN)

    def controlLED(self, pin, state):
        '''
        Activates RED LED...Indicates Engineer needs to
        Resolve Issue
        '''
        if state == 0:
            iO.output(pin, iO.LOW)
        if state == 1:
            iO.output(pin, iO.HIGH)

    def buttonHold(self, pin):
        '''
        Monitors Push Button. Passes/Proceeds when button
        is pushed.
        '''
        while not iO.input(pin):
            time.sleep(0.05)
            pass
        
    def clean(self):
        '''
        Calls GPIO.cleanup() function
        '''
        iO.cleanup()
