# The are all to creater ETL sistems
* Hadoop tutorial with MapReduce, 
* HDFS, 
* Spark, 
* Flink, 
* Hive,
* HBase,
* MongoDB,
* Cassandra, 
*  Kafka
* + more! Over 25 technologies.

## Как установить Apache Hadoop в Ubuntu 20.04 LTS
* sudo apt update
* sudo apt upgrade
### Установка Java 
sudo apt install default-jdk default-jre <br>
java -version
### Создайте пользователя Hadoop
* sudo adduser hadoop
* sudo addgroup hadoopgroup
* sudo usermod -a -G hadoopgroup hadoopuser
* su - hadoopuser
* ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
* cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
* chmod 0600 ~/.ssh/authorized_keys <br>
После этого проверьте SSH без пароля с помощью следующей команды:
* ssh localhost<br>

## Настройка Hadoop настраивается с помощью следующих файлов:

    * bashrc
    * hadoop-env.sh
    * core-site.xml
    * hdfs-site.xml
    * mapred-site-xml
    * yarn-site.xml <br>

### Configure Hadoop Environment Variables (bashrc)
sudo nano .bashrc<br>

>"Hadoop Related Options"
>export HADOOP_HOME=/home/hdoop/hadoop-3.2.1<br>
>export HADOOP_INSTALL=$HADOOP_HOME<br>
>export HADOOP_MAPRED_HOME=$HADOOP_HOME<br>
>export HADOOP_COMMON_HOME=$HADOOP_HOME<br>
>export HADOOP_HDFS_HOME=$HADOOP_HOME<br>
>export YARN_HOME=$HADOOP_HOME<br>
>export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native<br>
>export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin<br>
>export HADOOP_OPTS"-Djava.library.path=$HADOOP_HOME/lib/nativ"<br>

Крайне важно применить изменения к текущей рабочей среде, используя следующую команду:<br>
 **source ~/.bashrc**
### Edit hadoop-env.sh File
При настройке кластера Hadoop с одним узлом вам необходимо определить, какая реализация 
Java будет использоваться. 
Используйте ранее созданную переменную <br> 
$HADOOP_HOME для доступа к файлу hadoop-env.sh:
