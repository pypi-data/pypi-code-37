import time
import socket
import sys

try:
    from quarchpy.connection_specific.connection_USB import importUSB#, USBConn
except:
    print ("System Compatibility issue - Is your Python architecture consistent with the Operating System?")
    pass
from quarchpy.device import quarchDevice, quarchArray
from quarchpy.connection_specific.connection_Serial import serialList, serial
from quarchpy.device.quarchArray import isThisAnArrayController
from quarchpy.connection_specific.connection_USB import TQuarchUSB_IF

'''
Merge two dictionaries and return the result
'''
def mergeDict(x, y):
    if (y is None):
        return x
    else:
        merged = x.copy()
        merged.update(y)
        return merged

'''
Scan for Quarch modules across all available COM ports
'''
def list_serial(debuPrint=False):
    serial_ports = serialList.comports()
    serial_modules = dict()

    for i in serial_ports:
        try:
            ser = serial.Serial(i[0], 19200, timeout=0.5)
            ser.write(b'*serial?\r\n')            
            s = ser.read(size = 64)
            serial_module = s.splitlines()[1]
            
            serial_module = str(serial_module)[1:].replace("'","")
            
            if "QTL" not in serial_module:
                serial_module = "QTL" + serial_module
            
            module = str(i[0]), str(serial_module)

            if serial_module[7] == "-" and serial_module[10] == "-":
                serial_modules["SERIAL:" + str(i[0])] = serial_module

            ser.close()
        except:
            pass
    return serial_modules

'''
Scan for all Quarch devices available over USB
'''
def list_USB(debuPrint=False):    

    QUARCH_VENDOR_ID = 0x16d0
    QUARCH_PRODUCT_ID1 = 0x0449

    usb1 = importUSB()

    context = usb1.USBContext()
    usb_list = context.getDeviceList()

    if (debuPrint): print(usb_list)

    usb_modules = dict()
    hdList = []

    for i in usb_list:
        if hex(i.device_descriptor.idVendor) == hex(QUARCH_VENDOR_ID) and hex(i.device_descriptor.idProduct) == hex(QUARCH_PRODUCT_ID1):
            try:
                i_handle = i.open()
            except:
                if (debuPrint): print("FAIL - Module detected but handle will not open")
                usb_modules["USB:???"] = "LOCKED MODULE"
                continue

            try:
                module_sn = i_handle.getASCIIStringDescriptor(3)
                if "1944" in  module_sn: #if 1944 use enclosure number instead of seiral number
                    hdList.append(i)
            except:
                if (debuPrint): print("FAIL - Module detected but unable to get serial number")
                usb_modules["USB:???"] = "LOCKED MODULE"
                continue

            try:
                if (debuPrint): print(i_handle.getASCIIStringDescriptor(3) +" "+ i_handle.getASCIIStringDescriptor(2) +" "+ i_handle.getASCIIStringDescriptor(1))
            except:
                if (debuPrint): print("FAIL - Module detected but unable to get descriptors")
                usb_modules["USB:???"] = "LOCKED MODULE"
                continue

            if "QTL" not in module_sn:
                module_sn = "QTL" + module_sn.strip()    
            else:
                module_sn = module_sn.strip()

            if (debuPrint): print(module)
                
            usb_modules["USB:" + module_sn] = module_sn
                
            try:
                i_handle.close()
            except:
                continue

    # before returning the list of usb modules scan through the list for a 1944 create a quarch device and use sendCommand("*enclosure?")

    for module in hdList:

        QquarchDevice = None
        quarchDevice = None
        quarchDevice =  module
        QquarchDevice = TQuarchUSB_IF( context )
        QquarchDevice.connection = quarchDevice
        QquarchDevice.OpenPort()
        time.sleep(0.02) #sleep sometimes needed before sending comand directly after opening device
        QquarchDevice.SetTimeout(2000)
        serialNo = (QquarchDevice.RunCommand("*serial?")).replace("\r\n", "")
        enclNo = (QquarchDevice.RunCommand("*enclosure?")).replace("\r\n", "")

        keyToFind = "USB:QTL" + serialNo

        if keyToFind in usb_modules:
             del usb_modules[keyToFind]
             usb_modules["USB:QTL" + enclNo] = "QTL" + enclNo

        QquarchDevice.ClosePort()
    return usb_modules

