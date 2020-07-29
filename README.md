# Wifi Fake Access Point Generator

###### This is an old script, found in the maze of my hard disk, created to experiment with the Scapy library. It has been adapted to use Python 3 instead of Python 2.7. Command-line options have been added.



## Installation

```pip install -r requirements.txt```

## Usage

First of all set your wifi interface to monitor mode. This script does not set it automatically.
With Ubuntu 18.04 I used the following commands

```
ifconfig <your-interface-name> down
iwconfig <your-interface-name> mode monitor
ifconfig <your-interface-name> up
```
After this step you can run apspam.py. Use ```apspam.py --help``` for a list of command line options


```--iface <your-interface-name>```
Select monitor mode interface

```--ssid SSID```           
Set a static fake ssid to probe (default: random ssid for each beacon)

```--mac_address MAC_ADDRESS```
Set a static fake mac address to probe (default: random mac address for each beacon)

```--count COUNT```         
Set the number of beacons to probe (Default: 1). Set count to -1 for a loop

```--list LIST```           
pass a ssid - mac address list to use in json format (check ap.json-example for more information)
