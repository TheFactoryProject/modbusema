"""
######################################################################

Simple Modbus Sensor Polling Code
Coded By "The Intrigued Engineer" over a coffee

Minimal Modbus Library Documentation
https://minimalmodbus.readthedocs.io/en/stable/

Thanks For Watching!!!

######################################################################
"""

import minimalmodbus # Don't forget to import the library!!

mb_address = 1 # Modbus address of sensor

start_offset = 40501
start_addr = start_offset - 40001

sensy_boi = minimalmodbus.Instrument('/dev/ttyUSB1',mb_address) # Make an "instrument" object called sensy_boi (port name, slave address (in decimal))

sensy_boi.serial.baudrate = 4800                                # BaudRate
sensy_boi.serial.bytesize = 8                                   # Number of data bits to be requested
sensy_boi.serial.parity = minimalmodbus.serial.PARITY_NONE      # Parity Setting here is NONE but can be ODD or EVEN
sensy_boi.serial.stopbits = 1                                   # Number of stop bits
sensy_boi.serial.timeout  = 0.5                                 # Timeout time in seconds
sensy_boi.mode = minimalmodbus.MODE_RTU                         # Mode to be used (RTU or ascii mode)

# Good practice to clean up before and after each execution
sensy_boi.clear_buffers_before_each_transaction = True
sensy_boi.close_port_after_each_call = True

## Uncomment this line to print out all the properties of the setup a the begining of the loop
print(sensy_boi)

print("")
print("Requesting Data From Sensor...") # Makes it look cool....

# NOTE-- Register addresses are offset from 40001 so inputting register 0 in the code is actually 40001, 3 = 40004 etc...

## Example of reading SINGLE register
## Arguments - (register address, number of decimals, function code, Is the value signed or unsigned)
## Uncomment to run this to just get temperature data

#single_data= sensy_boi.read_register(1, 1, 3, False)
#print (f"Single register data = {single_data}")

# Get list of values from MULTIPLE registers
# Arguments - (register start address, number of registers to read, function code)
data =sensy_boi.read_registers(start_addr, 13, 3)

print("")
print(f"Raw data is {data}") # Shows the raw data list for the lolz

# Process the raw data by deviding by 10 to get the actual floating point values
#hum = data[0]/10
#temp = data[1]/10
wind_speed = data[0]/100
wind_strenght = data[1]
wind_dir_range = data[2]
wind_dir_angle = data[3]
humitidy = data[4]/10
temperature = data[5]/10
noise = data[6]/10
pm2_5 = data[7]
pm10 = data[8]
pressure = data[9]/10
illuminance_hi = data[10]
illuminance_lo = data[11]
illuminance_prom = data[12]*100


# Print out the processed data in a little table
# Pro-tip > \u00B0 is the unicode value for the degree symbol which you can see before the "C" in temperature
print("-------------------------------------\n")
print('''data; wind_speed: {}; wind_strenght: {}; wind_dir_range: {}; humitidy: {}; temperature: {};  noise: {}; pm2_5: {}; pm10: {}; pressure: {}; illuminance_hi: {}; illuminance_lo: {}; illuminance_prom: {}\n'''.format(wind_speed, wind_strenght, wind_dir_range, humitidy, temperature, noise, pm2_5, pm10, pressure, illuminance_hi, illuminance_lo, illuminance_prom))
#print(f"Temperature = {temp}\u00B0C")
#print(f"Relative Humidity = {hum}%")
print("-------------------------------------\n")
print("")

# Piece of mind close out
sensy_boi.serial.close()
print("Ports Now Closed")

