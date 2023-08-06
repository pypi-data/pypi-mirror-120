#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import time
import datetime
import keyring
import subprocess


from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Chrome


#Chrome(executable_path='/path/to/chromedriver')

prohlizec = webdriver.Firefox(firefox_binary=FirefoxBinary('/usr/lib/firefox-esr/firefox-esr'))

#prohlizec = Chrome()


# TODO HLASIT JEN NOVE ZADOSTI - OSETRIT V DB?


#.# :pripojime k db
#.# a nacteme vsechny joby
#.# o ktere jsme zadali
#.# -
#.# vysledek_z_db;
#.# note right:toto je take v selen_zamestnani.py

#minimalni_sqlite

pripojeni = sqlite3.connect("zamestnani.db")

#with pripojeni:

pripojeni.row_factory = sqlite3.Row

kurzor = pripojeni.cursor()

#sql_prikaz = "CREATE TABLE uzivatel (name text, age integer)"
#sql_prikaz = "INSERT INTO uzivatel VALUES ('User A', 42)"


# TODO DNESNI DATUM!

#sql_prikaz = "SELECT * FROM zadosti"
#sql_prikaz = "SELECT * FROM zadosti WHERE date(datum) = '2021-05-10'"
sql_prikaz = "SELECT * FROM zadosti WHERE date(datum) = DATE()"
#sql_prikaz = kwargs['sql_prikaz']

#kurzor.execute("INSERT INTO friends(name) VALUES ('Ferda');")
#kurzor.executemany("INSERT INTO cars VALUES(?, ?, ?)", cars)
kurzor.execute(sql_prikaz)

#vysledek_z_db = kurzor.fetchone()
#vysledek_z_db = kurzor.fetchmany(size)
vysledek_z_db = kurzor.fetchall()

#print(vysledek_z_db)
#print(vysledek_z_db.keys()) # vystup: ['id', 'name', 'email', 'address']
#print(vysledek_z_db['id'])
#print(__file__, '> vysledek_z_db:', vysledek_z_db)

for i in vysledek_z_db:
    print(f"{i['id']}, {i['nazev_pozice']}, {i['zamestnavatel']},\
 {i['datum']}, {i['poznamky']}")

pripojeni.commit()
pripojeni.close()












#with Chrome() as driver:
    #your code inside this indent


#prohlizec.get("https://www.python.org")

#assert "Python" in prohlizec.title

#prvek = prohlizec.find_element_by_name("q")

#prvek.clear()
#prvek.send_keys("pycon")
#prvek.send_keys(Keys.RETURN)

#assert "No results found." not in prohlizec.page_source



#prohlizec.execute_script("window.open('');")
#prohlizec.switch_to.window(prohlizec.window_handles[len(prohlizec.window_handles) - 1])
#prohlizec.get("https://www.startpage.com")



#time.sleep(7)
#prohlizec.get("https://www.yandex.com")

#print("Current Page Title is : %s" %prohlizec.title)
#print("Current Page Name is : %s" %prohlizec.name)
#print("Current Window handle is: %s" %prohlizec.current_window_handle)

#time.sleep(3)
#prohlizec.switch_to.window(prohlizec.window_handles[0])

#print("Current Page Title is : %s" %prohlizec.title)



#prohlizec.execute_script("window.open('');")
#prohlizec.switch_to.window(prohlizec.window_handles[len(prohlizec.window_handles) - 1])

#.# :Prihlasime se s udaji z keyringu;

# Sign in
adresa = keyring.get_password('gov', 'url')
prohlizec.get(adresa)


pockame = WebDriverWait(prohlizec, 60)
prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-userName')))
uzivatel = keyring.get_password('gov', 'uzivatel')
prvek.send_keys(uzivatel)


prvek = prohlizec.find_element_by_id("id-password")
heslo = keyring.get_password('gov', 'heslo')
prvek.send_keys(heslo)
time.sleep(2)
prvek.submit()


# dalsi stranka
# Security question
prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-answer')))
kontrolni_otazka = keyring.get_password('gov', 'kontrolni_otazka')
prvek.send_keys(kontrolni_otazka)
time.sleep(2)
prvek.submit()

#.# :otevreme stranku 'home';


#css selector: li.claimant-tabbed-navigation__item:nth-child(1) > a:nth-child(1)

prvek = pockame.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.claimant-tabbed-navigation__item:nth-child(1) > a:nth-child(1)')))
time.sleep(2)
prvek.click()


#.# :otevreme stranku 'work search';

# dalsi stranka
# Home
prvek = pockame.until(EC.presence_of_element_located((By.ID, 'work-search')))
time.sleep(2)
prvek.click()


# dalsi stranka
# Job applications
def zadej_nove_zamestnani(udaje_z_db):
    """Nahlas podane zadosti na pracak.
    
    Nacte zaznamy o podanych zadostech z db a vyplni prislusne formulare.
    """

    #.# detach
    #.# (.)
    #.# detach
    #.# #khaki:zadej_nove_zamestnani(udaje_z_db);
    #.# note right:toto je take v selen_zamestnani.py
    #.# :klikneme na tlacitko 'add job';
    
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'add-job')))
    prvek.click()

    #.# :na dalsi strance vyplnime formular;

    # dalsi stranka
    # Add a job
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-jobTitle')))
    text = udaje_z_db['nazev_pozice'] #'id-jobTitle'
    prvek.send_keys(text)


    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-employer')))
    text = udaje_z_db['zamestnavatel'] #'id-employer'
    prvek.send_keys(text)


    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'clickable-INTERESTED')))
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'clickable-APPLIED')))
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'clickable-INTERVIEW')))
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'clickable-SUCCESSFUL')))
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'clickable-UNSUCCESSFUL')))
    prvek.click()


    #datetime.datetime.strptime('2020-09-22 12:00:00', '%Y-%m-%d %H:%M:%S')
    datum_z_db = datetime.datetime.strptime(udaje_z_db['datum'], '%Y-%m-%d %H:%M:%S')


    # For example, 29 9 2020
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-applicationDate.day')))
    text = datum_z_db.strftime('%d') #'08'
    prvek.send_keys(text)


    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-applicationDate.month')))
    text = datum_z_db.strftime('%m') #'12'
    prvek.send_keys(text)


    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-applicationDate.year')))
    text = datum_z_db.strftime('%Y') #'2020'
    prvek.send_keys(text)


    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-notes')))
    text = udaje_z_db['poznamky'] #'poznamky poznamky poznamky'
    prvek.send_keys(text)
    #time.sleep(2)
    #prvek.submit()

    #.# :a odesleme tlacitkem 'submit';
    #.# detach
    #.# (.)
    #.# detach

    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-submit-button')))
    time.sleep(2)
    prvek.click()


#.# :pro kazdy zaznam v db o podane zadosti
#.# zavolame v cyklu funkci
#.# -
#.# zadej_nove_zamestnani();
#.# note right
#.# toto se resi take v selen_zamestnani.py
#.# end note


for i in vysledek_z_db:
    zadej_nove_zamestnani(i)


subprocess.Popen(['mpv', 'applications_reported.mp3'])



#prohlizec.close() # zavre tab nebo cely prohlizec
#prohlizec.quit() # zavre cely prohlizec - vsechny taby
