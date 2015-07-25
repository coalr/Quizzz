__author__ = 'franzgraml'

import nltk, re, pprint
import nltk.data
import urllib.request
import pickle
import random
from bs4 import BeautifulSoup


# Klassendefinition
class Frageundantwort(object):
    def __init__(self, textsource, begriff):
        self.textsource = textsource
        self.begriff = begriff
        ##print('textsource = ',textsource)
        ##print('begriff = ',begriff)

        # Speichere HTML-Dokument vom Internet auf lokale Binärdatei 
        # bei Tests nur 1 mal durchführen,
        # dann kann mit lokaler Datei weiterexperimentiert werden

        # Lesen aus Textquelle
        url = textsource+begriff
        ##html = urllib.request.urlopen(url).read() # Alles einlesen
        html = urllib.request.urlopen(url).read(20000) # Nur einen Teil einlesen
        f = open('daten.dmp','wb')
        pickle.dump(html,f)
        f.close()

        # Einlesen der Binärdatei
        f = open('daten.dmp','rb')
        htmlsaved = pickle.load(f)
        f.close()

        # Umwandlung in 'class str'
        decoded = htmlsaved.decode("utf-8")
        ##decoded = """<p>Satz 1</p><p>Satz 2</p><p>Satz 3</p>""" # Nur zum Test

        ##print(decoded[:500]) # zum Test
        ##print(decoded) # zum Test
        ##print('============')

        l = len(decoded)
        ##print('============')
        ##print('len(decoded) = ',l) # nur zum Test
        ##print('============')


        # Absatzanfänge suchen
        ##print('decoded = ',decoded)
        texta = decoded
        ##print('texta initial = ',texta)
        mla = [] # ml = Matchliste Satzanfang
        gefa = 0 # Initialisieren Hilfszähler
        x = '<p>' # Gesuchter Ausdruck
        lx = len(x)
        ##print('len(x) = ',len(x))
        for i in range(l): # Alle Positionen von x in eine Liste schreiben
            gef = texta.find(x)
            gefn = gefa+gef
            if gef != -1:
                mla.append(gefn)
                texta = texta[gef+lx:]
                ##print('texta ',i,':',texta)
                gefa = gefn
        ##print('Absatzanfangsliste = ',mla) # nur zum Test

        # Absatzenden suchen
        textb = decoded
        ##print('textb initial = ',textb)
        mle = [] # ml = Matchliste Satzende
        gefa = 0 # Initialisieren Hilfszähler
        y = '</p>' # Gesuchter Ausdruck
        ly = len(y)
        for j in range(l): # Alle Positionen von y in eine Liste schreiben
            gef = textb.find(y)
            gefn = gefa+gef
            if gef != -1:
                mle.append(gefn)
                textb = textb[gef+ly:]
                ##print('textb ',j,':',textb)
                gefa = gefn
        ##print('Absatzendeliste = ',mle) # nur zum Test

        # Absätze ohne Markups in Liste schreiben
        absatzlist = []
        ##for i in range(len(mla)): # Achtung: falls Absatz abgeschnitten wurde: indexüberlauf!!!
        for i in range(len(mle)): # mle kann kürzer sein als mla, wenn Absatz abgeschnitten wurde
            absatzanfang = mla[i]
            absatzende = mle[i] 
            absatz = decoded[absatzanfang+lx:absatzende]
            ##print('============')
            ##print('Absatz',i,':', absatz)
            ##print('============')
            # Absätze von Markups reinigen
            cabsatz = BeautifulSoup(absatz, "html.parser").get_text() # Entfernen der Markups
            ##print('============')
            ##print('cabsatz = ',cabsatz)
            ##print('============')
            absatzlist.append(cabsatz)
        ##print('============')
        ##print(absatzlist)


        # Sätze aus den einzelnen Absätzen bilden
        sentencelist = []
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle') # Sentencer laden

        for k in range(len(absatzlist)):
            satzlist = sent_detector.tokenize(absatzlist[k].strip())
            #Achtung: satz ergibt eine Liste von Sätzen!!!
            ##print('satzlist',k,':',satzlist)
            sentencelist.append(satzlist)
        ##print('sentencelist = ',sentencelist) # Achtung: sentencelist ist eine liste von Listen von Sätzen!!!

        # Bestimmten Ausdruck im Satz suchen
        t = ' is a '

        qcounter = 0
        index = -1 # Index zurücksetzen
        # Einzelne Sätze auslesen
        for i in range(len(sentencelist)):
            if qcounter > 0: break
            for j in range(len(sentencelist[i])):
                satz = sentencelist[i][j]
                ##print('============')
                ##print('sentencelist[',i,',[',j,'] = ', satz)
                index = satz.find(t) # Ausdruck t im Satz finden
                ##print('index =',index)
                if index == -1: break   # Wenn Ausdruck nicht enthalten, Abbruch
                                        # und neue Internetseite laden
                    
                if index != -1: # Nur wenn wirklich der Ausdruck im Satz enthalten ist
                    question = satz[:index+len(t)-1] # Frage generieren und ausgeben
                    questionlist.append(question)
                    ##print(question + ':')
                    answer = satz[index+len(t):] # richtige Antwort generieren und ausgeben
                    answer = answer.rstrip('.')
                    answerlist.append(answer)
                    qcounter = qcounter+1 # Nur 1 Frage generieren
                    if qcounter > 0: break
      
