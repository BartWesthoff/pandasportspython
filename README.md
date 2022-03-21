
## Pipeline uitleg

#### stappen
<pre>
1.0 preprocessor
    Maakt alle data 'gelijk' aan elkaar zodat er mee gewerkt kan worden.
2.0 Embedder 
    Zet data (video's) om naar data punten (x,y,z,likelihood)
3.0 training 
    Een model dat gemaakt is, wordt gebruikt om data puntne te herkennen en zo een binaire uitslag te geven (goed/fout)
    
    3.1 ** bepalen 1 model per oefening of een 'super' model dat alle oefeningen bijhoud?
4.0 output
    Lokaal opslaan / deployen van het getrained model bij stap 3.
</pre>
## Project structuur

### Folder structuur
<pre>
--data   
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

##### Data
Hier komen alle video's in voor de training data
//TODO even kijken of we deze niet van de cloud af willen halen?

##### Pipeline
Hier zijn de folders voor alles wat in de pipeline komt.
Pipeline.py start de pipeline

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