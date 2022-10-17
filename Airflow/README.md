# How install Airflow on Windows

It exist three ways to install Airflow on OS Windows.

Metod First.

1. Start PowerShell from administrator.
2. dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
3. creater directory on C:\Users\NameUser\airflow
4. In Microsoft Store find the Ubuntu and Installer
5. sudo apt update && sudo apt upgrade
6. sudo nano /etc/wsl.conf <br>
   castom wsl - https://habr.com/ru/post/481746/
7. [automount]<br>
root = /<br>
options = "metadata"
8. reload Ubuntu
   All right. Your have way to windows

Next step install environment.
1. sudo apt install python3-pip
2. pip3 install apache-airflow[gcp, statsd, sentry]
3. pip3 install pyspark
4. export AIRFLOW_HOME=/mnt/c/Users/alwin/auirflow/
5. nano ~/.bashrc and add  -> export AIRFLOW_HOME=/mnt/c/Users/alwin/auirflow/
6. check - echo $AIRFLOW_HOME -> /mnt/c/Users/alwin/
7. airflow db init
