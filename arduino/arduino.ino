String inByte;         // incoming serial byte
bool newByteComing = false;
int knockPin = 10; // Use Pin 10 as our Input
int knockVal = HIGH;
unsigned long lastKnockTime; // Record the time that we measured a shock
int knockAlarmTime = 3000; // Number of milli seconds to keep the knock alarm high
bool knockActive = true;

void setup() {
  // start serial port at 9600 bps and wait for port to open:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode (knockPin, INPUT) ; // input from the KY-031
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.readString();
    //Serial.print(inByte,DEC);
    newByteComing = true;
  }
  if(newByteComing){
    if(inByte == "lightOn"){
      digitalWrite(13, HIGH);
    }else if (inByte == "lightOff"){
      digitalWrite(13, LOW);
    }
    else if (inByte == "knockActive"){
      knockActive = true;
    }
    else if (inByte == "knockDesactive"){
      knockActive = false;
    }
    newByteComing = false;
  }
  if(knockActive && millis() - lastKnockTime > knockAlarmTime){
    knockVal = digitalRead(knockPin) ;
    if(knockVal == LOW){
      Serial.println("knock");
      lastKnockTime = millis();
    }
  }
  //delay(20); //keep arduino calm no more for geet knock sensing
}

