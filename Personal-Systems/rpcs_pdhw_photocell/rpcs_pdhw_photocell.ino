#define PHOTOCELL A0
#define POLL_RATE 20
void setup() 
{
 Serial.begin(9600);
}
 
void loop() 
{
  int value = analogRead(PHOTOCELL);
  Serial.print("The current ambient light value is ");
  Serial.println(value, DEC); 
  delay(1000/POLL_RATE);
}
