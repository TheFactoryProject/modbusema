systemctl stop dio-ema-server
systemctl disable dio-ema-server
rm /etc/systemd/system/dio-ema-server.service
systemctl daemon-reload
cp /srv/dio/ema-server/dio-ema-server.service /etc/systemd/system/dio-ema-server.service
systemctl enable dio-ema-server
systemctl restart dio-ema-server