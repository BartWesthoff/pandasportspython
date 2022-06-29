
## Panda Sports (fitness posture tracking app)

## Project structuur

### Folder structuur
<pre>
--classes
--data   (mogelijk geschrapt)
--pipeline  
  |-- models  
  |-- steps  
      |--embedder  
      |--output  
      |--preprocessors  
      |--training
--readme-files
--research
</pre>

### Uitleg folders

##### classes
Hier komen alle losse niet-ML gerelateerde classes
Denk aan de lichaam van een persoon, oefening of mogelijke foto"s

##### Data 
Hier komen alle video"s in voor de training data

##### Pipeline
Hier zijn de folders voor alles wat in de pipeline komt.
Pipeline.py start de pipeline

<pre>
--pipeline  
  |-- models  
  |-- steps  
      |--embedder  
      |--output  
      |--preprocessors  
      |--training
</pre>
###### models
Hier komen alle Machine learning models 

###### steps (in chronologische volgorde)
Hier komen alle stappen die in een reeks uitgevoerd moeten worden.

<pre>
  |-- steps  
      |--input
      |--preprocessors  
      |--embedder
      |--training
      |--output
</pre>

<pre>
1.0 input
    haalt de data op waar mee gewerkt wordt.
    Een voorbeeld kan zijn de train data of testdata.

2.0 preprocessor
    Maakt alle data "gelijk" aan elkaar zodat er 
    mee gewerkt kan worden.

3.0 Embedder 
    Zet data (video"s) om naar data punten (x,y,z,likelihood).

4.0 training 
    Een model dat wordt getrained om datapunten te herkennen.

5.0 output
    Lokaal opslaan / deployen van het getrained model van stap 3.
    Eventueel opgesplits worden in grafisch weergeven en opslaan.
</pre>

##### Readme-files
Hier komen alle files die nodig zijn om de README.md file mooi te maken.

##### Research
Hier komen alle bestanden die met research hebben te maken. Maakt niet uit of het netjes is of niet


## Git werkwijze

<pre>
--main   
--development
--feature
--Bug
</pre>

### Branches uitleg

#### Main
Dit is de hoofdbranch. Hier komt het uiteindelijke resultaat.

#### Development
Dit is de hoofdbranch voor development. Alle features en bugs worden hier naartoe gepusht.

#### Feature
Als je een nieuwe feature wilt toevoegen doe je dat met feature/<feature naam>.

#### Bug
Als een bug wilt oplossen dan maak je een branch aan met bug/<feature naam>.

## Gebruiksaanwijzing

### use case 1: Model trainen
Om een model te trainen moet je goed op de volgende onderdelen letten:
    1. Zorg dat 
