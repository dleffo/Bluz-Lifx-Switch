#include "application.h"

SYSTEM_MODE(AUTOMATIC);

const uint8_t buttonPin = 2;     // the number of the pushbutton pin
volatile int push = false;
String myID;
char data[28] = {};

void interruptus(void);

void setup() {
    pinMode(buttonPin, INPUT);
    attachInterrupt(buttonPin,interuptus, RISING);
    myID = System.deviceID();
    Particle.publish("Bluz DeviceID", myID);
    memcpy(data,myID.c_str(),24);
}


void loop() {
    if (push){
        data[24] = '|';
        data[25] = 'B';
        data[26] = '0' + buttonPin;
        BLE.sendData((uint8_t*)data,28);
        push = false;
    }
    System.sleep(SLEEP_MODE_CPU);
}

void interuptus(){
        // read the state of the switch into a local variable:
        push = true;
}
