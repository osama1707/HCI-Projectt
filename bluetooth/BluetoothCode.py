import bluetooth
from datetime import date
from datetime import datetime
#import bluetooth
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
     print(" %s - %s" % (addr, name))




today = date.today()
now = datetime.now()
target_name = "AirPods"
target_address = None

nearby_devices = bluetooth.discover_devices()



for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print ("found target bluetooth device with address ", (target_address))
else:
    print ("could not find target bluetooth device nearby")


#with open("C:\\Users\\osama\\Desktop\\BluezAddresses.txt", "w") as f:
    #for addr in nearby_devices:
       # f.write(addr)
       # f.write("\n")


print("Writing in text file is Done!!")

g = open('C:\\Users\\osama\\Desktop\\BluezAddresses.txt','r')

for line in g:
        #line = g.readline()
    #print(line)
    x = line.strip()
    y= x.split(",")
    
    for addr in nearby_devices:
        #print(addr)
        #print(" %s - %s" % (addr, name))

        if addr == y[0]:
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("Found this adress",addr, "at this date and time =", dt_string)
            print(y)
            with open("C:\\Users\\osama\\Desktop\\AddressesStartTime.txt", "w") as f:
                f.write(addr)
                f.write(",")
                f.write((y[1]))
                f.write(",")
                f.write(dt_string)
                f.write("\n")
            break  
        else:
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("Not found any adress at this date and time =", dt_string)
            with open("C:\\Users\\osama\\Desktop\\AddressesFinishTime.txt", "w") as f:
                f.write(addr)
                f.write(",")
                f.write((y[1]))
                f.write(",")
                f.write(dt_string)
                f.write("\n") 
g.close()

       

            

    

  
   
   
   
   
    #contents = f.read()
    #print("Iam found address-->",contents)
    #print("Here the adrsses-->",addr)
    #print("ddddd:",contents.strip())  


    #if addr==contents.strip():
        #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #print("Found this adress",addr, "at this date and time =", dt_string)
        #print("Today's date:", today)
    #else:
        #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
       # print("Not found any adress at this date and time =", dt_string)            
        #print("not found any adress")
    #for addr in nearby_devices:
    #for contents in f: