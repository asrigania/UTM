#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 18);
IPAddress server(192, 168, 1, 10);

void callback(char* topic, byte* payload, unsigned int length) {  
  char masuk[100];
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    masuk[i] = (char)payload[i];
    Serial.print((char)payload[i]);
  }
  Serial.println();

  char act_stat=masuk[0];
  String blade_Slider=String( String(masuk[0]) + String(masuk[1]) + String(masuk[2]) + String(masuk[3]) );
  if (((String)topic=="blade_stat") && (act_stat=='1')){digitalWrite(blade,LOW);}
  else if (((String)topic=="blade_stat") && (act_stat=='0')){digitalWrite(blade,HIGH);}
  if (((String)topic=="captor_stat") && (act_stat=='1')){digitalWrite(captor,LOW);}
  else if (((String)topic=="captor_stat") && (act_stat=='0'))digitalWrite(captor,HIGH);
  if (act_stat=='x'){
    digitalWrite(blade,HIGH);
    digitalWrite(captor,HIGH);
  }
  if((String)topic=="blade_Vpos"){
    int Slider_Val = map(blade_Slider.toInt(), 00, 1023, 00, 255);
    analogWrite(motorA, Slider_Val);
  }
}

EthernetClient ethClient;
PubSubClient client(ethClient);

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("arduinoClient")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic","hello world");

      client.subscribe("engine_stat");
//      client.subscribe("act_stat");
      client.subscribe("blade_stat");
      client.subscribe("blade_Vpos");
      client.subscribe("captor_stat");

      client.subscribe("left_blade");
      client.subscribe("right_blade");
      client.subscribe("blade_input");
      client.subscribe("en_loop_blade");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

char msgBuffer[20];
void data_pub(){
  client.publish("voltage_supply",dtostrf(voltage_ac, 10, 2, msgBuffer));
  //client.publish("yaw","yaw");
///  client.publish("yaw_body",dtostrf(yaw, 10, 2, msgBuffer));
  //client.publish("pitch","pitch");
//  /client.publish("pitch_body",dtostrf(pitch, 10, 2, msgBuffer));
  //client.publish("roll","roll");
// / client.publish("roll_body",dtostrf(roll, 10, 2, msgBuffer));
  client.publish("roll_blade",dtostrf(blade_pos, 10, 2, msgBuffer));
  client.publish("pressure",dtostrf(pressure_val, 10, 2, msgBuffer));
  client.publish("depth",dtostrf(depth_val, 10, 2, msgBuffer));
  client.publish("trench_depth",dtostrf(trenchdepth_val, 10, 2, msgBuffer));
  client.publish("UTM_active",dtostrf(UTM_stat, 10, 2, msgBuffer));
  client.publish("captor",dtostrf(captor_stat, 10, 2, msgBuffer));
}

void eth_setup()
{
//  Serial.begin(57600);

  client.setServer(server, 1883);
  client.setCallback(callback);

  Ethernet.begin(mac, ip);
  // Allow the hardware to sort itself out
  delay(1500);
}

void eth_UTM()
{
  if (!client.connected()) {
    reconnect();
  }

//  if(topic
  
  client.loop();
}
