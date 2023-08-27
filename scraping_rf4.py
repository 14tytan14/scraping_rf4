'''
STATUS: PISANY

created : 27-08-2023
LAST UPDATE:

POMYSL NA PROGRAM - ZASADY SA PROSTE - UROCHAMIAM BOCISZKA --
1. odpalam baze rf4, bede sprzwdzac kazda stronez osobna,
dane ktore widze uploaduje do bazy

2. Na koniec wszystkiego wysylam komunikat na telegramie ze koledzy maja rekordy,
koledzy to:
pijak :
rumszy :
stary rumszego:

3. czesc projektu po stronie flaska - diagramy, podglad danych z kolejnej czesci / pliku

'''



import sys
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


#test crap for getting title
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#end of test crap

import datetime
import time

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "123",
    database = "rf4")

mycursor = mydb.cursor()

print('')
print('/*********************Uruchomienie skryptu scraping_rf4.py')


sprawiajace_problemy = []
chory = 0

#wczytanie drivera
s = Service(r"/usr/bin/chromedriver")
driver = webdriver.Chrome(service=s)

strony = [
          ['https://rf4.pl/records/region/GL/',             'total','absolut','global'               ],['https://rf4.pl/records/region/PL/','total','absolut','pl'],
          ['https://rf4.pl/records/weekly/region/GL/',      'total','weekly','global'       ],['https://rf4.pl/records/weekly/region/PL/','total','weekly','pl'],
          ['https://rf4.pl/ultralight/region/GL/',          'ultralight','absolut','global'            ],                          [ 'https://rf4.pl/ultralight/region/PL/','ultralight','absolut','pl'   ],
          ['https://rf4.pl/ultralight/weekly/region/GL/',    'ultralight','weekly','global'     ],                          ['https://rf4.pl/ultralight/weekly/region/PL/','ultralight','weekly','pl' ],
          ['https://rf4.pl/telestick/region/GL/',           'teleskop','absolut','global'     ],                          [ 'https://rf4.pl/telestick/region/PL/','teleskop','absolut','pl'   ],
          ['https://rf4.pl/telestick/weekly/region/GL/',      'teleskop','weekly','global'     ],                          ['https://rf4.pl/telestick/weekly/region/PL/','teleskop','absolut','pl'   ]


          ]



baits = []
data = []
for a in range (0,len(strony)):
    driver.get(strony[a][0])
    time.sleep(0.2)
    website = (strony[a][1])
    cat = (strony[a][2])
    reg = (strony[a][3])
    bait = driver.find_elements(By.CLASS_NAME,"bait_icon")
    for element in bait:        
        bait = element.get_attribute("title")
        baits.append(bait)
        
    wpisy = driver.find_elements(By.CLASS_NAME,"overflow ")
    menu_boczne = 5
    ilosc_wpisy = len(wpisy)-menu_boczne
    i =-1     

    for b in range(6,ilosc_wpisy):        
    #for b in range(6,30):      #dev   
        if (b % 6) == 0:
            wpisy[b].click()
            time.sleep(0.05)
            i+=1

            #print(wpisy[b].text,'LEN:',len(wpisy[b].text))
            if len(wpisy[b].text) == 0:
                data.append(ryba)
                #print('ryba dodana')
                continue
            else:
                data.append(wpisy[b].text)
                ryba = wpisy[b].text
                continue
        
            
            
        if ((b-3) % 6) == 0:
            #print(baits[i]) #dev
            data.append(baits[i])
        else: 
            #print(wpisy[b].text) #dev
            data.append(wpisy[b].text)
        
    
        if b == ilosc_wpisy-1:
            break
        
    

    for a in range (0,len(data),6):
        if (a%6)==0 :
            dzisiaj = data[a+5]
            dzisiaj = dzisiaj.replace('.','-')
            dzisiaj = dzisiaj[:-2] + '2023'
            date_object = datetime.datetime.strptime(dzisiaj, '%d-%m-%Y').date()
            date_object = date_object.strftime('%Y-%m-%d')
            #print(date_object)
        #dzisiaj = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO rankingi(web,cat,reg,fish,weight,place,bait,player,week,day,date) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"        
        val = (website, cat,reg, data[a],data[a+1], data[a+2],data[a+3], data[a+4],'nic', 'noc',date_object)

          
        #val = ('test','test2')
        mycursor.execute(sql, val)
        mydb.commit()
    

