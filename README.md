This is my e-commerce website using Python, Flask, SQLalchemy (and also HTML, CSS, Jinja).
sudo apt update
sudo apt install python3.10
python3.10 --version
sudo apt install -y net-tools
python3 -m venv venv
sudo apt-get install python3.8-venv
python3 -m venv venv
source venv/bin/activate
pip3 install flask
sudo apt-get install python3-dev
sudo apt-get install libmysqlclient-dev
sudo apt-get install zlib1g-dev
sudo apt-get install pkg-config
sudo pip3 install mysqlclient
sudo apt-get install python3-mysql.connector
deactivate
...
$ python3
>>> import MySQLdb
>>> MySQLdb.version_info 
(2, 0, 3, 'final', 0)
Install SQLAlchemy module version 1.4.x
$ sudo pip3 install SQLAlchemy
...
$ python3
>>> import sqlalchemy
>>> sqlalchemy.__version__ 
'1.4.22'
