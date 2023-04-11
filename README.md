# Trophées ouvrir la Science

Le projet Ouvrir la Science est un prix à l'initiative  du Ministère de l'Enseignement Supérieur et de la Recherche. Il consiste à récompenser les chercheur·euses français·es qui publient librement leurs outils numérique.  Pour sa première édition,  les trophées remis aux lauréats on été conçus par quatre étudiant·es de l'école des Arts Décoratifs de Paris :  Alix Nadeau, Lorris Sahli, Rose Vidal et Hugo Bijaoui.


[![Watch the video](https://i.imgur.com/vKb2F1B.png)](https://user-images.githubusercontent.com/106762643/228660883-8d30bfee-2681-4922-8bea-3df94b5a8ea7.mp4)

Cette documentation concerne l'élaboration et la fabrication des trophées de ce prix. 

Ce document `Readme.md` concerne la dimension numérique du trophée et le détail des programme nécessaire à sa conception. 

Le fichier `Process_A_a_Z.pdf` présent sur le répertoire se concentre sur la fabrcation plastique des trophées. Nous vous invitons à le consulter pour tout renseignements sur cet aspect de la récompense.


## Le programme

L'objectif de ce programme est de générer une sphère composée $n$ éléments à partir de $n$ *string*s (chaînes de caractères), ainsi que des fichiers aidant à sa fabrication. 
![doc_schematic](https://user-images.githubusercontent.com/91726252/229767439-15274b76-7629-405d-8ef8-0d283c0d15f1.png)



#### Cahier des charges

Pour que le programme génère correctement les trophées, il faut valider les conditions suivantes : 

* Pour une même entrée, les formes de sortie doivent être les mêmes.

* Les formes générées doivent respecter l'esthétique arborescente définie lors de la phase de recherche du projet. 

* Une forme composant la sphère ne peut pas chevaucher ses formes adjacentes (par conséquent, une forme de la sphère n'est pas indépendante des autres)

* La sortie doit permettre la prévisualisation de la sphère en 3D

* La sortie doit contenir les formes 2D, qui une fois 'cintrée' donne les formes en 3D qui composent la sphère; dans un format SVG permettant leur découpe. 

# Guide d'utilisation

### Exemple : L'édition 2022

Voici un exemple d'utilisation du programme, utilisant les description des lauréats de l'édition 2022 du prix. 

#### Entrée

L'entrée est une liste de *string*, entrée par l'utilisateur dans l'invité de commande lors de l'éxécution du programme, ou alors définie dans la variable `descriptifs_projets` du fichier `Trophee_generator.py`. Par exemple, la liste des lauréats 2022 catégorie 'Données de la recherche'.

```
Evolution des différents zonages de la troisième République
Corpus de débats parlementaires français, allemands et britanniques 
EMM, Ethnic and Migrant Minority Survey Registry
NORINE, BD de peptides non-ribosomiques et outils pour leur analyse et visualisation
MOBILISCOPE, cartes et graphiques interactifs de visualisation des variations de la population
Prospection d’Amathonte, site archéologique de l’île de Chypre fouillé par une mission française
MouseTube, enregistrements de vocalisations de souris
YAGO, base de connaissances
```
#### Sortie

Vous trouverez les sorties attendues dans le dossier `Exemple_Sortie`, à savoir : 
* `Blender.png` image de préviusalisation en 3D de l'ensemble des trophées généré par Blender
* `Trophee_2D_view.png` image de prévisualisation 2D des trophée
* `Trophee_SVG.svg` fichier vectoriel des trophée utiles à leur production.

### Procédure d'éxécution

#### Pré-requis logiciel

Il est nécessaire d'avoir installé au préalable :

* Blender (version 3.2.0, non testé sur d'autres versions )

* Python 3.10.4 ou ultérieur 
  
  et les bibliothèques suivantes : 
  
  * Numpy
  
  * pygame
  
  * drawSVG

#### Marche à suivre

* Ouvrir Blender

* Se rendre dans son onglet *script*ing, ouvrir et éxécuter le fichier `Trophee_generator.py` . 
  
  Sont générés les fichiers `Tophee.txt` et `Trophee_3D_preview.png`.

* S'assurer que `2D_view_generator.py` et `Trophee.txt` sont dans le même répertoire et éxécuter `python 2D_view_generator.py`.
  
  Sont générés les fichiers `Trophee_2D_view.png` et `Trophee_SVG.svg`
  
Ou alors, entrer les commandes suivantes : 
  ```
  blender --background --python Trophee_generator.py
  python 2D_view_generator.py
  mv 2D_trophee_view.png Trophee_2D_view.png
  mv SVG_trophee.svg Trophee_SVG.svg
  ```

# Limites et pistes d'améliorations

Cette première version du programme, bien qu'utilisée pour l'édition 2022 prix Ouvrir la Science, reste à l'état de protoptype. Elle contient donc de nombreuses limites. Nous vous invitons à en prendre connaissance avant toute utilisation.

### Algorithme

* `Trophee_generator.py`contient une fonction récursive dont la condition de sortie est dépendante de génération de nombre aléatoire. Par conséquent, il est possible que selon l'entrée, le programme s'arrête si la profondeur maximale admise par Python est atteinte. Un workaround consiste à changer légèrement l'entrée (en rajoutant des espaces à la fin par exemple) jusqu'à ce que le programme s'éxécute entièrement. 
* Les tests de collision entre les branches sont effectué avant leur projection dans l'espace. L'approximation est efficace et simplifie beaucoup le calcule, mais il arrive que dans certains cas limites, les formes se chevauchent une fois projetés. Il faut alors, ou les retoucher à la main, ou changer les paramètre de l'algorithme pour augmenter les marges (plus elles sont petites, plus les résultats peuvent être différents, mais plus les chances que des branches se chevauchent sont grandes; il faut donc trouver un compromis).   
   
En conclusion, Il serait nécessaire d'imaginer un algorithme de génération des formes plus flexible et plus fiable permettant des résultats plus variés (faire les tests de collision sur les formes projetés [nécessite un maillage de la sphère ? Renoncer à une solution analytique ? Au prix de quelle performance ?]). 

### Implémentation

* Une structure de classe aiderait beaucoup à clarifier le code, qui manque aussi de fiabilité.
* L'écriture du fichier Trophee.txt s'arrêtes parfois sans raison, sortant un ficher incomplet (conditions de réplicabilité du bug inconnues).

### Sortie

Les traverses sont absentes sur les fichiers de découpe générés. Elle doivent être rajoutée à la main, selon les directive donnée dans le PDf `Process_A_a_Z.pdf`.
On pourrait imaginer leur automatisation, ce qui compliquerait beaucoup le pogramme de construction du fichier .SVG, alors même que l'ajout manuel des traverses est assez rapide (mais doit être répété sur chaque trophée). 

### Interface

* Une interface graphique et une prévisualisation du résultat en 3D en temps réel permettrait une manipulation facile des différents paramètres.

* Améliorer la construction du modèle 3D de prévisualisation (meilleur utilisation de l'API Blender [notamment les chemins], materials, présence des socles, ect...)

### Documentation

Une documentation plus précise des paramètres du programme, qui conditionnent à la fois l'esthétique du résultat et le fonctionnement l'implémentation serait bienvenue pour faciliter son appropriation.
