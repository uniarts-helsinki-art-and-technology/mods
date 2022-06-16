#include "protothreads.h"

const int DIGITAL_SIGNAL_PIN_2 = 2;   // INPUT PULSE
const byte DIGITAL_OUTPUT_PIN_10 = 10;   // RELAY

int pulse_input_state = 0;
bool signal_detected = false;
bool relay_on = false;

pt ptDigitalIn;
pt ptDigitalOut;

int digitalIn(struct pt* pt) {
  PT_BEGIN(pt);
  for(;;) 
  {
    pulse_input_state = digitalRead(DIGITAL_SIGNAL_PIN_2);

    if(pulse_input_state != 1 && signal_detected==false)
    {
      signal_detected = true;
    }
    else
    {
      signal_detected = false;
      relay_on = false;
    }
    return 0;
  }
  PT_END(pt);
}

int digitalOut(struct pt* pt) {
  PT_BEGIN(pt);
  for(;;) {
    if(signal_detected && relay_on == false)
    {
      digitalWrite(DIGITAL_OUTPUT_PIN_10,HIGH);
      delay(5);
      relay_on = true;
    }
    else if(signal_detected==false)
    {
      digitalWrite(DIGITAL_OUTPUT_PIN_10,LOW);
    }
    else
    {
    }
    return 0;
  }
  PT_END(pt);
}


void setup() {
  pinMode (DIGITAL_OUTPUT_PIN_10, OUTPUT); 
  pinMode (DIGITAL_SIGNAL_PIN_2, INPUT); 

  PT_INIT(&ptDigitalIn);
  PT_INIT(&ptDigitalOut);
}

void loop() 
{
  PT_SCHEDULE(digitalIn(&ptDigitalIn));
  PT_SCHEDULE(digitalOut(&ptDigitalOut));
}
