# Programme effectue dans le cadre de la fabrication des trophee du prix Open Science 2022 
# par l'ENSAD et ses etudiant.es Rose Vidal, Alix Nadeau, Lorris Sahli et Hugo Bijaoui.
# Sous programme No. 1 : Generation des formes a partir des intitules
# Envirennement d'execution : Python 3

import os
import math
from math import pi
import numpy as np
from numpy import linalg as LA
import pygame
import drawSvg as draw


################## Initialisation #################

all_droite = []
all_gauche = []

coef_scale_fin = 2.834868887

# To do :
#  - changer les couvercles
#  - rajouter le bas de 7,151 cm
#  - rajouter les cercles
#  -rajouter les clef

#valeur pour cercle : 0.55191502449351
coef_bezier =0.55191502449351

demi_largeur = 2

d = draw.Drawing(1500, 1500, origin=[0,0], displayInline=False)

start_2D = np.array([100,-250])
ecart_y = 550
nb_trophee_ligne = 5

r_sphere = 0
c_sphere = 0
len_corde = 0
coef = 8/5



save = False

possible_prefix = ["debut_branche","fin_branche","debut_trophee","fin_trophee","r_sphere","c_sphere","len_corde"]
#                          0            1               2               3           4           5           6

###### Ouverture du fichier ######
file = "Trophee.txt"
#file = "test.txt"
find = False
if os.path.isfile(file):
    f=open(file,'r')
    find = True
else :
    print("Fichier Trophee.txt manquant")

######################## Fonctions de construction du fichier SVG ############

def rotation (teta, v = []) :
    x = v[0]
    y = v[1]
    return [ math.cos(teta)*x-math.sin(teta)*y , math.sin(teta)*x + math.cos(teta)*y ]


def normal_vector(a = [], b = []) :


    c = (b[0]-a[0])/(b[1]-a[1]) #Coefficient directeur de la droite AB
    #print ("c de base : ",c)
    #if c> 1 or c<-1:
        #c = 1/c
        #print("on a inversé c : ",c)


    n = [1/math.sqrt(math.fabs(1-math.pow(c,2))),-c/math.sqrt(math. fabs(1-math.pow(c,2)))] #vecteur normal de AB

    return n

def intersection_droite(a = [], b = []) : #trouve l'intersection de deux droites de format [[vect_directeur_x,vect_directeur_y],[px,py]]

    n1x = a[0][0]
    n1y = a[0][1]

    p1x = a[1][0]
    p1y = a[1][1]

    n2x = b[0][0]
    n2y = b[0][1]

    p2x = b[1][0]
    p2y = b[1][1]

    c1 = n1x*p1y - n1y*p1x

    c2 = n2x*p2y - n2y*p2x

    x = -(n2x/n1x + c2) / (n2y - n2x*n1y/n1x)
    y = (n1y*x + c1)/n1x

    return [x,y]



