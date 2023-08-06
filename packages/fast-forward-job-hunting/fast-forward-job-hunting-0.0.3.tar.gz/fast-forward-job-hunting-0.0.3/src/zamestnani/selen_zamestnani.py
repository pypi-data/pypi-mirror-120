#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Vyhleda joby, posle zadosti a zivotopisy na vybrane a zapise o tom report na pracak.
"""

#TODO PRIDAT DO NOVY_SOUBOR.PY


import time

startTime = time.time()

import datetime
import keyring
import sqlite3
import subprocess
import os

from threading import Thread
from queue import Queue
from pathlib import Path

import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver import Chrome
#from selenium.webdriver.chrome.options import Options

import cv_automat




# TODO driver.quit()


#Chrome(executable_path='/path/to/chromedriver')

#prohlizec = Chrome()




volby = Options()

volby.page_load_strategy = 'eager'

#volby.page_load_strategy = 'none'

#prohlizec = webdriver.Chrome(options=volby)


#options.add_argument("-profile")
#options.add_argument("/home/gabriel/.mozilla/firefox/whatever.selenium")

#fp = webdriver.FirefoxProfile()

#nastaveni_prohlizece = webdriver.FirefoxProfile()

# 1 - Allow all images
# 2 - Block all images
# 3 - Block 3rd party images 

#nastaveni_prohlizece.set_preference("permissions.default.image", 2)

# 0 means to download to the desktop
# 1 means to download to the default "Downloads" directory
# 2 means to use the directory

#fp.set_preference("browser.download.folderList", 2)

#fp.set_preference("browser.helperApps.alwaysAsk.force", False)

#fp.set_preference("browser.download.manager.showWhenStarting",False)

#fp.set_preference("browser.download.dir", "H:\Downloads") 

#profile.update_preferences()

#firefox_capabilities = DesiredCapabilities.FIREFOX

#schopnosti_firefoxu = DesiredCapabilities.FIREFOX.copy()

#firefox_capabilities['marionette'] = True

#schopnosti_firefoxu['marionette'] = True

#driver = webdriver.Firefox(fp, options=options, executable_path="path-to-geckodriver")

#driver = webdriver.Firefox(capabilities=firefox_capabilities,firefox_binary=binary, firefox_profile = fp)

binarka_firefoxu = FirefoxBinary('/usr/lib/firefox-esr/firefox-esr')

#prohlizec = webdriver.Firefox(capabilities = schopnosti_firefoxu,
                              #firefox_binary = binarka_firefoxu,
                              #firefox_profile = nastaveni_prohlizece)

#prohlizec = webdriver.Firefox(firefox_binary = binarka_firefoxu,
#                              firefox_profile = nastaveni_prohlizece)

#prohlizec = webdriver.Firefox(firefox_binary=FirefoxBinary('/usr/lib/firefox-esr/firefox-esr'))

#prohlizec = webdriver.Firefox(firefox_binary=binarka_firefoxu)

prohlizec = webdriver.Firefox(options=volby, firefox_binary=binarka_firefoxu)



def uloz_do_db(**kwargs):
    """Uloz do db zaznamy o zadostech poslanych na joby.
    """

    #.# partition uloz_do_db {
    #.# #khaki:uloz_do_db(**kwargs);
    #.# :Ulozime do db zaznamy
    #.# o zadostech poslanych na joby.;
    #.# }
    #.# detach
    #.# #white:(.)
    #.# detach

    pripojeni = sqlite3.connect("zamestnani.db")

    pripojeni.row_factory = sqlite3.Row

    kurzor = pripojeni.cursor()
    
    kurzor.execute("INSERT INTO zadosti VALUES (NULL, ?, ?, datetime('now'), ?)", (kwargs['nazev_pozice'], kwargs['zamestnavatel'], kwargs['poznamky']))
    
    kurzor.execute(sql_prikaz)

    pripojeni.commit()

    pripojeni.close()


#.# :pripojime k db
#.# a nacteme vsechny joby
#.# o ktere jsme zadali
#.# -
#.# vysledek_z_db;
#.# note right:toto je take v selen.py
#.# detach
#.# #white:(.)
#.# detach


pripojeni = sqlite3.connect("zamestnani.db")

pripojeni.row_factory = sqlite3.Row

kurzor = pripojeni.cursor()

sql_prikaz = "SELECT * FROM zadosti"

kurzor.execute(sql_prikaz)

vysledek_z_db = kurzor.fetchall()

pripojeni.commit()

pripojeni.close()


#pripojeni = sqlite3.connect("cv.db")

#pripojeni.row_factory = sqlite3.Row

#kurzor = pripojeni.cursor()

#sql_prikaz = "SELECT * FROM applicant_name ORDER BY id DESC LIMIT 1"

#kurzor.execute(sql_prikaz)

##vysledek_z_db = kurzor.fetchall()

#vysledek_z_db = kurzor.fetchone()

#pripojeni.commit()

#pripojeni.close()


#pripona_do_nazvu_souboru = "".join(x for x in vysledek_z_db['suffix'] if x.isalnum())

#osoba_do_nazvu_souboru = f"{vysledek_z_db['surname']}_{vysledek_z_db['first_name']}_{pripona_do_nazvu_souboru}".lower().replace(' ', '_')

##print('\nosoba_do_nazvu_souboru:', osoba_do_nazvu_souboru)

#osoba_do_bezneho_textu = f"{vysledek_z_db['first_name']} {vysledek_z_db['surname']} {vysledek_z_db['suffix']}"

##print('\nosoba_do_bezneho_textu:', osoba_do_bezneho_textu)


def interakce_findajob_dwp_gov_uk():
    """Vyhledej joby na gov.uk a posli zadosti na vybrane. 

    prime zadosti, ale nelze rozlisit predem
    napr. https://findajob.dwp.gov.uk/apply/5105233
    """



    pripojeni = sqlite3.connect("cv.db")

    pripojeni.row_factory = sqlite3.Row

    kurzor = pripojeni.cursor()

    sql_prikaz = "SELECT * FROM applicant_name ORDER BY id DESC LIMIT 1"

    kurzor.execute(sql_prikaz)

    #vysledek_z_db = kurzor.fetchall()

    vysledek_z_db = kurzor.fetchone()

    pripojeni.commit()

    pripojeni.close()


    pripona_do_nazvu_souboru = "".join(x for x in vysledek_z_db['suffix'] if x.isalnum())

    osoba_do_nazvu_souboru = f"{vysledek_z_db['surname']}_{vysledek_z_db['first_name']}_{pripona_do_nazvu_souboru}".lower().replace(' ', '_')

    #print('\nosoba_do_nazvu_souboru:', osoba_do_nazvu_souboru)

    osoba_do_bezneho_textu = f"{vysledek_z_db['first_name']} {vysledek_z_db['surname']} {vysledek_z_db['suffix']}"

    #print('\nosoba_do_bezneho_textu:', osoba_do_bezneho_textu)





    #.# partition interakce_findajob_dwp_gov_uk {
    #.# #khaki:interakce_findajob_dwp_gov_uk()
    #.# -
    #.# Vyhledej joby na gov.uk a posli zadosti na vybrane. 
    #.# -
    #.# prime zadosti, ale nelze rozlisit predem
    #.# napr. https://findajob.dwp.gov.uk/apply/5105233;    
    #.# :Prihlasime se s udaji z keyringu;
    #.# note right:Sign in
    
    adresa = keyring.get_password('findajob_dwp_gov_uk', 'url')

    prohlizec.get(adresa)


    pockame = WebDriverWait(prohlizec, 60)


    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'email')))

    uzivatel = keyring.get_password('findajob_dwp_gov_uk', 'uzivatel')

    prvek.send_keys(uzivatel)


    prvek = prohlizec.find_element_by_id("password")

    heslo = keyring.get_password('findajob_dwp_gov_uk', 'heslo')

    prvek.send_keys(heslo)

    time.sleep(2)

    prvek.submit()

    
    #.# :Zadame vyhledani podle specifikace.
    #.# Kriteria zde mame rucne v odkazu;
    #.# note right
    #.# dalsi stranka
    #.# Your account
    #.# end note


    time.sleep(5)


    #.# :zalozime frontu pro multithreading;


    global fronta
    
    fronta = Queue()
    
    fronta.put('otevri dalsi vlakno')
    

    #funkce pro cyklus ze seznamu adres
    
    def zpracuj_adresu_pro_hledani(adresa_pro_hledani):

        prohlizec.get(adresa_pro_hledani)


        #.# :najdeme vsechny odkazy;
        #.# note right
        #.# dalsi stranka
        #.# vysledky hledani
        #.# end note

        # TODO pokud nejsou ve vysledku hledani zadne joby, dostaneme timeut hlasku

        seznam_prvku = pockame.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.search-result h3 .govuk-link')))

        for i in seznam_prvku:

            print(i.text)

            print(i.get_attribute('href'))


        #.# :nacteme adresy odkazu do seznamu
        #.# -
        #.# adresy;
        #.# #white:(.)
        #.# detach

        adresy = []

        for i in seznam_prvku:

            adresy.append(i.get_attribute('href'))

        #print('adresy:', adresy)


        #mame odkaz na "next"?

        
        try:
                        
            prvek = prohlizec.find_element(By.CSS_SELECTOR, '.pager-next')
            
            url_dalsi_stranky_vysledku_hledani = prvek.get_attribute('href')
            
            print('\nurl_dalsi_stranky_vysledku_hledani:', url_dalsi_stranky_vysledku_hledani)
            
        except Exception as vyjimka:
            
            print('\nNenasli jsme odkaz "next". Vyjimka:', vyjimka)
        

        def zjisti_volne_okno():

            """Projed otevrene zalozky a vrat identifikator prvni prazdne.
            """


            #.# partition zjisti_volne_okno {
            #.# #khaki:zjisti_volne_okno()
            #.# -
            #.# Projed otevrene zalozky
            #.# a vrat identifikator prvni prazdne;
            #.# }
            #.# detach
            #.# #white:(.)
            #.# detach

            
            for i in prohlizec.window_handles:

                prohlizec.switch_to.window(i)

                #print(i)

                #print("\nprohlizec.current_window_handle: %s" %prohlizec.current_window_handle)

                #print("\nprohlizec.title: %s" %prohlizec.title)

                #print('\nprohlizec.current_url:', prohlizec.current_url)

                if prohlizec.current_url == 'about:blank':

                    return i


        def zavri_predchozi_okno():

            """Zavri predchozi okno.

            Prepni na predchozi okno,
            zavri ho a prepni se zpet.
            """


            #.# partition zavri_predchozi_okno {
            #.# #khaki:zavri_predchozi_okno()
            #.# -
            #.# Prepni na predchozi okno,
            #.# zavri ho a prepni se zpet.;
            #.# }
            #.# detach
            #.# #white:(.)
            #.# detach
            
            
            prohlizec.switch_to.window(prohlizec.window_handles[len(prohlizec.window_handles) - 2])

            time.sleep(0.5)

            prohlizec.close()

            prohlizec.switch_to.window(prohlizec.window_handles[len(prohlizec.window_handles) - 1])


        def posli_zadost_o_zamestnani(url):

            """Otevri detaily jobu na nove zalozce a posli zadost.
            """

            #.# partition posli_zadost_o_zamestnani {
            #.# #khaki:posli_zadost_o_zamestnani(url);
            #.# :otevreme novou zalozku
            #.# prepneme na ni
            #.# a nacteme adresu s jobem;

        
            prohlizec.execute_script("window.open('');")

            prohlizec.switch_to.window(zjisti_volne_okno())

            prohlizec.get(url)

            zavri_predchozi_okno()

            #.# note right
            #.# NOVA STRANKA
            #.# napr. https://findajob.dwp.gov.uk/details/5105233
            #.# detaily zamestnani. klikneme na "apply for this job"
            #.# end note

            #.# :nacteme podrobnosti jobu
            #.# pro db do seznamu
            #.# -
            #.# kwargs;


            try:
                
                prvek = pockame.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.govuk-button.govuk-button--start')))

                url = prvek.get_attribute('href')

            except Exception as vyjimka:
                
                print('\nNenasli jsme tlacitko "Apply".')
                
                print('\nvyjimka:\n', vyjimka)
                
                #fronta.put('otevri dalsi vlakno')

                #url = 'https://findajob.dwp.gov.uk/apply/6150830'
                
                url = 'https://findajob.dwp.gov.uk/apply/5731889'
                
                #url = ''

            #url = prvek.get_attribute('href')
            
            kwargs = {}
            
            kwargs['nazev_pozice'] = prohlizec.title
            

            #dava toto smysl?

            try:
                
                prvek = prohlizec.find_element(By.CSS_SELECTOR, 'tr.govuk-table__row:nth-child(6) > td:nth-child(2)')

                kwargs['zamestnavatel'] = prvek.text

            except Exception as vyjimka:
                
                print('\nNazev zamestnavatele nenalezen. Vyjimka:\n', vyjimka)

                kwargs['zamestnavatel'] = ''


            kwargs['poznamky'] = url



            #.# :nacteme job summary nebo
            #.# nahradime nejakym textem;


            try:

                prvek = prohlizec.find_element(By.CSS_SELECTOR, 'div.govuk-body:nth-child(5)')            

            except:

                job_summary = 'lawyer developer manager director'

                print('\nnenasli jsme popis nabizeneho zamestnani')


            job_summary = prvek.text
            

            #.# :otevreme novou zalozku
            #.# prepneme na ni
            #.# a otevreme stranku pro odeslani zadosti;


            # presunout do extra funkce?

            pripojeni = sqlite3.connect("zamestnani.db")

            pripojeni.row_factory = sqlite3.Row

            kurzor = pripojeni.cursor()

            sql_prikaz = f"SELECT * FROM zadosti WHERE poznamky LIKE '{url}'"

            kurzor.execute(sql_prikaz)

            vysledek_z_db = kurzor.fetchall()

            #print(vysledek_z_db)
            #print(vysledek_z_db.keys()) # vystup: ['id', 'name', 'email', 'address']
            #print(vysledek_z_db['id'])
            #print(__file__, '> vysledek_z_db:', vysledek_z_db)

            # TODO zde vypsat take cislo vlakna

            #print('\nkwargs:', len(kwargs), kwargs)

            #print('\nlen(vysledek_z_db):', len(vysledek_z_db))

            if len(vysledek_z_db) > 0:

                kwargs = {}

                #print('len(kwargs) po znovudeklaraci:', len(kwargs))

                print(f'\nZadost uz byla poslana {len(vysledek_z_db)}x:\n')

                for i in vysledek_z_db:

                    print(f"{i['id']}, {i['nazev_pozice']}, {i['zamestnavatel']},\
                {i['datum']}, {i['poznamky']}")

                fronta.put('otevri dalsi vlakno')

            pripojeni.close()


            if len(vysledek_z_db) == 0:

                prohlizec.execute_script("window.open('');")

                prohlizec.switch_to.window(zjisti_volne_okno())


                try:

                    prohlizec.get(url)

                except Exception as vyjimka:

                    print('\nNepodarilo se otevrit stranku "Apply".')
                    
                    print('\nvyjimka:\n', vyjimka)

                    #prohlizec.execute_script("window.stop();")

                    #zavri_predchozi_okno()
                    
                    #fronta.put('otevri dalsi vlakno')


                #.# note right
                #.# NOVA STRANKA
                #.# detaily konkretniho zamestnani
                #.# napr. https://findajob.dwp.gov.uk/apply/5105233
                #.# Pokud neni toto url, byli jsme presmerovani mimo web gov
                #.# a nelze poslat zadost primo takze zavreme tab.
                #.# muzeme se vratit k puvodnimu tabu a ten zavrit take.
                #.# jinak vyplnime a odesleme.
                #.# end note

                
                #time.sleep(5)
                
                if prohlizec.current_url != url:
                    
                    prohlizec.execute_script("window.stop();")

                    zavri_predchozi_okno()
                    
                    fronta.put('otevri dalsi vlakno')
                
                else:

                    zavri_predchozi_okno()

                    #pri vypadku pouzit nahradni cv?

                    print('\n\n⚫⚫⚫ SESTAVUJEME ZIVOTOPIS\n\n')

                    #print(job_summary)

                    url_do_nazvu_souboru = "".join(x for x in url[8:50] if x.isalnum())
                    
                    cv_automat.sestav_zivotopis(job_summary,
                                                osoba_do_nazvu_souboru,
                                                url_do_nazvu_souboru)


                    #.# :vyplnime formular pro odeslani zadosti;

                    try:

                        prvek = pockame.until(EC.presence_of_element_located((By.ID, 'full_name')))

                        prvek.send_keys(osoba_do_bezneho_textu)
                    
                    except Exception as vyjimka:
                        
                        print('\nNemame kam vyplnit jmeno u odeslani zadosti:', vyjimka)
                        
                        #prohlizec.execute_script("window.stop();")

                        #zavri_predchozi_okno()
                        
                        #fronta.put('otevri dalsi vlakno')

                
                    #.# :vyplnime cover letter;
                    #.# note right
                    #.# TODO SESTAVOVAT COVER LETTER NA MIRU
                    #.# zatim doplnit nejaky univerzalni
                    #.# end note

                    
                    # toto smazat?
                    
                    #cover_letter = f'''Dear Sir or Madam,

    #As a highly skilled lawyer, I read your posting with interest. My experience aligns well with the qualifications you are seeking and I am certain I would make a valuable addition to your organisation.
    #With more than 8 years’ experience as a lawyer, I am adept in case preparation, client consultations, and courtroom litigation. Moreover, while my on-the-job experience has afforded me a well-rounded skill set, including first-rate leadership and interpersonal abilities, I excel at  getting results.

    #In addition to my legal experience and personal qualities, I have a solid educational foundation and a passion for information technologies. I would welcome the opportunity to contribute to your leading reputation in the field.
    #Please review my attached CV for additional details regarding my expertise and career achievements. I will be happy to discuss how my experience and background meets your needs.
    #Thank you for your time and consideration.

    #Sincerely,

    #{osoba_do_bezneho_textu}'''
                    
                    
                    #print(cover_letter)
                    
                    
                    pripojeni = sqlite3.connect("cv.db")

                    pripojeni.row_factory = sqlite3.Row

                    kurzor = pripojeni.cursor()

                    sql_prikaz = "SELECT * FROM pruvodni_dopis ORDER BY id DESC LIMIT 1"

                    kurzor.execute(sql_prikaz)

                    #vysledek_z_db = kurzor.fetchall()

                    vysledek_z_db = kurzor.fetchone()

                    pripojeni.commit()

                    pripojeni.close()


                    cover_letter = f"{vysledek_z_db['zneni']}\n\n{osoba_do_bezneho_textu}"


                    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'message')))
                    
                    prvek.clear()
                    
                    prvek.send_keys(cover_letter)


                    #.# :pripojime predvoleny zivotopis pdf
                    #.# a klikneme na tlacitko odeslat;


                    prvek = prohlizec.find_element(By.ID, 'cv_upload')
                    
                    prvek.send_keys(f'{Path.cwd()}/{osoba_do_nazvu_souboru}_cv_{url_do_nazvu_souboru}.pdf')

                    prvek = prohlizec.find_element(By.ID, 'cc_self')


                    if prvek.is_selected() == False:
                    
                        prvek.click()


                    # potrebujeme cekat na upload? az se jmeno cv objevi ve volbach nad uploadem?
                    
                    time.sleep(10)
                    
                    prvek = prohlizec.find_element(By.CSS_SELECTOR, '.govuk-form-group .govuk-button')
                    
                    prvek.click()

                    #.# :detaily o odeslane zadosti ulozime do db.
                    #.# na to volame funkci
                    #.# -
                    #.# uloz_do_db(**kwargs);


                    if len(kwargs) > 0:
                        
                        uloz_do_db(**kwargs)

                    
                    #.# :smazeme uploadovane cv;
                    #.# :klikneme na link 'my account';


                    time.sleep(5)

                    prvek = prohlizec.find_element(By.CSS_SELECTOR, '.govuk-header-auth > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)')

                    prvek.click()

                    print('\n\nklikli jsme na "my account"')
                    

                    #.# :klikneme na link 'my cvs';
                                    
                    #.# note right:dalsi stranka 'My Account'
        

                    # zde jsme meli timeout

                    prvek = pockame.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.my-account-row:nth-child(1) > div:nth-child(3) > h2:nth-child(1) > a:nth-child(1)')))
                    
                    time.sleep(2)
                    
                    prvek.click()
                    
                    print('\n\nklikli jsme na "my cvs"')

                    
                    #.# :klikneme na link 'delete cv';


                    def smaz_zivotopis():
                        
                        """Smaz prave uploadovany zivotopis i drive ulozene.
                        """

                        #.# partition smaz_zivotopis {
                        #.# #khaki:smaz_zivotopis();
                        #.# :najdeme link na 'delete'
                        #.# a klikneme na nej;

                        
                        prvek = pockame.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(2) > a:nth-child(3)')))
                                        
                        time.sleep(2)

                        prvek.click()

                        print('\n\nklikli jsme na "delete"')
                    
                        del prvek
                        
                        
                        #.# :klikneme na 'opravdu delete?';
                        
                        
                        prvek = pockame.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.govuk-button')))

                        time.sleep(2)

                        prvek.click()                

                        print('\nklikli jsme na "yes, opravdu smazat"')

                        print('\nzivotopis smazan, otevri dalsi vlakno')


                        #.# :pokud neni co mazat, spustime dalsi vlakno.
                        #.# pokud je, spustime odsud tuto funkci znovu od zacatku.;


                        try:

                            findElements(By.CSS_SELECTOR, 'td:nth-child(2) > a:nth-child(3)')

                        except:

                            fronta.put('otevri dalsi vlakno')

                            print('\nuz neni co mazat, otevri dalsi vlakno')

                        else:

                            smaz_zivotopis()

                    
                        #.# }
                    #.# :spustime smaz_zivotopis();
                    #.# }
                    
                    
                    time.sleep(2)

                    smaz_zivotopis()
                    

        #.# :zadosti budeme posilat v multithreadingu
        #.# pro to si pripravime seznam
        #.# -
        #.# vlakniny
        #.# -
        #.# a ulozime do nej url adresy z
        #.# -
        #.# adresy;


        def spust_vlakno():

            if fronta.empty():

                #print('\nprazdna fronta')

                time.sleep(0.5)

                spust_vlakno()

            else:

                polozka_fronty = fronta.get()

                print('\npolozka z fronty:', str(polozka_fronty))

                fronta.task_done()
                        
                vlakno = Thread(target=posli_zadost_o_zamestnani, args=(i,))
                
                
                time.sleep(0.5)
                
                if polozka_fronty == 'otevri dalsi vlakno':

                    vlakno.start()
                    
                    vlakniny.append(vlakno)



        global vlakniny

        vlakniny = []

        for i in adresy:
            
            print('\n', i)

            spust_vlakno()

            
            #.# :otevreme vlakno pro kazdou adresu v seznamu
            #.# a zavolame v nem funkci
            #.# -
            #.# posli_zadost_o_zamestnani();
            

        #.# :pozdrzime program dokud neskonci vsechna vlakna;
        #.# }
        #.# detach
        #.# #white:(.)
        
        
        for i in vlakniny:

            i.join()



        #sem pridat opetovne spusteni teto funkce pokud mame odkaz "next page"?

        if url_dalsi_stranky_vysledku_hledani:
            
            print('\n🌑 🌑 🌑 DALSI STRANKA VYSLEDKU HLEDANI ...')
            
            #zpracuj_adresu_pro_hledani(url_dalsi_stranky_vysledku_hledani)

            try:

                zpracuj_adresu_pro_hledani(url_dalsi_stranky_vysledku_hledani)

            except Exception as vyjimka:
                
                print('\nNeco se nepovedlo. Vyjimka:\n', vyjimka)


    #zde konci funkce?









    #.# :urcime si adresu pro hledani jobu;


    #adresa_pro_hledani = ''

    adresa_pro_hledani = pyperclip.paste()

    seznam_adres_pro_hledani = [adresa_pro_hledani]

    #kategorie od nejvyssiho poctu nabidek:

    #other/general
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=19&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=19&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000&page=2'


    #accounting and finance
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=1&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=1&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000&page=2'
    
    
    #pokusna adresa
    
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=1&cti=full_time&cty=permanent&loc=86384&pp=29&sf=35000&page=4'





    #it
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=14&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=14&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000&page=2'


    #scientific
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=24&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #marketing
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=20&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #creative and design
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=5&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #legal
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=15&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #property
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=21&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'

    #consultancy
    #adresa_pro_hledani = 'https://findajob.dwp.gov.uk/search?cat=4&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000'


    #PLATNY SEZNAM

    #seznam_adres_pro_hledani = [
        'https://findajob.dwp.gov.uk/search?cat=19&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',

        'https://findajob.dwp.gov.uk/search?cat=1&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',
        
        'https://findajob.dwp.gov.uk/search?cat=14&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',

        'https://findajob.dwp.gov.uk/search?cat=24&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',

        'https://findajob.dwp.gov.uk/search?cat=20&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',

        'https://findajob.dwp.gov.uk/search?cat=5&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',

        'https://findajob.dwp.gov.uk/search?cat=15&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',
        
        'https://findajob.dwp.gov.uk/search?cat=21&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',

        'https://findajob.dwp.gov.uk/search?cat=4&cti=full_time&cty=permanent&loc=86384&pp=50&sf=35000',
        ]

    #pokusny seznam pro hledani

    #seznam_adres_pro_hledani = [
        #'https://findajob.dwp.gov.uk/search?cat=19&cti=full_time&cty=permanent&loc=86384&pp=2&sf=35000',

        #'https://findajob.dwp.gov.uk/search?cat=1&cti=full_time&cty=permanent&loc=86384&pp=2&sf=35000',
        
        #'https://findajob.dwp.gov.uk/search?cat=14&cti=full_time&cty=permanent&loc=86384&pp=2&sf=35000',
        #]


    for i in seznam_adres_pro_hledani:

        print('\nadresa_pro_hledani:\n',i)

        try:

            zpracuj_adresu_pro_hledani(i)

        except Exception as vyjimka:
            
            print('\nNeco se nepovedlo. Vyjimka:\n', vyjimka)



    #zpracuj_adresu_pro_hledani(adresa_pro_hledani)








#.# :spustime odesilani zadosti
#.# zavolanim funkce
#.# -
#.# interakce_findajob_dwp_gov_uk();
#.# :zavreme prohlizec;
#.# :zahrajeme znelku;
#.# #white:(.)
#.# detach

interakce_findajob_dwp_gov_uk()

prohlizec.quit()

#os.unlink('*.log')

#os.unlink('*.aux')

#os.unlink('*.tex')

#os.unlink('*.pdf')

subprocess.Popen(['mpv', 'applications_sent.mp3'])

executionTime = (time.time() - startTime)

print('\nExecution time in seconds: ' + str(executionTime))














































































































# PRIME ZADOSTI - EASILY APPLY TO THIS JOB

def interakce_indeed_co_uk():
    """popis
    """

    #.# partition interakce_indeed_co_uk {
    #.# #khaki:interakce_indeed_co_uk();
    #.# :Prihlasime se s udaji z keyringu;
    #.# }

    # Sign in
    adresa = keyring.get_password('indeed_co_uk', 'url')
    prohlizec.get(adresa)


    pockame = WebDriverWait(prohlizec, 60)
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'login-email-input')))
    uzivatel = keyring.get_password('indeed_co_uk', 'uzivatel')
    prvek.send_keys(uzivatel)


    prvek = prohlizec.find_element_by_id("login-password-input")
    heslo = keyring.get_password('indeed_co_uk', 'heslo')
    prvek.send_keys(heslo)
    #time.sleep(2)
    #prvek.submit()


    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'login-submit-button')))
    prvek = prohlizec.find_element_by_id("login-submit-button")
    time.sleep(2)
    prvek.click()


    # dalsi stranka
    # Account settings

    time.sleep(2)

    #https://www.indeed.co.uk/?from=gnav-passport-view
    prohlizec.get("https://www.indeed.co.uk")


#<span class="iaLabel iaIconActive">Easily apply to this job</span>

    ## dalsi stranka
    ## Your account
    #time.sleep(5)

    #prohlizec.get("https://findajob.dwp.gov.uk/search?cat=15&cty=permanent&cti=full_time&f=1&loc=86590&sf=50000&pp=50&sb=salary&sd=down")
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-answer')))
    #kontrolni_otazka = keyring.get_password('gov', 'kontrolni_otazka')
    #prvek.send_keys(kontrolni_otazka)
    #time.sleep(2)
    #prvek.submit()


    ## dalsi stranka
    ## Search for jobs



    ## dalsi stranka
    ## Home
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'work-search')))
    #prvek.click()


#interakce_indeed_co_uk()





# CAPCHA

def interakce_totaljobs_com():
    """popis
    """

    #.# detach
    #.# #white:(.)
    #.# detach
    #.# partition interakce_totaljobs_com {
    #.# #khaki:interakce_totaljobs_com();
    #.# :Prihlasime se s udaji z keyringu;
    #.# }

    # Sign in
    adresa = keyring.get_password('totaljobs_com', 'url')
    prohlizec.get(adresa)


    pockame = WebDriverWait(prohlizec, 60)
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'Form_Email')))
    uzivatel = keyring.get_password('totaljobs_com', 'uzivatel')
    prvek.send_keys(uzivatel)


    prvek = prohlizec.find_element_by_id("Form_Password")
    heslo = keyring.get_password('totaljobs_com', 'heslo')
    prvek.send_keys(heslo)
    #time.sleep(2)
    #prvek.submit()


    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'login-submit-button')))
    prvek = prohlizec.find_element_by_id("btnLogin")
    time.sleep(2)
    prvek.click()




    #<a class="govuk-link" href="https://findajob.dwp.gov.uk/search">Search for jobs</a>

    ## dalsi stranka
    ## Your account
    #time.sleep(5)

    #prohlizec.get("https://findajob.dwp.gov.uk/search?cat=15&cty=permanent&cti=full_time&f=1&loc=86590&sf=50000&pp=50&sb=salary&sd=down")
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-answer')))
    #kontrolni_otazka = keyring.get_password('gov', 'kontrolni_otazka')
    #prvek.send_keys(kontrolni_otazka)
    #time.sleep(2)
    #prvek.submit()


    ## dalsi stranka
    ## Search for jobs



    ## dalsi stranka
    ## Home
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'work-search')))
    #prvek.click()


#interakce_totaljobs_com()







#capcha
#https://www.reed.co.uk/account/signin#&card=signin

def interakce_reed_co_uk():
    """popis
    """

    #.# detach
    #.# #white:(.)
    #.# detach
    #.# partition interakce_reed_co_uk {
    #.# #khaki:interakce_reed_co_uk();
    #.# :Prihlasime se s udaji z keyringu;
    #.# }

    # Sign in
    adresa = keyring.get_password('reed_co_uk', 'url')
    prohlizec.get(adresa)


    #pockame = WebDriverWait(prohlizec, 60)
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'Form_Email')))
    #uzivatel = keyring.get_password('totaljobs_com', 'uzivatel')
    #prvek.send_keys(uzivatel)


    #prvek = prohlizec.find_element_by_id("Form_Password")
    #heslo = keyring.get_password('totaljobs_com', 'heslo')
    #prvek.send_keys(heslo)
    ##time.sleep(2)
    ##prvek.submit()


    ##prvek = pockame.until(EC.presence_of_element_located((By.ID, 'login-submit-button')))
    #prvek = prohlizec.find_element_by_id("btnLogin")
    #time.sleep(2)
    #prvek.click()




    #<a class="govuk-link" href="https://findajob.dwp.gov.uk/search">Search for jobs</a>

    ## dalsi stranka
    ## Your account
    #time.sleep(5)

    #prohlizec.get("https://findajob.dwp.gov.uk/search?cat=15&cty=permanent&cti=full_time&f=1&loc=86590&sf=50000&pp=50&sb=salary&sd=down")
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-answer')))
    #kontrolni_otazka = keyring.get_password('gov', 'kontrolni_otazka')
    #prvek.send_keys(kontrolni_otazka)
    #time.sleep(2)
    #prvek.submit()


    ## dalsi stranka
    ## Search for jobs



    ## dalsi stranka
    ## Home
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'work-search')))
    #prvek.click()


#interakce_reed_co_uk()












def interakce_monster_co_uk():
    """popis
    """

    #.# detach
    #.# #white:(.)
    #.# detach
    #.# partition interakce_monster_co_uk {
    #.# #khaki:interakce_monster_co_uk();
    #.# :Prihlasime se s udaji z keyringu;
    #.# }

    # Sign in
    adresa = keyring.get_password('monster_co_uk', 'url')
    prohlizec.get(adresa)


    pockame = WebDriverWait(prohlizec, 60)
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'email')))
    uzivatel = keyring.get_password('monster_co_uk', 'uzivatel')
    prvek.send_keys(uzivatel)


    prvek = prohlizec.find_element_by_id("password")
    heslo = keyring.get_password('monster_co_uk', 'heslo')
    prvek.send_keys(heslo)
    #time.sleep(2)
    #prvek.submit()


    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'login-submit-button')))
    prvek = prohlizec.find_element_by_id("btn-login")
    time.sleep(2)
    prvek.click()


#jdi na https://www.monster.co.uk/jobs/


    #<a class="govuk-link" href="https://findajob.dwp.gov.uk/search">Search for jobs</a>

    ## dalsi stranka
    ## Your account
    #time.sleep(5)

    #prohlizec.get("https://findajob.dwp.gov.uk/search?cat=15&cty=permanent&cti=full_time&f=1&loc=86590&sf=50000&pp=50&sb=salary&sd=down")
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-answer')))
    #kontrolni_otazka = keyring.get_password('gov', 'kontrolni_otazka')
    #prvek.send_keys(kontrolni_otazka)
    #time.sleep(2)
    #prvek.submit()


    ## dalsi stranka
    ## Search for jobs



    ## dalsi stranka
    ## Home
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'work-search')))
    #prvek.click()


#interakce_monster_co_uk()






def interakce_jobs_ac_uk():
    """popis
    """

    #.# detach
    #.# #white:(.)
    #.# detach
    #.# partition interakce_jobs_ac_uk {
    #.# #khaki:interakce_jobs_ac_uk();
    #.# :Prihlasime se s udaji z keyringu;
    #.# }

    # Sign in
    adresa = keyring.get_password('jobs_ac_uk', 'url')
    prohlizec.get(adresa)


    pockame = WebDriverWait(prohlizec, 60)
    prvek = pockame.until(EC.presence_of_element_located((By.ID, 'signin-email')))
    uzivatel = keyring.get_password('jobs_ac_uk', 'uzivatel')
    prvek.send_keys(uzivatel)


    prvek = prohlizec.find_element_by_id("signin-password")
    heslo = keyring.get_password('jobs_ac_uk', 'heslo')
    prvek.send_keys(heslo)
    #time.sleep(2)
    #prvek.submit()


    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'login-submit-button')))
    prvek = prohlizec.find_element_by_id("submit")
    time.sleep(2)
    prvek.click()


#jdi na https://www.jobs.ac.uk/

    #<a class="govuk-link" href="https://findajob.dwp.gov.uk/search">Search for jobs</a>

    ## dalsi stranka
    ## Your account
    #time.sleep(5)

    #prohlizec.get("https://findajob.dwp.gov.uk/search?cat=15&cty=permanent&cti=full_time&f=1&loc=86590&sf=50000&pp=50&sb=salary&sd=down")
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'id-answer')))
    #kontrolni_otazka = keyring.get_password('gov', 'kontrolni_otazka')
    #prvek.send_keys(kontrolni_otazka)
    #time.sleep(2)
    #prvek.submit()


    ## dalsi stranka
    ## Search for jobs



    ## dalsi stranka
    ## Home
    #prvek = pockame.until(EC.presence_of_element_located((By.ID, 'work-search')))
    #prvek.click()


#interakce_jobs_ac_uk()


#interakce_findajob_dwp_gov_uk()
#interakce_indeed_co_uk()
#interakce_totaljobs_com()
#interakce_reed_co_uk()
#interakce_monster_co_uk()
#interakce_jobs_ac_uk()
