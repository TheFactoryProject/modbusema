import sys
import json
import socket
import datetime
import traceback
import threading
import os
from os.path import join
import time
import minimalmodbus  # Don't forget to import the library!!

def imprimir_rojo(texto):
    print("\033[1;31m"+texto+'\033[0;m')

def imprimir_azul(texto):
    print("\033[1;34m"+texto+'\033[0;m')

def imprimir_verde(texto):
    print("\033[1;32m"+texto+'\033[0;m')

def imprimir_amarillo(texto):
    print("\033[1;33m"+texto+'\033[0;m')

def discoveryPort(self, name, type_usb):
        id_vendor, id_product = self.getIdDevice(name)
        return self.find_tty_usb(id_vendor, id_product, type_usb)




def find_tty_usb(self, idVendor, idProduct, type_usb):

        for dnbase in os.listdir('/sys/bus/usb/devices'):
                dn = join('/sys/bus/usb/devices', dnbase)
                if not os.path.exists(join(dn, 'idVendor')):
                        continue
                idv = open(join(dn, 'idVendor')).read().strip()
                if idv != idVendor:
                        continue
                idp = open(join(dn, 'idProduct')).read().strip()
                if idp != idProduct:
                        continue
                for subdir in os.listdir(dn):
                        if subdir.startswith(dnbase+':'):
                                for subsubdir in os.listdir(join(dn, subdir)):
                                        if type_usb=="USB" and subsubdir.startswith('ttyUSB'):
                                                return join('/dev', subsubdir)
                                        elif type_usb== "ACM" and subsubdir.startswith('tty'):
                                                d = os.listdir(join(dn,subdir,subsubdir))
                                                print(d)
                                                return join('/dev', d[0])



class serialRead():
        def __init__(self, port='/dev/ttyUSB1', baudrate=9600, log_id="modbus"):
                self.baudrate = baudrate
                self.timeout = 0.5
                self.log_id = log_id
                self.port = port
                self.setup_sensor()

                self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
                self.serverAddressPort = ("127.0.0.1", 20003)

                x = threading.Thread(target=self.serialReadData)
                x.start()
                self.log("MODBus listener init [%s @ %s bps]" % (self.port, self.baudrate))
                self.data_dic = {}

        def setup_sensor(self):
                mb_address = 7

                self.sensy_boi = minimalmodbus.Instrument(self.port, mb_address)

                self.sensy_boi.serial.baudrate = self.baudrate
                self.sensy_boi.serial.bytesize = 8
                self.sensy_boi.serial.parity = minimalmodbus.serial.PARITY_NONE
                self.sensy_boi.serial.stopbits = 1
                self.sensy_boi.serial.timeout = self.timeout
                self.sensy_boi.mode = minimalmodbus.MODE_RTU

                self.sensy_boi.clear_buffers_before_each_transaction = True
                self.sensy_boi.close_port_after_each_call = True

        def serialReadData(self):
                while True:

                        try:
                                read_start = 40501 - 40001
                                data = self.sensy_boi.read_registers(read_start, 13, 3)

                                self.data_dic["wind_speed"] = data[0]/100
                                self.data_dic["wind_strenght"] = data[1]
                                self.data_dic["wind_dir_range"] = data[2]
                                self.data_dic["humitidy"] = data[4]/10
                                self.data_dic["temperature"] = data[5]/10
                                self.data_dic["noise"] = data[6]/10
                                self.data_dic["pm2_5"] = data[7]
                                self.data_dic["pm10"] = data[8]
                                self.data_dic["pressure"] = data[9]/10
                                self.data_dic["illuminance_hi"] = data[10]
                                self.data_dic["illuminance_lo"] = data[11]
                                self.data_dic["illuminance_prom"] = data[12]*100

                                self.data_dic["timestamp"] = int(time.time())
                                self.emit(self.log_id, json.dumps({'id': self.log_id, 'msg': self.data_dic}))

                                for clave, valor in self.data_dic.items():
                                        self.log(f"{clave}: {valor}")

                                self.data_dic = {}

                        except:
                                imprimir_rojo("Error en lectura del puerto serial")
                                imprimir_rojo("Verifica que el servicio no este corriendo")
                                self.traceback()
                                time.sleep(3)
                                def getDateTime(self):
                                        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def getDateTime(self):
                return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def getIdDevice(self, name):
                devices = subprocess.check_output('lsusb', shell=True).decode('utf-8').split('\n')
                for device in devices:
                        try:
                                data = device.split(" ")
                                if data[6] == name:
                                        IDs = data[5].split(":")
                                        id_vendor = IDs[0]
                                        id_product = IDs[1]
                                        return id_vendor, id_product
                        except:
                                continue

def log(self,message):
                dt = self.getDateTime()
                print("[%s] %s | %s" % (self.log_id, dt, message))
                with open ("/log.txt", "a") as myfile:
                        myfile.write("[%s] %s | %s\n" % (self.log_id, dt, message))



def traceback(self):
                try:
                        e = sys.exc_info()
                        self.log("dumping traceback for [%s: %s]" % (str(e[0].__name__), str(e[1])))
                        traceback.print_tb(e[2])
                except:
                        foo = "bar"

def emit(self, event, data=None, namespace=None, callback=None):
                bytesToSend = str.encode(data)
                self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)
                        #self.log("Trying to emit(%s,%s) but there is no socket.io server" % (str(event), str(data)))




serialRead()