def draw_lines (dot_seq) : #Prend une branche en arguement

    global all_gauche
    global all_droite
    global d

    normals = []
    n = [1,0]
    last = None

    dot_seq_droite = []
    dot_seq_gauche = []

    for i in dot_seq : #Calcul des vecteurs normaux et initialisation des SVG path



        if last != None :

            n = normal_vector (last,i)
            norme = math.sqrt(math.pow(n[0],2)+math.pow(n[1],2))
            print(norme)
            n = [n[0]/norme,n[1]/norme]

            dot_seq_droite.append([last[0]+n[0]*demi_largeur,last[1]+n[1]*demi_largeur])
            dot_seq_gauche.append([last[0]-n[0]*demi_largeur,last[1]-n[1]*demi_largeur])

            dot_seq_droite.append([i[0]+n[0]*demi_largeur,i[1]+n[1]*demi_largeur])
            dot_seq_gauche.append([i[0]-n[0]*demi_largeur,i[1]-n[1]*demi_largeur])

            normals.append(n)

        else :
            p_droite = draw.Path(stroke_width=0.3, stroke='black',
                          fill='none', fill_opacity=0.2)

            p_gauche = draw.Path(stroke_width=0.3, stroke='black',
                          fill='none', fill_opacity=0.2)

            temp_droite = [i[0]+n[0]*demi_largeur,i[1]+n[1]*demi_largeur]
            temp_gauche = [i[0]-n[0]*demi_largeur,i[1]-n[1]*demi_largeur]


            p_droite.M(temp_droite[0],temp_droite[1])
            p_gauche.M(temp_gauche[0],temp_gauche[1])


        last = i

    print(normals)



    bezier1 = rotation(pi/2,normals[0])
    bezier2 = rotation(-pi/2,normals[1])

    bezier1[0] = bezier1[0]*coef_bezier*demi_largeur
    bezier1[1] = bezier1[1]*coef_bezier*demi_largeur

    bezier2[0] = bezier2[0]*coef_bezier*demi_largeur
    bezier2[1] = bezier2[1]*coef_bezier*demi_largeur



    intersec = []
    intersec = intersection_droite([bezier2 , dot_seq_gauche[2]] , [ bezier1 , dot_seq_gauche[1] ] )

    c_1 = [intersec[0]-bezier1[0]  , intersec[1]-bezier1[1] ]
    c_2 = [intersec[0]-bezier2[0]  , intersec[1]-bezier2[1] ]

    p_gauche.L( c_1[0] , c_1[1] )

    p_gauche.C( intersec[0] , intersec[1],
                intersec[0] , intersec[1],
                c_2[0] , c_2[1] )


    intersec = []
    intersec = intersection_droite([bezier2 , dot_seq_gauche[2]] , [ bezier1 , dot_seq_gauche[4] ] )

    c_1 = [intersec[0]+bezier2[0]  , intersec[1]+bezier2[1] ]
    c_2 = [intersec[0]+bezier1[0]  , intersec[1]+bezier1[1] ]

    p_gauche.L( c_1[0] , c_1[1] )

    p_gauche.C( intersec[0] , intersec[1],
                intersec[0] , intersec[1],
                c_2[0] , c_2[1] )

    p_gauche.L( dot_seq_gauche[5][0] , dot_seq_gauche[5][1]  )


    #Partie droite

    intersec = []
    intersec = intersection_droite([bezier2 , dot_seq_droite[2]] , [ bezier1 , dot_seq_droite[1] ] )
    c_1 = [intersec[0]-bezier1[0]  , intersec[1]-bezier1[1] ]
    c_2 = [intersec[0]-bezier2[0]  , intersec[1]-bezier2[1] ]

    p_droite.L( c_1[0] , c_1[1] )

    p_droite.C( intersec[0] , intersec[1],
                intersec[0] , intersec[1],
                c_2[0] , c_2[1] )

    intersec = []
    intersec = intersection_droite([bezier2 , dot_seq_droite[2]] , [ bezier1 , dot_seq_droite[4] ] )
    c_1 = [intersec[0]+bezier2[0]  , intersec[1]+bezier2[1] ]
    c_2 = [intersec[0]+bezier1[0]  , intersec[1]+bezier1[1] ]

    p_droite.L( c_1[0] , c_1[1] )

    p_droite.C( intersec[0] , intersec[1],
                intersec[0] , intersec[1],
                c_2[0] , c_2[1] )



    p_droite.L( dot_seq_droite[5][0] ,dot_seq_droite[5][1] )



    #On fait le couvercle

    couvercle = draw.Path(stroke_width=0.3, stroke='black',
                  fill='none', fill_opacity=0.2)

    couvercle.M(dot_seq_droite[5][0], dot_seq_droite[5][1])
    couvercle.C( dot_seq_droite[5][0] , dot_seq_droite[5][1] + coef_bezier * demi_largeur,
                dot_seq_droite[5][0] , dot_seq_droite[5][1] + coef_bezier * demi_largeur,
                dot_seq_droite[5][0] - coef_bezier * demi_largeur , dot_seq_droite[5][1] + coef_bezier * demi_largeur )

    couvercle.L(dot_seq_gauche[5][0] + coef_bezier * demi_largeur  , dot_seq_gauche[5][1] + coef_bezier * demi_largeur)

    couvercle.C( dot_seq_gauche[5][0] , dot_seq_gauche[5][1] + coef_bezier * demi_largeur,
                dot_seq_gauche[5][0] , dot_seq_gauche[5][1] + coef_bezier * demi_largeur,
                dot_seq_gauche[5][0] , dot_seq_gauche[5][1])

    d.append(p_droite)
    d.append(p_gauche)
    d.append(couvercle)

    all_gauche.append(dot_seq_gauche)
    all_droite.append(dot_seq_droite)




