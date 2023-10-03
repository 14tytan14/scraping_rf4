'''
STATUS: PISANY

created : 25-09-2023
LAST UPDATE: 25-09-2023

POMYSL NA PROGRAM - ZASADY SA PROSTE - UROCHAMIAM BOCISZKA --
1. odpalam baze rf4, bede sprzwdzac kazda stronez osobna,
dane ktore widze uploaduje do bazy

2. Na koniec wszystkiego wysylam komunikat na telegramie ze koledzy maja rekordy,
koledzy to:
pijak :
rumszy :
stary rumszego:

3. czesc projektu po stronie flaska - diagramy, podglad danych z kolejnej czesci / pliku

25-09-2023
integracja z cleanerem - dodaje tylko wartosci ktore nie ma w bazie


'''



import sys
import mysql.connector
import requests
import datetime
import time
import re
import bs4

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


strony = [
          ['https://rf4.pl/records/region/GL/',             'total','absolut','global'               ],
          ['https://rf4.pl/records/region/PL/',             'total','absolut','pl'],

          ['https://rf4.pl/records/weekly/region/GL/',      'total','weekly','global'       ],
          ['https://rf4.pl/records/weekly/region/PL/',      'total','weekly','pl'],

          ['https://rf4.pl/ultralight/region/GL/',          'ultralight','absolut','global'            ],
          ['https://rf4.pl/ultralight/region/PL/',          'ultralight','absolut','pl'   ],
          ['https://rf4.pl/ultralight/weekly/region/GL/',   'ultralight','weekly','global'     ],
          ['https://rf4.pl/ultralight/weekly/region/PL/',   'ultralight','weekly','pl' ],

          ['https://rf4.pl/telestick/region/GL/',           'teleskop','absolut','global'     ],
          ['https://rf4.pl/telestick/region/PL/',           'teleskop','absolut','pl'   ],
          ['https://rf4.pl/telestick/weekly/region/GL/',    'teleskop','weekly','global'     ],
          ['https://rf4.pl/telestick/weekly/region/PL/',    'teleskop','weekly','pl'   ]


          ]