'''
List all Quarch devices found over LAN, using a UDP broadcast scan
'''
def list_network(target_conn = "all", debugPring = False, lanTimeout = 1):
    # Create and configure the socket for broadcast.
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mySocket.settimeout(lanTimeout)

    # Broadcast the message.
    mySocket.sendto(b'Discovery: Who is out there?\0\n',('255.255.255.255', 30303))
        
    lan_modules = dict()
    
    # Receive messages until timeout.
    while True:
        network_modules = {}

        # Receive raw message until timeout, then break.
        try:
            msg_received = mySocket.recvfrom(256)
        except:
            break
        cont = 0

        for lines in msg_received[0].splitlines():
            if cont <= 1:
                index = cont
                data = repr(lines).replace("'","").replace("b","")
                cont += 1
            else:
                index = repr(lines[0]).replace("'","")
                data = repr(lines[1:]).replace("'","").replace("b","")

            network_modules[index] = data
                    
        # Filter the raw message to get the module and ip adress.
        module_name = network_modules.get(0).strip()
        
        ip_module = msg_received[1][0].strip()      
                
        try:
            # Add a QTL before modules without it.
            if "QTL" not in module_name.decode("utf-8"):
                module_name = "QTL" + module_name.decode("utf-8")
        except:
            # Add a QTL before modules without it.
            if "QTL" not in module_name:
                module_name = "QTL" + module_name
            
        # Checks if there's a value in the TELNET key.
        if (target_conn.lower() == "all" or target_conn.lower() == "telnet"):
            if network_modules.get("\\x8a") or network_modules.get("138"):
                # Append the information to the list.
                lan_modules["TELNET:" + ip_module] = module_name

        # Checks if there's a value in the REST key.
        if (target_conn.lower() == "all" or target_conn.lower() == "rest"):
            if network_modules.get("\\x84") or network_modules.get("132"):
                # Append the information to the list.
                lan_modules["REST:" + ip_module] = module_name

        # Checks if there's a value in the TCP key.
        if (target_conn.lower() == "all" or target_conn.lower() == "rest"):
            if network_modules.get("\\x85") or network_modules.get("133"):
                # Append the information to the list.
                lan_modules["TCP:" + ip_module] = module_name               
                
    return lan_modules

'''
Scans for Quarch modules across the given interface(s).  Returns a dictionary of
module addresses and serial numbers
'''
def scanDevices(target_conn = "all", debugPrint = False, lanTimeout=1, scanInArray=False, favouriteOnly = True):
    foundDevices = dict()
    scannedArrays = list()
    
    if target_conn.lower() == "all":
        foundDevices = list_USB()
        foundDevices = mergeDict (foundDevices, list_serial())
        foundDevices = mergeDict (foundDevices, list_network("all"))

    if target_conn.lower() == "serial":
        foundDevices =  list_serial()

    if target_conn.lower() == "usb":
        foundDevices =  list_USB()

    if target_conn.lower() == "rest" or target_conn.lower() == "telnet":
        foundDevices =  list_network(target_conn)

    if (scanInArray):
        for k, v in foundDevices.items():
            if (v not in scannedArrays):
                scannedArrays.append (v)
                if (isThisAnArrayController(v)):
                    scanDevice = quarchDevice(k)
                    scanArray = quarchArray(scanDevice)
                    scanDevices = scanArray.scanSubModules()
                    foundDevices = mergeDict (foundDevices, scanDevices)

    #Sort list in order of connection type preference. Can be changed by changing position in conPref list.
    index = 0
    sortedFoundDevices = {}
    conPref = ["USB" , "TCP" ,"SERIAL", "REST", "TELNET" ]
    while len(sortedFoundDevices) != len(foundDevices):
        for k, v in foundDevices.items():
            if conPref[index] in k:
                sortedFoundDevices[k] = v
        index += 1
    foundDevices = sortedFoundDevices

    if (favouriteOnly):
        #new dictionaty only containing one favourite connection to each device.
        favConFoundDevices = {}
        index = 0
        for k, v in sortedFoundDevices.items():
            if (favConFoundDevices == {} or not v in favConFoundDevices.values()):
                favConFoundDevices[k] = v
        foundDevices = favConFoundDevices

    return foundDevices

'''
Prints out a list of Quarch devices nicely onto the terminal, numbering each unit
'''
def listDevices(scanDictionary):
    if (not scanDictionary):
        print ("No quarch devices found to display")
    else:
        x = 1
        print ("Located Quarch devices")
        for k, v in scanDictionary.items():
            print (str(x) + ")\t" + v + "\t" + k)
            x += 1

'''
Requests the user to select one of the devices in the given list
'''
def userSelectDevice(scanDictionary):
    # Print the provided list of devices with a numbered prefix
    listDevices(scanDictionary)
    print ("")
    # Request user selection
    if sys.version_info.major >= 3:
        userStr = input("Enter the module number to use: ")
    else:
        userStr = raw_input("Enter the module number to use: ")

    # Validate as an int
    try:
        userNumber = int(userStr)
    except:
        raise ValueError ("User did not enter a valid integer")

    # Validate the range
    if (userNumber > len(scanDictionary) or userNumber < 1):
        raise ValueError ("User number is out of range")        

    # Return the address string of the selected module
    return list(scanDictionary)[userNumber-1]
