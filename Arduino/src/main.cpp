#include <Arduino.h>

int Sensor = A0;
int Value;
int Ledpin = 13;

void setup() 
{
  Serial.begin(9600);
  pinMode(Ledpin, OUTPUT); 
  digitalWrite(Ledpin, LOW); 
  pinMode(Sensor, INPUT);
}

void loop() 
{
  Value = analogRead(Sensor);
  Serial.print("Value read from sensor: ");
  Serial.println(Value);

  if (Value >= 200)
    digitalWrite(Ledpin, HIGH);
  else 
    digitalWrite(Ledpin, LOW); 
    
  delay(1000);
}
 