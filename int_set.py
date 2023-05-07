# ReconfigureInternet
# author: nobleRadical
# version 0.0.1

import subprocess
import sys

interface = "wlan0" ##CHANGEME
network_id = 0 ##CHANGEME

def strToHex(string):
    out = ""
    for char in string:
        out += hex(ord(char))[2:4]
    return out

def connect(interface, network_id, ssid, password):
    ssid_hex = strToHex(ssid)
    setNetworkSSID = subprocess.run(f'sudo /usr/sbin/wpa_cli -i{interface} set_network {network_id} ssid "{ssid_hex}"', shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if setNetworkSSID.returncode != 0:
        print(setNetworkSSID.stdout)
        print("____________________")
        print(setNetworkSSID.stderr)
    if password:
        setNetworkPwd = subprocess.run(f'sudo /usr/sbin/wpa_cli -i{interface} set_network {network_id} psk \'"{password}"\'', shell=True, check=True)
    setNetworkSSID = subprocess.run(f'sudo /usr/sbin/wpa_cli -i{interface} enable_network {network_id}"', shell=True, check=True)
    setNetworkSSID = subprocess.run(f'sudo /usr/sbin/wpa_cli -i{interface} select_network {network_id}"', shell=True, check=True)
    
        
def main():
    ssid = sys.argv[1]
    if len(sys.argv) > 2:
        password = sys.argv[2]
    connect(interface, network_id, ssid, password or None)

if __name__ == "__main__":
    main()