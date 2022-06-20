
byte PWM_PIN = 2;

int pwm_value;
int output;

void setup() {
  pinMode(PWM_PIN, INPUT);
  Serial.begin(115200);
}

void loop() {

  pwm_value = pulseIn(PWM_PIN, HIGH);
  Serial.print(pwm_value);
  output = constrain(map(pwm_value, 8, 2022, 0, 1023), 0, 1023);
  Serial.print(" ");
  Serial.println(output);
}
