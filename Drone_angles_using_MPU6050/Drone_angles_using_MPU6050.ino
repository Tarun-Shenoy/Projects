
#include "Wire.h"
#include <MPU6050_light.h>


MPU6050 mpu(Wire);
float x,y,z;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");
  Serial.println("Roll             Pitch              Yaw ");
}

void loop() {
  mpu.update();
  x=mpu.getAngleX();
  y=mpu.getAngleY();
  z=mpu.getAngleZ();
	Serial.print(x);
	Serial.print("               ");
	Serial.print(y);
	Serial.print("               ");
	Serial.println(z);
  delay(1000);
}
