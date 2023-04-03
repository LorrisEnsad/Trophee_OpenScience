# Programme effectue dans le cadre de la fabrication des trophee du prix Open Science 2022 
# par l'ENSAD et ses etudiant.es Rose Vidal, Alix Nadeau, Lorris Sahli et Hugo Bijaoui.
# Sous programme No. 1 : Generation des formes a partir des intitules
# Envirennement d'execution : Blender


import random
import bpy
import bmesh
from math import pi
import math
import numpy

descriptifs_projet = ["Evolution des différents zonages de la troisième République",
"Corpus de débats parlementaires français, allemands et britanniques" ,
"EMM, Ethnic and Migrant Minority Survey Registry" ,
"NORINE, BD de peptides non-ribosomiques et outils pour leur analyse et visualisation" ,
"MOBILISCOPE, cartes et graphiques interactifs de visualisation des variations de la population" ,
"Prospection d’Amathonte, site archéologique de l’île de Chypre fouillé par une mission française" ,
"MouseTube, enregistrements de vocalisations de souris" ,
"YAGO, base de connaissances"]

# descriptifs_projet = ["Coq est un assistant de preuve, c’est à dire un langage formel pour décrire des définitions mathématiques et des outils pour vérifier formellement des algorithmes ou des théorèmes, si nécessaire de manière interactive. Ce logiciel est souvent utilisé pour faire de la preuve de programmes (par exemple dans le cadre du compilateur C certifié comp-cert), mais aussi pour formaliser les mathématiques et pour l’enseignement. Le projet a démarré en 1984 et concerne les sciences du numérique et des mathématiques.",
# "Coriolis est un outil de placement et de routage de circuits intégrés sur silicium. Le projet a débuté en 2000 et concerne les sciences du numérique et des mathématiques.",
# "Scikit-learn est une bibliothèque d’apprentissage statistique, conçue pour être intégrée dans d’autres logiciels ou être utilisée comme outil d’analyse par des scientifiques ou des analystes des données. Ce logiciel intègre l’état de l’art du domaine et le rend accessible au plus grand nombre. Démarré en 2009, ce projet concerne les sciences du numérique et des mathématiques.",
# "Vidjil est une plateforme logicielle d’analyse de séquences d’ADN des globules blancs utilisée par une quarantaine de laboratoires nationaux et internationaux pour diagnostiquer et suivre les leucémies. Le projet a commencé en 2011 et concerne la biologie et la santé.",
# "WebObs est un outil d’observation temps-réel pluridisciplinaire utilisé dans le cadre de l’observation de phénomènes naturels. Au service des observatoires volcanologiques et sismologiques, il est utilisé dans une douzaine de laboratoires dans le monde, et a été adopté par plusieurs pays pour surveiller leurs volcans (Indonésie, Singapour, Pérou). Le projet a débuté en 2001 et concerne le système terrestre et l’environnement.",
# "Faust est un langage de programmation utilisé dans le domaine de la recherche en informatique musicale, en particulier pour la synthèse sonore, le traitement du signal et les lutheries numériques. Il rend accessible à des musiciens non-informaticiens des manipulations qui demanderaient une expertise importante dans des langages de plus bas niveau. Ce projet a débuté en 2002 et concerne les sciences du numérique et des mathématiques.",
# "OpenViBE est un logiciel pour les neurosciences qui permet d’acquérir, filtrer, traiter, classer et visualiser les signaux cérébraux en temps réel. Le projet a commencé en 2006 et concerne la biologie et la santé.",
# "Gammapy est un logiciel d’analyse des données astrophysiques issues de télescopes. Cet outil reconnu comme un standard pour le traitement des données astrophysiques est notamment utilisé par l’observatoire européen CTA (Cherenkov Telescope Array) pour l’analyse de ses données ouvertes et aussi par la NASA pour son téléscope LAT (Large Area Telescope). Débuté en 2014, le projet concerne les domaines de l’astronomie et l’astrophysique.",
# "GAMA est une plate-forme de simulation, qui vise à fournir aux experts de terrain, aux modélisateurs et aux informaticiens un environnement complet de développement, de modélisation et de simulation pour la construction de simulations multi-agents spatialement explicites. Le projet a démarré en 2007 et concerne les sciences du numérique et des mathématiques.",
# "SPPAS est un logiciel de linguistique computationnelle et de linguistique de corpus. Cet outil est capable de produire automatiquement des annotations à partir de paroles enregistrées, de vidéos et de leur transcription orthographique. Commencé en 2011, le projet concerne les sciences humaines et sociales."]





