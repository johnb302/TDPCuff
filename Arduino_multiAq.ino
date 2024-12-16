//--NOTE--:
//  This script is designed to work in Arduino IDE: https://www.arduino.cc/en/software
//  in conjunction with the Python scripts rather than as a standalone script. 
//
//Instructions:
//  1) Download and Install Arduino IDE
//  2) Connect the boards using their respective serial ports
//  3) Compile + upload to each board
//  4) Close the IDE (or at least Serial Monitor) so that the port isn't busy 
//     when executing Python

void setup() {
  // Start the serial connection at 115200 baud:
  Serial.begin(115200);
}

void loop() {

  // If there's any serial available, read it
  while (Serial.available() > 0) {

    // read command from serial.write in arduino.py
    String command = Serial.readStringUntil('\n');

    // If the command is 'A4', take an analog reading and send it back:
    if (command == "A4") {
      int reading = analogRead(A4);
      Serial.println(reading * (5.0/1024.0));
    }
    else if (command == "A5"){
      int reading = analogRead(A5);
      Serial.println(reading * (5.0/1024.0));
    }
    else if (command == "A6"){
      int reading = analogRead(A6);
      Serial.println(reading * (5.0/1024.0));
    }
  }
}