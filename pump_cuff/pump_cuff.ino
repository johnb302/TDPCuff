// Pin #s for pumps, solenoid, and sensor. Change here if need be.
int pump = 5;
int vacu = 7;
int valve = 6;
int sensr = 7;

// Desired cuff pressure in mmHg
int targetPressure = 75;
String command = "empty";

void setup() {
  Serial.begin(9600);
  pinMode(pump, OUTPUT); // set pin 2 to output for pump
  pinMode(vacu, OUTPUT); // set pin 4 to output for pump
  pinMode(valve, OUTPUT); // set pin 6 to output for solenoid
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
  }

  if (command == "Start") {
    double sensorVoltage = (analogRead(sensr) * (5.0 / 1024));  // reading voltage from sensor
    //Serial.println(sensorVoltage);

    // linear relationship obtained from calibration
    double cuffPressure = 63.9531 * sensorVoltage - 34.9409;  // current pressure in the cuff
    // Serial.println(cuffPressure);

    if (cuffPressure < targetPressure) {
      // turn pump on to cuff
      digitalWrite(vacu, LOW);
      digitalWrite(valve, HIGH);
      digitalWrite(pump, HIGH);
    } else {
      command = "Finish";
    }
  } else if (command == "Finish") {
    double sensorVoltage = (analogRead(sensr) * (5.0 / 1024));  // reading voltage from sensor
    //Serial.println(sensorVoltage);

    // linear relationship obtained from calibration
    double cuffPressure = 63.9531 * sensorVoltage - 34.9409;  // current pressure in the cuff
    // Serial.println(cuffPressure);

    if (cuffPressure > 0) {
      // turn pump on to cuff
      digitalWrite(vacu, HIGH);
      digitalWrite(valve, LOW);
      digitalWrite(pump, LOW);
    } else {
      digitalWrite(vacu, LOW);
      Serial.write("End\n");
    }
  }
}
