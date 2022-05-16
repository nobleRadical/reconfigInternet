# ReconfigureInternet
# author: nobleRadical
# version 0.0.1

import subprocess
import re

# TODO get SSID, password from file
ssid = "2.4 Managment"
pwd = "Nimrod123"

# TODO add network to supplicant
# check if network already exists in list first; get network ID
regex = f'(\\d)       {ssid}'
networkList = subprocess.run("wpa_cli -iwlan0 list_networks", shell=True, check=True, capture_output=True, text=True)
match = re.findall(regex, networkList.stdout)
print("regex:" + regex)
print("string:" + networkList.stdout)

if not match: # no matches
    print(match[0])
    # TODO create network
    addNetwork = subprocess.run(['wpa_cli', '-iwlan0', 'add_network'], shell=True, check=True, capture_output=True, text=True)
    networkID = addNetwork.stdout
    setNetworkSSID = subprocess.run(['wpa_cli', '-iwlan0', 'set_network', networkID, 'ssid', ssid], shell=True, check=True)
    setNetworkPwd = subprocess.run(['wpa_cli', '-iwlan0', 'set_network', networkID, 'psk', pwd], shell=True, check=True)
else:
    # make that network id the one to select.
    networkID = matches[0]


# TODO select network

selectNetwork = subprocess.run(['wpa_cli', '-iwlan0', 'select_network', networkID], shell=True, check=True)
