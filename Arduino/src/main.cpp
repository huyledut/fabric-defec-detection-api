#include <Arduino.h>

int step = 5;
int dir = 4;
int ena = 6;

int sensor = A0;
int value;

String data;
bool isStart = false;

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
  if (!isStart)
  {
    if (Serial.available())
    {
      data = Serial.readString();
      if (data == "Start")
      {
        isStart = true;
        Serial.println("Started");
      }
      delay(1000);
    }
  }
  else
  {
    // send Value read from sensor
    value = analogRead(sensor);
    Serial.print("Value read from sensor:");
    Serial.println(value);

    if (value > 350)
    {
      // move 6 steps
      digitalWrite(dir, HIGH);
      for (int x = 0; x < 1200; x++)
      {
        digitalWrite(step, HIGH);
        delayMicroseconds(2100);
        digitalWrite(step, LOW);
        delayMicroseconds(2100);
      }

      delay(1000);
      while (true)
      {
        Serial.println("A");
        if (Serial.available() > 0)
        {
          data = Serial.readString();
          if (data == "B")
          {
            digitalWrite(dir, LOW);
            for (int x = 0; x < 1200; x++)
            {
              digitalWrite(step, HIGH);
              delayMicroseconds(2100);
              digitalWrite(step, LOW);
              delayMicroseconds(2100);
            }
            delay(2000);
            break;
          }
        }
        delay(1000);
      }
      delay(1000);
    }
  }
}