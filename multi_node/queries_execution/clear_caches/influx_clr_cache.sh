sudo service influxdb stop
sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
sudo service influxdb start
