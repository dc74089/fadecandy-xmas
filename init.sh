/usr/local/bin/fcserver /home/pi/fadecandy-xmas/server-config.json > /var/log/fcserver.log 2>&1 &
python /home/pi/fadecandy-xmas/runme.py >/var/log/fadecandy-xmas.log 2>&1 &
