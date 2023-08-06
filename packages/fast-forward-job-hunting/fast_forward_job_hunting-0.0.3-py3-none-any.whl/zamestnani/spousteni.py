#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webbrowser
import time
import subprocess


#def otevri_novinky():
    #webbrowser.open('https://yandex.com')
    ##time.sleep(5)
    #webbrowser.open('https://www.ceskenoviny.cz/')
    
    
def zaloz_novou_osobu():
    subprocess.Popen(['/usr/bin/sqlitebrowser', 'cv.db'])


def zaloz_novy_pripad():
    subprocess.Popen(['/usr/bin/python3', '-m', 'cv'])


def sepisuj_chronologii():
    #subprocess.Popen(['/usr/bin/python3', '-m', 'litigationgui'])
    subprocess.Popen(['/usr/bin/sqlitebrowser', 'zamestnani.db'])


def sestav_predzalobku():
    subprocess.Popen(['/usr/bin/python3', '-m', 'selen_zamestnani'])


def sestav_svedeckou_vypoved():
    subprocess.Popen(['/usr/bin/python3', '-m', 'selen'])
    
    
def sestav_particulars_of_claim():
    #subprocess.Popen(['start', 'terms_conditions.txt'], shell=True) #pro widle
    subprocess.Popen(['see', 'terms_conditions.pdf'])

def sestav_bundle():
    subprocess.Popen(['/usr/bin/python3', '-m', 'create_bundle'])
