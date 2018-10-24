/*
The MIT License (MIT)

Copyright (c) 2016 British Broadcasting Corporation.
This software is provided by Lancaster University by arrangement with the BBC.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
*/

#include "MicroBit.h"
#include "DynamicType.h"
#include "PeridoBridge.h"

MicroBit uBit;

char disp = 'a';

extern const char* SCHOOL_ID;
extern const char* HUB_ID;

PeridoBridge bridge(uBit.radio, uBit.serial, uBit.messageBus, uBit.display);

void change_display()
{
    // disp++;
    // uBit.display.print(disp);
}

void log_string_ch(const char* c)
{
    // uBit.serial.printf("%s ", c);
}

void log_string(char c)
{
    // uBit.serial.printf("%c ", c);
}

void log_num(int c)
{
    // uBit.serial.printf("%d ", c);
}

void blink()
{
    int toggle = 0;
    while(1)
    {
        uBit.display.image.setPixelValue(RUNNING_TOGGLE_PASTE_COLUMN, RUNNING_TOGGLE_PASTE_ROW, toggle);
        toggle = !toggle;
        uBit.sleep(400);
    }
}

int main()
{
    // Initialise the micro:bit runtime.
    uBit.init();
    bridge.enable();
    uBit.radio.enable();

    create_fiber(blink);

    // uBit.display.print(disp);
    // uBit.display.scroll(SCHOOL_ID);
    // uBit.display.scroll(HUB_ID);

    // If main exits, there may still be other fibers running or registered event handlers etc.
    // Simply release this fiber, which will mean we enter the scheduler. Worse case, we then
    // sit in the idle task forever, in a power efficient sleep.
    release_fiber();
}

