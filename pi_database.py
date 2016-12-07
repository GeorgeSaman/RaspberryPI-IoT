import MySQLdb

#-----Creating a link to database
db = MySQLdb.connect('localhost','user1','piUser','piDB');
#(host,user,pass,database)

#-----Creating a cursor object which allows us to use mysql database commands
cursor = db.cursor();


class PiDatabase(object):
    def checkIfPresent(self,entry): 
        pass
    def incrementNOR(self,command):     #increment NumberOfRuns
        cursor.execute("update commandsFrequency set NumberOfRuns = NumberOfRuns +1 where Command=%s",command)
        db.commit()

    def addCommand(self,command):
        cursor.execute("Insert into commandsFrequency(Command,NumberOfRuns) values (%s,'0')",command )
        db.commit()
 
    def displayTable(self):
        pass
    
    
