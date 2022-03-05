int buzzPin =3;    //Connect Buzzer on Digital Pin3
 void setup()  
 {        
  pinMode(buzzPin, OUTPUT);     
}

void buzz(int ms)
{
  int cnt_ms = 0;
  while(cnt_ms < ms){
    digitalWrite(buzzPin, HIGH);
    delay(1);
    digitalWrite(buzzPin, LOW); 
    delay(1);
    cnt_ms+=2;
  }
  digitalWrite(buzzPin, LOW);
}
 void loop()                     
{
  buzz(1000);
  delay(1000);
}