def make_SVG (at = []) :
    global d
    global all_droite
    global all_gauche


    for i in at : #I est un trophée
        for j in i : #j est une branche du trophée
            draw_lines(j)

        #On fait les cercles en base

        for k in range(len(i)-1) :

            add_l = 71.5

            if k % 2 == 0 :
                cercle = draw.Path(stroke_width=0.3, stroke='black',
                              fill='none', fill_opacity=0.2)

                cercle.M(all_gauche[k][0][0],all_gauche[k][0][1])

                cercle.L(all_gauche[k][0][0],all_gauche[k][0][1] - add_l)

                r = math.fabs((all_gauche[k][0][0] - all_droite[k+1][0][0])/2)

                a = [all_gauche[k][0][0],all_gauche[k][0][1] - add_l]
                b = [all_gauche[k][0][0] - r ,all_gauche[k][0][1] - r - add_l]

                cercle.C( a[0]  , a[1] - coef_bezier*r ,
                        b[0] + coef_bezier * r , b[1] ,
                        b[0] , b[1] )

                a = b

                b = [all_droite[k+1][0][0] ,all_droite[k+1][0][1] - add_l]

                cercle.C(a[0] - coef_bezier * r , a[1] ,
                        b[0]  , b[1] - coef_bezier * r ,
                        b[0], b[1] )

                cercle.L(all_droite[k+1][0][0] ,all_droite[k+1][0][1] )

                d.append(cercle)

                cercle = draw.Path(stroke_width=0.3, stroke='black',
                              fill='none', fill_opacity=0.2)

                cercle.M(all_droite[k][0][0],all_droite[k][0][1])

                cercle.L(all_droite[k][0][0],all_droite[k][0][1] - add_l)

                r = math.fabs((all_droite[k][0][0] - all_gauche[k+1][0][0])/2)

                a = [all_droite[k][0][0],all_droite[k][0][1] - add_l]
                b = [all_droite[k][0][0] - r ,all_droite[k][0][1] - r - add_l]

                cercle.C( a[0]  , a[1] - coef_bezier*r ,
                        b[0] + coef_bezier * r , b[1] ,
                        b[0] , b[1] )

                a = b

                b = [all_gauche[k+1][0][0] ,all_gauche[k+1][0][1] - add_l]

                cercle.C(a[0] - coef_bezier * r , a[1] ,
                        b[0]  , b[1] - coef_bezier * r ,
                        b[0], b[1] )
                cercle.L(all_gauche[k+1][0][0] ,all_gauche[k+1][0][1] )
                d.append(cercle)



        all_gauche = []
        all_droite =[]

    d.saveSvg('SVG_trophee.svg')


############################### Fonction de lecture d'un point 3D ############
#Prend une ligne se terminant par \n en entrée, et la séquence pour en tirer
#3 coordonnées d'un point de l'espace dans un format [x,y,z], qui sont des float


def str_to_float_array (s) :
    l = list(s)
    fs = ''
    array = []
    for i in l :
        if i == ',' or i == '\n':
            array.append(float(fs))
            fs = ''

        else :
            fs = fs + i


    return array

########################### Fonction is debut branche ######################
#Prend une ligne de string en entrée se terminant par \n et renvoit si
#elle indiqueun début de branche/trophee/variable, et si oui,renvoit l'argument
#sinon, renvoit False

def is_debut(s) :

    if s == '' :
        return n

    l = list(s)
    len_l = len(l)


    prefix=''
    arg = ''
    space = False
    for i in l :
        if i == ' ' :
            space = True

        if space == False :
            prefix = prefix + i
        elif i != ' ' and i!='\n' and i!='[' and i!=']' :
            arg = arg + i

    for i in possible_prefix :
        if prefix == i :
            return [prefix,arg]

    return False

