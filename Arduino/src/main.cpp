#include <Arduino.h>

int step = 5;
int dir = 4;
int ena = 6;

int sensor = A0;
int value;

String data;

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

  if (value > 350)
  {
    delay(1000);

    digitalWrite(dir, HIGH);
    for (int x = 0; x < 1000; x++)
    {
      digitalWrite(step, HIGH);
      delayMicroseconds(500);
      digitalWrite(step, LOW);
      delayMicroseconds(500);
    }
    Serial.println("A");
    while (true)
    {
      if (Serial.available() > 0)
      {
        data = Serial.readString();
        if (data == "B")
        {
          digitalWrite(dir, LOW);
          for (int x = 0; x < 1000; x++)
          {
            digitalWrite(step, HIGH);
            delayMicroseconds(500);
            digitalWrite(step, LOW);
            delayMicroseconds(500);
          }
          break;
        }
      }
    }

    delay(1000);

    // if (Serial.available() > 0)
    // {
    //   data = Serial.readString();
    //   if (data == "B")
    //   {
    //     digitalWrite(dir, LOW);
    //     for (int x = 0; x < 1000; x++)
    //     {
    //       digitalWrite(step, HIGH);
    //       delayMicroseconds(500);
    //       digitalWrite(step, LOW);
    //       delayMicroseconds(500);
    //     }
    //     delay(1000);
    //   }
    // }
    // else
    // {
    //   digitalWrite(dir, LOW);
    //   for (int x = 0; x < 1000; x++)
    //   {
    //     digitalWrite(step, HIGH);
    //     delayMicroseconds(1500);
    //     digitalWrite(step, LOW);
    //     delayMicroseconds(1500);
    //   }
    //   delay(1000);
    // }
  }
}