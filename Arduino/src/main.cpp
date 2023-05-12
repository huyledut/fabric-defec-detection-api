#include <Arduino.h>

int step = 4;
int dir = 5;
int ena = 8;
int sensor = A0;
int value;

void setup()
{
  Serial.begin(9600);

  // motor
  pinMode(ena, OUTPUT);
  pinMode(step, OUTPUT);
  pinMode(dir, OUTPUT);
  digitalWrite(ena, LOW);

  // sensor
  pinMode(sensor, INPUT);
}

void loop()
{

  value = analogRead(sensor);
  Serial.print("Value read from sensor:");
  Serial.println(value);

  if (value < 150)
  {
    digitalWrite(dir, HIGH);
    for (int x = 0; x < 1000; x++)
    {
      digitalWrite(step, HIGH);
      delayMicroseconds(500);
      digitalWrite(step, LOW);
      delayMicroseconds(500);
    }

    delay(1000);

    digitalWrite(dir, LOW);
    for (int x = 0; x < 1000; x++)
    {
      digitalWrite(step, HIGH);
      delayMicroseconds(500);
      digitalWrite(step, LOW);
      delayMicroseconds(500);
    }
    delay(1000);
  }
}