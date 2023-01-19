#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>  
Servo myservo;
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);
#define SERVOMAX  102
#define SERVOMIN  510
#define SERVO_0  102 
#define SERVO_45  187 
#define SERVO_90  280 
#define SERVO_135  373 
#define SERVO_180  510 
int x;
int y; 
int z; 
//  当前运动距离  (0,0）代表左下角 
// x轴单次运动5mm
int x_running=0;
int y_running=0;  
int z_running=0; 
int pos = 0;
int value_guangmin = 0;
int servoMin =  102;       
int servoMax =  280;  
void setup()

{
  Serial.begin(9600);
  pinMode(9,OUTPUT);  // spin_dir 
  digitalWrite(9,HIGH); 
  pinMode(8,OUTPUT); // Enable: EN可以使用单片机端口控制，也可以直接连接GND使能 ok //x轴
 
  pinMode(2,OUTPUT); // steps:脉冲个数 ok //x轴

  pinMode(5,OUTPUT); // dir:为方向控制 ok //x轴

  digitalWrite(8,LOW); // Set Enable low  //x轴
  
 
  pinMode(3,OUTPUT); // steps:脉冲个数 ok //y轴

  pinMode(6,OUTPUT); // dir:为方向控制 ok //y轴

  digitalWrite(8,LOW); // Set Enable low  //y轴

   
  pinMode(4,OUTPUT); // steps:脉冲个数 ok //z轴

  pinMode(7,OUTPUT); // dir:为方向控制 ok //z轴
  
  digitalWrite(8,LOW); // Set Enable low  //Z轴
  

  pinMode(12,OUTPUT); // steps:脉冲个数 ok //A轴

  pinMode(13,OUTPUT); // dir:为方向控制 ok //A轴

  digitalWrite(8,LOW); 
  
  // pinMode(12,OUTPUT);  // 舵机 
  myservo.attach(10);
  pwm.begin();             //Start each board
  //pwm.setOscillatorFrequency(27000000);    //Set the PWM oscillator frequency, used for fine calibration
  pwm.setPWMFreq(50);          //Set the servo operating frequency

  delay(10);

  

  

}
  void setServoPulse(uint8_t n, double pulse) {
   double pulselength;
   pulselength = 1000000;   // 1,000,000 us per second
   pulselength /= 50;   // 50 Hz
   Serial.print(pulselength); 
   Serial.println(" us per period");
   pulselength /= 4096;  // 12 bits of resolution
   Serial.print(pulselength); 
   Serial.println(" us per bit");
   pulse *= 1000;
   pulse /= pulselength;
   Serial.println(pulse);
   pwm.setPWM(n, 0, pulse);
}
  void servo_9g_write(uint8_t n,int Angle){
    double pulse = Angle;
    pulse = pulse/90 + 0.5;
    setServoPulse(n,pulse);//0到180度映射为0.5到2.5ms
}


void loop()

