#!/usr/bin/env python
version = 0.1

import lifx
import paho.mqtt.client as mqtt
from lifxlan import *
import time
import MySQLdb
import MySQLdb.cursors
import myinit
import thread

deviceID = "InternetButton"
deviceID2 = "gamma"
deviceID3 = "bluzgateway"
mqttclient = "mqtt.home.local"
robeBluzID = "b1e24886b1ae937c1e168b1e"



def get_bulb(label):
    cursor.execute("""SELECT * FROM lifxlan WHERE label='%s'""" %(label))
    row = cursor.fetchone()
    mac = row['mac']
    ip = row['ip']
    bulb = Light(mac,ip)
    return bulb



def toggle_power(bulb,duration = 0):
    power_state = bulb.get_power()
    if bulb.get_power() > 0:
        bulb.set_power("off",duration)
    else:
        bulb.set_power("on")


def toggle_kitchen(button):
    if button == 1:
        label = "Family1"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,30000))
        label = "Family2"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,30000))
        label = "Family3"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,30000))
        label = "Family4"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,30000))

    if button == 2:
        label = "Dining1"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))

        label = "Dining2"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))


    if button == 3:
        label = "Kitchen3"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))

        label = "Kitchen5"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))


    if button == 4:
        label = "Kitchen1"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))

        label = "Kitchen2"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))

        label = "Kitchen4"
        bulb = get_bulb(label)
        thread.start_new_thread(toggle_power,(bulb,))



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("particle/#", 2)
    client.subscribe("lifx/#", 2)
    client.publish("particle/status","lifxinternetbutton is alive, version" + str(version))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload)
    topic = msg.topic
    print topic
    print payload
    print " "
    try:
        cursor.execute('''INSERT INTO mqtt (topic, message) VALUES('%s','%s')''' % (payload, topic))
        cnx.commit()
    except:
        print "SQL error trying to insert into mqtt table:"
        print "topic: " + topic
        print "payload: " + payload
    try:

        if str(msg.topic) == "particle/" + str(deviceID2) + "/buttons":
            if str(msg.payload) == 'Button 1 Pressed':
                button = 1
            if str(msg.payload) == 'Button 2 Pressed':
                button = 2
            if str(msg.payload) == 'Button 3 Pressed':
                button = 3
            if str(msg.payload) == 'Button 4 Pressed':
                button = 4
            toggle_kitchen(button)

        if str(msg.topic) == "particle/" + str(deviceID3) + "/buttons":
            if str(msg.payload) == 'Button ' + robeBluzID + "|B2 Pressed":
                label = "Robe"
                bulb = get_bulb(label)
                thread.start_new_thread(toggle_power,(bulb,))




    except KeyError:
        print "Hokey lightbulb code shat it's duds on a KeyError!"
        cursor.execute("""INSERT INTO error (app, error) VALUES ('%s','%s')""" % ('lifxinternetbutton.py','KeyError'))
        cnx.commit()
        raise
    except AttributeError:
        cursor.execute('''INSERT INTO error (app, error) VALUES ('%s','%s')''' % ('lifxinternetbutton.py', 'AttributeError'))
        cnx.commit()
        raise
    except KeyboardInterrupt:
        print "Keyboard Interrupt.  Exiting"

user = myinit.user()
password = myinit.password()
ipaddress = myinit.get_lan_ip()
cnx = MySQLdb.connect(user=user, passwd=password, host='127.0.0.1', db='automation',cursorclass=MySQLdb.cursors.DictCursor)
cursor=cnx.cursor()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttclient, 1883, 60)
client.loop_forever()
