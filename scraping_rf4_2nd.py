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
import re

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
wpis_problem = ''
for a in range (0,len(strony)):
#for a in range(3,4):
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

    for b in range(6,ilosc_wpisy-1,6):
    #for b in range(6,1800,6):
        try: 
            wpisy[b].click()
            time.sleep(0.10)
            
            data_small = []
            ab = re.findall('[0-9]+',wpisy[b].text)            
            if ((wpisy[b+1].text).find(" kg") > 0 or (wpisy[b+1].text).find(" g") >0) and (len(ab)==0)  :
                
                if len(wpisy[b].text) == 0:
                    data_small.append(ryba)
                else:
                    data_small.append(wpisy[b].text)
                    ryba = wpisy[b].text
                    
                data_small.append(wpisy[b+1].text)
                data_small.append(wpisy[b+2].text)                
                data_small.append(wpisy[b+4].text)
                data_small.append(wpisy[b+5].text)
            else:
                
                
                data_small = []                
                for problem in range (b,b+6):
                    #print('problem data',problem,wpisy[problem].text,wpisy[problem-1].text,wpisy[problem+1].text,)
                    
                    if (wpisy[problem].text).find(" kg") > 0 or  (wpisy[problem].text).find(" g")   > 0  :                      
                       
                       if len(wpisy[problem-1].text) == 0:
                            data_small.append(ryba)                    
                       else:
                           if len(re.findall('[0-9]+',wpisy[problem-1].text  ))==0:
                               data_small.append(wpisy[problem-1].text)
                               ryba = wpisy[problem-1].text
                                                
                                              
                       data_small.append(wpisy[problem].text)
                       data_small.append(wpisy[problem+1].text)
                       data_small.append(wpisy[problem+3].text)
                       data_small.append(wpisy[problem+4].text)
                       #print('  dodalismy z bledu',data_small)
                       break
                    else:
                       #print('  dalej')
                       continue
                    
                    
                
            
            #print(data_small) #dev
            #time.slepp(10) #devc
            #print(len(data_small))
            if len(data_small) ==5 and len(re.findall('[0-9]+',data_small[0])  )==0:
                data.append(data_small)            
        except Exception as e:
            print (e)
            print('problem krytyczny z ', b, wpisy[b].text )
            
                    
    # for datas in data:
    #     print (datas)
    #print(dupa)
    #print(data)
    complete_data = []
    i = 0
    for row in data:
        if len(row[0]) ==0 or row[0] =='':
            print('brak')            
        else:
            #print([row,baits[i]],i) #dev
            complete_data.append([row[0],row[1],row[2],row[3],row[4],baits[i]])            
        i+=1     
    for a in range (0,len(complete_data)-2):
        #print (a,website, cat,reg, complete_data[a][0],complete_data[a][1], complete_data[a][2],complete_data[a][5], complete_data[a][3],'no_data', 'no_data',complete_data[a][4])
        dzisiaj = complete_data[a][4]
        dzisiaj = dzisiaj.replace('.','-')
        dzisiaj = dzisiaj[:-2] + '2023'
        date_object = datetime.datetime.strptime(dzisiaj, '%d-%m-%Y').date()
        date_object = date_object.strftime('%Y-%m-%d')
        #print(date_object)
        #dzisiaj = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if (complete_data[a][1]).find(" kg") > 0:
            complete_data[a][1] = complete_data[a][1].replace(' kg','')
        else:
            if (complete_data[a][1]).find(" g")   > 0:
                complete_data[a][1] = complete_data[a][1].replace(' g','')
                complete_data[a][1] = '0.'+ complete_data[a][1]
        sql = "INSERT INTO rankingi(web,cat,reg,fish,weight,place,bait,player,week,day,date) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"        
        val = (website, cat,reg, complete_data[a][0],complete_data[a][1], complete_data[a][2],complete_data[a][5], complete_data[a][3],'no_data', 'no_data',date_object)

         
        #val = ('test','test2')
        mycursor.execute(sql, val)
        mydb.commit()
    

