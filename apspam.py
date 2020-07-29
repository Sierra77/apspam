#!/usr/bin/env python

import string
import random
import argparse
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap
from scapy.sendrecv import sendp
import json


def load_config():
    options = argparse.ArgumentParser()
    options.add_argument("--iface",
                         help="Set monitor mode interface")
    options.add_argument("--list",
                         help="pass a ssid / mac address list to use")
    options.add_argument("--ssid",
                         help="Set a static fake ssid to probe (default: random ssid for each beacon)")
    options.add_argument("--mac_address",
                         help="Set a static fake mac address to probe (default: random mac address for each beacon)")
    options.add_argument("--count",
                         type=int,
                         help="Set the number of beacons to probe (Default: 1). Set count to -1 for a loop")

    return options.parse_args()


def random_name():
    return ''.join(random.choice(string.ascii_letters) for x in range(random.randint(0, 25)))


def random_mac():
    raw_mac = [
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]

    return ':'.join(map(lambda x: "%02x" % x, raw_mac))


def send_beacon(iface, ssid, mac_address, count, list_path):
    if count is None:
        count = 1

    if ssid is None:
        ssid = random_mac()

    if mac_address is None:
        mac_address = random_mac()

    if list_path is not None:
        file = open(list_path)
        data = json.load(file)

        for single_count in range(0, count):
            for single_data in data:
                dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2='22:22:22:22:22:22',
                              addr3=single_data['mac'])

                beacon = Dot11Beacon(cap='ESS+privacy')

                essid = Dot11Elt(ID='SSID', info=single_data['ssid'], len=len(single_data['ssid']))

                rsn = Dot11Elt(ID='RSNinfo', info=(
                    '\x01\x00'
                    '\x00\x0f\xac\x02'
                    '\x02\x00'
                    '\x00\x0f\xac\x04'
                    '\x00\x0f\xac\x02'
                    '\x01\x00'
                    '\x00\x0f\xac\x02'
                    '\x00\x00'))

                frame = RadioTap() / dot11 / beacon / essid / rsn

                frame.show()

                sendp(frame, iface=iface, count=1)

    if list_path is None:
        dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2='22:22:22:22:22:22', addr3=mac_address)

        beacon = Dot11Beacon(cap='ESS+privacy')

        essid = Dot11Elt(ID='SSID', info=ssid, len=len(ssid))

        rsn = Dot11Elt(ID='RSNinfo', info=(
            '\x01\x00'
            '\x00\x0f\xac\x02'
            '\x02\x00'
            '\x00\x0f\xac\x04'
            '\x00\x0f\xac\x02'
            '\x01\x00'
            '\x00\x0f\xac\x02'
            '\x00\x00'))

        frame = RadioTap() / dot11 / beacon / essid / rsn

        frame.show()

        sendp(frame, iface=iface, count=count)


def main():
    config = load_config()
    send_beacon(config.iface, config.ssid, config.mac_address, config.count, config.list)


if __name__ == '__main__':
    main()
