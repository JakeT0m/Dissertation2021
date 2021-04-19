from bluezero import microbit
from time import sleep
from time import time
from datetime import datetime

#Setting up the microbits
ubit1 = microbit.Microbit(adapter_addr='DC:A6:32:7C:35:D2',
                         device_addr='D6:CA:A9:57:F7:72')
ubit2 = microbit.Microbit(adapter_addr='DC:A6:32:7C:35:D2',
                         device_addr='E4:E1:14:75:E1:E5')

#Setting up any files or variables
loop = True
time = datetime.__str__(datetime.today())
name = "Accelerometer data: " + time
bad = ' '
good = '_'
name = name.replace(bad,good)
bad = ':'
good = '_'
name = name.replace(bad,good)
file = open(name, "w")
file.close()
#Connecting to microbits
print("Attempting to connect to Microbit 1...")
try:
    ubit1.connect()
    print("Connected!")
except:
    print("Could not connect to Microbit 1")

print("Attempting to connect to Microbit 2...")
try:
    ubit2.connect()
    print("Connected!")
except:
    print("Could not connect to Microbit 2")

#gathering the data
while loop:
    file = open(name, 'a')
    x1, y1, z1 = ubit1.accelerometer
    time = datetime.__str__(datetime.utcnow())
    x2, y2, z2 = ubit2.accelerometer
    file.write('time: ' + time + '        x1: ' + str(x1) + '    y1: '+ str(y1) + '    z1: ' + str(z1) +'\n')
    file.write('time: ' + time + '        x2: ' + str(x2) + '    y2: '+ str(y2) + '    z2: ' + str(z2) +'\n')
    print('x1: ', x1, 'y1: ', y1, 'z1: ', z1)
    print('x2: ', x2, 'y2: ', y2, 'z2: ', z2)
    if (ubit1.button_a >= 1 and ubit1.button_b >= 1) or (ubit2.button_a >= 1 and ubit2.button_b >= 1):
        loop = False

#Disconnecting from the microbits and the file
try:
    file.close()
    print("File closed")
except:
    print("File unable to be closed, data may have been lost")
try:
    ubit1.disconnect()
    print("Microbit 1 sucessfully disconnected")
except:
    print("Could not disconnect from Microbit 1")
    
try:
    ubit2.disconnect()
    print("Microbit 2 sucessfully disconnected")
except:
    print("Could not disconnect from Microbit 2")