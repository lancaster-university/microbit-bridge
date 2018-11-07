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
// void process_packet(PeridoFrameBuffer*)
// {

// }

// void change_display()
// {
//     // disp++;
//     // uBit.display.print(disp);
// }

// void log_string_ch(const char* c)
// {
//     // uBit.serial.printf("%s\r\n", c);
// }

// void log_string(const char* c)
// {
//     // uBit.serial.printf("%c ", c);
// }

// void log_ptr(uint8_t* ptr)
// {
//     // uBit.serial.printf("%p\r\n", ptr);
// }

// void log_num(int c)
// {
//     // uBit.serial.printf("%d\r\n", c);
// }

// void set_gpio0(int val)
// {
//     uBit.io.P0.setDigitalValue(val);
// }

// void set_gpio1(int val)
// {
//     uBit.io.P1.setDigitalValue(val);
// }

// void set_gpio2(int val)
// {
//     uBit.io.P2.setDigitalValue(val);
// }

// void set_gpio3(int val)
// {
//     uBit.io.P8.setDigitalValue(val);
// }

// void set_gpio4(int val)
// {
//     uBit.io.P12.setDigitalValue(val);
// }

// void set_gpio5(int val)
// {
//     uBit.io.P13.setDigitalValue(val);
// }

// void set_gpio6(int val)
// {
//     uBit.io.P14.setDigitalValue(val);
// }

// void set_gpio7(int val)
// {
//     uBit.io.P15.setDigitalValue(val);
// }

// void display_text(const char* text)
// {
//     uBit.display.scroll(text);
// }

// void display_number(int num)
// {
//     uBit.display.scroll(num);
// }

void blink()
{
    int toggle = 0;
    while(1)
    {
        uBit.display.image.setPixelValue(BLINK_POSITION_X, BLINK_POSITION_Y, toggle);
        toggle = !toggle;
        uBit.sleep(500);
    }
}
extern uint32_t radio_status;
int main()
{
    // Initialise the micro:bit runtime.
    uBit.init();
    bridge.enable();
    uBit.radio.enable();

    create_fiber(blink);

    // while(1)
    // {
    //     uBit.serial.printf("TXQ DEPTH: %d\r\n", uBit.radio.txQueueDepth);
    //     uBit.serial.printf("RXQ DEPTH: %d\r\n", uBit.radio.rxQueueDepth);
    //     uBit.serial.printf("RADIO_STATE: %d\r\n", NRF_RADIO->STATE);
    //     uBit.serial.printf("RADIO_STATUS: %d\r\n", radio_status);
    //     uBit.sleep(1000);
    // }

    // uBit.display.print(disp);
    // uBit.display.scroll(SCHOOL_ID);
    // uBit.display.scroll(HUB_ID);

    // If main exits, there may still be other fibers running or registered event handlers etc.
    // Simply release this fiber, which will mean we enter the scheduler. Worse case, we then
    // sit in the idle task forever, in a power efficient sleep.
    release_fiber();
}

