#include<Servo.h>

int GREEN = 8;  //red led connect to digital output pin 8
int RED = 9;   //green led to pin 9

Servo s1;

void setup() {
  pinMode(GREEN, OUTPUT);  //setting pins to output
  pinMode(RED, OUTPUT);
  
  s1.attach(5);  //servo motor connected to pin 5

}
void loop()
{
s1.write(0); //servo rotates to 0 position
 
 digitalWrite(RED, HIGH);  //turn on red led
  delay(500);
  
  delay(7000);
  digitalWrite(RED, LOW);   //start blinking red led
  delay(500);
  digitalWrite(RED, HIGH);
  delay(500);
  digitalWrite(RED, LOW);
  delay(500);
  digitalWrite(RED, HIGH);
  delay(500);
  
  
  digitalWrite(RED, LOW);    
  delay(500);
  digitalWrite(RED, HIGH);
  delay(500);
  digitalWrite(RED, LOW);

s1.write(90);    //servo rotates to 90 position
  
  digitalWrite(GREEN, HIGH);    //turn on green led
  delay(7000);
 
  digitalWrite(GREEN, LOW);    //blink green led
  delay(500);
  digitalWrite(GREEN, HIGH);
  delay(500);
  digitalWrite(GREEN, LOW);
  delay(500);
  digitalWrite(GREEN, HIGH);
  delay(500);
  digitalWrite(GREEN, LOW);
  delay(500);
  digitalWrite(GREEN, HIGH);
  delay(500);
  digitalWrite(GREEN, LOW);
}
