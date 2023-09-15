import pyrebase
import random
import serial

# Set the serial port and baud rate
SERIAL_PORT = '/dev/ttyACM0'  # Replace with the actual serial port
BAUD_RATE = 9600


SERIAL_PORTFIXED = "/dev/ttyACM2"
BAUD_RATEFIXED = 115200

# Open the serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

ser1 = serial.Serial(SERIAL_PORTFIXED, BAUD_RATEFIXED)

config = {
  "apiKey":"AIzaSyBiualaUsrhKMrCZn8rangGoZqlYecdpWg",
  "authDomain": "iot-thing-7736f.firebaseapp.com",
  "databaseURL": "https://iot-thing-7736f-default-rtdb.europe-west1.firebasedatabase.app",
  "storageBucket": "iot-thing-7736f.appspot.com"
  }

firebase = pyrebase.initialize_app(config)

db = firebase.database()

#mobile1 = ser.readline().decode().strip()

#print(mobile1)


#fix1 = ser1.readline().decode().strip()

#print(fix1)

while True:

    dataMobile = {
    "Mobile" : ser.readline().decode().strip()      }
    
    temp = dataMobile['Mobile'].split('=')
    
    dataFixed = {
        "Fixed" : ser1.readline().decode().strip()
        }
    tempFix = dataFixed['Fixed'].split(':')
    if(len(tempFix) == 1):
        continue
    print(tempFix)
    
    print(dataMobile)
    
    updateMobile = {
        temp[0]: temp[1]
    }
    updateFix = {
        tempFix[0]: tempFix[1]    
    }

    #db.child(“Status").push(data)

    db.update(updateMobile)
    db.update(updateFix)