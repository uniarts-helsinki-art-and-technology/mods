#include "protothreads.h"




const int DIGITAL_SIGNAL_PIN_2 = 2;   // TEST BUTTON
const int DIGITAL_SIGNAL_PIN_3 = 3;   // SENSOR
const byte ANALOG_INPUT_PIN_0 = A0;   // SENSOR
const byte ANALOG_INPUT_PIN_7 = A7;   // THRESHOLD POT

const byte DIGITAL_OUTPUT_PIN = 13;   // RELAY
const byte ANALOG_OUTPUT_PIN = 10;    // TRANSISTOR

int button_input_state = 0;
int sensor_input_state = 0;
int sensor_input_value = 0;
int sensor_threshold = 512;
const int sensor_threshold_margin = 5;


pt ptDigitalIn;
pt ptDigitalOut;
pt ptAnalogIn;
pt ptAnalogOut;

int digitalIn(struct pt* pt) {
  PT_BEGIN(pt);
  for(;;) 
  {
    button_input_state = digitalRead(DIGITAL_SIGNAL_PIN_2);
    sensor_input_state = digitalRead(DIGITAL_SIGNAL_PIN_3);
    return 0;
  }
  PT_END(pt);
}

int digitalOut(struct pt* pt) {
  PT_BEGIN(pt);
  for(;;) {
    if(sensor_input_state == 1 || sensor_input_value>sensor_threshold+sensor_threshold_margin)
    {
      digitalWrite(DIGITAL_OUTPUT_PIN,HIGH);
    }
    else if(sensor_input_value<sensor_threshold-sensor_threshold_margin)
    {
      digitalWrite(DIGITAL_OUTPUT_PIN,LOW);
    }
    else
    {
      digitalWrite(DIGITAL_OUTPUT_PIN,LOW);
    }
    return 0;
  }
  PT_END(pt);
}

int analogIn(struct pt* pt) {
  PT_BEGIN(pt);
  for(;;) 
  {
    sensor_input_value = analogRead(ANALOG_INPUT_PIN_0);
    sensor_threshold = analogRead(ANALOG_INPUT_PIN_7);
    return 0;
  }
  PT_END(pt);
}

int analogOut(struct pt* pt) {
  PT_BEGIN(pt);
  for(;;) {
    //int sensor_output_value = map(sensor_input_value,0,1023,0,255); // 12 bit >> 8 bit
    analogWrite(ANALOG_OUTPUT_PIN,sensor_input_value);
    return 0;
  }
  PT_END(pt);
}

void setup() {
  pinMode (ANALOG_OUTPUT_PIN, OUTPUT); 
  pinMode (DIGITAL_OUTPUT_PIN, OUTPUT); 
  pinMode (DIGITAL_SIGNAL_PIN_2, INPUT); 
  pinMode (DIGITAL_SIGNAL_PIN_3, INPUT); 

  PT_INIT(&ptDigitalIn);
  PT_INIT(&ptDigitalOut);
  PT_INIT(&ptAnalogIn);
  PT_INIT(&ptAnalogOut);

}

void loop() {

  PT_SCHEDULE(digitalIn(&ptDigitalIn));
  PT_SCHEDULE(analogIn(&ptAnalogIn));

  PT_SCHEDULE(digitalOut(&ptDigitalOut));
  PT_SCHEDULE(analogOut(&ptAnalogOut));

}
