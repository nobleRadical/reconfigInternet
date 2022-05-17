# ReconfigureInternet
# author: nobleRadical
# version 0.0.1

import subprocess
import re
import os

# get filePath to external drive: ri.txt
filePath: str = None
for root, dirs, files in os.walk("/media/pi", followlinks=True):
        for name in files:
            if name == "ri.txt":
                filePath = os.path.join(root, name)
                break

def ReInt():
    # get SSID, password from file

    # get file: take as string

    file = open(filePath, 'r')
    fileString = file.read()
    file.close()

    # get ssid, password from file
    ssid = re.findall(r'[sS][sS][iI][dD]:(?: ?| *{)([^{}\n]*)(?:}|\n)', fileString)
    pwd = re.findall(r'[pP][aA][sS][sS][wW][oO][rR][dD]:(?: ?| *{)([^{}\n]*)(?:}|\n)', fileString)
    assert ssid, "SSID not found in file"
    assert pwd, "password not found in file"
    ssid = ssid[0]
    pwd = pwd[0]
    print("connecting to " + ssid)
    print(f'password: {pwd}')
    return

    # add network to supplicant
    # check if network already exists in list first; get network ID
    regex = f'(\\d)\\t{ssid}'
    networkList = subprocess.run("wpa_cli -iwlan0 list_networks", shell=True, check=True, capture_output=True, text=True)
    match = re.findall(regex, networkList.stdout)

    if not match: # no matches
        print("No known network by that name. Creating...")
        # create network
        addNetwork = subprocess.run('wpa_cli -iwlan0 add_network', shell=True, check=True, capture_output=True, text=True)
        networkID = addNetwork.stdout
        setNetworkSSID = subprocess.run(f'wpa_cli -iwlan0 set_network {networkID} ssid {ssid}', shell=True, check=True)
        setNetworkPwd = subprocess.run(f'wpa_cli -iwlan0 set_network {networkID} psk {pwd}', shell=True, check=True)
    else:
        # make that network id the one to select.
        print("Found known network.")
        networkID = match[0]

    print("Network id: ", networkID)

    # select network
    print("reconfiguring...")
    selectNetwork = subprocess.run(f'wpa_cli -iwlan0 select_network {networkID}', shell=True, check=True)

def main():
    assert filePath, "input file (ri.txt) not found"
    print(filePath)
    message: str
    try:
        ReInt()
    except Exception as e:
        # write error type, message to file
        print("wow, that didn't work. whoops!")
        message = f'ERROR {e}'
    else:
        # no errors, write success to file
        print("succeeded.")
        message = 'OK'
    finally:
        # write message to file
        print(message)
        file = open(filePath, 'r')
        lines = file.readlines()
        file.close()
        changed = False
        for i in range(len(lines)):
            if re.match(r'\[STATUS\]', lines[i]):
                lines[i] = f'[STATUS] {message}'
                changed = True
        if changed: # there was a [STATUS] line
            file = open(filePath, 'w')
            file.writelines(lines)
            file.close()
            
        else: # there was none; create one
            file = open(filePath, 'a')
            file.write(f'\n[STATUS] {message}')
            file.close()
           


if __name__ == "__main__":
    main()