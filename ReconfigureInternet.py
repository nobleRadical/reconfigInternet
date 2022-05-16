# ReconfigureInternet
# author: nobleRadical
# version 0.0.1

import subprocess

# TODO get SSID, password from file
ssid = "2.4 Managment"
pwd = "Nimrod123"

# write to config file: /home/pi/wpaConfig.conf
configHandle = open("/home/pi/wpaConfig.conf", 'w')
configString = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
        ssid={ssid}
        psk={pwd}
}""".format(ssid=ssid, pwd=pwd)
configHandle.write(configString)
configHandle.close()

# run bash commands

subprocess.run("wpa_cli terminate", Shell=True, check=True)
subprocess.run("wpa_supplicant -B -c/home/pi/wpaConfig.conf -iwlan0", check=True)


