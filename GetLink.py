import driver as driver
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

import time

PATH= "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.meetup.com/de-DE/") #Site to scrape

# search = driver.find_element_by_xpath("")
arr= []
try:
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "navbar_search_input_id"))
    )

    search.send_keys("Medizin") #Thema hier ersetzen
    search.send_keys(Keys.RETURN)

    ortSuch = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//a[@class='dropdown-toggle'])[2]"))
    )

    ortSuch.send_keys(Keys.RETURN)

    locationFind = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "locationSearch"))
    )

    locationFind.send_keys("B")
    time.sleep(2)
    locationFind.send_keys("e")
    time.sleep(2)
    locationFind.send_keys("r")
    # locationFind.send_keys(Keys.RETURN)

    time.sleep(4)

    location = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Berlin, Deutschland"))
    )

    location.click()

    time.sleep(4)

    art = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'groupCard--gradient'))
    )

    elements = driver.find_elements_by_xpath("//h3[contains(@class,'padding-none inline-block')]")

    time.sleep(3)
    cityArray = []
    name = []

    for element in elements:
        print(element.text)
        name.append(element.text)

    mitgliedern = driver.find_elements_by_xpath("//p[@class='small ellipsize']")

    anzahlMitglieder = []
    for mitglieder in mitgliedern:
        print(mitglieder.text)
        anzahlMitglieder.append(mitglieder.text)

    urls = []
    i=0
    # for i in range(len(elements)):
    for i in range(len(elements)):
        try:
            p = driver.find_element_by_xpath('//*[@id="simple-view"]/div[1]/ul/li[{}]/div/a[2]'.format(i + 1))
            url = p.get_attribute('href')
            urls.append(url)
        except Exception as s:
            print(s)
            pass

    infosArray = []
    beschreibubg ="NONE"
    for e in urls:
        gruppeMitgliederInfos = []
        scrollMitglieder = True;
        mehrBool = True;
        j = 0
        b = True
        t= True
        pp = 1
        driver.get(e)
        time.sleep(3)
        mehrLesen = driver.find_element_by_xpath('//*[@id="overview"]/div/div/button')
        time.sleep(5)
        actions = ActionChains(driver)
        actions.move_to_element(mehrLesen).perform()
        mehrLesen.click()
        time.sleep(3)
        beschreibung = driver.find_element_by_xpath("(//p[@class='group-description margin--bottom'])[2]")
        beschreibugText = beschreibung.text
        print(beschreibung.text)
        time.sleep(3)
        try:
            alleMitgliederButton = driver.find_element_by_xpath('//*[@id="members"]/div[1]/div[2]/a')
            time.sleep(5)
            actions = ActionChains(driver)
            actions.move_to_element(alleMitgliederButton).perform()
            alleMitgliederButton.click()
            time.sleep(3)
            for h in range(4): #Wir machen die 4 mögliche Scroll down, um die Button 'Mehr Anzeigen' zu sehen
                inDerNaehe = driver.find_element_by_xpath('//*[@id="mupMain"]/div[5]/div/section/div[1]/div/div[1]/h4')
                actions = ActionChains(driver)
                actions.move_to_element(inDerNaehe).perform()
                time.sleep(3)
            while(mehrBool==True):#Wird immer nach 'Mehr Anzeigen' gesucht, bis es keine Mehr gibt
                try:
                    mehrMit = driver.find_element_by_xpath('//*[@id="member-list-card-id"]/div[3]/div[2]/button')
                    mehrMit.click()
                    actions = ActionChains(driver)
                    actions.move_to_element(inDerNaehe).perform()
                    time.sleep(3)
                except:
                    pass
                    mehrBool = False;
            mitgliederLocalise = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="member-list-card-id"]/div[3]/div[1]'))
            )
            while (t == True): #Wenn wir am Ende der Liste sind, nehmen wir die Daten der Mitglieder der Gruppe
                try:
                    mitgName = driver.find_element_by_xpath('//*[@id="member-list-card-id"]/div[3]/div[1]/ul/li[{}]/div/div[2]/div[1]/div/a/h4'.format(pp + 1))
                    mitgEintritt = driver.find_element_by_xpath('//*[@id="member-list-card-id"]/div[3]/div[1]/ul/li[{}]/div/div[2]/div[2]'.format(pp+1))
                    pp = pp + 1
                    gruppeMitgliederInfos.append((mitgName.text,mitgEintritt.text))
                except:
                    t = False
                    pass
            print(pp) #Um sicher zu sein dass alle Mitgliedern ausgegeben wurden
            print(len(gruppeMitgliederInfos))
        except:
            pass
        cityName = driver.find_element_by_class_name("groupHomeHeaderInfo-cityLink").text
        grName = driver.find_element_by_class_name("groupHomeHeader-groupNameLink").text
        anzahlMit = driver.find_element_by_class_name("groupHomeHeaderInfo-memberLink").text
        organisator = driver.find_element_by_xpath('//*[@id="mupMain"]/div[1]/div/section/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div[2]/a')
        findOrga = organisator.get_attribute('href')
        driver.get(findOrga)
        time.sleep(3)
        fuehrgunsTeamElements = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="member-list-card-id"]/div[2]/div/ul'))
        )
        print("ddd")

        orgArray = []
        stelleArray=[]
        while (b==True):
            try:
                fuehrgunsTeam = driver.find_element_by_xpath('//*[@id="member-list-card-id"]/div[2]/div/ul/li[{}]/div/div[2]/div[1]/div/a/h4'.format(j + 1))
                stelle = driver.find_element_by_xpath('//*[@id="member-list-card-id"]/div[2]/div/ul/li[{}]/div/div[2]/div[2]/div/span'.format(j+1))
                beigetretenAm = driver.find_element_by_xpath('//*[@id="member-list-card-id"]/div[2]/div/ul/li[{}]/div/div[2]/div[2]/span'.format(j+1))
                j =j+1
                orgArray.append((fuehrgunsTeam.text, stelle.text,beigetretenAm.text))
                print(fuehrgunsTeam.text)
                print(stelle.text)
                print(beigetretenAm.text)
            except:
                b = False
                pass
        infosArray.append((grName, cityName, anzahlMit, e, orgArray, beschreibugText, gruppeMitgliederInfos))
        time.sleep(3)


except Exception as s:
   print(s)




data_df = pd.DataFrame(data=infosArray,columns=['GruppenName','Location','Anzahl Mitglieder','Link','Organisatoren','Beschreibung','MitgliderInfos'])

data_df.to_json('e.json', orient='index', default_handler=str)

# data_df = pd.read_json('a.json', orient='index')

