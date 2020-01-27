/*
  Hyperkin Xbox One LCD module

  Play bootanim trigger

  D0 -> LCD module connector DAT0

  Author: tuxuser - 2020
*/

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin D0 as an output.
  pinMode(D0, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(D0, HIGH);   // Pull D0 high
  delay(10);                // wait for 10ms
  digitalWrite(D0, LOW);    // Pull D0 low again
  delay(8000);              // wait for 8 seconds
}
