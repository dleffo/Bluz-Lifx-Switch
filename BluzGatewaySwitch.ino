// This #include statement was automatically added by the Particle IDE.
#include "MQTT/MQTT.h"

// This #include statement was automatically added by the Particle IDE.
#include "bluz_gateway/bluz_gateway.h"
#define POLL_CONNECTIONS_INTERVAL 30000

SYSTEM_MODE(AUTOMATIC);
bluz_gateway gateway;

void callback(char* topic, byte* payload, unsigned int length);

void callback(char* topic, byte* payload, unsigned int length) {
}

char server[] = "mqtt.home.local";
String deviceID = "bluzgateway";
MQTT client(server, 1883, callback);
int lastButtonState[5] = {LOW,LOW,LOW,LOW,LOW};
int connected = FALSE;
int lastconnected = FALSE;
int lifxswitch[5] = {D1,D1,D2,D3,D4};
char name[] = "bluzgateway.home.local";
unsigned long t;
unsigned long deltat = 1000;        //keep alive time for mqtt queue
std::string message = "";
std::string topic = "";
char* chrtopic;
std::string pressed = "";
int debouncefix;
int debounce = 200;



void handle_custom_data(uint8_t *data, uint16_t length) {
    //if you use BLE.send from any connected DK, the data will end up here
    Particle.publish("Bluz Custom Data", String((char*)data));
    pressed = String((char*)data);
}

void handle_gateway_event(uint8_t event, uint8_t *data, uint16_t length) {
    //will return any polling queries from the gateway here
}

void setup() {
    gateway.init();

    //register the callback functions
    gateway.register_data_callback(handle_custom_data);
    gateway.register_gateway_event(handle_gateway_event);
    // Connect mqtt to broker
    while(client.isConnected() == FALSE){
        client.connect(name);
        delay(10);
    }
    debouncefix = millis();


}

long timeToNextPoll = POLL_CONNECTIONS_INTERVAL;
void loop() {
    if (client.isConnected()){
        client.loop();
        connected = TRUE;
        if (connected != lastconnected){
            Spark.publish("reconnected", NULL, 60, PRIVATE);    //publish the event for IFTTT to consume
            lastconnected = connected;
        }
    }
    gateway.loop();
    if (pressed != ""){
        if (millis()-debouncefix > debounce){
            topic = "particle/" + deviceID + "/buttons";                    //build topic
            char* chrtopic = strdup(topic.c_str());                         //need to convert string to char
            message = "Button " + pressed + " Pressed";
            char* chrmessage = strdup(message.c_str());
            client.publish(chrtopic, chrmessage);                               //publish click to MQTT.
            Particle.publish("Pressed",chrmessage, 60, PRIVATE);      //publish button press to particle cloud for IFTTT to consume.
            free(chrmessage);
            free(chrtopic);                                                 //free memory. Not sure if this is needed.
            debouncefix = millis();
        }
        pressed = "";
    }
    if (millis() > timeToNextPoll) {
        timeToNextPoll = POLL_CONNECTIONS_INTERVAL + millis();
        gateway.poll_connections();
    }
    if(client.isConnected() == FALSE){
        client.connect(name);
    }

}
