# Multi-Node Node Setup:


## VM Specs:
- 3 VMs
- Ubuntu 22.04 Jammy Cloud
- 4 CPUs
- 4Gb Ram
- 30Gb Disk

The three VMs

- Node A

        Domain: snf-42806.ok-kno.grnetcloud.net
        Password: 4oTyYffoDg

- Node B
  
        Domain: snf-42798.ok-kno.grnetcloud.net
        Password: HaPI7BusVR
      

- Node C

        Domain: snf-42792.ok-kno.grnetcloud.net
        Password: mArHF77Hly

## Installation and Setup Procces for all nodes

### Updating

```
sudo apt update
sudo apt upgrade
```

To any popups we select OK
```
sudo reboot
```
	
Now the kernel is version linux 5.15.0-89-generic
	
### Install InfluxDB (all nodes):


### Install PostgressDB (all nodes):
Source -> https://docs.timescale.com/self-hosted/latest/install/installation-linux/

```
sudo apt install gnupg postgresql-common apt-transport-https lsb-release wget
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
sudo apt upgrade
```

```
sudo apt install timescaledb-2-postgresql-14
```

```
sudo timescaledb-tune --quiet --yes
```

```
sudo -i -u postgres
```
```
echo "shared_preload_libraries = 'timescaledb'" >> /etc/postgresql/14/main/postgresql.conf
exit
```
```
sudo /etc/init.d/postgresql restart
```
```
sudo -i -u postgres
psql
```
```
CREATE EXTENSION IF NOT EXISTS timescaledb;
```
```
ALTER USER postgres WITH PASSWORD 'password';
```

## Access Node Installation and configuration

### Install Golang:
```
sudo apt update
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

### Clone this repository into the virtual machine
To do this, the machine has to have SSH access to the private repository and this can be done by generating an SSH key-pair using `ssh-keygen` and adding it to the repository SSH keys.
```
cd && git clone git@github.com:EEMplekei/TimeseriesDB_Benchmarks.git
```

### Timescale Configuration (Access Node)


### InfluxDB Configuration (Access Node)



## Data Node Configuration

### Timescale Configuration (Data Nodes)


### Influx Configuration (Data Nodes)


## Generate Data:
```
cd ~/TimeseriesDB_Benchmarks/single_node/data_generate
bash data_generate.sh
```

Now the data is in the ~/TimeseriesDB_Benchmarks/single_node/iot_data folder
