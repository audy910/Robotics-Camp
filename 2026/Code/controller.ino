#include<SoftwareSerial.h>

//Setup pins
const int L_xPin = A1;
const int L_yPin = A0;
const int R_xPin = A3;
const int R_yPin = A2;

//Values associated with pins
int L_xVal;
int L_yVal;
int R_xVal;
int R_yVal;
const int rx = 10;
const int tx = 11;

//tracks throttle and direction from joysticks
String prev_throttle = "'";
String prev_direction = "'";
SoftwareSerial mySerial(rx, tx);

void setup() {
//put your setup code here, to run once:
Serial.begin(9600);
mySerial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 // Serial.print("stopped");
  L_xVal = analogRead(L_xPin);
  L_yVal = analogRead(L_yPin);
  R_xVal = analogRead(R_xPin);
  R_yVal = analogRead(R_yPin);
  
  Serial.print("Joystick Left: X = ");
  Serial.print(L_xVal);
  Serial.print(" Y = ");
  Serial.println(L_yVal);
  Serial.print("Joystick Right: X = ");
  Serial.print(R_xVal);
  Serial.print(" Y = ");
  Serial.println(R_yVal);

  String data;

  // ------- LEFT JOYSTICK -------
  data = String(L_yVal);
  data += ",";

  // ------- RIGHT JOYSTICK -------
  // go left
  if (R_yVal > 570){
    prev_direction = "l";
    data += "l";
  }

  // go right
   else if (R_yVal < 500) {
    prev_direction = "r";
    data += "r";
  }

  // idle 
  else {
    prev_direction = "i";
    data += "i";
  }

  Serial.println(data);
  mySerial.println(data);
  Serial.println("-----");

  delay(1500);
}