input = True   #Si vrai, le programme demandera les intitules a l'utilisateur via le terminal.
                #Si Faux, le programme prendra ceux definis plus haut dans la liste 'descriptifs_projets'


range_nb_branche = [5,8] #Bornes inferieur et superieur du nombre de branches par trophee 

nombre_trophee = len(descriptifs_projet)
tilt_trophee = -pi/40

r_cercle = 150
r_sphere = 175
c_sphere = [0,r_sphere,r_sphere]

ecart_branche = 7 #ecartement horizontal entre les branches
pas = 10

emax = 80
coef_eb = 3/5 #Coefficient d'écartement vertical entre les branches

angle_possible = pi/4 #Angle lorsqu'une branche bifurque 

hmax_emin = [550,20]

hmin = 10

#Parametre de creation du model 3D (n'a d'importance que pour la previsualisation)
r_cyl = 1      #Rayon de base des cylindres
v_cyl = 5      #Nombre de sommet pour faire le cylindre
shape = "Cylinder"


arbre = []
previous_arbre = []
first_arbre = []

cylinder_number = 0
t_number = 0
print(cylinder_number)


len_corde = 5/4*(2*pi/nombre_trophee*r_sphere)

last_trophee = False



########################"mise en place du fichier de stoquage de coordonnées #####

file = "Trophee.txt"

import os
if os.path.isfile(file):
    f=open(file,'w')
else :
    f = open(file, 'x')

f.write("r_sphere "+str(r_sphere)+"\n")
f.write("c_sphere "+str(c_sphere)+"\n")
f.write("len_corde "+str(len_corde)+"\n")


################################## Fonction Multiplicatino par un scalaire #############

def mult_scal (alpha,a=[0,0,0]) :
    return [a[0]*alpha,a[1]*alpha,a[2]*alpha]



################################## Fonction norme #############

def norme(x,y,z) :
    return math.sqrt(math.pow(x,2) + math.pow(y,2) + math.pow(z,2))


################################## Fonction get_rotation #############

def get_rotation (x,y,z) :
    p = norme(x,y,z)
    ry = math.acos(z/p)
    rz = math.atan2(y,x)
    return (0,ry,rz)

################################## Fonction sous_vect #############


def sous_vect (a=[0,0,0], b =[0,0,0] ) :

    c = []
    for i in range (0,3):
        c.append(b[i]-a[i])
    return c
################################## Fonction sous_vect2 #############


def sous_vect2 (a=[0,0,0], b =[0,0,0] ) :

    c = []
    for i in range (0,3):
        c.append((b[i]-a[i])/2)
    return c

################################## Fonction add_vect #############

def add_vect (a=[0,0,0], b =[0,0,0] ) :

    c = []
    for i in range (0,3):
        c.append(b[i]+a[i])
    return c

################################## Fonction faire cylindre #############

def make_cylinder(r,pos,h,rot) :
    if shape == "Cylinder" :
        bpy.ops.mesh.primitive_cylinder_add(vertices = v_cyl,
                                        radius = r,
                                        depth = h,
                                        end_fill_type = 'NGON',
                                        calc_uvs = True,
                                        enter_editmode = False,
                                        align = 'WORLD',
                                        location = pos,
                                        rotation = rot,
                                        scale = (1, 1, 1))
    else :
        bpy.ops.mesh.primitive_cube_add(size=1.0,
                                     calc_uvs=True,
                                    enter_editmode=False,
                                    align='WORLD',
                                    location=pos,
                                    rotation=rot,
                                    scale=(r, 0.2, h))
    global cylinder_number
    cylinder_number = cylinder_number + 1