# Programmablaufteil
questionlist = []
answerlist = []
reihenfolge = []

# Textkorpus wählen
korpus = 'https://en.wikipedia.org/wiki/' # Wikipedia englisch

# Begriffe wählen; falls random aus Wiki en sein soll: 'Special:Random'
##f1 = Frageundantwort(korpus, 'Nellipaka') # für Test
##f2 = Frageundantwort(korpus, 'Maxomys') # für Test
##f3 = Frageundantwort(korpus, 'Luostarinen') # für Test
##f3 = Frageundantwort(korpus, 'Siemens') # für Test
                                               
##f1 = Frageundantwort(korpus, 'Kerry Mayo') # fester Begriff für Test, wenn 'is a ' nicht enthalten
##f2 = Frageundantwort(korpus, 'Maxomys') # fester Begriff für Test
##f3 = Frageundantwort(korpus, 'Luostarinen') # fester >Begriff für Test

##f1 = Frageundantwort(korpus, 'Special:Random') # Zufallsartikel


# Solange Zufalls-Internetseiten laden, bis Antwortliste 3 Elemente hat
while len(answerlist) < 1:
    f1 = Frageundantwort(korpus, 'Special:Random')
while len(answerlist) < 2:
    f2 = Frageundantwort(korpus, 'Special:Random')
while len(answerlist) < 3:
    f3 = Frageundantwort(korpus, 'Special:Random')


# Ausgabe von Frage und Antworten
print(questionlist[0] + ':')

# Merken, welche Antwort die richtige ist
korranswer = answerlist[0]
##print('korranswer = ',korranswer)

### Antworten ohne Würfeln ausgeben (zum Test); die erste ist immer die richtige
##print ('a)', answerlist[0])
##print ('b)', answerlist[1])
##print ('c)', answerlist[2])

# Den Antworten true-false-Attribute hinzufügen
tflist = [] #true false Hilfs-Liste
t = 'true'
f = 'false'
tflist.append([answerlist[0],t])
tflist.append([answerlist[1],f])
tflist.append([answerlist[2],f]) 
##print(tflist)

# Antworten durcheinanderwürfeln und ausgeben
s = [0,1,2]
random.shuffle(s) # << shuffle before print or assignment. funktioniert das Würfeln wirklich???
##print(s)

### Antworten mit true/false-Marker ausgeben, zum Test
##print ('a)', tflist[s[0]]) 
##print ('b)', tflist[s[1]])
##print ('c)', tflist[s[2]])

print ('a)', tflist[s[0]][0])
print ('b)', tflist[s[1]][0])
print ('c)', tflist[s[2]][0])

#Benutzereingabe
x = ' ' # x zurücksetzen
print('==================')
x = input('Welche Antwort ist richtig? Bitte geben Sie a, b oder c ein.   ')
print('==================')
print('Ihr Tipp ist: ',x)
##print('type(x) = ',type(x))


# Buchstaben zu Index machen. 
if x == 'a': ndex=0
elif x == 'b': ndex=1
elif x == 'c': ndex=2
else:
    ndex = -1 
##print('ndex = ',ndex)

# Richtige Antwort gewählt?
if ndex == -1:
    print('Error: Sie haben weder a noch b noch c gedrückt!')
elif tflist[s[ndex]][1] == t:
    print('Das ist richtig! Gratuliere!')
else:
    print('Das ist leider falsch! Richtig wäre gewesen:')
    print(questionlist[0]+' '+korranswer)



##zu klären:
## 'Citroën C4': bringt UnicodeEncodeError.
## Wahrscheinlich kennt er das e mit zwei Punkten drüber nicht
## Welcher decodierungscode wäre da zu nehmen?

 
## still to do:
## Abfangen, falls gar kein Absatz gefunden wurde







         
