// Pin #s for pumps, solenoid, and sensor. Change here if need be.
int pump = 5;
int vacu = 7;
int valve = 6;
int sensr = 7;

// Desired cuff pressure in mmHg
int targetPressure = 75;

void setup() {
  Serial.begin(9600);
  pinMode(pump, OUTPUT); // set pin 2 to output for pump
  pinMode(vacu, OUTPUT); // set pin 4 to output for pump
  pinMode(valve, OUTPUT); // set pin 6 to output for solenoid
}

void loop() {
  double sensorVoltage = (analogRead(sensr) * (4.5/1024)); // reading voltage from sensor
  Serial.println(sensorVoltage);

  // linear relationship obtained from calibration
  double cuffPressure = 63.9531*sensorVoltage - 34.9409; // current pressure in the cuff
  //Serial.println(cuffPressure);

  if (cuffPressure < targetPressure)
  {
    // turn pump on to cuff
    digitalWrite(vacu, LOW);
    digitalWrite(valve, HIGH);
    digitalWrite(pump, HIGH);
  }
  else if (cuffPressure > targetPressure*1.05)
  {
    // turn vacuum on to cuff
    digitalWrite(pump, LOW);
    digitalWrite(valve, LOW);
    digitalWrite(vacu, HIGH);
  }
  else
  {
    // turn valve on. no air in or out
    digitalWrite(pump, LOW);
    digitalWrite(valve, HIGH);
    while(1){;} // loop to hold pressure
  }
}