{   
  value_guangmin = analogRead(A3);
  Serial.print("Track-X=");
  Serial.print(x_running,DEC);
  Serial.print("|Track-Y=");
  Serial.print(y_running,DEC);
  Serial.print("|Track-Z=");
  Serial.print(z_running,DEC);
  Serial.print("|guangmin=");
  Serial.print(value_guangmin,DEC);
  Serial.println();
  
  
  int inByte = Serial.read();
  char user = (char)inByte;
  

    

   if(user=='l'){

    for (int pulseLength = servoMin ; pulseLength <= servoMax ; pulseLength++)    //Move each servo from servoMin to servoMax
    {
      pwm.setPWM(0, 0, pulseLength);           //Set the current PWM pulse length on board 1, servo i
      delay(1);
    }
    Serial.print("库1开启! ");
    Serial.println();
    delay(100);
          }
    
  
     if(user=='L'){
    for (int pulseLength = servoMax ; pulseLength >= servoMin ; pulseLength--)    // Move each servo from servoMax to servoMin
    {
      pwm.setPWM(0, 0, pulseLength);           //Set the current PWM pulse length on board 1, servo i
      delay(1);
    }                    // waits 15ms for the servo to reach the position
        Serial.print("库1关闭!");
    Serial.println();
    delay(100);   
  }
   
    
   

   if(user=='n'){
    for (int pulseLength = servoMin ; pulseLength <= servoMax ; pulseLength++)    //Move each servo from servoMin to servoMax
    {
      pwm.setPWM(1, 0, pulseLength);           //Set the current PWM pulse length on board 1, servo i
      delay(1);
    }
    
    Serial.print("库2开启! ");
    Serial.println();
    delay(100);
    
    }
     if(user=='N'){
    for (int pulseLength = servoMax ; pulseLength >= servoMin ; pulseLength--)    // Move each servo from servoMax to servoMin
    {
      pwm.setPWM(1, 0, pulseLength);           //Set the current PWM pulse length on board 1, servo i
      delay(1);
    }

    Serial.print("库2关闭! ");
    Serial.println();
    delay(100);
    
    
    }


   if(user=='o'){
    for (int pulseLength = servoMin ; pulseLength <= servoMax ; pulseLength++)    //Move each servo from servoMin to servoMax
    {
      pwm.setPWM(2, 0, pulseLength);           //Set the current PWM pulse length on board 1, servo i
      delay(1);
    }
    
    Serial.print("库3开启! ");
    Serial.println();
    delay(100);
    
    
    }
     if(user=='O'){
    for (int pulseLength = servoMax ; pulseLength >= servoMin ; pulseLength--)    // Move each servo from servoMax to servoMin
    {
      pwm.setPWM(2, 0, pulseLength);           //Set the current PWM pulse length on board 1, servo i
      delay(1);
    }

    Serial.print("库3关闭! ");
    Serial.println();
    delay(100);
   
    
    
    }

    

    

    
    
   if (user == 'w'){
    digitalWrite(9,LOW);
    //delay(3000);
   Serial.print("Start warning! ");
   Serial.println();
    }
       if (user == 'm'){
    digitalWrite(9,HIGH);
    //delay(3000);
   Serial.print("Stop warning! ");
   Serial.println();
    }
  if (user == '0'){
    Serial.print("左!");
    digitalWrite(6,HIGH); // Set Dir high
    
    for(x = 0; x < 2000; x++) // Loop 200 times

  {   
      
      digitalWrite(3,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(3,LOW); // Output low
  
      delayMicroseconds(200); // Wait 1/2 a ms

    }
  x_running-=5;
  delay(500); // pause one second
    
    }
  
  if (user == '1'){
    Serial.print("右!");
    digitalWrite(6,LOW); // Set Dir high

    for(x = 0; x < 2000; x++) // Loop 200 times

  {

      digitalWrite(3,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(3,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  x_running+=5;
  delay(500); // pause one second
    
    }
   if (user == '2'){
    Serial.print("前!");
    digitalWrite(5,LOW); // Set Dir high

    for(y = 0; y < 2000; y++) // Loop 200 times

  {

      digitalWrite(2,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(2,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  y_running+=5;
  delay(500); // pause one second
    
    }

   if (user == '3'){
    Serial.print("后!");
    digitalWrite(5,HIGH); // Set Dir high

    for(y = 0; y < 2000; y++) // Loop 200 times

  {
      
      digitalWrite(2,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(2,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  y_running-=5;
  delay(500); // pause one second
    
    }

   if (user == '4'){
    Serial.print("上!");
    digitalWrite(7,HIGH); // Set Dir high

    for(z = 0; z < 2000; z++) // Loop 200 times

  {
      
      digitalWrite(4,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(4,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  z_running-=5;
  delay(500); // pause one second
    
    }
    
   if (user == '5'){
    Serial.print("下!");
    digitalWrite(7,LOW); // Set Dir high

    for(z = 0; z < 2000; z++) // Loop 200 times

  {
      
      digitalWrite(4,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(4,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  z_running+=5;
  delay(500); // pause one second
    
    }

   if (user == '6'){
    Serial.print("补充模块平台向下!");
    digitalWrite(13,LOW); // Set Dir high

    for(z = 0; z < 2000; z++) // Loop 200 times

  {
      
      digitalWrite(12,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(12,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  //z_running+=5;
  delay(500); // pause one second
    
    }

   if (user == '7'){
    Serial.print("补充模块平台向上!");
    digitalWrite(13,HIGH); // Set Dir high

    for(z = 0; z < 2000; z++) // Loop 200 times

  {
      
      digitalWrite(12,HIGH); // Output high

      delayMicroseconds(200); // Wait 1/2 a ms

      digitalWrite(12,LOW); // Output low

      delayMicroseconds(200); // Wait 1/2 a ms

    }
  //z_running+=5;
  delay(500); // pause one second
    
    }
    



    
    
   if (user == 'c'){
    Serial.print("自动中心!");
    digitalWrite(7,LOW); // Set Dir high

    for(z = 0; z < 2000*10; z++) // Loop 200 times

  {
      
      digitalWrite(4,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(4,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
        for(z = 0; z < 2000*10; z++) // Loop 200 times

  {
      
      digitalWrite(4,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(4,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
    
  z_running+=100;
    digitalWrite(5,HIGH); // Set Dir high

    for(y = 0; y < 2000*8; y++) // Loop 200 times

  {
      
      digitalWrite(2,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(2,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
  y_running+=40;
    digitalWrite(6,LOW); // Set Dir high

    for(x = 0; x < 2000*11; x++) // Loop 200 times

  {

      digitalWrite(3,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(3,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
        for(x = 0; x < 2000*3; x++) // Loop 200 times

  {

      digitalWrite(3,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(3,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
  x_running+=60;
  
  delay(500); // pause one second
    
    }
     if (user == 'b'){
    Serial.print("自动归零!");
    digitalWrite(7,HIGH); // Set Dir high
    
    for(z = 0; z < 2000*z_running/10; z++) // Loop 200 times

  {
      
      digitalWrite(4,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(4,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
        for(z = 0; z < 2000*z_running/10; z++) // Loop 200 times

  {
      
      digitalWrite(4,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(4,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
  z_running=0;
    digitalWrite(5,LOW); // Set Dir high

    for(y = 0; y < 2000*y_running/5; y++) // Loop 200 times

  {
      
      digitalWrite(2,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(2,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
  y_running=0;
    digitalWrite(6,HIGH); // Set Dir high

    for(x = 0; x < 2000*x_running/5; x++) // Loop 200 times

  {

      digitalWrite(3,HIGH); // Output high

      delayMicroseconds(100); // Wait 1/2 a ms

      digitalWrite(3,LOW); // Output low

      delayMicroseconds(100); // Wait 1/2 a ms

    }
  x_running=0;
  delay(500); // pause one second
    
    }

   if (user == 'a'){
    for (pos = 60; pos <= 95; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

   Serial.print("servo move ");
   Serial.println();
    }
   if (user == 'd'){
    for (pos = 95; pos >= 60; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  

   Serial.print("servo return ");
   Serial.println();
    }
   if (user == 's'){
    for (pos = 60; pos <= 95; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
    for (pos = 95; pos >= 60; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
      for (pos = 60; pos <= 95; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
   Serial.print("servo self checking ");
   Serial.println();
    }
  delay(500);
}
