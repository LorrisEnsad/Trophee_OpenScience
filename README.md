# Ouvrir la Science

Le projet Ouvrir la Science est un prix à l'initiative  du Ministère de l'Enseignement Supérieur et de la Recherche. Il consiste à récompenser les chercheur·euses français·es qui publient librement leurs outils numérique.  Pour sa première édition,  les trophées remis aux lauréats on été conçus par quatre étudiant·es de l'école des Arts Décoratifs de Paris :  Alix Nadeau, Lorris Sahli, Rose Vidal et Hugo Bijaoui.

https://user-images.githubusercontent.com/106762643/228660883-8d30bfee-2681-4922-8bea-3df94b5a8ea7.mp4


Cette documentation concerne l'élaboration et la fabrication des trophées de ce prix. 

Ce document `Readme.md` concerne la dimension numérique du trophée et le détail des programme nécessaire à sa conception. 

Le fichier `Process_A_a_Z.pdf` présent sur le répertoire se concentre sur la fabrcation plastique des trophées. Nous vous invitons à le consulter pour tout renseignements sur cet aspect de la récompense.

## Le programme

L'objectif de ce programme est de générer une sphère composée $n$ éléments à partir de $n$ *string*s (chaînes de caractères), ainsi que des fichiers aidant à sa fabrication. 

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

# Structure du programme

Programmé en python, le programme utilise Blender et son API Python, ainsi que les bibliothèques numpy, pygame et drawSVG. Il se décompose en deux sous-programme.
Le premier `Trophee_generator.py` génère les trophées selon les contraintes du cahier des charges, et construit une scène Blender permettant leur prévisualisation en 3D.
Le Second `2D_view_generator.py` reprojette les formes 3D sur un plan 2D, puis génére le fichier SVG nécessaire à leur découpe. 

### Représentation d'un trophée dans l'implémentation

Un trophée est un $m$-uplet de branches ordonnées. Une branche est un quintuplet $(n,o,a,b,c) \in$ $\N \times (\bigcup_{i\in \N} \{ (-1)^{i}ie_{branche}\} \times \{0\} \times \{0\}) \times \R³ \times \R³ \times \R³$  avec $e_{branche} \in \R^{+*}$ un paramètre de l'algorithme représentant l'espace entre deux branches. 

- $n$ est le numéro de la branche 

- $o$ est l'origine de la branche tel que $o=((-1)^n ne_{branche},0,0)$

- $a$ est la position dans l'espace du premier coude de la branche

- $b$ est la position dans l'espace du second coude de la branche

- $c$ est la position de la fin de la branche

Autrement dit, chaque trophée est composé de plusieurs branches. Une branche est toujours composée de trois segments.

### Algorithme de génération

Les longeur de chaque segments de chaque branche sont généré à partir d'un aléatoire dont la *seed* est déterminée par 

Le trophée est d'abord généré sur un plan. Par définition, $n$ et $o$ sont prédéterminés pour chaque branche. 

### Préparation à la prévisualisation 3D

## Format d'exportation des trophées

## Préparation du fichier SVG de découpe

# Limites et pistes d'améliorations

Cette première version du programme, bien qu'utilisée pour l'édition 2022 prix Ouvrir la Science, reste à l'état de protoptype. Elle contient donc de nombreuses limites. Nous vous invitons à en prendre connaissance avant toute utilisation.

### Algorithme

La fonction récusrsive avec RNG. Comment faire autrement ? Imaginer un mapping de la sphère sur que les trophee viendrait remplir ?

Imaginer un algorithme de génération des formes plus flexibles permettant des résultats plus variés 

### Implémentation

une structure de classe aiderait beaucoup à clarifier le code.

### Sortie

Abscence des traverses sur le SVG

### Interface

Interface graphique et prévisualisation du résultat en 3D, en temps réel

Améliorer la construction du modèle 3D de prévisualisation (meilleur utilisation de l'API Blender, materials, présence des socles, ect...)

### Documentation

Documentation plus précise des paramètres du programme, qui conditionnent à la fois l'esthétique du résultat et l'efficacité de l'implémentation.

De nombreuse algorigrammes et shémas pourrait simplifier la compréhension de l'algorithme.

  