baits = []
data = []
wpis_problem = ''
for a in range (0,len(strony)):
    print('  ',a, ' z ',len(strony),'sprawdzam',strony[a][0])
    website = (strony[a][1])
    cat = (strony[a][2])
    reg = (strony[a][3])

    response = requests.get(strony[a][0])
    print('     pobralem tresc strony')
    if response.status_code == 200:
        html = response.text
    else:
        print("Błąd podczas pobierania strony. Kod statusu:", response.status_code)
    soup = bs4.BeautifulSoup(html, "html.parser")


    rows = soup.find_all("div", class_="row")
    i = 0
    iab =0
    errors = 0
    #print(len(rows))
    clean_data_ryby = []
    for rowa in rows:
        c_data = rowa.find_all("div", class_="overflow")

        data_one_ryba = []
        for data in c_data:
            #print(data.text)
            try:     #czesc odpowiedzialna za probe pobrania titla diva - przynety
                div = data.find("div", class_="bait_icon")
                #print(div) #dev
                title = div["title"]
                #print('title',title)     #dev
                data_one_ryba.append(title)
            except:
                errors +=1

            if iab ==0:
                continue
            if iab !=0:
                #print(len(data.text),data.text )
                data_one_ryba.append(data.text)

        if iab !=0 and len(data_one_ryba[0]) >0:
            if len(clean_data_ryby) == 0:
                clean_data_ryby.append(data_one_ryba)
            else:
                if data_one_ryba[0] != clean_data_ryby[len(clean_data_ryby)-1][0]:
                    #print('unikat trzeba dodac',data_one_ryba[0])
                    clean_data_ryby.append(data_one_ryba)
        iab +=1


    #czesc odpwoiedzialna za czyszczenie wagi

    for a in range(0,len(clean_data_ryby)):
        for ab in range(0,len(clean_data_ryby[a])):
            if (clean_data_ryby[a][ab].find('\xa0kg')) >0:
                clean_data_ryby[a][ab] = clean_data_ryby[a][ab].replace('\xa0kg','')
                clean_data_ryby[a][ab] = clean_data_ryby[a][ab].replace(' ','')
                waga = clean_data_ryby[a][ab]                
                waga = float(waga)                
                clean_data_ryby[a][ab]   = "%0.3f" % waga                
            if (clean_data_ryby[a][ab].find('\xa0g')) >0:
                clean_data_ryby[a][ab] = clean_data_ryby[a][ab].replace('\xa0g','')
                clean_data_ryby[a][ab] = '0.'+ clean_data_ryby[a][ab]
                waga = clean_data_ryby[a][ab]                
                waga = float(waga)                
                clean_data_ryby[a][ab]   = "%0.3f" % waga
                
            pattern = re.compile(r"\d{2}.\d{2}.\d{2}")
            matches = pattern.findall(clean_data_ryby[a][ab])
            if len(matches)>0:
                try:
                 #print(clean_data_ryby[a][ab])
                 dzisiaj = clean_data_ryby[a][ab]
                 dzisiaj = dzisiaj.replace('.','-')
                 rok = datetime.datetime.now()
                 rok = rok.year
                 dzisiaj = dzisiaj[:-2] + str(rok)
                 #print(dzisiaj)
                 date_object = datetime.datetime.strptime(dzisiaj, '%d-%m-%Y').date()
                 clean_data_ryby[a][ab] = date_object.strftime('%Y-%m-%d')
                 #print(clean_data_ryby[a][ab])
                except:
                    #print('warunek innej daty')
                    pattern = re.compile(r"\d{1}.\d{2}.\d{2}")
                    matches = pattern.findall(clean_data_ryby[a][ab])
                    if len(matches) > 0:
                        try:
                            dzisiaj = clean_data_ryby[a][ab]
                            dzisiaj = dzisiaj.replace('.', '-')
                            rok = datetime.datetime.now()
                            rok = rok.year
                            dzisiaj = dzisiaj[:-2] + str(rok)
                            date_object = datetime.datetime.strptime(dzisiaj, '%d-%m-%Y').date()
                            clean_data_ryby[a][ab] = date_object.strftime('%Y-%m-%d')
                        except:
                            errors += 1
            else:
                pattern = re.compile(r"\d{1}.\d{2}.\d{2}")
                matches = pattern.findall(clean_data_ryby[a][ab])
                if len(matches) > 0:

                        try:
                            #print('warunek pierwszych 10 dni spelciony',clean_data_ryby[a][ab]) #dev
                            #time.sleep(1)
                            dzisiaj = clean_data_ryby[a][ab]
                            dzisiaj = dzisiaj.replace('.', '-')
                            rok = datetime.datetime.now()
                            rok = rok.year
                            dzisiaj = dzisiaj[:-2] + str(rok)
                            date_object = datetime.datetime.strptime(dzisiaj, '%d-%m-%Y').date()
                            clean_data_ryby[a][ab] = date_object.strftime('%Y-%m-%d')
                        except:
                            errors += 1

    for a in range(0,len(clean_data_ryby)):
        if len(clean_data_ryby[a])>1:
            for ab in range(0,len(clean_data_ryby[a]),7):
                mycursor.execute("SELECT id FROM test_new WHERE  web = '" + str(website) + "' AND cat = '" + str(
                    cat) + "' AND reg = '" + str(reg) + "' AND fish = '" + str(
                    clean_data_ryby[a][0]) + "' AND weight LIKE '" + str(
                    clean_data_ryby[a][ab + 1]) + "'  AND place = '" + str(
                    clean_data_ryby[a][ab + 2]) + "' AND bait = '" + str(
                    clean_data_ryby[a][ab + 3]) + "' and date LIKE '%" + str(
                    clean_data_ryby[a][ab + 6]) + "%'  and player = '" + str(clean_data_ryby[a][ab + 5]) + "'  ")
                myres2 = mycursor.fetchall()
                

                
                if len(myres2) == 0:                                                           
                    sql = "INSERT INTO test_new(web,cat,reg,fish,weight,place,bait,player,week,day,date) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    #val = (website, cat,reg, complete_data[a][0],complete_data[a][1], complete_data[a][2],complete_data[a][5], complete_data[a][3],'no_data', 'no_data',date_object)
                    # print('test', 'test','test', clean_data_ryby[a][0],clean_data_ryby[a][ab+1], clean_data_ryby[a][ab+2],clean_data_ryby[a][ab+3], clean_data_ryby[a][ab+5],'no_data', 'no_data',clean_data_ryby[a][ab+6])
                    val = (website, cat,reg, clean_data_ryby[a][0],clean_data_ryby[a][ab+1], clean_data_ryby[a][ab+2],clean_data_ryby[a][ab+3], clean_data_ryby[a][ab+5],'no_data', 'no_data',clean_data_ryby[a][ab+6])
                    mycursor.execute(sql, val)
                    mydb.commit()






print('koniec')

