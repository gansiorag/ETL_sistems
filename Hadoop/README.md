# Key commands
* Start process
  * ./start-dfs.sh
  * ./start-yarn.sh
* jps - показывает какие процессы запущены
* для псевдораспределенного режима верно следующее по default
  * Hadoop NameNode UI - http://localhost:9870
  * DataNodes directly from your browser - http://localhost:9864
  * The YARN Resource Manager - http://localhost:8088
# Install Hadoop
## Install OpenJDK on Ubuntu
* sudo apt update
* sudo apt install openjdk-8-jdk -y
* java -version; javac -version
## Install OpenSSH on Ubuntu
* sudo apt install openssh-server openssh-client -y
## Create Hadoop User
* sudo adduser hdoop
* su - hdoop
## Enable Passwordless SSH for Hadoop User
Generate an SSH key pair and define the location is is to be stored in:
* ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
* cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
* chmod 0600 ~/.ssh/authorized_keys
* ssh localhost
## Download and Install Hadoop on Ubuntu
* https://hadoop.apache.org/releases.html
* wget ******* url from first step *******
* tar xzf hadoop-3.2.1.tar.gz
## Single Node Hadoop Deployment (Pseudo-Distributed Mode)
A Hadoop environment is configured by editing a set of configuration files:
    * bashrc
    * hadoop-env.sh
    * core-site.xml
    * hdfs-site.xml
    * mapred-site-xml
    * yarn-site.xml
### Configure Hadoop Environment Variables (bashrc)
* sudo nano .bashrc
* insert code 
```
#Hadoop Related Options <br>
export HADOOP_HOME=/home/hdoop/hadoop-3.2.1
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```
* source ~/.bashrc
### Edit hadoop-env.sh File
* sudo nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
* insert string -<br>
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
* Use the provided path to find the OpenJDK directory with the following command:<br>
readlink -f /usr/bin/javac
### Edit core-site.xml File
* sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
* Insert code:
```
<configuration>
<property>
  <name>hadoop.tmp.dir</name>
  <value>/home/hdoop/tmpdata</value>
</property>
<property>
  <name>fs.default.name</name>
  <value>hdfs://127.0.0.1:9000</value>
</property>
</configuration>
```
### Edit hdfs-site.xml File
* sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
* Insert code:
```
<configuration>
<property>
  <name>dfs.data.dir</name>
  <value>/home/hdoop/dfsdata/namenode</value>
</property>
<property>
  <name>dfs.data.dir</name>
  <value>/home/hdoop/dfsdata/datanode</value>
</property>
<property>
  <name>dfs.replication</name>
  <value>1</value>
</property>
</configuration>
```
### Edit mapred-site.xml File
* sudo nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
* Insert code:
```
<configuration> 
<property> 
  <name>mapreduce.framework.name</name> 
  <value>yarn</value> 
</property> 
</configuration>
```
### Edit yarn-site.xml File
* sudo nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
```
<configuration>
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>127.0.0.1</value>
</property>
<property>
  <name>yarn.acl.enable</name>
  <value>0</value>
</property>
<property>
  <name>yarn.nodemanager.env-whitelist</name>   
  <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PERPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
</configuration>
```
### Format HDFS NameNode
* hdfs namenode -format