################################## Fonction trace cylindre #############
#Fait un cylindre qui relie deux points

def trace_cylinder (a=[0,0,0],b=[0,0,0]) :

    pos = add_vect(a,sous_vect2(a,b))
    sous = sous_vect(a,b)
    rot = get_rotation(sous[0],sous[1],sous[2])
    h = norme(sous[0],sous[1],sous[2])
    make_cylinder(r_cyl,pos,h,rot)


################################## Fonction Project_sphere #############

def project_sphere (a=[0,0,0],c=c_sphere,r=r_sphere) :
    p = [0,0,0]
    t = sous_vect(a,c)
    p = add_vect(c,mult_scal(r/(norme(t[0],t[1],t[2])),t))
    return p
################################## Fonction Project_cylinder #############

def project_cylinder (a=[0,0,0]) :
    p = [0,0,0]
    centre = add_vect(c_sphere, [a[0],0,0])
    p = project_sphere(a,centre,r_sphere)
    return p



################################ Fonction Simplify branche ######################

def simplify_branche(branche) :

    simplified = []

    simplified.append(branche[0])
    simplified.append(branche[0])
    simplified.append(branche[len(branche)-1])

    for i in branche :
        if i[0] == simplified[0][0] and i[2] > simplified[0][2] :
            simplified[0] = i
        elif  i[0] == simplified[2][0] :
            simplified[1] = i
            return simplified

################################# Fonction Collision branche ####################

def collision (n_branche, branche = []) :
    global previous_arbre

    if previous_arbre == [] :
        return False


    simple_arbre = []
    compte = 0
    for i in previous_arbre : #Simplification
        if compte%2 == 1 :
            simple_arbre.append(simplify_branche(i))
        compte = compte+1
    compte = 0
    compte2 = 0
    for i in simple_arbre : #Translation à la bonne origine
        compte2 = 0
        for j in i :
            simple_arbre[compte][compte2] = add_vect(i[compte2],[len_corde,0,0])
            compte2=compte2+1

        compte = compte + 1

    #Test de collision

    for branche_2 in simple_arbre :
        for i in branche :
            if i[0] > branche_2[0][0] or (i[0]>branche[1][0] and i[2] > branche_2[0][2]
                                                            and i[2] < branche_2[2][2] ) :
                return True

    return False


def collision_a_gauche (n_branche, branche = [],first_arbre=[]) :

    if first_arbre == [] : #Au cas ou mais normalement useless
        return False

    simple_arbre = []
    compte = 0
    for i in first_arbre : #Simplification
        if compte%2 == 0 :
            simple_arbre.append(simplify_branche(i))
        compte = compte+1
    compte = 0
    compte2 = 0
    for i in simple_arbre : #Translation à la bonne origine
        compte2 = 0
        for j in i :
            simple_arbre[compte][compte2] = add_vect(i[compte2],[-len_corde,0,0])
            compte2=compte2+1

        compte = compte + 1

    #Test de collision

    for branche_2 in simple_arbre :
        for i in branche :
            if i[0] < branche_2[0][0] or (i[0]<branche[1][0] and i[2] > branche_2[0][2]
                                                            and i[2] < branche_2[2][2] ) :
                return True

    return False



################################## Fonction make_branche #############



