systemctl stop dio-ema-autoupload
systemctl disable dio-ema-autoupload
rm /etc/systemd/system/dio-ema-autoupload.service
systemctl daemon-reload
cp /srv/dio/autoupload_ema/dio-ema-autoupload.service /etc/systemd/system/dio-ema-autoupload.service
systemctl enable dio-ema-autoupload
systemctl restart dio-ema-autoupload