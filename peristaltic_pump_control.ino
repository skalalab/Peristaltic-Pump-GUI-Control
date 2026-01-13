const int ledPin = 13;
// speed is the speed at which the pump will run
// values can range from 0 - 225. This can be changed
int speed = 0;
// the pin that the arduino is connected to.
// the pin should be a PWM pin, see https://docs.arduino.cc/tutorials/uno-r4-minima/cheat-sheet/
int pin = 9;

// runs when the board is powered on or resets
void setup() {
  Serial.begin(9600);
  analogWriteResolution(8); //built in default is 8
  Serial.setTimeout(100); //how long in ms to wait for serial input. When using python should be small value, 
                          // when using serial monitor should be how long it should wait before shutting off/ larger value
                          // find a way to change this without having to upload every time
  delay(200);
  pinMode(ledPin, OUTPUT);
  // sets pin 9 to output signal
  pinMode(pin, OUTPUT);
}

void loop() {
  
  //stops the pump from running when given an input
  if(Serial.available() > 0){ // returns the number of bytes available from serial

    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    
    int serialVal = Serial.parseInt();
    if(serialVal == 0){
      //Serial.print("Serial value is ");
      //Serial.println(serialVal);
      Serial.print("Stopping pump ");
      analogWrite(pin, 0);
      speed = 0;
    } else{
      //input is validated in python program
      //Serial.print("Serial value is ");
      //Serial.println(serialVal);
      Serial.print("Setting speed to ");
      Serial.println(serialVal);
      speed = serialVal;
      // runs the pump at speed
      analogWrite(pin, speed);
    }
  }

}