def make_branche (n_branche) : #Argument : n°de branche

    branche = []

    global hmax_emin
    global last_trophee
    global nb_recursion
    global recursion_max
    hmax_emin_temp = hmax_emin


    #On fait le tronc

    origine = n_branche%2
    if origine == 0 : #si paire
        branche.append([ n_branche/2*ecart_branche , 0 , 0 ])
    else :  #si impaire
        branche.append([ -(((n_branche//2)+1)*ecart_branche) , 0 , 0 ] )


    if n_branche == 0 :
        taille = random.randint(int(4/5*hmax_emin[0]),hmax_emin[0])
    else :
        taille = random.randint(int(coef_eb*hmax_emin[0]),hmax_emin[0])
    hmax_emin_temp[0] = taille
    for i in range (1,taille//pas) :
        branche.append(add_vect(branche[0], [0,0, i*pas ] ))
    debut_branche = add_vect(branche[0] , [ 0 , 0 , taille ] ) #debut de la bifurcation
    branche.append(debut_branche)

    #On fait la première branche

    taille = random.randint(hmax_emin[1], max(hmax_emin[1] + 10 , emax//(nb_branche_2 - n_branche )))
    angle = angle_possible

    vect = []
    if origine == 0 :
        vect = [ math.cos(angle)*taille , 0 , math.sin(angle)*taille ]
    else :
        vect = [ -(math.cos(angle)*taille) , 0 , math.sin(angle)*taille ]

    fin_branche = add_vect(debut_branche, vect )
    vect_norm = mult_scal (pas/norme(vect[0],vect[1],vect[2]),vect)

    for i in range (1,taille//pas) :
        branche.append(add_vect(debut_branche,mult_scal(i,vect_norm)))
    branche.append(fin_branche)


    #On fait le seconde branche

    taille = random.randint(20,50)
    for i in range (1,taille//pas) :
        branche.append(add_vect(fin_branche,[ 0 , 0 , i*pas ]))
    branche.append(add_vect(fin_branche,[ 0 , 0 , taille ]))

    if last_trophee == False : #Si ce n'est pas le derneir trophee/arbre
        if collision(n_branche,branche) == False :
            hmax_emin = hmax_emin_temp
            return branche

        else :
            make_branche(n_branche)

    else :   #Si c'est le dernier trophee/arbre
        if collision(n_branche,branche) == False and collision_a_gauche(n_branche,branche,first_arbre) == False :
            hmax_emin = hmax_emin_temp
            return branche

        else :
            make_branche(n_branche)



################################## Fonction write arbre ##############

def write_arbre(arbre,n) :
    global f


    f.write("debut_trophee "+str(n)+"\n")
    print("debut_trophee "+str(n))
    compte = 0

    for j in arbre : #J est une branche


        if j != None:
            print("debut_branche "+str(compte))
            f.write("debut_branche "+str(compte)+ "\n")
            temp = simplify_branche2(j)

            for k in temp : #K est un point de la branche

                print(str(k[0])+","+str(k[1])+","+str(k[2]))
                f.write(str(k[0])+","+str(k[1])+","+str(k[2])+"\n")

            f.write("fin_branche "+str(compte)+ "\n")
            print("fin_branche "+str(compte))
            compte=compte+1



    f.write("fin_trophee "+str(n)+"\n")
    print("fin_trophee "+str(n))

def simplify_branche2 (branche) :

    simplified = []
    for i in range(4):
        simplified.append([0,0,0])
    simplified[0] = branche[0]
    simplified[1] = simplified[0]
    simplified[3] = branche[len(branche)-1]
    simplified[2] = simplified[3]
    for i in branche :
        if i[0] == simplified[0][0] and i[2] < simplified[1][2] :
            simplified[1] = i
        if i[0] == simplified[3][0] and i[2] > simplified[2][2] :
            simplified[2] = i

    return simplified



################################## Construction Arbre 3D #############
#Up_to_date

def build_trophee (n) :

    global last_trophee
    global cylinder_number
    cylinder_number = 0

    global hmax_emin
    hmax_emin = [620,20]

    global previous_arbre
    global first_arbre

    if input == True :

        print("Entrer le texte generateur de forme : ")
        texte_1 = list(input())
        texte_1V = 0
    else :
        texte_1 = list(descriptifs_projet[n] )
        texte_1V = 0

    for i in texte_1 :
        texte_1V =texte_1V + ord(i)
    #print(texte_1V)

    random.seed(texte_1V)

    global nb_branche_2

    nb_branche_2 = random.randint(range_nb_branche[0],range_nb_branche[1])
    if nb_branche_2%2 == 1 :
        nb_branche_2 = nb_branche_2 - 1

    global arbre


    arbre = []

    for i in range (nb_branche_2) :
        arbre.append(make_branche(i))

    previous_arbre = arbre

    compte = 0
    #print(arbre)

    for i in arbre :
        if i == None :
            break
        for j in range (len(i)) :
            arbre[compte][j] = project_cylinder(i[j])
            if j != 0 :
                trace_cylinder(arbre[compte][j-1],arbre[compte][j])

        compte = compte + 1

    write_arbre(arbre,n)  #écriture de l'arbre dans le fichier

    for i in range(cylinder_number) :
        if i == 0 :
            number = ""
        elif i//100 > 0 :
            number = "."+str(i)
        elif i //10 > 0 :
            number = ".0"+str(i)
        else :
            number = ".00"+str(i)

        bpy.data.objects[shape+number].select_set(True)

    bpy.ops.object.join()

    bpy.context.scene.cursor.location = arbre[0][0]

    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    global t_number
    t_number = t_number + 1

    for obj in bpy.context.scene.objects:
        if obj.name == shape+number :
            obj.name = "T"+str(t_number)
            obj.data.name = "T"+str(t_number)

    for obj in bpy.context.scene.objects:
        obj.select_set(False)


################################# Disposition en sphere #################

def put_sphere (n) :

    position = []
    rotation = []

    for i in range(n) :
        position.append([ -(math.sin(i*2*pi/n)*r_cercle) , math.cos(i*2*pi/n)*r_cercle , 50 ])
        rotation.append(i*2*pi/n)
        #print(rotation)

    for i in range(n) :
        obj = bpy.data.objects["T"+str(i+1)]

        obj.location = position[i]
        obj.delta_rotation_euler = [pi+tilt_trophee,0,pi+rotation[i]]


###################################### Boucle principale ###############

for i in range (nombre_trophee):
    print("===============================")
    print("\tBOUCLE N°",i)
    print("===============================")
    build_trophee(i)
    if i == 0 :
        first_arbre = arbre


put_sphere(nombre_trophee)

#for i in range(nombre_trophee) :
#    obj = bpy.data.objects["T"+str(i+1)]
#
#    obj.delta_rotation_euler = [pi+tilt_trophee,0,pi+i*2*pi/nombre_trophee]



######################################## Rendu de la previsualisation 3D et sortie PNG ##############################""



import bpy

# we first create the camera 
cam_data = bpy.data.cameras.new('camera')
cam = bpy.data.objects.new('camera', cam_data)
bpy.context.collection.objects.link(cam)# add camera to scene
scene = bpy.context.scene
scene.camera=cam

#scene.camera.rotation_euler(3.1415927/4, 0.0, 0.0)

scene.camera.rotation_euler[0] = 0.977
scene.camera.rotation_euler[2] = -3.1415927

scene.camera.location.x = 0
scene.camera.location.y = 800
scene.camera.location.z = 700

scene.camera.data.clip_end = 2000

light_data = bpy.data.lights.new(name="light_2.80", type='POINT')
light_data.energy = 1000000

# create new object with our light datablock
light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)

# link light object
bpy.context.collection.objects.link(light_object)

# make it active 
bpy.context.view_layer.objects.active = light_object

#change location
light_object.location = (0,300, 300)

light_data = bpy.data.lights.new(name="light_2.80", type='POINT')
light_data.energy = 1000000

# create new object with our light datablock
light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)

# link light object
bpy.context.collection.objects.link(light_object)

# make it active 
bpy.context.view_layer.objects.active = light_object

#change location
light_object.location = (0,0, 400)







scene = bpy.context.scene
scene.render.image_settings.file_format='PNG'
scene.render.filepath='Trophee_3D_preview.png'
bpy.ops.render.render(write_still=1)

print("done") 