// This #include statement was automatically added by the Particle IDE.
#include "MQTT/MQTT.h"

// This #include statement was automatically added by the Particle IDE.
#include "MQTT/MQTT.h"

void callback(char* topic, byte* payload, unsigned int length);

void callback(char* topic, byte* payload, unsigned int length) {
}

char server[] = "mqtt.home.local";
String deviceID = "gamma";
MQTT client(server, 1883, callback);
int lastButtonState[5] = {LOW,LOW,LOW,LOW,LOW};
int connected = FALSE;
int lastconnected = FALSE;
int lifxswitch[5] = {D1,D1,D2,D3,D4};
char name[] = "gamma.home.local";
unsigned long t;
unsigned long deltat = 1000;        //keep alive time for mqtt queue
std::string message = "";
std::string topic = "";
char* chrtopic;

void setup() {
    // Connect mqtt to broker
    while(client.isConnected() == FALSE){
        client.connect(name);
        delay(1000);
    }
    for (int n=1; n < 5; n++){
    lastButtonState[n]=digitalRead(lifxswitch[n]);
    }
}

void loop(){
        // Process individual buttons and LED response
    for (int n=1; n < 5; n++){
        if (digitalRead(lifxswitch[n]) != lastButtonState[n]) {                              //Button state has changed.  For edge detection.
            if(client.isConnected() == FALSE){
                client.connect(name);
                topic = "particle/" + deviceID + "/#";
                chrtopic = strdup(topic.c_str());
                client.subscribe(chrtopic);
                free(chrtopic);
                topic = "particle/" + deviceID;
                chrtopic = strdup(topic.c_str());
                client.publish(chrtopic, "Gamma's back in business baby!");
                free(chrtopic);
            }
            topic = "particle/" + deviceID + "/buttons";                    //build topic
            char* chrtopic = strdup(topic.c_str());                         //need to convert string to char
            message = "Button " + String(n) + " Pressed";
            char* chrmessage = strdup(message.c_str());
            client.publish(chrtopic, chrmessage);                               //publish click to MQTT.
            Particle.publish("Pressed",chrmessage, 60, PRIVATE);      //publish button press to particle cloud for IFTTT to consume.
            free(chrmessage);
            free(chrtopic);                                                 //free memory. Not sure if this is needed.
            lastButtonState[n] = digitalRead(lifxswitch[n]);                             //for edge detection
            delay(20);                                                     //debounce
        }
    }
    delay(20);
    client.loop();
}
