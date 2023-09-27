'''
STATUS: CLOSED

created : 30-08-2023
LAST UPDATE:

Projekt zamknięty, zmigrował na scraping_rf4_v2

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

mycursor.execute('''SELECT web,cat,reg,fish,weight,place,bait,date,player, COUNT(*) as "COUNT" from test_new GROUP BY web,cat,reg,fish,weight,place,bait,date,player HAVING COUNT(*) >1''')
myres = mycursor.fetchall()
i = 0
usuniete = 0
print('do przejebania',len(myres))
for row in myres:
    i+=1
    if not (i %500):
        print('  sprawdzam i',i ,'z ',len(myres))     
    data = (row[7]).strftime('%Y-%m-%d')      
    mycursor.execute("SELECT id FROM test_new WHERE  web = '"+str(row[0])+"' AND cat = '"+str(row[1])+"' AND reg = '"+str(row[2])+"' AND fish = '"+str(row[3])+"' AND weight LIKE '"+str(row[4])+"'  AND place = '"+str(row[5])+"' AND bait = '"+str(row[6])+"' and date LIKE '"+str(row[7])+"'  and player = '"+str(row[8])+"'  ")
    
    myres2 = mycursor.fetchall()       
    if row[9] == len(myres2):
        for abc in range (1,len(myres2)):
            usuniete +=1            
            mycursor.execute("DELETE FROM test_new WHERE id = '"+str(myres2[abc][0])+"' ")
            mydb.commit()
            
  

print('usuniete',usuniete)





