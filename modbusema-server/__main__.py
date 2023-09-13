#!/usr/bin/python
import subprocess
import sys
import time
import json
import socket
import MySQLdb
import datetime
import traceback
import threading
from time import time, sleep
import os
import pprint
import requests
import schedule

# Carga de datos cada 60 seg


# Identificacion del equipo
EYE3_PRODUCT_ID = subprocess.check_output(['machineid'])[:-1].decode('utf-8')
EYE3_PRODUCT_NAME = subprocess.check_output(['machinename'])[:-1].decode('utf-8')


class server():
    def __init__(self, log_id="Server"):
        self.log_id = log_id
        self.MYSQL_HOSTNAME = 'localhost'
        self.MYSQL_USERNAME = 'root'
        self.MYSQL_PASSWORD = 'claveEye3##'
        self.MYSQL_DATABASE = 'ecom_data'
        self.TABLE_DATABASE = 'station_data_new'
        self.TIPO_DATA = 'modbusema'

        self.data_dic = {}
        self.microdata = []
        self.bandera = False

        self.localIP = "127.0.0.1"
        self.localPort = 20003
        self.bufferSize = 1024
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDPServerSocket.bind((self.localIP, self.localPort))

        x = threading.Thread(target=self.readDataClient)
        x.start()
        self.lock = threading.Lock()

    def readDataClient(self):
        self.log("Server init listening [%s port %s]" % (self.localIP, self.localPort))
        while True:
            try:
                bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
                message = bytesAddressPair[0].decode('utf-8')
                msg = json.loads(message)
                header = msg['id']

                if header == 'ema':
                    self.updateData(msg)

            except:
                self.traceback()

    def updateData(self, data):
        try:
            data = data['msg']
            with self.lock:
                self.data_dic.update(data)
                self.bandera = True
                if len(self.data_dic) > 2:
                    self.microdata.append(self.data_dic.copy())

        except:
            print("Falla al decodificar serial")

    def insertData(self, data, time):
        try:
            if not data:
                print("Data está vacío. No se realizará la inserción en la base de datos.")
                return False
            now = datetime.datetime.now()
            print('now1->'+str(now))
            sql = "INSERT INTO ema_data (timestamp, fecha, hora, microdatos) VALUES (%s,%s,%s,%s)"
            conn = MySQLdb.connect(self.MYSQL_HOSTNAME, self.MYSQL_USERNAME, self.MYSQL_PASSWORD, self.MYSQL_DATABASE)
            cursor = conn.cursor()
            now = datetime.datetime.now()
            print('now->'+str(now))

            minuto_actual = now.replace(second=0, microsecond=0)
            one_minute_ago = minuto_actual + datetime.timedelta(minutes=1)

            # Obtener la hora formateada como cadena de texto
            hora = one_minute_ago.strftime("%H:%M:%S")
            fecha = now.strftime("%Y/%m/%d")
            print('hora' +str(hora))

            print(data)

            cursor.execute(sql, (
                int(one_minute_ago.timestamp()),
                fecha,
                hora,
                str(data)
            ))
            
            print('paso la consulta ')

            conn.commit()
            cursor.close()
            conn.close()
            return True

        except:
            self.traceback()
            return False

    def uploadDataToDatabase(self):
        if self.bandera and len(self.data_dic) > 2:
            print("### Ingreso a BD --->")
            fecha = datetime.datetime.now()
            minuto = fecha.replace(second=0, microsecond=0)
            hora = datetime.datetime.now().strftime('%H:%M:%S')
            print("minuto --->" + str(minuto))
            #print(self.microdata)

            if self.insertData(self.microdata, minuto):
                print("Conexión exitosa")
            else:
                data_sensor = {
                    "MicroDatos": self.microdata,
                    "Fecha": fecha.strftime("%Y/%m/%d"),
                    "Hora": hora,
                    "Timestamp": int(minuto.timestamp()),
                    "ID": EYE3_PRODUCT_ID,
                    "Name": EYE3_PRODUCT_NAME
                }
                print(data_sensor)
                try:
                    STATION_PUSH_URL = "https://us-central1-smart-try-33e78.cloudfunctions.net/webApi/api/ambientCubic"
                    r = requests.post(STATION_PUSH_URL, json=data_sensor, timeout=15)
                    estado = r.json()['status']
                    print("Estado -> " + str(estado))

                    if estado == 'success':
                        print("\033[1;34m" + "Datos publicados en el servidor" + '\033[0;m')
                    else:
                        print("Estado -> " + str(estado))

                except Exception as ex:
                    print(ex)
                    print("\033[1;31m" + "Error enviando data... " + '\033[0;m')

            self.microdata = []
            self.bandera = False
            self.data_dic = {}

    def start_scheduler(self):
    
        while True:
            sleep(1)
            now = datetime.datetime.now()
            if now.second == 59:
                self.uploadDataToDatabase()
                
            if now.second == 0:
               self.microdata = []

            print(now.second)
       
        
        

    def traceback(self):
        try:
            e = sys.exc_info()
            self.log("dumping traceback for [%s: %s]" % (str(e[0].__name__), str(e[1])))
            traceback.print_tb(e[2])
        except:
            foo = "bar"

    def log(self, message):
        dt = self.getDateTime()
        print("[%s] %s | %s" % (self.log_id, dt, message))
        with open("/log.txt", "a") as myfile:
            myfile.write("[%s] %s | %s\n" % (self.log_id, dt, message))

    def getDateTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(' ')
print(' ')
print('inicio funcion start')
now = datetime.datetime.now()
minute = now.minute
print(now.second)
while True:
    sleep(1)
    now = datetime.datetime.now()
    if now.second == 0:
        break
    print(now.second)
print('Iniciando la recoleccion de datos')

s = server()
s.start_scheduler()

