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

```bash
sudo apt update
sudo apt upgrade
```

To any popups we select OK
```bash
sudo reboot
```
	
Now the kernel is version linux 5.15.0-89-generic

### Install Influx:
The Influx database supports clustering mode only in the Enterprise edition which requires some financial resources but it also supports a free 14 trial that we used for our project and we got a license key from their website. The installation and configuration proccess is different for the meta (access) node and the data nodes and for this reason it is stated below seperately for both the meta and the data nodes.


### Install PostgressDB (all nodes):
Source -> https://docs.timescale.com/self-hosted/latest/install/installation-linux/

```bash
sudo apt install gnupg postgresql-common apt-transport-https lsb-release wget
```

```bash
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
```

Press Enter

```bash
echo "deb https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main" | sudo tee /etc/apt/sources.list.d/timescaledb.list
```


```bash
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/timescaledb.gpg
```

```bash
sudo apt update
sudo apt upgrade
```

```bash
sudo apt install timescaledb-2-postgresql-14
```

```bash
sudo timescaledb-tune --quiet --yes
```

```bash
sudo -i -u postgres
```
```bash
echo "shared_preload_libraries = 'timescaledb'" >> /etc/postgresql/14/main/postgresql.conf
exit
```
```bash
sudo /etc/init.d/postgresql restart
```
```bash
sudo -i -u postgres
psql
```
```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
```
```sql
ALTER USER postgres WITH PASSWORD 'password';
```

## Access Node Installation and configuration

### Install Golang:
```bash
sudo apt update
sudo apt install golang-go
```
		
### Install TSBS:
```bash
sudo apt install make
```

```bash
sudo apt install golang-golang-x-tools
```

```bash
go install github.com/timescale/tsbs@latest
```

```bash
cd go/pkg/mod/github.com/timescale/tsbs@v0.0.0-20230921131859-37fced794d56/
```

```bash
sudo make all
```


```bash
echo "export PATH=$PATH:~/go/pkg/mod/github.com/timescale/tsbs@v0.0.0-20230921131859-37fced794d56/bin" >> ~/.profile
```

```bash
source ~/.profile
```

### Clone this repository into the virtual machine
```bash
cd && git clone git@github.com:EEMplekei/TimeseriesDB_Benchmarks.git
```

### Timescale Configuration (Access Node)
- Open the following file with an editor like vim `/etc/postgresql/14/main/pg_hba.conf` and add the following line in the ipv4 configuration `host all all 10.0.0.0/24 trust`
- Open the following file with an editor like vim `/etc/postgresql/14/main/postgresql.conf` and make the following changes `jit = off` and `enable_partitiowise_aggragate = on`
- After that restart the postgresql service with the following command `sudo /etc/init.d/postgresql restart`
- After you have configured the data node configuration that is stated below procced to the following:
```bash
sudo -i -u postgres
psql
```
```sql
CREATE DATABASE benchmark_small;
\c benchmark_small;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT add_data_node('nodeB', '10.0.0.2');
SELECT add_data_node('nodeC', '10.0.0.3');
```
```sql
CREATE DATABASE benchmark_medium;
\c benchmark_medium;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT add_data_node('nodeB', '10.0.0.2');
SELECT add_data_node('nodeC', '10.0.0.3');
```
```sql
CREATE DATABASE benchmark_large;
\c benchmark_large;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
SELECT add_data_node('nodeB', '10.0.0.2');
SELECT add_data_node('nodeC', '10.0.0.3');
```

### Install and configure Influx Meta (Access Node):
In Influx configuration the access node is called Meta Node and it has a different installer from data node. The installation and configuration proccess for the meta node is the following:

```bash
wget https://dl.influxdata.com/enterprise/releases/influxdb-meta_1.11.3-c1.11.3-1_amd64.deb
sudo dpkg -i influxdb-meta_1.11.3-c1.11.3-1_amd64.deb
```

- After that open the following file with an editor like vim `/etc/influxdb/influxdb-meta.conf` and set `license-key = <your-license-key>` and set `hostname="enterprise-meta-A"`

