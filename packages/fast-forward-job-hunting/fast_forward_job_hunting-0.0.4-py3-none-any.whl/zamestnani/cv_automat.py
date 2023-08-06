#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Vytvori CV na miru popisu pozice
"""


import glob
import os
import pprint
import sqlite3
import subprocess
import time

from nltk import word_tokenize          
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# Download stopwords list
#nltk.download('punkt')

job_description_summary = r'''
Judicium UK Work Permits Ltd is a Level 1 OISC regulated consultancy providing corporate immigration services to numerous public and private sector organisations throughout the UK. An opportunity has now arisen for an immigration consultant to join our Corporate Immigration team.

The candidate will be required to undertake a mixture of applications under the Immigration Rules for private individuals as well as Points Based System work for corporate clients.

Key responsibilities:
• To manage and be responsible for one’s own casework, processing applications and providing advice and assistance to clients and general service delivery, efficiently and diligently, ensuring that the highest standards are consistently met.
• Ensuring that all enquiries and service agreements are dealt with in line with agreed service standards and in the short-term and long-term interests of the company as well as the client.
• Remaining abreast of all relevant rules, laws and best practice affecting the company’s core activities
• Taking an active role in business development, and ensuring that agreed revenue targets are exceeded.
• Helping ensure adherence to OISC Rules and Codes.

The successful applicant will have:
• OISC Accreditation at Level 1
• Established UK immigration experience, having previously managed and undertaken casework in corporate immigration and general immigration
• Good legal research skills
• The ability to work independently and take ownership for their work
• Sound IT skills

Additionally, the individual will need to demonstrate excellent communication skills, good time management skills, commercial awareness, and a flair for business development as well as a positive attitude, conscientious approach to their work and the willingness to work as part of a team.

This is a great opportunity for the right person to make a contribution to the company’s success, and be rewarded accordingly. There are real prospects for growth and advancement for the right individual.
'''

global vybrane_dilci_texty

vybrane_dilci_texty = {}

# tuto funkci nikde nevolame?

def ukaz_vybrane_dilci_texty(self, button):

    """Ukaz vybrane dilci texty
    """


    #.# partition ukaz_vybrane_dilci_texty {
    #.# #khaki:ukaz_vybrane_dilci_texty(self, button);
    #.# }
    #.# detach
    #.# #white:(.)
    #.# detach


    for klic, hodnota in vybrane_dilci_texty.items():

        print(hodnota)

        
def vytvor_soubor(osoba_do_nazvu_souboru, url_do_nazvu_souboru):

    """Vytvor soubor
    """


    #.# partition vytvor_soubor {
    #.# #khaki:vytvor_soubor(self, button);
    #.# }
    #.# detach
    #.# #white:(.)
    #.# detach


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
    
    with open(f"{osoba_do_nazvu_souboru}_cv_{url_do_nazvu_souboru}.tex", "w") as file:

        for klic, hodnota in vybrane_dilci_texty.items():

            text = text + hodnota

        #print(text)

        file.write(hlavicka_latexoveho_souboru + text + paticka_latexoveho_souboru)
    
    prikazova_radka = subprocess.Popen(['pdflatex', f"{osoba_do_nazvu_souboru}_cv_{url_do_nazvu_souboru}.tex"])

    prikazova_radka.communicate()

    os.unlink(f"{osoba_do_nazvu_souboru}_cv_{url_do_nazvu_souboru}.log")
    
    print("\nVytvorili jsme soubor")


def sestav_zivotopis(job_description_summary, osoba_do_nazvu_souboru, url_do_nazvu_souboru = ''):

    """Vytvor okno programu
    """

    startTime_cv_automat = time.time()

    pripojeni = sqlite3.connect("cv.db")

    pripojeni.row_factory = sqlite3.Row


    #.# partition sestav_zivotopis {
    #.# #khaki:vytvor_zivotopis(job_description_summary, url_do_nazvu_souboru = '');
    #.# :z db nacteme tabulku applicant_name
    

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM applicant_name ORDER BY id DESC LIMIT 1")

    zaznamy = kurzor.fetchall()
    
    #zaznamy = kurzor.fetchone()

    text_vybrana_osoba = ""

                
    for i in zaznamy:

        text_vybrana_osoba = text_vybrana_osoba + "\n" + str(i['prefix'] or "") + i['first_name'] + " " + str(i['middle_name'] or "") + " " + i['surname'] + " " + str(i['suffix'] or "")


    #print(text_vybrana_osoba)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrana_osoba' : r'''
\begin{center}
\section*{''' + text_vybrana_osoba + r'''}'''} )







    #.# :z db nacteme sloupec contact;


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM contact WHERE id = 3")

    zaznamy = kurzor.fetchall()

    text_vybrany_kontakt = ""

    
    for i in zaznamy:

        text_vybrany_kontakt = text_vybrany_kontakt + "\n" + i['city'] + ", mobile: " + i['mobile'] + ", email: " + i['email'] + " " + str(i['url'] or "" + r"\\")

    #print(text_vybrany_kontakt)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrany_kontakt' : text_vybrany_kontakt + r'''
\end{center}'''} )








    #.# :z db nacteme tabulku introduction;


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM introduction ORDER BY id")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    class DelicSlovnichZakladu:

        """Interface lemma tokenizer from nltk with sklearn
        """

        #.# partition DelicSlovnichZakladu {
        #.# #LightSalmon:DelicSlovnichZakladu;
        #.# :otevreme pripojeni k db;


        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            """init
            """


            #.# partition __init__ {
            #.# #khaki:__init__(self);
            #.# }
            #.# detach
            #.# '#white:(.)
            #.# detach


            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            """call
            """


            #.# partition __call__ {
            #.# #khaki:__call__(self, doc);
            #.# }
            #.# detach
            #.# '#white:(.)
            #.# detach
            
            
            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


        #.# detach
        #.# #white:(.)
        #.# detach
        #.# }


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(i['summary'])


    #print('jednotlive_texty:', jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\nkosinove_podobnosti:', kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('seznam_podobnosti:', seznam_podobnosti)

    # inbuilt function to find the position of minimum 

    #minpos = a.index(min(a))        

    # inbuilt function to find the position of maximum 

    #maxpos = a.index(max(a)) 

    index_nejvyssi_hodnoty_seznamu = seznam_podobnosti.index(max(seznam_podobnosti))

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})



            
            


    #.# :z db nacteme tabulku experience

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM experience ORDER BY start DESC")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['employer']}\
{i['location']}\
{i['country']}\
{i['position']}\
{i['activities']}")


    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 5
    
    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrane_praxe = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrane_praxe = text_vybrane_praxe + "\n" + r"\subsubsection*{" + zaznamy[i]['position'].title() + "}" + "\n" + zaznamy[i]['employer'].title() + ", " + zaznamy[i]['location'].title() + ", " + zaznamy[i]['country'].upper() + r"\\" + zaznamy[i]['activities']


    #print(text_vybrane_praxe)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_praxe' : r"\subsection*{CAREER SUMMARY \hrulefill{}}" + text_vybrane_praxe} )







    #.# :z db nacteme tabulku legal_skills

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM legal_skills ORDER BY id DESC")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['lawyering_skill']}")


    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 20
    
    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrane_pravnicke_dovednosti = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrane_pravnicke_dovednosti = text_vybrane_pravnicke_dovednosti + "\n" + zaznamy[i]['lawyering_skill'] + ", "

    
    #print(text_vybrane_pravnicke_dovednosti)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_pravnicke_dovednosti' : r"\subsection*{EXPERTISE \hrulefill{}}" + text_vybrane_pravnicke_dovednosti} )








    #.# :z db nacteme tabulku computer_skills


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM computer_skills ORDER BY it_skill")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['it_skill']}")


    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 30
    
    # TODO VYBRAT JEN POLOZKY VETSI NEZ NULA?

    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrana_programovani = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrana_programovani = text_vybrana_programovani + "\n" + zaznamy[i]['it_skill'] + ", "


    #print(text_vybrana_programovani)    

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrana_programovani' : r"\subsection*{PROGRAMMING LANGUAGES AND SOFTWARE \hrulefill{}}" + text_vybrana_programovani} )










    #.# :z db nacteme tabulku other_skills

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM other_skills ORDER BY additional_skill")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['additional_skill']}")

    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 20
    
    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrane_ruzne_dovednosti = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrane_ruzne_dovednosti = text_vybrane_ruzne_dovednosti + "\n" + zaznamy[i]['additional_skill'] + ", "


    #print(text_vybrane_ruzne_dovednosti)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_ruzne_dovednosti' : r"\subsection*{SKILLS \hrulefill{}}" + text_vybrane_ruzne_dovednosti} )








    #.# :z db nacteme tabulku publications


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM publications ORDER BY citation")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['citation']}")


    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 20

    # TODO VYBIRAT JEN POLOZKY VETSI NEZ NULA?

    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrane_publikace = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrane_publikace = text_vybrane_publikace + "\n" + zaznamy[i]['citation'] + r'''\\
\\'''


    #print(text_vybrane_publikace)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_publikace' : r"\subsection*{PUBLICATIONS \hrulefill{}}" + text_vybrane_publikace} )







    #.# :z db nacteme sloupec education

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM education ORDER BY start DESC")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['award']}\
{i['institution']}\
{i['location']}\
{i['country']}\
{i['exam']}\
{i['grades']}\
{i['notes']}")


    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 10

    # TODO VYBIRAT JEN PODOBNOSTI VYSSI NEZ NULA

    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrana_vzdelani = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrana_vzdelani = text_vybrana_vzdelani + "\n\n" + r"\subsubsection*{" + zaznamy[i]['award'] + "}\n" + zaznamy[i]['institution'].title() + ", " + zaznamy[i]['location'] + ", " + zaznamy[i]['country'].upper() + ", " + str(zaznamy[i]['exam'] or "") + r"\\" + "\n" + str(zaznamy[i]['grades'] or "") + "\n" + str(zaznamy[i]['notes'] or "")


    #print(text_vybrana_vzdelani)

    #print("*****************")

    vybrane_dilci_texty.update({'text_vybrana_vzdelani' : r"\subsection*{EDUCATION AND QUALIFICATIONS \hrulefill{}}" + text_vybrana_vzdelani})








    #.# :z db nacteme tabulku licences

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM licences ORDER BY licence_type")

    zaznamy = kurzor.fetchall()

    text_vybrana_osvedceni = ""

    
    for i in zaznamy:

        text_vybrana_osvedceni = text_vybrana_osvedceni + "\n" + i['licence_type'] + ", "


    #print(text_vybrana_osvedceni)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrana_osvedceni' : r"\subsection*{LICENCES \hrulefill{}}" + text_vybrana_osvedceni} )








    #.# :z db nacteme tabulku languages

    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM languages ORDER BY language_spoken")

    zaznamy = kurzor.fetchall()

    text_vybrane_jazyky = ""

    
    for i in zaznamy:

        text_vybrane_jazyky = text_vybrane_jazyky + "\n" + i['language_spoken'] + " " + i['proficiency_level'] + ", "


    #print(text_vybrane_jazyky)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_jazyky' : r"\subsection*{LANGUAGES \hrulefill{}}" + text_vybrane_jazyky} )









    #.# :z db nacteme tabulku other_activities


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM other_activities ORDER BY start DESC")

    zaznamy = kurzor.fetchall()


    #.# :porovname podobnost jednotlivych zaznamu s popisem zamestnani;


    stop_words = set(stopwords.words('english')) 


    # Interface lemma tokenizer from nltk with sklearn

    class DelicSlovnichZakladu:

        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']


        def __init__(self):

            self.vyhledavac_slovnich_zakladu = WordNetLemmatizer()


        def __call__(self, doc):

            return [self.vyhledavac_slovnich_zakladu.lemmatize(i) for i in word_tokenize(doc) if i not in self.ignore_tokens]


    # Lemmatize the stop words

    delic_na_slova=DelicSlovnichZakladu()

    smysluplna_slova = delic_na_slova(' '.join(stop_words))

    text_k_porovnani = job_description_summary

    jednotlive_texty = []


    for i in zaznamy:

        #print(i['id'], i['summary'])

        jednotlive_texty.append(f"{i['organisation']}\
{i['location']}\
{i['country']}\
{i['role']}\
{i['work_done']}")


    #print('\n\njednotlive_texty:\n')

    #pprint.pprint(jednotlive_texty)

    # Create TF-idf model

    menic_na_vektory = TfidfVectorizer(stop_words=smysluplna_slova, tokenizer=delic_na_slova)

    vektory_dokumentu = menic_na_vektory.fit_transform([text_k_porovnani] + jednotlive_texty)

    # Calculate similarity

    kosinove_podobnosti = linear_kernel(vektory_dokumentu[0:1], vektory_dokumentu).flatten()

    #print('\n\nkosinove_podobnosti:\n')

    #pprint.pprint(kosinove_podobnosti)

    seznam_podobnosti = list(kosinove_podobnosti[1:])

    #print('\n\nseznam_podobnosti:\n')

    #pprint.pprint(seznam_podobnosti)

    #print('zaznamy[index_nejvyssi_hodnoty_seznamu]["summary"]:', zaznamy[index_nejvyssi_hodnoty_seznamu]['summary'])
    
    #text_vybrany_uvod = "\n" + zaznamy[index_nejvyssi_hodnoty_seznamu]['summary']

    #print(text_vybrany_uvod)

    #print("*****************")

    #vybrane_dilci_texty.update({'text_vybrany_uvod' : text_vybrany_uvod})
    
    # initialize N 

    N = 5
    
    # Indices of N largest elements in list

    # using sorted() + lambda + list slicing

    indexy_nejvyssich_hodnot_seznamu = sorted(range(len(seznam_podobnosti)), key = lambda sub: seznam_podobnosti[sub])[-N:]
    
    # printing result

    #print("Indices list of max N elements: " + str(sorted(indexy_nejvyssich_hodnot_seznamu)))

    text_vybrane_jine_aktivity = ""


    for i in sorted(indexy_nejvyssich_hodnot_seznamu):

        text_vybrane_jine_aktivity = text_vybrane_jine_aktivity + "\n" + r"\subsubsection*{" + zaznamy[i]['role'] + "}" + "\n" + zaznamy[i]['organisation'].title() + ", " + zaznamy[i]['location'].title() + ", " + zaznamy[i]['country'].upper() + r"\\" + zaznamy[i]['work_done']

                                                                                            
    #print(text_vybrane_jine_aktivity)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_jine_aktivity' : r"\subsection*{MEMBERSHIPS AND VOLUNTEERING \hrulefill{}}" + text_vybrane_jine_aktivity} )

        
        
        
        
        
        


    #.# :z db nacteme tabulku hobbies


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM hobbies ORDER BY personal_interest")

    zaznamy = kurzor.fetchall()

    text_vybrane_zaliby = ""

                
    for i in zaznamy:

        text_vybrane_zaliby = text_vybrane_zaliby + "\n" + i['personal_interest'] + ", "

    #print(text_vybrane_zaliby)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_zaliby' : r"\subsection*{PERSONAL INTERESTS \hrulefill{}}" + text_vybrane_zaliby} )









    #.# :z db nacteme tabulku notes


    kurzor = pripojeni.cursor()

    kurzor.execute("SELECT * FROM notes ORDER BY closing_note")

    zaznamy = kurzor.fetchall()

    text_vybrane_poznamky = ""

    
    for i in zaznamy:

        text_vybrane_poznamky = text_vybrane_poznamky + "\n" + i['closing_note'] + " "


    #print(text_vybrane_poznamky)

    #print("*****************")

    vybrane_dilci_texty.update( {'text_vybrane_poznamky' : r"\subsection*{NOTES \hrulefill{}}" + text_vybrane_poznamky} )








    vytvor_soubor(osoba_do_nazvu_souboru, url_do_nazvu_souboru)


    #.# :zavreme pripojeni k db;


    pripojeni.close()

    executionTime_cv_automat = (time.time() - startTime_cv_automat)

    print('\nExecution time in seconds: ' + str(executionTime_cv_automat))

    
    #.# }
    #.# detach
    #.# (.)
    #.# detach




if __name__ == "__main__":
    
    url_do_nazvu_souboru = 'url_do_nazvu_souboru'

    osoba_do_nazvu_souboru = 'doe_john'

    sestav_zivotopis(job_description_summary, osoba_do_nazvu_souboru, url_do_nazvu_souboru)
