import BluetoothCode
import bluetooth

# the address of the Bluetooth device you want to connect to
address = "44:1B:88:E2:33:99"

# the Bluetooth service you want to connect to on the device
port = 1

# create a Bluetooth socket and connect to the device
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((address, port))

# send data to the device
sock.send('Hello, world!')

# receive data from the device
data = sock.recv(1024)
print(f'Received: {data}')

# close the socket when done
sock.close()




#import bluetooth

#bd_addr = "44:1B:88:E2:33:99"

#port = 5000

#sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#sock.connect((BluetoothCode.target_address, port))

#sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#sock.connect((bd_addr, port))

#sock.send("hello!!")

#sock.close()