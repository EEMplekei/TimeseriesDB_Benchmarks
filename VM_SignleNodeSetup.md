# VM Single Node Setup:


## VM Specs:
- Ubuntu 22.04 Jammy Cloud
- 8 CPUs
- 16Gb Ram
- 30Gb Disk

## Installation and Setup Procces

### Updating

```
sudo apt update
```

```
sudo apt upgrade
```

To any popups we select OK
```
reboot
```
	
Now the kernel is version linux 5.15.0-89-generic
	
### Install InfluxDB
Source -> https://medium.com/yavar/install-and-setup-influxdb-on-ubuntu-20-04-22-04-3d6e090ec70c)
		
```
sudo apt update
```

```
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
```

```
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
```

```
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
```

```
sudo apt update
```

```
sudo apt install influxdb2
```

```
sudo systemctl start influxdb
```

```
sudo systemctl enable influxdb
```

```
sudo ufw allow 8086/tcp
```
		
Now we are able to access the influxDB UI through port 8086 and using the systems public IP address (or domain)
We set up username and password:
- Username: influxDB
- Password: m01g48p96
- Organization: NTUA
- Initial Bucket Name: system
- API Token: 

### Install PostgressDB:
Source -> https://docs.timescale.com/self-hosted/latest/install/installation-linux/

```
apt install gnupg postgresql-common apt-transport-https lsb-release wget
```

```
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
```

Press Enter

```
echo "deb https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main" | sudo tee /etc/apt/sources.list.d/timescaledb.list
```


```
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/timescaledb.gpg
```

```
sudo apt update
```

```
sudo apt upgrade
```

```
sudo apt install timescaledb-2-postgresql-14
```

```
sudo timescaledb-tune --quiet --yes
```

### Install Golang:
```
sudo apt update
```

```
sudo apt install golang-go
```
		
### Install TSBS:
```
sudo apt install make
```

```
sudo apt install golang-golang-x-tools
```

```
go install github.com/timescale/tsbs@latest
```

```
cd go/pkg/mod/github.com/timescale/tsbs@v0.0.0-20230921131859-37fced794d56/
```

```
sudo make all
```


```
echo "export PATH=$PATH:~/go/pkg/mod/github.com/timescale/tsbs@v0.0.0-20230921131859-37fced794d56/bin" >> ~/.profile
```

```
source ~/.profile
```

### Install python3 and pip3

```
which python3 (sudo apt install python3)
```

```
sudo apt-get -y install python3-pip
```

```
install with pip3 the requirements
```
	

### Generate Data:
```
cd ~/data_generate
```

```
bash data_timescale_small.sh
bash data_timescale_medium.sh
bash data_timescale_large.sh
bash data_influx_small.sh
bash data_influx_medium.sh
bash data_influx_large.sh
```

Now the data is in the ~/iot_data folder
		
#### Load data into DBs:

- Load into timescale:

	- cd into tsbs/scripts/load
	- get filename as command line parameters
	- change database name to have each data set in its own database
	- remove --partition-on-hostname,  --use_copy
- Load into InfluxDB: