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
    

# Definitions
# NOR = NumberOfRuns