- Open with an editor the file `/etc/hosts` with root privilage and add the lines `10.0.0.2 enterprise-data-B` and `10.0.0.3 enterprise-data-C` and `10.0.0.1 enterprise-meta-A`

- After you have configured the data nodes for Influx with the proccedure stated below, procced with the addition of the meta node and the data nodes in the cluster and after that show the configuration in order to ensure that everything is congfigured properly.
```bash
influxd-ctl add-meta enterprise-meta-A:8091
influxd-ctl add-data enterprise-data-B:8088
influxd-ctl add-data enterprise-data-C:8088
influxd-ctl show
```


## Data Node Configuration

### Timescale Configuration (Data Nodes)
- Open the following file with an editor like vim `/etc/postgresql/14/main/pg_hba.conf` and add the following line in the ipv4 configuration `host all all 10.0.0.0/24 trust`
- Open the following file with an editor like vim `/etc/postgresql/14/main/postgresql.conf` and make the following changes `listening_addresses = "*"` and `max_prepared_transactions = 150` and `wal_level = 'logical'`
- After that restart the postgresql service with the following command `sudo /etc/init.d/postgresql restart`

### Install and configure Influx Data (Data Node):
The installation and configuration proccess for the data node is the following:

```bash
wget https://dl.influxdata.com/enterprise/releases/influxdb-data_1.11.3-c1.11.3-1_amd64.deb
sudo dpkg -i influxdb-data_1.11.3-c1.11.3-1_amd64.deb
```

- After that open the following file with an editor like vim `/etc/influxdb/influxdb.conf` and set `license-path = <your-license-key>` and set `hostname="enterprise-data-B"` and `hostname="enterprise-data-C"` respectively.

- Open with an editor the file `/etc/hosts` with root privilage and add the lines `10.0.0.2 enterprise-data-B` and `10.0.0.3 enterprise-data-C` and `10.0.0.1 enterprise-meta-A`

## Generate Data:
We use the same data as with the single node testing locaded at `~/TimeseriesDB_Benchmarks/data_generate/iot_data`
```bash
cd ~/TimeseriesDB_Benchmarks/data_generate
bash data_generate.sh
```

## Load Data:

### Load into Timescale:

After the configuration of the data nodes and the configuration of the access node is done and the databases have been created in the configuration proccess in the access node (as we show above). We can continue in inserting the data into the databases. For this proccess we use the modified TSBS script that can be found in [load_timescaledb.sh](./data_load/load_timescaledb.sh) (We modified the `--do-create-db=false` and the `--replication-factor=1`).

```bash
cd ~/TimeseriesDB_Benchmarks/multi_node/data_load
bash load_timescaledb.sh small
bash load_timescaledb.sh medium
bash load_timescaledb.sh large
```
### Load into Influx:

Now that the cluster is configured properly we can load the data into the cluster. For this proccess we use the modified TSBS script that can be found in [load_influx.sh](./data_load/load_influx.sh) (We modified the `--replication-factor=1` and added the parameter `--urls=http://enterprise-data-B:8086,http://enterprise-data-C:8086` in order to connect to the data nodes).

```bash
cd ~/TimeseriesDB_Benchmarks/multi_node/data_load
bash load_influx.sh small
bash load_influx.sh medium
bash load_influx.sh large
```

## [Query Generation Proccess](../queries_generate/README.md):

We used the same queries with the single node testing
- Single queries
- Repetitive queries (10)

The following command will generate all queries for both influx and timescaledb for every dataset size.
```bash
cd ~/TimeseriesDB_Benchmarks/queries_generate
bash generate_queries_all.sh
```

## [Query Execution Proccess](./queries_execution/README.md):
Scripts for this proccess are [here](./queries_execution/). There are 2 scripts to run the queries that have already been generated by the previous proccess.
```bash
cd ~/TimeseriesDB_Benchmarks/multi_node/queries_execution
```

Once you have all the datasets in InfluxDB run the following command to execute the queries:
```bash
bash run_all_queries_influx.sh
```
Once you have all the datasets in TimescleDB run the following command to execute the queries:
```bash
bash run_all_queries_timescale.sh
```

The result of these commands will be in `~/TimeseriesDB_Benchmarks/multi_node/performance/queries`.