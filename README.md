# RaspberryPI-IoT
An IoT project utilizing RS232(UART),FLASK,MYSQL and rendering a website on a RPI.

##Index

* What you need?.
* Introduction.
* Hardware Connections.
* Serial Read and Write.
* Connecting to MYSQL DB.
* Flask.
* Website.



## What you need?
* RaspberryPI with access to a network.
* USB to RS232 cable.
* Python programming skills.

##Introduction
This project uses RaspberryPI 3 to host a website from which it receives and records data/commands and send them serially using UART.
Meaning you can **control** a machine that receives serial commands **remotely**. 
> In this repository the RPI is controlling an **Automated Carousel**.

The diagram below illustrates the system in which the RPI is embedded in,
![System_Overview](/System_Overview.png?raw=true "System Overview")

The RPI will:
* In normal mode..
  * Pass serial commands from Chromeleon to the Carousel.
* In debug mode..
  * Pass serial commands from the website to the Carousel.
  
> Commands sent are in ASCII format.


##Hardware Connections
Since the RPI doesn't support RS-232 connection, a USB to RS-232 is connected as follows.

![RS-232](/RS232.png?raw=true "RS-232 Connection")

As for internet access, if you are using RPI3 it has a built in Wifi module. For older versions you may want to buy a wifi module or use ethernet.

##Serial Read and Write
This file will be used by **FLask** to create an object of PiSerial to send ASCII commands received from the browser.
> You can find this code in this repo under **pi_serial.py**

```python
import serial
import time

#-----Instantiating a serial write object
serial_Write_Object = serial.Serial(
            port='/dev/serial0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
       )

#-----Instantiating a serial Read object
serial_Read_Object = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
       )

#--------Declaring a new Class for serial comm.--------
class PiSerial(object):
   
    def serialWrite(self, text):
        serial_Write_Object.write(text)

    def serialRead(self):
       	readValue = serial_Read_Object.readline()
       	print readValue
        return readValue

```


##Connecting to MYSQL DB

Before you can connect to the DB, you need to install MYSQL server.

*	On your RPI, run this command. It’ll probably prompt you to create a root password for the database. 
```
sudo apt-get install mysql-server 
```

*	Now that you have the server running, you need the python library that links python to the database.
```
sudo apt-get install python-mysqldb
```

* To access MYSQL, In terminal run
```
$ mysql -u root –p
```
and it’ll prompt you to enter your password created earlier. 


* Now To create a database, i named mine **piDB**
```
create database YOUR_DB_NAME_HERE; ....Dont forget the semicolon
```

* To create a user that can access this DB and grant him permission
```
create user ‘user1’@localhost’ indentified by ‘George’; 
use piDB;
grant all on piDB.* to ‘user1’@’localhost’;
```

*	To create our desired table, i created a table called commandsFrequency since i am counting the number of commands being sent
```
 create table commandsFrequency(Commands varchar(255), NumberOfRuns int); 
```
NumberOfRuns indicates the number of times each command in the table is run/sent.


* To insert values into this table
```
Insert into commandsFrequency(Command,NumberOfRuns) values (%s,'0')",command
```
This will insert a new row into the table with columns being **Command** (the command to add) and its **NumberOfRuns** (NOR).


below is the python code to connect to and use this Database:

```python
import MySQLdb

#-----Creating a link to database
db = MySQLdb.connect('localhost','user1','piUser','piDB');
#(host,user,pass,database)

#-----Creating a cursor object which allows us to use mysql database commands
cursor = db.cursor();


class PiDatabase(object):
   
    def incrementNOR(self,command):     #increment NumberOfRuns
        cursor.execute("update commandsFrequency set NumberOfRuns = NumberOfRuns +1 where Command=%s",command)
        db.commit()

    def addCommand(self,command):
        cursor.execute("Insert into commandsFrequency(Command,NumberOfRuns) values (%s,'0')",command )
        db.commit()
 

```
This file will be used by **FLask** to create an object of PiSerial to send ASCII commands received from the browser.
> You can find this code in this repo under **pi_database.py**



##Flask
Flask is a python microframework and it is well documented on their [website](http://flask.pocoo.org/).

> View the [**FLask_Illustration**](/Flask_Illustration.pdf) file that is available with this repo for more details on how flask is implemented in this project.

Below is the python code to use Flask

```python

#-----Import the serial communication, Database class and flask library
from pi_serial import PiSerial
from pi_database import PiDatabase
from flask import *


#-----Instantiate a PiSerial object and a Flask object
serial_object = PiSerial()
database_object = PiDatabase()
piApp = Flask(__name__)


#-----Declaring the main route
@piApp.route("/")
def main():
    return render_template('main.html')

#-----Declaring the serialSend route
@piApp.route("/serial/sendSerial/<serialText>", methods=['POST'])
def sendSerial(serialText):
    serial_object.serialWrite(serialText)   # send serially
    database_object.incrementNOR(serialText)# increment NOR for that command
    return ('',204)         


#-----Declaring the addCommand route
@piApp.route("/database/addCommand/<command>", methods=['POST'])
def addCommand(command):
    database_object.addCommand(command)# add new command to database
    return ('',204)



if __name__ == "__main__":
    piApp.run(host= "0.0.0.0", port=80, debug=True)
    #host=0.0.0.0 to allow the server public for other users on network
    
```

##Website
> **NOTE**: This file should be placed in a directory called **templates** for flask to render it.

Since i am not a professional front end designer, my webpage is simple but you can use a framework such as [**bootsrap**](http://getbootstrap.com/) for aesthetic purposes.

```html
<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">


        
    </head>
    <body>

	 <h1>Pi Serial Control </h1>
        <p><input type="text" name="serialText" id='serialText' value="Enter text here">
	 	<button type='button' id='send'>Send</button> </p>
	<p><input type="text" name="addCommand" id='addCommand' value="addCommand">
	 	<button type='button' id='add'>Add</button></p>
	

        <script src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.12.0.min.js"><\/script>')</script>


        <script>
	$(document).ready(function(){
		$('#send').click(function() {
			var x = $('#serialText').val();
                        console.log('sending..'+x);
			$.post('/serial/sendSerial/' + x);
		
		});
                $('#add').click(function() {
			var x = $('#addCommand').val();
                        console.log('sending..'+x);
			$.post('/database/addCommand/' + x);
		
		});

	});
	</script>
      
      
    </body>
</html>


```