########################### Fonction de projection stéréoscopique depuis un
#point de la  sphere sur le plan tengent passant par ce point,
#Soit un point de forme [x,z] car y est 0 (etant donné qu'on projette sur le plan à l'origine)

def projection (p = [0,0,0], c = [0,0,0] ) :
    global r_sphere


    norme_p_c = LA.norm(np.array([p[1],p[2]])-np.array([c[1],c[2]]))
    # print("norme p-c : ",norme_p_c)
    # print("norme p-c au carre : ",np.square(norme_p_c))
    # print("2rcarre : ", 2*np.square(r_sphere))
    div = np.square(norme_p_c)/(2*np.square(r_sphere))
    # print("la division : ",div)
    # print("la formul : ", math.acos(1-div))
    len_arc = r_sphere * math.acos(1-div)
    projected = [p[0],c[2]+len_arc]

    return projected

def projection2 (p) :
    return [p[0],p[2]]



########################### Translation d'un trophé à l'origine correspondant
#a son numero [mise en page]

def translation (n,trophee) :

    origine = start_2D+np.array([ (n%nb_trophee_ligne)*len_corde , (n//nb_trophee_ligne)*ecart_y ])
    print("numero du trophee : ",n)
    print("origine :\n",origine)
    print("trophee :\n",np.array(trophee))
    translated = origine + np.array(trophee)

    return np.ndarray.tolist(translated)

########################### Boucle de lecture du fichier #####################

if find == True :


    all_trophee = []

    en_cours = [-1,-1]
    #Represente si oui ou non on est dans un trophee, ou une branche, si oui
    #indique son numero, sinon, indique -1

    lines = f.readlines()
    last_line = ''
    compte = 0
    for ligne in lines :
        compte = compte+1
        id = is_debut(ligne) #[prefix,arg] ou False
        #print(id)
        if id != False :

            if id[0] == possible_prefix[2] : #Si c'est debut trophee
                en_cours[0] = int(id[1])
                all_trophee.append([])
            elif id[0] == possible_prefix[3] : #Si c'est fin trophee
                en_cours[0] = -1
            elif id[0] == possible_prefix[0] : #Si c'est debut branche
                en_cours[1] = int(id[1])
                all_trophee[en_cours[0]].append([])
            elif id[0] == possible_prefix[1] : #Si c'est fin branche
                en_cours[1] = -1
            elif id[0] == possible_prefix[4] :
                r_sphere = float(id[1])
            elif id[0] == possible_prefix[5] :
                c_sphere = str_to_float_array(id[1]+'\n')
            elif id[0] == possible_prefix[6] :
                len_corde = coef * float(id[1])

        else :
            # print(en_cours)
            # print(all_trophee)
            # print(compte)
            all_trophee[en_cours[0]][en_cours[1]].append(str_to_float_array(ligne))



########################## Projection sur le plan #############################

    all_trophee_p = []

    for i in all_trophee :

        all_trophee_p.append([])
        n = len(all_trophee_p) - 1

        for j in i :
            all_trophee_p[n].append([])
            m = len(all_trophee_p[n]) - 1
            c = j[0]
            for k in j :
                all_trophee_p[n][m].append(projection(k,[k[0],c[1],c[2]]))

        all_trophee_p[n] = translation(n,all_trophee_p[n])


######################## Affichage ###########################################


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
grey = (250, 250, 250)


size = [1500,1500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

pygame.init()

while not done:

    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen,"2D_trophee_view.png")
            make_SVG(all_trophee_p)
            save == True
            print("saved")
            done=True

    screen.fill(grey)

    for i in all_trophee_p :
        for j in i :
            pygame.draw.aalines( screen , BLACK , False , j ,2)

    # if save == False :
    #      pygame.image.save(screen,"2D_trophee_view.png")
    #      make_SVG(all_trophee_p)
    #      save == True
    #      print("saved")

    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
