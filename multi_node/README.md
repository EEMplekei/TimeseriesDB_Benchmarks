# Multi-Node Node Setup:
![](https://i.imgur.com/KN8YUhy.png)

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

### Install Influx:
The Influx database supports clustering mode only in the Enterprise edition which requires some financial resources but it also supports a free 14 trial that we used for our project and we got a license key from their website. The installation and configuration proccess is different for the meta (access) node and the data nodes and for this reason it is stated below seperately for both the meta and the data nodes.


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
- Open the following file with an editor like vim `/etc/postgresql/14/main/pg_hba.conf` and add the following line in the ipv4 configuration `host all all 10.0.0.0/24 trust`
- Open the following file with an editor like vim `/etc/postgresql/14/main/postgresql.conf` and make the following changes `jit = off` and `enable_partitiowise_aggragate = on`
- After that restart the postgresql service with the following command `sudo /etc/init.d/postgresql restart`
- After you have configured the data node configuration that is stated below procced to the following:
```
sudo -i -u postgres
psql
```
```
CREATE DATABASE benchmark_small;
\c benchmark_small;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT add_data_node('nodeB', '10.0.0.2');
SELECT add_data_node('nodeC', '10.0.0.3');
```
```
CREATE DATABASE benchmark_medium;
\c benchmark_medium;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT add_data_node('nodeB', '10.0.0.2');
SELECT add_data_node('nodeC', '10.0.0.3');
```
```
CREATE DATABASE benchmark_large;
\c benchmark_large;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT add_data_node('nodeB', '10.0.0.2');
SELECT add_data_node('nodeC', '10.0.0.3');
```

### Install and configure Influx Meta (Access Node):
In Influx configuration the access node is called Meta Node and it has a different installer from data node. The installation and configuration proccess for the meta node is the following:

```
wget https://dl.influxdata.com/enterprise/releases/influxdb-meta_1.11.3-c1.11.3-1_amd64.deb
sudo dpkg -i influxdb-meta_1.11.3-c1.11.3-1_amd64.deb
```

- After that open the following file with an editor like vim `/etc/influxdb/influxdb-meta.conf` and set `license-key = <your-license-key>` and set `hostname="enterprise-meta-A"`

- Open with an editor the file `/etc/hosts` with root privilage and add the lines `10.0.0.2 enterprise-data-B` and `10.0.0.3 enterprise-data-C` and `10.0.0.1 enterprise-meta-A`

## Data Node Configuration

### Timescale Configuration (Data Nodes)
- Open the following file with an editor like vim `/etc/postgresql/14/main/pg_hba.conf` and add the following line in the ipv4 configuration `host all all 10.0.0.0/24 trust`
- Open the following file with an editor like vim `/etc/postgresql/14/main/postgresql.conf` and make the following changes `listening_addresses = "*"` and `max_prepared_transactions = 150` and `wal_level = 'logical'`
- After that restart the postgresql service with the following command `sudo /etc/init.d/postgresql restart`

### Install and configure Influx Data (Data Node):
The installation and configuration proccess for the data node is the following:

```
wget https://dl.influxdata.com/enterprise/releases/influxdb-data_1.11.3-c1.11.3-1_amd64.deb
sudo dpkg -i influxdb-data_1.11.3-c1.11.3-1_amd64.deb
```

- After that open the following file with an editor like vim `/etc/influxdb/influxdb.conf` and set `license-path = <your-license-key>` and set `hostname="enterprise-data-B"` and `hostname="enterprise-data-C"` respectively.

- Open with an editor the file `/etc/hosts` with root privilage and add the lines `10.0.0.2 enterprise-data-B` and `10.0.0.3 enterprise-data-C` and `10.0.0.1 enterprise-meta-A`

## Generate Data:
```
cd ~/TimeseriesDB_Benchmarks/multi_node/data_generate
bash data_generate.sh
```

Now the data is in the `~/TimeseriesDB_Benchmarks/multi_node/iot_data` folder

## Load Data:

### Load into Timescale:

After the configuration of the data nodes and the configuration of the access node is done and the databases have been created in the configuration proccess in the access node (as we show above). We can continue in inserting the data into the databases. For this proccess we use the modified TSBS script that can be found in [load_timescaledb.sh](./data_load/load_timescaledb.sh) (We modified the `--do-create-db=false` and the `--replication-factor=1`).

```
cd ~/TimeseriesDB_Benchmarks/multi_node/data_load
bash load_timescaledb.sh small
bash load_timescaledb.sh medium
bash load_timescaledb.sh large
```
### Load into Influx:


## Query Generation

We use the same proccess with the single node.

## Query Execution

