#define LED 13
#define BUTTON 3
#define POLL_RATE 100 //in Hz
void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);
}

void buttonPressed(){
  Serial.print("Button Pressed!\n");
}

void buttonReleased(){
  Serial.print("Button Released!\n");
}

int prev_val = HIGH;

void loop(){
  int val = digitalRead(BUTTON);
  if (val == HIGH) {
    digitalWrite(LED, LOW);
    if (prev_val == LOW){
      buttonReleased();
    }
  } else {
    digitalWrite(LED, HIGH);
    if (prev_val == HIGH){
      buttonPressed();
    }
  }
  prev_val = val;
  delay(1000/POLL_RATE);
}
