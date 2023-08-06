#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#shebang predelat u vsech modulu

import os, sys, stat, time
import pyperclip
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pathlib import Path
import subprocess



print(__file__, f"Current directory: {Path.cwd()}")
print(__file__, f"Home directory: {Path.home()}")


import spousteni
#from litigation.litigation import spousteni

#import brouzdani
#import editovani
#import sachovani

# pridat tlacitka na jednotlive formulare




text_ze_schranky = pyperclip.paste()
#print('text_ze_schranky:', text_ze_schranky)


class Handler:

    def __init__(self):
        self.pripona_souboru = 'py'
        self.adresar_souboru = ''
        #self.gladefile = "novy_soubor.glade"
        #pass


    def on_window1_destroy(self, *args):
        Gtk.main_quit()


    #def on_rbpython_toggled(self, widget):
        #if widget.get_active():
            #print("radiobutton selection changed to rbpython")
            #self.pripona_souboru = 'py'


### BROUZDANI

    #def on_btn_vytvor_summary_clicked(self, *args):
        #subprocess.Popen(['/usr/bin/python3', 'summary.py'])


    #def on_btn_otevri_novinky_clicked(self, *args):
        #brouzdani.otevri_novinky()


### SPOUSTENI

    def on_btn_zaloz_novou_osobu_clicked(self, *args):
        spousteni.zaloz_novou_osobu()


    def on_btn_zaloz_novy_pripad_clicked(self, *args):
        spousteni.zaloz_novy_pripad()
        
        
    def on_button_sepisuj_chronologii_clicked(self, *args):
        spousteni.sepisuj_chronologii()


    def on_button_sestav_predzalobku_clicked(self, *args):
        spousteni.sestav_predzalobku()


    def on_button_sestav_svedeckou_vypoved_clicked(self, *args):
        spousteni.sestav_svedeckou_vypoved()


    def on_button_sestav_particulars_of_claim_clicked(self, *args):
        spousteni.sestav_particulars_of_claim()
        

    def on_button_sestav_bundle_clicked(self, *args):
        spousteni.sestav_bundle()




class Example:
    
    def __init__(self):
        
        self.gladefile = "centrala.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(Handler())


        #handlers = {
            #"onDestroy": Gtk.main_quit,
            #"onButtonPressed": hello
        #}
        #builder.connect_signals(handlers)


        window = self.builder.get_object("window1")
        window.show_all()

    def main(self):
        Gtk.main()


x = Example()
x.main()
