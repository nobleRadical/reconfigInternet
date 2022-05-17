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
    removeBool = re.findall(r'[pP][aA][sS][sS][wW][oO][rR][dD][Rr][eE][mM][oO][vV][eE]', fileString) # are we removing a network?
        
    assert ssid, "SSID not found in file"
    ssid = ssid[0]
    if pwd:
        pwd = pwd[0]
    else:
        pwd = None
    print("connecting to " + ssid)

    # add network to supplicant
    # check if network already exists in list first; get network ID
    regex = f'(\\d)\\t{ssid}'
    networkList = subprocess.run("wpa_cli -iwlan0 list_networks", shell=True, check=True, capture_output=True, text=True)
    match = re.findall(regex, networkList.stdout)

    if not match: # no matches
        if removeBool:
            raise NameError("Tried to remove a network, but no known network by that name.")
        
        print("No known network by that name. Creating...")
        # create network
        addNetwork = subprocess.run('wpa_cli -iwlan0 add_network', shell=True, check=True, capture_output=True, text=True)
        networkID = addNetwork.stdout
        setNetworkSSID = subprocess.run(f'wpa_cli -iwlan0 set_network {networkID} ssid "{ssid}"', shell=True, check=True)
        if pwd:
            setNetworkPwd = subprocess.run(f'wpa_cli -iwlan0 set_network {networkID} psk "{pwd}"', shell=True, check=True)
            passwordSet = True
        else:
            passwordSet = False
        networkAdded = True
    else:
        # make that network id the one to select.
        networkID = match[0]
        print(f"Found known network.")
        if removeBool:
            print("Removing network from list.")
            removeNetwork = subprocess.run(f'wpa_cli -iwlan0 remove_network {networkID}', shell=True, check=True)
            return False, False, True # network removed
        networkAdded = False
        passwordSet = False
        

    print("Network id: ", networkID)

    # select network
    print("reconfiguring...")
    selectNetwork = subprocess.run(f'wpa_cli -iwlan0 select_network {networkID}', shell=True, check=True)
    return networkAdded, passwordSet, False

def main():
    assert filePath, """input file (ri.txt) not found. File format should be: 
    ssid: <ssid>
    password: <password> OR PASSWORDREMOVE (to remove a network)

    [STATUS]
    """
    print(filePath)
    message: str
    try:
        networkAdded, passwordSet, networkRemoved = ReInt()
    except Exception as e:
        # write error type, message to file
        message = f'ERROR {e}'
    else:
        # no errors, write success to file
        message = 'OK'
        if networkAdded:
            message += ' network_added'
        else:
            message += ' network_found'
        if passwordSet:
            message += ' password_set'
        if networkRemoved:
            message += ' network_removed'
    finally:
        # write message to file
        print("message: " + message)
        file = open(filePath, 'r')
        lines = file.readlines()
        file.close()
        newlines = [""] * len(lines)
        changed = False
        for i in range(len(lines)):
            if re.match(r'\[STATUS\]', lines[i]):
                newlines[i] = f'[STATUS] {message}'
                changed = True
                break
            else:
                newlines[i] = lines[i]
            
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