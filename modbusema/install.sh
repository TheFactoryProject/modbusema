#!/bin/bash

# Comprobar si se ingresó contraseña
if [ -z "$1" ]; then
    echo "Por favor, ingrese una contraseña para Mysql."
    exit 1
fi

CONTRASENIA=$1

# Define el nombre del servicio aquí:
SERVICE_NAME="modbusEmaEsp32"
DIRECTORY_NAME="modbusema"

mysql -u root -p[$CONTRASENIA] < install.sql
systemctl stop dio-$SERVICE_NAME
systemctl disable dio-$SERVICE_NAME
rm /etc/systemd/system/dio-$SERVICE_NAME
systemctl daemon-reload
cp /srv/dio/$DIRECTORY_NAME/dio-$SERVICE_NAME.service /etc/systemd/system/dio-$SERVICE_NAME.service
systemctl enable dio-$SERVICE_NAME
systemctl restart dio-$SERVICE_NAME


SERVICE_NAME="modbusema-autoupload"
DIRECTORY_NAME="modbusema-autoupload"

mysql -u root -p[$CONTRASENIA] < install.sql
systemctl stop dio-$SERVICE_NAME
systemctl disable dio-$SERVICE_NAME
rm /etc/systemd/system/dio-$SERVICE_NAME
systemctl daemon-reload
cp /srv/dio/$DIRECTORY_NAME/dio-$SERVICE_NAME.service /etc/systemd/system/dio-$SERVICE_NAME.service
systemctl enable dio-$SERVICE_NAME
systemctl restart dio-$SERVICE_NAME



SERVICE_NAME="modbusema-server"
DIRECTORY_NAME="modbusema-server"

mysql -u root -p[$CONTRASENIA] < install.sql
systemctl stop dio-$SERVICE_NAME
systemctl disable dio-$SERVICE_NAME
rm /etc/systemd/system/dio-$SERVICE_NAME
systemctl daemon-reload
cp /srv/dio/$DIRECTORY_NAME/dio-$SERVICE_NAME.service /etc/systemd/system/dio-$SERVICE_NAME.service
systemctl enable dio-$SERVICE_NAME
systemctl restart dio-$SERVICE_NAME
