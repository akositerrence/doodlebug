#include <Arduino.h>

#include "wiring_private.h" 
#include "pins_arduino.h"   
#include <SPI.h>            

#include "max6675.h"
#include <SD.h>            

const int SCK1 = 49;
const int CS1 = 47;
const int SO1 = 45;
const int SCK2 = 41;
const int CS2 = 39;
const int SO2 = 37;
MAX6675 entranceThermocouple(SCK1, CS1, SO1); 
MAX6675 exitThermocouple(SCK2, CS2, SO2);

const int entranceCoolingValve = 4;
const int exitCoolingValve = 5;
const int entranceGasSolenoid = 6;
const int exitGasSolenoid = 7;

const int transducer = A8;
const int flowSensor = A9;

void setup() {

  Serial.begin(9600);

  pinMode(entranceCoolingValve, OUTPUT);
  pinMode(exitCoolingValve, OUTPUT);
  pinMode(entranceGasSolenoid, OUTPUT);
  pinMode(exitGasSolenoid, OUTPUT);

  digitalWrite(entranceCoolingValve, LOW);
  digitalWrite(exitCoolingValve, LOW);
  digitalWrite(entranceGasSolenoid, LOW);
  digitalWrite(exitGasSolenoid, LOW);

  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {

  digitalWrite(LED_BUILTIN, HIGH);

  digitalWrite(exitGasSolenoid, HIGH);
  delay(2000);

  digitalWrite(LED_BUILTIN, LOW);

  digitalWrite(exitGasSolenoid, LOW);
  delay(2000);

}