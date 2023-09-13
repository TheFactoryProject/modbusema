

#!/usr/bin/python
import subprocess
import traceback
import requests
import MySQLdb
import time
import json
import sys
import os
import pprint



# Identificacion del equipo
EYE3_PRODUCT_ID = subprocess.check_output(['machineid'])[:-1].decode('utf-8')
EYE3_PRODUCT_NAME = subprocess.check_output(['machinename'])[:-1].decode('utf-8')
print(EYE3_PRODUCT_ID)
print(EYE3_PRODUCT_NAME)


# Local database config
MYSQL_HOSTNAME = 'localhost'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'claveEye3##'
MYSQL_DATABASE = 'ecom_data'

STATION_PUSH_URL = "https://us-central1-smart-try-33e78.cloudfunctions.net/webApi/api/ambientCubic"


def log(message):
                print(message)



def checkAndUpload( push_url=STATION_PUSH_URL, mysql_user=MYSQL_USERNAME, mysql_passwd=MYSQL_PASSWORD, mysql_host=MYSQL_HOSTNAME, mysql_db=MYSQL_DATABASE):

                log("checkAndUpload(%s,%s,%s,%s,%s)" % (push_url, mysql_user, mysql_passwd, mysql_host, mysql_db))

                sql = "select fecha, hora , microdatos, timestamp, id from ema_data where uploaded=0  order by timestamp limit 1"
                db = MySQLdb.connect(
                                user=mysql_user,
                                host=mysql_host,
                                passwd=mysql_passwd,
                                db=mysql_db
                )

                log(str(db))
                cursor = db.cursor()
                log(sql)
                cursor.execute(sql)
                db.commit()
               
                for record in cursor:
                                log("%s" % str(record))
                                (fecha, hora , microdatos, timestamp, id) = record
                                data_sensor= {
                                                "Fecha"         : record[0].strftime("%Y/%m/%d"),
                                                "Hora"          : str(record[1]),
                                                "MicroDatos"    : eval(record[2]),
                                                "Timestamp"     : record[3],
                                                "ID"            : EYE3_PRODUCT_ID,
                                                "Name"          : EYE3_PRODUCT_NAME
                                                }


                #pprint.pprint(data_sensor)
                #data_sensor = json.dumps(data_sensor)
                print(data_sensor)

                try:
                                r = requests.post(push_url, json = data_sensor, timeout=15)
                                
                                estado =(r.json())['status']
                                log(r.content)
                                
                                if estado =='success':
                                        sql = "UPDATE ema_data SET uploaded = %s WHERE id = %s"
                                        val = (1, record[4])
                                        print(data_sensor["Timestamp"])
                                        cursor.execute(sql, val)
                                        db.commit()

                except Exception as ex:
                                log('Error request')
                                print(ex)
                                pass

                cursor.close()
                db.close()



# Main loop
if __name__ == "__main__":
                log("---")
                log("STATION_PUSH_URL: [%s]" % STATION_PUSH_URL)
                log("MYSQL_USERNAME: [%s]" % MYSQL_USERNAME)
                log("MYSQL_PASSWORD: [%s]" % MYSQL_PASSWORD)
                log("MYSQL_HOSTNAME: [%s]" % MYSQL_HOSTNAME)
                log("MYSQL_DATABASE: [%s]" % MYSQL_DATABASE)
                log("---")


                while True:
                                try:            
                                                checkAndUpload(STATION_PUSH_URL, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOSTNAME, MYSQL_DATABASE)

                                except:
                                                log('error')
                                                e = sys.exc_info()
                                                log("dumping traceback for [%s: %s]" % (str(e[0].__name__), str(e[1])))
                                                traceback.print_tb(e[2])


                                log("sleeping 1 seconds")
                                time.sleep(15)

