#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Vytvori CV na miru
"""

# TODO OTEVRI PDF SOUBOR PO VYTVORENI

import gi, sqlite3, os, glob, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pathlib import Path
from shutil import copyfile

class Cv(Gtk.Window):
    """Hlavni trida
    """

    #.# partition Cv {
    #.# #LightSalmon:Cv(Gtk.Window);
    #.# :otevreme pripojeni k db;
    #.# 'detach
    #.# #white:(.)
    #.# detach
        
    global pripojeni
    pripojeni = sqlite3.connect("cv.db")
    
    global vybrane_dilci_texty
    vybrane_dilci_texty = {}

    global vybrana_osoba
    vybrana_osoba = {}
    
    def pri_prepnuti_zaskrtavatka_osoby(self, zaskrtavatko, nazev, id):
        """Vyber osobu
        """

        #.# partition pri_prepnuti_zaskrtavatka_osoby {
        #.# #khaki:pri_prepnuti_zaskrtavatka_osoby(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach
    
        if zaskrtavatko.get_active():
            state = "za"
            vybrana_osoba[id] = slovnikdict_applicant_name[id]
        else:
            state = "od"
            del vybrana_osoba[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")

        global text_vybrana_osoba
        text_vybrana_osoba = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrana_osoba.items(), key=lambda x: x[1][5], reverse=False):
            text_vybrana_osoba = str(i[1][1] or "") + i[1][2] + " " + str(i[1][3] or "") + " " + i[1][4] + " " + str(i[1][5] or "")
        print(text_vybrana_osoba)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrana_osoba' : r'''
\begin{center}
\section*{''' + text_vybrana_osoba + r'''}'''} )
        print(vybrana_osoba)

        
    global vybrany_kontakt
    vybrany_kontakt = {}

    def pri_prepnuti_zaskrtavatka_kontaktu(self, zaskrtavatko, nazev, id):
        """Vyber kontakt
        """

        #.# partition pri_prepnuti_zaskrtavatka_kontaktu {
        #.# #khaki:pri_prepnuti_zaskrtavatka_kontaktu(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrany_kontakt[id] = slovnikdict_contact[id]
        else:
            state = "od"
            del vybrany_kontakt[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")

        global text_vybrany_kontakt
        text_vybrany_kontakt = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrany_kontakt.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrany_kontakt = text_vybrany_kontakt + "\n" + i[1][1] + ", mobile: " + i[1][2] + ", email: " + i[1][3] + " " + str(i[1][4] or "" + r"\\")
        print(text_vybrany_kontakt)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrany_kontakt' : text_vybrany_kontakt + r'''
\end{center}'''} )
        print(vybrany_kontakt)
        
        
    global vybrany_uvod
    vybrany_uvod = {}

    def pri_prepnuti_zaskrtavatka_uvodu(self, zaskrtavatko, nazev, id):
        """Vyber uvod
        """

        #.# partition pri_prepnuti_zaskrtavatka_uvodu {
        #.# #khaki:pri_prepnuti_zaskrtavatka_uvodu(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrany_uvod[id] = slovnikdict_introduction[id]
        else:
            state = "od"
            del vybrany_uvod[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")

        global text_vybrany_uvod
        text_vybrany_uvod = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrany_uvod.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrany_uvod = text_vybrany_uvod + "\n" + i[1][1]
        print(text_vybrany_uvod)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrany_uvod' : text_vybrany_uvod} )
        print(vybrany_uvod)
        
        
    global vybrana_vzdelani
    vybrana_vzdelani = {}

    def pri_prepnuti_zaskrtavatka_vzdelani(self, zaskrtavatko, nazev, id):
        """Vyber vzdelani
        """

        #.# partition pri_prepnuti_zaskrtavatka_vzdelani {
        #.# #khaki:pri_prepnuti_zaskrtavatka_vzdelani(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach
        
        if zaskrtavatko.get_active():
            state = "za"
            vybrana_vzdelani[id] = slovnikdict_education[id]
        else:
            state = "od"
            del vybrana_vzdelani[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")

        global text_vybrana_vzdelani
        text_vybrana_vzdelani = ""

        global vybrane_dilci_texty
        
        for i in sorted(vybrana_vzdelani.items(), key=lambda x: x[1][3], reverse=True):
            text_vybrana_vzdelani = text_vybrana_vzdelani + "\n\n" + r"\subsubsection*{" + i[1][2] + "}\n" + i[1][1].title() + ", " + i[1][5] + ", " + i[1][6].upper() + ", " + str(i[1][8] or "") + r"\\" + "\n" + str(i[1][7] or "") + "\n" + str(i[1][9] or "")
        print(text_vybrana_vzdelani)
        print("*****************")
        vybrane_dilci_texty.update({'text_vybrana_vzdelani' : r"\subsection*{EDUCATION AND QUALIFICATIONS \hrulefill{}}" + text_vybrana_vzdelani})
        #print(vybrana_vzdelani)
        
        
    global vybrane_praxe
    vybrane_praxe = {}

    def pri_prepnuti_zaskrtavatka(self, zaskrtavatko, nazev, id):
        """Vyber praxi
        """

        #.# partition pri_prepnuti_zaskrtavatka {
        #.# #khaki:pri_prepnuti_zaskrtavatka(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_praxe[id] = slovnikdict[id]
        else:
            state = "od"
            del vybrane_praxe[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_praxe
        text_vybrane_praxe = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_praxe.items(), key=lambda x: x[1][4], reverse=True):
            text_vybrane_praxe = text_vybrane_praxe + "\n" + r"\subsubsection*{" + i[1][3].title() + "}" + "\n" + i[1][0].title() + ", " + i[1][1].title() + ", " + i[1][2].upper() + r"\\" + i[1][6]
        print(text_vybrane_praxe)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_praxe' : r"\subsection*{CAREER SUMMARY \hrulefill{}}" + text_vybrane_praxe} )
        print(vybrane_praxe)

        
    global vybrane_jine_aktivity
    vybrane_jine_aktivity = {}

    def pri_prepnuti_zaskrtavatka_jinych_aktivit(self, zaskrtavatko, nazev, id):
        """Vyber jine aktivity
        """

        #.# partition pri_prepnuti_zaskrtavatka_jinych_aktivit {
        #.# #khaki:pri_prepnuti_zaskrtavatka_jinych_aktivit(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_jine_aktivity[id] = slovnikdict_other_activities[id]
        else:
            state = "od"
            del vybrane_jine_aktivity[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_jine_aktivity
        text_vybrane_jine_aktivity = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_jine_aktivity.items(), key=lambda x: x[1][5], reverse=True):
            text_vybrane_jine_aktivity = text_vybrane_jine_aktivity + "\n" + r"\subsubsection*{" + i[1][2] + "}" + "\n" + i[1][1].title() + ", " + i[1][3].title() + ", " + i[1][4].upper() + r"\\" + i[1][7]
        print(text_vybrane_jine_aktivity)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_jine_aktivity' : r"\subsection*{MEMBERSHIPS AND VOLUNTEERING \hrulefill{}}" + text_vybrane_jine_aktivity} )
        print(vybrane_jine_aktivity)
        
        
    global vybrane_publikace
    vybrane_publikace = {}

    def pri_prepnuti_zaskrtavatka_publikaci(self, zaskrtavatko, nazev, id):
        """Vyber publikace
        """

        #.# partition pri_prepnuti_zaskrtavatka_publikaci {
        #.# #khaki:pri_prepnuti_zaskrtavatka_publikaci(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_publikace[id] = slovnikdict_publications[id]
        else:
            state = "od"
            del vybrane_publikace[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_publikace
        text_vybrane_publikace = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_publikace.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrane_publikace = text_vybrane_publikace + "\n" + i[1][1] + r'''\\
 \\'''
        print(text_vybrane_publikace)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_publikace' : r"\subsection*{PUBLICATIONS \hrulefill{}}" + text_vybrane_publikace} )
        print(vybrane_publikace)
        
        
    global vybrana_programovani
    vybrana_programovani = {}

    def pri_prepnuti_zaskrtavatka_programovani(self, zaskrtavatko, nazev, id):
        """Vyber programovani
        """

        #.# partition pri_prepnuti_zaskrtavatka_programovani {
        #.# #khaki:pri_prepnuti_zaskrtavatka_programovani(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrana_programovani[id] = slovnikdict_computer_skills[id]
        else:
            state = "od"
            del vybrana_programovani[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrana_programovani
        text_vybrana_programovani = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrana_programovani.items(), key=lambda x: x[1][1], reverse=False):
            text_vybrana_programovani = text_vybrana_programovani + "\n" + i[1][1] + ", "
        print(text_vybrana_programovani)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrana_programovani' : r"\subsection*{PROGRAMMING LANGUAGES AND SOFTWARE \hrulefill{}}" + text_vybrana_programovani} )
        print(vybrana_programovani)
        
        
    global vybrane_jazyky
    vybrane_jazyky = {}

    def pri_prepnuti_zaskrtavatka_jazyku(self, zaskrtavatko, nazev, id):
        """Vyber jazyky
        """

        #.# partition pri_prepnuti_zaskrtavatka_jazyku {
        #.# #khaki:pri_prepnuti_zaskrtavatka_jazyku(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_jazyky[id] = slovnikdict_languages[id]
        else:
            state = "od"
            del vybrane_jazyky[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_jazyky
        text_vybrane_jazyky = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_jazyky.items(), key=lambda x: x[1][1], reverse=False):
            text_vybrane_jazyky = text_vybrane_jazyky + "\n" + i[1][1] + " " + i[1][2] + ", "
        print(text_vybrane_jazyky)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_jazyky' : r"\subsection*{LANGUAGES \hrulefill{}}" + text_vybrane_jazyky} )
        print(vybrane_jazyky)
        
        
    global vybrane_pravnicke_dovednosti
    vybrane_pravnicke_dovednosti = {}

    def pri_prepnuti_zaskrtavatka_pravnickych_dovednosti(self, zaskrtavatko, nazev, id):
        """Vyber pravnicke dovednosti
        """

        #.# partition pri_prepnuti_zaskrtavatka_pravnickych_dovednosti {
        #.# #khaki:pri_prepnuti_zaskrtavatka_pravnickych_dovednosti(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_pravnicke_dovednosti[id] = slovnikdict_legal_skills[id]
        else:
            state = "od"
            del vybrane_pravnicke_dovednosti[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_pravnicke_dovednosti
        text_vybrane_pravnicke_dovednosti = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_pravnicke_dovednosti.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrane_pravnicke_dovednosti = text_vybrane_pravnicke_dovednosti + "\n" + i[1][1] + ", "
        print(text_vybrane_pravnicke_dovednosti)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_pravnicke_dovednosti' : r"\subsection*{EXPERTISE \hrulefill{}}" + text_vybrane_pravnicke_dovednosti} )
        print(vybrane_pravnicke_dovednosti)
        
        
    global vybrane_ruzne_dovednosti
    vybrane_ruzne_dovednosti = {}

    def pri_prepnuti_zaskrtavatka_ruznych_dovednosti(self, zaskrtavatko, nazev, id):
        """Vyber ruzne dovednosti
        """

        #.# partition pri_prepnuti_zaskrtavatka_ruznych_dovednosti {
        #.# #khaki:pri_prepnuti_zaskrtavatka_ruznych_dovednosti(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_ruzne_dovednosti[id] = slovnikdict_other_skills[id]
        else:
            state = "od"
            del vybrane_ruzne_dovednosti[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_ruzne_dovednosti
        text_vybrane_ruzne_dovednosti = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_ruzne_dovednosti.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrane_ruzne_dovednosti = text_vybrane_ruzne_dovednosti + "\n" + i[1][1] + ", "
        print(text_vybrane_ruzne_dovednosti)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_ruzne_dovednosti' : r"\subsection*{SKILLS \hrulefill{}}" + text_vybrane_ruzne_dovednosti} )
        print(vybrane_ruzne_dovednosti)


    global vybrana_osvedceni
    vybrana_osvedceni = {}

    def pri_prepnuti_zaskrtavatka_osvedceni(self, zaskrtavatko, nazev, id):
        """Vyber osvedceni
        """

        #.# partition pri_prepnuti_zaskrtavatka_osvedceni {
        #.# #khaki:pri_prepnuti_zaskrtavatka_osvedceni(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrana_osvedceni[id] = slovnikdict_licences[id]
        else:
            state = "od"
            del vybrana_osvedceni[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrana_osvedceni
        text_vybrana_osvedceni = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrana_osvedceni.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrana_osvedceni = text_vybrana_osvedceni + "\n" + i[1][1] + ", "
        print(text_vybrana_osvedceni)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrana_osvedceni' : r"\subsection*{LICENCES \hrulefill{}}" + text_vybrana_osvedceni} )
        print(vybrana_osvedceni)


    global vybrane_zaliby
    vybrane_zaliby = {}

    def pri_prepnuti_zaskrtavatka_zalib(self, zaskrtavatko, nazev, id):
        """Vyber zaliby
        """

        #.# partition pri_prepnuti_zaskrtavatka_zalib {
        #.# #khaki:pri_prepnuti_zaskrtavatka_zalib(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_zaliby[id] = slovnikdict_hobbies[id]
        else:
            state = "od"
            del vybrane_zaliby[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_zaliby
        text_vybrane_zaliby = ""
        
        global vybrane_dilci_texty
        
        for i in sorted(vybrane_zaliby.items(), key=lambda x: x[1][1], reverse=False):
            text_vybrane_zaliby = text_vybrane_zaliby + "\n" + i[1][1] + ", "
        print(text_vybrane_zaliby)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_zaliby' : r"\subsection*{PERSONAL INTERESTS \hrulefill{}}" + text_vybrane_zaliby} )
        print(vybrane_dilci_texty)
    
    
    global vybrane_poznamky
    vybrane_poznamky = {}

    def pri_prepnuti_zaskrtavatka_poznamek(self, zaskrtavatko, nazev, id):
        """Vyber poznamky
        """

        #.# partition pri_prepnuti_zaskrtavatka_poznamek {
        #.# #khaki:pri_prepnuti_zaskrtavatka_poznamek(self, zaskrtavatko, nazev, id);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        if zaskrtavatko.get_active():
            state = "za"
            vybrane_poznamky[id] = slovnikdict_notes[id]
        else:
            state = "od"
            del vybrane_poznamky[id]
        print("\nZaskrtavatko", nazev, id, "bylo "+state+"skrtnuto.\n")
        
        global text_vybrane_poznamky
        text_vybrane_poznamky = ""
     
        global vybrane_dilci_texty
     
        for i in sorted(vybrane_poznamky.items(), key=lambda x: x[1][0], reverse=True):
            text_vybrane_poznamky = text_vybrane_poznamky + "\n" + i[1][1] + " "
        print(text_vybrane_poznamky)
        print("*****************")
        vybrane_dilci_texty.update( {'text_vybrane_poznamky' : r"\subsection*{NOTES \hrulefill{}}" + text_vybrane_poznamky} )
        print(vybrane_dilci_texty)

    def ukaz_vybrane_dilci_texty(self, button):
        """Ukaz vybrane dilci texty
        """

        #.# partition ukaz_vybrane_dilci_texty {
        #.# #khaki:ukaz_vybrane_dilci_texty(self, button);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        global vybrane_dilci_texty
        for klic, hodnota in vybrane_dilci_texty.items():
            print(hodnota)
            
    def vytvor_soubor(self, button):
        """Vytvor soubor
        """

        #.# partition vytvor_soubor {
        #.# #khaki:vytvor_soubor(self, button);
        #.# }
        #.# detach
        #.# #white:(.)
        #.# detach

        global vybrane_dilci_texty
        hlavicka_latexoveho_souboru = r'''\documentclass[11pt, a4paper]{article}
\addtolength{\voffset}{-2cm}
\addtolength{\textheight}{2.5cm}
\addtolength{\hoffset}{-2cm}
\addtolength{\textwidth}{4cm}
\usepackage[utf8]{inputenc}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{tabularx}

\begin{document}'''

        text = ""
        
        paticka_latexoveho_souboru = r'''
\end{document}'''
        
        with open("cv_z_optimizeru.tex", "w") as file:
            for klic, hodnota in vybrane_dilci_texty.items():
                text = text + hodnota
            print(text)
            file.write(hlavicka_latexoveho_souboru + text + paticka_latexoveho_souboru)
        
        prikazova_radka = subprocess.Popen(['pdflatex', 'cv_z_optimizeru.tex'])
        prikazova_radka.communicate()

        os.unlink('cv_z_optimizeru.log')
        os.unlink('cv_z_optimizeru.tex')
        os.unlink('cv_z_optimizeru.aux')

        source = Path('cv_z_optimizeru.pdf')
        destination = Path.home() / 'cv_tailored.pdf'
        copyfile(source, destination)
        os.unlink(source)

        print("\nVytvorili jsme soubor")

    def __init__(self):
        """Vytvor okno programu
        """

        #.# partition __init__ {
        #.# #khaki:__init__(self);
        #.# :definujeme zakladni rozvrzeni okna;

        Gtk.Window.__init__(self, title="Tailor CV")
        self.set_border_width(10)
        self.set_default_size(700, 550)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_icon_name('arrow-right-double')
        
        self.svisly_ramec_tlacitek_a_zalozek = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.svisly_ramec_tlacitek_a_zalozek)
        
        self.lezaty_ramec_tlacitek = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.svisly_ramec_tlacitek_a_zalozek.add(self.lezaty_ramec_tlacitek)

        #.# :tlacitkem volame ukaz_vybrane_dilci_texty();

        self.tlacitko_ukaz_vybrane_dilci_texty = Gtk.Button(label="Show Selected Texts")
        self.tlacitko_ukaz_vybrane_dilci_texty.connect("clicked", self.ukaz_vybrane_dilci_texty)
        #self.lezaty_ramec_tlacitek.pack_start(self.tlacitko_ukaz_vybrane_dilci_texty, True, True, 0)

        #.# :tlacitkem volame vytvor_soubor();

        self.tlacitko_vytvor_soubor = Gtk.Button(label="Create File")
        self.tlacitko_vytvor_soubor.connect("clicked", self.vytvor_soubor)
        self.lezaty_ramec_tlacitek.pack_start(self.tlacitko_vytvor_soubor, True, True, 0)

        #.# :definujeme notebook;
        
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(0)
        self.notebook.set_scrollable(True)
        self.svisly_ramec_tlacitek_a_zalozek.add(self.notebook)

        #.# :zalozka applicant_name;

        self.applicant_name = Gtk.Box()
        self.applicant_name.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec applicant_name
        #.# a vytvorime z nej radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM applicant_name ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_applicant_name
        slovnikdict_applicant_name = {}
        for i in zaznamy:
            slovnikdict_applicant_name[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(str(i[1] or "") + i[2] + " • " + str(i[3] or "") + " • " + i[4] + " • " + str(i[5] or ""), xalign=0)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_osoby();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_osoby, i[5], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.applicant_name.add(rolovaci_okno)
        self.notebook.append_page(self.applicant_name, Gtk.Label("Applicant's Name"))

        #.# :zalozka contact;

        self.contact = Gtk.Box()
        self.contact.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec contact
        #.# a vytvorime z nej radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM contact ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_contact
        slovnikdict_contact = {}
        for i in zaznamy:
            slovnikdict_contact[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1] + " • " + i[2] + " • " + i[3] + " • " + str(i[4] or ""), xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_kontaktu();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_kontaktu, i[2], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.contact.add(rolovaci_okno)
        self.notebook.append_page(self.contact, Gtk.Label('Contact'))

        #.# :zalozka introduction;

        self.introduction = Gtk.Box()
        self.introduction.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec introduction
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM introduction ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_introduction
        slovnikdict_introduction = {}
        for i in zaznamy:
            slovnikdict_introduction[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_uvodu();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_uvodu, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.introduction.add(rolovaci_okno)
        self.notebook.append_page(self.introduction, Gtk.Label('Introduction'))

        #.# :zalozka experience;

        self.experience = Gtk.Box()
        self.experience.set_border_width(10)
                
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec experience
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM experience ORDER BY start DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict
        slovnikdict = {}
        for i in zaznamy:
            slovnikdict[i[7]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[3] + " • " + i[0] + " • " + i[1] + " • " + i[2] + " • " + i[6], xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka, i[0], i[7])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.experience.add(rolovaci_okno)
        self.notebook.append_page(self.experience, Gtk.Label('Experience'))

        #.# :zalozka legal_skills;

        self.legal_skills = Gtk.Box()
        self.legal_skills.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec legal_skills
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM legal_skills ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_legal_skills
        slovnikdict_legal_skills = {}
        for i in zaznamy:
            slovnikdict_legal_skills[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()

            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_pravnickych_dovednosti();

            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_pravnickych_dovednosti, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.legal_skills.add(rolovaci_okno)
        self.notebook.append_page(self.legal_skills, Gtk.Label('Legal Skills'))

        #.# :zalozka computer_skills;

        self.computer_skills = Gtk.Box()
        self.computer_skills.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec computer_skills
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM computer_skills ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_computer_skills
        slovnikdict_computer_skills = {}
        for i in zaznamy:
            slovnikdict_computer_skills[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            zaskrtavatko = Gtk.CheckButton()

            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_programovani();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_programovani, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.computer_skills.add(rolovaci_okno)
        self.notebook.append_page(self.computer_skills, Gtk.Label('Computer Skills'))

        #.# :zalozka other_skills;

        self.other_skills = Gtk.Box()
        self.other_skills.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec other_skills
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM other_skills ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_other_skills
        slovnikdict_other_skills = {}
        for i in zaznamy:
            slovnikdict_other_skills[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_ruznych_dovednosti();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_ruznych_dovednosti, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.other_skills.add(rolovaci_okno)
        self.notebook.append_page(self.other_skills, Gtk.Label('Other Skills'))

        #.# :zalozka publications;

        self.publications = Gtk.Box()
        self.publications.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec publications
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM publications ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_publications
        slovnikdict_publications = {}
        for i in zaznamy:
            slovnikdict_publications[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_publikaci();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_publikaci, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.publications.add(rolovaci_okno)
        self.notebook.append_page(self.publications, Gtk.Label('Publications'))

        #.# :zalozka education;
        
        self.education = Gtk.Box()
        self.education.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec education
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM education ORDER BY start DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_education
        slovnikdict_education = {}
        for i in zaznamy:
            slovnikdict_education[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[2] + " • " + i[1] + " • " + i[5] + " • " + i[6] + " • " + str(i[8] or "") + " • " + str(i[7] or "") + " • " + str(i[9] or ""), xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_vzdelani();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_vzdelani, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.education.add(rolovaci_okno)
        self.notebook.append_page(self.education, Gtk.Label('Education'))

        #.# :zalozka licences;

        self.licences = Gtk.Box()
        self.licences.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec licences
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM licences ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_licences
        slovnikdict_licences = {}
        for i in zaznamy:
            slovnikdict_licences[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_osvedceni();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_osvedceni, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.licences.add(rolovaci_okno)
        self.notebook.append_page(self.licences, Gtk.Label('Licences'))

        #.# :zalozka languages;

        self.languages = Gtk.Box()
        self.languages.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec languages
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM languages ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_languages
        slovnikdict_languages = {}
        for i in zaznamy:
            slovnikdict_languages[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1] + " • " + i[2], xalign=0)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_jazyku();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_jazyku, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.languages.add(rolovaci_okno)
        self.notebook.append_page(self.languages, Gtk.Label('Languages'))

        #.# :zalozka other_activities;

        self.other_activities = Gtk.Box()
        self.other_activities.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec other_activities
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM other_activities ORDER BY start DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_other_activities
        slovnikdict_other_activities = {}
        for i in zaznamy:
            slovnikdict_other_activities[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[2] + " • " + i[1] + " • " + i[3] + " • " + i[4] + " • " + i[7], xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_jinych_aktivit();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_jinych_aktivit, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.other_activities.add(rolovaci_okno)
        self.notebook.append_page(self.other_activities, Gtk.Label('Other Activities'))

        #.# :zalozka hobbies;

        self.hobbies = Gtk.Box()
        self.hobbies.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec hobbies
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM hobbies ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_hobbies
        slovnikdict_hobbies = {}
        for i in zaznamy:
            slovnikdict_hobbies[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_zalib();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_zalib, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.hobbies.add(rolovaci_okno)
        self.notebook.append_page(self.hobbies, Gtk.Label('Hobbies'))

        #.# :zalozka notes;

        self.notes = Gtk.Box()
        self.notes.set_border_width(10)
        
        rolovaci_okno = Gtk.ScrolledWindow()
        rolovaci_okno.set_hexpand(True)
        rolovaci_okno.set_vexpand(True)
        
        rolovaci_ram = Gtk.Viewport()
        rolovaci_okno.add(rolovaci_ram)
        
        seznam = Gtk.ListBox()
        seznam.set_selection_mode(Gtk.SelectionMode.NONE)
        rolovaci_ram.add(seznam)

        #.# :z db nacteme sloupec notes
        #.# a z nej vytvorime radky se zaskrtavatky;

        kurzor = pripojeni.cursor()
        kurzor.execute("SELECT * FROM notes ORDER BY id DESC")
        zaznamy = kurzor.fetchall()
        global slovnikdict_notes
        slovnikdict_notes = {}
        for i in zaznamy:
            slovnikdict_notes[i[0]] = i[:]
            radek_seznamu = Gtk.ListBoxRow()
            lezaty_ram = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            radek_seznamu.add(lezaty_ram)
            popiska = Gtk.Label(i[1], xalign=0)
            popiska.set_line_wrap(True)
            zaskrtavatko = Gtk.CheckButton()
            
            #.# :zaskrtavatkem volame pri_prepnuti_zaskrtavatka_poznamek();
            
            zaskrtavatko.connect("toggled", self.pri_prepnuti_zaskrtavatka_poznamek, i[1], i[0])
            lezaty_ram.pack_start(zaskrtavatko, False, True, 0)
            lezaty_ram.pack_start(popiska, True, True, 0)
            seznam.add(radek_seznamu)

        self.notes.add(rolovaci_okno)
        self.notebook.append_page(self.notes, Gtk.Label('Notes'))

        #.# :zavreme pripojeni k db;

        pripojeni.close()
        
        #.# }
        #.# detach
        #.# (.)
        #.# detach

    #.# }

#.# detach
#.# #white:(.)
#.# detach
#.# :Vytvorime instanci Cv() - tridy programu;

okno = Cv()
okno.connect("destroy", Gtk.main_quit)
okno.show_all()

#.# :spustime ji;

Gtk.main()
