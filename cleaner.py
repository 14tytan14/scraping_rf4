'''
STATUS: PISANY

created : 30-08-2023
LAST UPDATE:

POMYSL NA PROGRAM - ZASADY SA PROSTE - UROCHAMIAM BOCISZKA --
1a. czyszcze baze z duplikatów, tego krok 1 nie ma
'''



import sys
import mysql.connector

import datetime
import time
import re

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "123",
    database = "rf4")

mycursor = mydb.cursor()

print('')
print('/*********************Uruchomienie skryptu cleaner_rf4.py')

mycursor.execute('''SELECT web,cat,reg,fish,weight,place,bait,date,player, COUNT(*) as "COUNT" from rankingi GROUP BY web,cat,reg,fish,weight,place,bait,date,player HAVING COUNT(*) >1''')
myres = mycursor.fetchall()
i = 0
usuniete = 0
print('do przejebania',len(myres))
for row in myres:
    i+=1
    print('  sprawdzam i',i ,'z ',len(myres))     
    data = (row[7]).strftime('%Y-%m-%d')      
    mycursor.execute("SELECT id FROM rankingi WHERE  web = '"+str(row[0])+"' AND cat = '"+str(row[1])+"' AND reg = '"+str(row[2])+"' AND fish = '"+str(row[3])+"' AND weight LIKE '"+str(row[4])+"'  AND place = '"+str(row[5])+"' AND bait = '"+str(row[6])+"' and date LIKE '"+str(row[7])+"'  and player = '"+str(row[8])+"'  ")
    
    myres2 = mycursor.fetchall()       
    if row[9] == len(myres2):
        for abc in range (1,len(myres2)):
            usuniete +=1            
            mycursor.execute("DELETE FROM rankingi WHERE id = '"+str(myres2[abc][0])+"' ")
            mydb.commit()
            
  

print('usuniete',usuniete)
print(dupa)


sql = "INSERT INTO rankingi(web,cat,reg,fish,weight,place,bait,player,week,day,date) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (website, cat,reg, complete_data[a][0],complete_data[a][1], complete_data[a][2],complete_data[a][5], complete_data[a][3],'no_data', 'no_data',date_object)


#val = ('test','test2')
mycursor.execute(sql, val)
mydb.commit()
    

