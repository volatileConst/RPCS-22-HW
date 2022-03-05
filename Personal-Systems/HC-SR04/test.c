int inputPin=4; // define ultrasonic signal receiver pin ECHO to D4 
int outputPin=5; // define ultrasonic signal transmitter pin TRIG to D5

void setup()
{
  Serial.begin(9600); 
  pinMode(inputPin, INPUT); 
  pinMode(outputPin, OUTPUT);
}

void loop()
{
  digitalWrite(outputPin, LOW); delayMicroseconds(2);
  
  digitalWrite(outputPin, HIGH); // Pulse for 10μ s to trigger ultrasonic detection
  
  delayMicroseconds(10); 
  digitalWrite(outputPin, LOW);
  
  int distance = pulseIn(inputPin, HIGH); // Read receiver pulse time 
  distance= distance/58; // Transform pulse time to distance 
  Serial.println(distance); //Output distance
  delay(50);
}
