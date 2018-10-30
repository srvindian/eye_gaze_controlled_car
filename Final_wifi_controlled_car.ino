#include<SoftwareSerial.h>
#define m11 4
#define m12 5
#define m21 6
#define m22 7
#define eA 8
#define eB 9
#define DEBUG true

SoftwareSerial esp8266(2,3);    //(TX,RX)

void setup() {
  pinMode(m11, OUTPUT);
  pinMode(m12, OUTPUT);
  pinMode(m21, OUTPUT);
  pinMode(m22, OUTPUT);
  pinMode(eA, OUTPUT);
  pinMode(eB, OUTPUT);
  analogWrite(eA,150);
  analogWrite(eB,150);
  
  Serial.begin(9600);
  esp8266.begin(115200);

  sendData("AT+RST\r\n",2000,DEBUG); // reset module
  sendData("AT+CWMODE=3\r\n",1000,DEBUG); // configure as access point
  sendData("AT+CIPMUX=1\r\n",1000,DEBUG); // configure for multiple connections
  sendData("AT+CIPSTART=0,\"UDP\",\"192.168.4.1\",80,80,2\r\n",1000,DEBUG);
  sendData("AT+CIPSEND=0,7,\"192.168.4.1\",80",1000,DEBUG); // turn on server on port 80
}
String command,response;
int choice;
void loop() {
  if(esp8266.available())
  {
    //command=Serial.readString();
    command=esp8266.read();
    String response = "";
    command+="\r\n";
    esp8266.print(command);
    if(esp8266.available())
    {
       if(esp8266.find("%")){
          response=esp8266.read();
          choice=response.toInt()-48;
          Serial.print(choice); 
          moveit(choice);
       }
    }
  }
}


String sendData(String command, const int timeout, boolean debug)
{
    String response = "";
    
    esp8266.print(command); // send the read character to the esp8266
    
    long int time = millis();
    
    while( (time+timeout) > millis())
    {
      while(esp8266.available())
      {
        
        // The esp has data so display its output to the serial window 
        char c = esp8266.read(); // read the next character.
        response+=c;
      }  
    }
    
    if(debug)
    {
      Serial.print(response);
    }
    
    return response;
}


///////////////////////////////////////////Move wheels/////////////////////
void moveit(int In)
  {
    if(In==3)            // Forward
    {
      digitalWrite(m11, HIGH);
      digitalWrite(m12, LOW);
      digitalWrite(m21, LOW);
      digitalWrite(m22, HIGH);
    }
    
     else if(In==4)            //backward
    {
      digitalWrite(m11, LOW);
      digitalWrite(m12, HIGH);
      digitalWrite(m21, HIGH);
      digitalWrite(m22, LOW);
    }
    
     else if(In==1)     // Left
    {
      digitalWrite(m11, HIGH);
      digitalWrite(m12, LOW);
      digitalWrite(m21, HIGH);
      digitalWrite(m22, LOW);
    }
    
     else if(In==2)     // Right
    {
      digitalWrite(m11, LOW);
      digitalWrite(m12, HIGH);
      digitalWrite(m21, LOW);
      digitalWrite(m22, HIGH);
    }
    
     else if(In==0)    // stop
    {
      digitalWrite(m11, LOW);
      digitalWrite(m12, LOW);
      digitalWrite(m21, LOW);
      digitalWrite(m22, LOW);
    }
    
    else
    {
      
    }
  }
