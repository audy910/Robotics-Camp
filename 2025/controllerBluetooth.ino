#include<SoftwareSerial.h>
const int x = A1;
const int y = A0;
int X;
int Y;
const int rx = 10;
const int tx = 11;
char prev_message = '`';
SoftwareSerial mySerial(rx, tx);

void setup() {
//put your setup code here, to run once:
Serial.begin(9600);
mySerial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 // Serial.print("stopped");
  X = analogRead(x);
  Y = analogRead(y);
  if(X>550 && Y>500 && prev_message != '1'){
    // Serial.print(X);
    Serial.print("1"); 
    mySerial.print('1');//forward
    prev_message = '1';
  }else if(Y < 500 && X > 500 && X <550 && prev_message != '2'){
    Serial.print("2"); 
    mySerial.print('2');//right
    prev_message = '2';
  }else if(Y > 550 && X > 500 && X <550 && prev_message != '3'){
   Serial.print("3"); 
    mySerial.print('3');//left
    prev_message = '3';
  }else if(Y < 530 && X < 500 && prev_message != '4'){
    Serial.print("4");
    mySerial.print('4');//back
    prev_message = '4';
   }else if(Y < 550 && X < 550 && Y > 450 && X > 450 && prev_message != '0'){
    mySerial.print('0');//idle
    prev_message = '0';
  }
    
}