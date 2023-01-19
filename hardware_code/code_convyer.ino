#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); //RX=2,TX=3
int PUL_2 = 7; //定义脉冲引脚
int DIR_2 = 6; //定义方向销  缺陷
int ENA_2 = 5; //定义启用引脚
int PUL_1 = 10; //定义脉冲引脚  
int DIR_1 = 9; //定义方向销   补充 
int ENA_1 = 8; //定义启用引脚   
int PUL = 13; //定义脉冲引脚
int DIR = 12; //定义方向销    底层传送带
int ENA = 11; //定义启用引脚
int value=0;
int value_x=0;
int value_y=0;
int value_z=0;
//int value_guangmin = 0;
double run_distance = 0;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);
  pinMode (PUL_1, OUTPUT);
  pinMode (DIR_1, OUTPUT);
  pinMode (ENA_1, OUTPUT);
  pinMode (PUL_2, OUTPUT);
  pinMode (DIR_2, OUTPUT);
  pinMode (ENA_2, OUTPUT);
  pinMode(4,INPUT_PULLUP);
 
  // 初始化复位 - 转3圈

}

void loop() {
  value_x = analogRead(A0);
  Serial.print("X=");
  Serial.print(value_x,DEC);
  value_y = analogRead(A1);
  Serial.print("|Y=");
  Serial.print(value_y,DEC);
  value=digitalRead(4);
  Serial.print("|Z=");
  Serial.print(value,DEC);
  Serial.print("|run_distance=");
  Serial.print(run_distance,DEC);
  //value_guangmin= analogRead(A0);
  //Serial.print("|value_guangmin=");
  //Serial.print(value_guangmin,DEC);
  /*mySerial.print(run_distance);*/
  delay(50);
  Serial.println();
  
  int inByte = Serial.read();
  char user = (char)inByte;
    
  while (value_x <450){  // 底层手动
    Serial.print("Forward!");
    Serial.println();
    mySerial.print("Forward!");
    for (int i = 0; i < 1600; i++) //正转1圈
    {

      digitalWrite(DIR_2, LOW);
      digitalWrite(ENA_2, HIGH);
      digitalWrite(PUL_2, HIGH);
      delayMicroseconds(50);
      //digitalWrite(PUL, LOW);
      //digitalWrite(PUL_1, LOW);
      digitalWrite(PUL_2, LOW);
      delayMicroseconds(50);
      
      
    }
    run_distance+=25.4;
    break;
  }
  while (value_x >650){ // 底层手动
    Serial.print("Backward!");
    Serial.println();
    mySerial.print("Backward!");
    for (int i = 0; i < 1600; i++) //倒转1圈
    {

      digitalWrite(DIR_2, HIGH);
      digitalWrite(ENA_2, HIGH);
      digitalWrite(PUL_2, HIGH);
      delayMicroseconds(50);
      digitalWrite(PUL_2, LOW);
      delayMicroseconds(50);
      
    }
    run_distance-=25.4;
    break;
}
  while (user == '4'){
    Serial.print("Self checking!");
    Serial.println();
    mySerial.print("Self checking!");
      for (int i = 0; i < 4800; i++) //前进4800步 SW1=OFF,SW2=ON,SW3=OFF(每圈1600脉冲)
  {
    digitalWrite(DIR, LOW); // 定义正转
    digitalWrite(ENA, HIGH);// 启动
    digitalWrite(PUL, HIGH);// 输出脉冲
    digitalWrite(DIR_1, HIGH); // 定义正转
    digitalWrite(ENA_1, HIGH);// 启动
    digitalWrite(PUL_1, HIGH);// 输出脉冲
    digitalWrite(DIR_2, LOW); // 定义正转
    digitalWrite(ENA_2, HIGH);// 启动
    digitalWrite(PUL_2, HIGH);// 输出脉冲
    delayMicroseconds(1000);
    digitalWrite(PUL, LOW);
    digitalWrite(PUL_1, LOW);  
    digitalWrite(PUL_2, LOW);    

  }
    Serial.print("Checking finished!");
    Serial.println();
    mySerial.print("Checking finished!");
  break;
  
    }
  while (user == '0'){
    Serial.print("Forward!");
    Serial.println();
    mySerial.print("Forward!");
    for (int i = 0; i < 1600; i++) //正转1圈
    {

      digitalWrite(DIR_2, LOW);
      digitalWrite(ENA_2, HIGH);
      digitalWrite(PUL_2, HIGH);
      delayMicroseconds(50);
      digitalWrite(PUL_2, LOW);
      delayMicroseconds(50);
      
      
    }
    run_distance+=25.4;
    break;
  }
  while (user == '1'){
    Serial.print("Backward!");
    Serial.println();
    mySerial.print("Backward!");
    for (int i = 0; i < 1600; i++) //倒转1圈
    {
      digitalWrite(DIR_2, HIGH);
      digitalWrite(ENA_2, HIGH);
      digitalWrite(PUL_2, HIGH);
      delayMicroseconds(50);

      digitalWrite(PUL_2, LOW);
      delayMicroseconds(50);
      
    }
    run_distance-=25.4;
    break;
}
  while (user == '2'){
    Serial.print("Auto running!");
    Serial.println();
    mySerial.print("Auto running!");
    for (int i = 0; i < 1600; i++) //正转1圈
    {

      digitalWrite(DIR_2, LOW);
      digitalWrite(ENA_2, HIGH);
      digitalWrite(PUL_2, HIGH);
      delayMicroseconds(700);
      //digitalWrite(PUL, LOW);
      //digitalWrite(PUL_1, LOW);
      digitalWrite(PUL_2, LOW);      
    }
    
    delay(300);
    run_distance+=12.7;
    int inByte = Serial.read();
    char user = (char)inByte;
    if (user == '3'){
    Serial.print("Auto STOP!");
    Serial.println();
      break;
      }
    }
   while (user == '5'){
    Serial.print("Supplementary belt moving!");
    Serial.println();
    mySerial.print("Supplementary belt moving!");
    for (int i = 0; i < 1600; i++) //倒转1圈
    {
      digitalWrite(DIR_1,HIGH);
      digitalWrite(ENA_1, HIGH);
      digitalWrite(PUL_1, HIGH);
      delayMicroseconds(50);
      digitalWrite(PUL_1, LOW);
      delayMicroseconds(50);
      
    }
    delay(300);
    int inByte = Serial.read();
    char user = (char)inByte;
    if (user == '6'){
    Serial.print("Supplementary belt STOP!");
    Serial.println();
      break;
      }
    
} 
  while (user == '7'){
    Serial.print("Defective belt moving!");
    Serial.println();
    mySerial.print("Defective belt moving!");
    for (int i = 0; i < 1600; i++) //倒转1圈
    {
      digitalWrite(DIR,LOW);
      digitalWrite(ENA, HIGH);
      digitalWrite(PUL, HIGH);
      delayMicroseconds(50);
      digitalWrite(PUL, LOW);
      delayMicroseconds(50);
      
    }
    delay(300);
    int inByte = Serial.read();
    char user = (char)inByte;
    if (user == '8'){
    Serial.print("Defective belt STOP!");
    Serial.println();
      break;
      }
    
} 
   while (user == '9'){
    Serial.print("Classification belt self checking!");
    Serial.println();
    mySerial.print("Classification belt self checking!");
    for (int i = 0; i < 4800; i++) //倒转1圈
    {
      digitalWrite(DIR,LOW);
      digitalWrite(ENA, HIGH);
      digitalWrite(PUL, HIGH);
      digitalWrite(DIR_1,HIGH);
      digitalWrite(ENA_1, HIGH);
      digitalWrite(PUL_1, HIGH);
      delayMicroseconds(1000);
      digitalWrite(PUL, LOW);
      digitalWrite(PUL_1, LOW);

    }
    delay(600);
    break;
    
}
  while(user =='q'){
      for (int i = 0; i < 1600; i++) //倒转1圈
    {
      digitalWrite(DIR,LOW);
      digitalWrite(ENA, HIGH);
      digitalWrite(PUL, HIGH);
      digitalWrite(DIR_1,HIGH);
      digitalWrite(ENA_1, HIGH);
      digitalWrite(PUL_1, HIGH);
      digitalWrite(DIR_2,LOW);
      digitalWrite(ENA_2, HIGH);
      digitalWrite(PUL_2, HIGH);
      delayMicroseconds(200);
      digitalWrite(PUL, LOW);
      digitalWrite(PUL_1, LOW);
      digitalWrite(PUL_2, LOW);
      
      
    }
    delay(400);
    int inByte = Serial.read();
    char user = (char)inByte;
    if (user == 'Q'){
    Serial.print("ALL STOP!");
    Serial.println();
      break;
      }  
    
    
    
    }  
  
  
  delay(300);
  

   /* 
  char str[20] = "";
  int i = 0;
  char s[] = "test！！"; //每隔3s发送一次字符数组s
  Serial.println("OK");
  mySerial.print(s);
  delay(3000);*/
  
}
