#!/usr/bin/env python
from lifxlan import *
import sys
import MySQLdb
import myinit


def main():
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    user = myinit.user()
    password = myinit.password()
    ipaddress = myinit.get_lan_ip()
    cnx = MySQLdb.connect(user=user, passwd=password, host='127.0.0.1', db='automation')
    cursor=cnx.cursor()



    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    # get devices
    devices = lifx.get_lights()
    print("\nFound {} light(s):\n".format(len(devices)))
    for d in devices:
        print(d)
        label = d.get_label()
        ip = d.get_ip_addr()
        mac = d.get_mac_addr()
        cursor.execute("""INSERT INTO lifxlan (label, ip, mac) VALUES('%s','%s','%s')""" % (label,ip,mac))
        cnx.commit()

if __name__=="__main__":
    main()
