import random
from PIL import Image, ImageDraw
import time
import sys
import webbrowser
import os

def affichage_text(texte, end="\n"): 
    """fonction faite par Clavin l'an dernier pour le projet pokémon (il reste encore des souvenirs de lui)"""
    for i in range(len(texte)):
        print(texte[i], end="")
        sys.stdout.flush()
        time.sleep(0.012)
    print(end, end="")

class Laby:
    def __init__(self, nbli, nbcol):
        """
        Utilitée : 
            Initialisation du labyrinthe (présentée sous la forme d'un tableau 3D avec les deux premières dimenssions pour
            le plan et la troisème pour savoir pour chaque case si il existe des murs autour ou non)
        Entrée : 
            Self et le nombre de ligne et de colones souhaitées
        Renvoie : 
            Ne renvoi rien
        """
        self.l, self.c = nbli, nbcol
        self.tab=[[[1]*4 for i in range(self.c)] for j in range(self.l)]
        self.visite=[[False for i in range (self.c)] for j in range (self.l)]

    def appartient(self, i, j):
        """
        Utilitée : 
            Permet de savoir si une case appartient ou non au le labyrinthe
        Entrée : 
            Self et la ligne "i" et la colone "j"
        Renvoie : 
            Renvoi True si la case appartient au labyrinthe et False sinon
        """
        return 0 <= i < self.c and 0 <= j < self.l

    def verifmur (self, case, direction):
        """
        Utilitée : 
            Permet de vérifier s'il y a un mur dans la direction donnée (Nord, Est, Sud et Ouest)
        Entrée : 
            Self et une case avec des coordonnée (car tableau 2D) et une direction (0 pour le Nord, 1 pour l'Est, 2 pour le Sud et 3 pour l'Ouest)
        Renvoie : 
            Renvoi False s'il n'y a pas de mur dans la direction donnée et False sinon
        """
        if self.tab[case][direction] == 0:
            return False
        return True
    
    def inversedirection (self, nb):
        """
        Utilitée : 
            Permet d'inversé la direction
        Entrée : 
            Self et une direction (0 pour le Nord, 1 pour l'Est, 2 pour le Sud et 3 pour l'Ouest)
        Renvoie : 
            Renvoi le numéro correspondant à la direction opposé de celle donnée
        """
        if nb==0:
            return 2
        if nb==1: 
            return 3
        if nb==2: 
            return 0
        if nb==3:
            return 1
    
    def retrait_mur (self, case, direction):
        """
        Utilitée : 
            Permet le retrait d'un mur et le l'actualiser dans la case d'à côté
        Entrée : 
            Self et une case avec des coordonées (car tableau 2D) et une direction (0 pour le Nord, 1 pour l'Est, 2 pour le Sud et 3 pour l'Ouest)
        Renvoie : 
            Ne renvoie rien
        """
        i,j=case
        if 0 <= i <= self.c-1 and 0<= j <= self.l-1:
            if direction == 0 and i>0:
                indice=self.inversedirection(direction)
                self.tab[i-1][j][indice]=0
            elif direction == 1 and j<self.c-1:
                indice=self.inversedirection(direction)
                self.tab[i][j+1][indice]=0
            elif direction == 2 and i<self.l-1:
                indice=self.inversedirection(direction)
                self.tab[i+1][j][indice]=0
            elif direction == 3 and j>0:
                indice=self.inversedirection(direction)
                self.tab[i][j-1][indice]=0
            self.tab[i][j][direction]=0

    def __str__(self):
        """
        Utilitée : 
            Permet l'affichage en mode console
        Entrée : 
            Self
        Renvoie : 
            Renvoi "s", c'est à dire le labyrinthe
        """
        s=""
        for j in range (self.c):
            s += "+"
            if (self.tab[0][j][0])==1:
                 s+="-"
            if (self.tab[0][j][0])==0:
                s+=" "
        s += "+\n"
        for i in range (self.l):
            for j in range (self.c):
                if (self.tab[i][j][3])==1:
                    s+="| "
                if (self.tab[i][j][3])==0:
                    s+="  "
            s+="|\n" if self.tab[i][self.c - 1][1] == 1 else " \n"
            for j in range (self.c):
                if (self.tab[i][j][2])==1:
                    s+="+-"
                if (self.tab[i][j][2])==0:
                    s+="+ "
            s+="+\n"
        return s

def enregistrement_image (laby, images):
    """
    Utilitée : 
        Permet de mettre toute les étapes du labyrinthe en mode image dans une list
    Entrée : 
        Le labyrinthe, un compteur pour mettre un bon numéro aux images et pour pas qu'elles aient le memes nom (pour mettre dans le bon ordre dans le gif)
    Renvoie : 
        renvoi rien
    """
    taille_case = 40
    epaisseur_mur = 4
    c_image = laby.c * taille_case + epaisseur_mur #longueur du laby fait tallie de la case fois le nombre de case dans un ligne
    l_image = laby.l * taille_case + epaisseur_mur #largeur du laby fait tallie de la case fois le nombre de case dans une colone
    couleur_mur=(75, 0, 130) #par ce qu'Achille aime le violet 
    img = Image.new("RGB", (c_image, l_image), "grey") #par ce que Lucas aime le gris
    draw = ImageDraw.Draw(img)
    for i in range (laby.l):
        for j in range(laby.c):
            x1 = j * taille_case #pour départ ordonné
            y1 = i * taille_case #pour départ abscisse
            x2 = x1 + taille_case #pour arrivée ordonné
            y2 = y1 + taille_case #pour arrivée abscisse
            if laby.tab[i][j][0] == 1: #mur du haut
                draw.line([(x1, y1), (x2, y1)], fill=couleur_mur, width=epaisseur_mur)
            if laby.tab[i][j][1] == 1: #mur de droite
                draw.line([(x2, y1), (x2, y2)], fill=couleur_mur, width=epaisseur_mur)
            if laby.tab[i][j][2] == 1: #mur du bas
                draw.line([(x1, y2), (x2, y2)], fill=couleur_mur, width=epaisseur_mur)
            if laby.tab[i][j][3] == 1: #mur de gauche
                draw.line([(x1, y1), (x1, y2)], fill=couleur_mur, width=epaisseur_mur)
            
            
    images.append(img) #mettre l'image dans la liste images

def gif (images, nom):
    """
    Utilitée : 
        Permet de créer un gif
    Entrée : 
        Les images, un nom
    Renvoie : 
        renvoi rien, créer un gif
    """
    images[0].save(nom, save_all=True, append_images=images[1:], duration=100, loop=1)

def ouvrir_gif_navigateur(GIF):
    """
    Utilité : 
        Permet d'ouvrir un fichier GIF dans le navigateur par défaut du système.
    Entrée : 
        Le chemin du fichier GIF.
    Renvoie : 
        Rien. Ouvre le fichier GIF dans le navigateur par défaut.
        #### Fait avec chat gtp car on voulait absolument cette option
    """
    chemin_gif = os.path.abspath(GIF)  # Obtenir le chemin absolu du fichier GIF
    url = f"file://{chemin_gif}"  # Créer l'URL locale pour le fichier GIF
    webbrowser.open(url)  # Ouvre l'URL dans le navigateur par défaut



def generation_rec(laby, i, j, deja_vus, images):
    """
    Utilitée : 
        permet au labyrinte de se génrer seul de manière récursive
    Entrée : 
        laby, (une case avec des coordonées i et j), et un ensemble contennt toute els case déjà vu
    Renvoie : 
        revoi rien
    """
    if (i, j) in deja_vus:
        return
    else :
        deja_vus.append((i, j))
        direction=[]
        if laby.appartient(i-1,j):
            direction.append((-1, 0, 0)) #nord
        if laby.appartient(i,j+1):
            direction.append((0, 1, 1)) #est
        if laby.appartient(i+1, j):
            direction.append((1, 0, 2)) #sud
        if laby.appartient(i, j-1):
            direction.append((0, -1, 3)) #ouest
        random.shuffle(direction)
        for dir in direction:
            ligne, colone, d = dir
            n_ligne, n_colone = ligne + i, colone + j
            if (n_ligne, n_colone) not in deja_vus:
                laby.retrait_mur((i,j), d)
                enregistrement_image(laby, images)
                generation_rec(laby, n_ligne, n_colone, deja_vus, images)


def generation(nb_l, nb_c, avec_gif):
    """
    Utilité : 
        Permet de gérer l'appel récursif du labyrinthe.
    Entrée : 
        Le nombre de lignes et de colonnes souhaitées pour le labyrinthe et avec_gif (0 si pas de GIF, 1 si oui).
    Renvoie : 
        Le labyrinthe généré.
    """
    laby = Laby(nb_l, nb_c)
    deja_vus = []
    images = []
    generation_rec(laby, 0, 0, deja_vus, images)
    if avec_gif == 1:
        """partie faite avec chat gpt""" 
        gif(images, "laby.gif")  # Crée le GIF
        # Vérifie que le fichier GIF existe avant d'essayer de l'ouvrir
        if os.path.exists("laby.gif"):
            ouvrir_gif_navigateur("laby.gif")  # Ouvre le GIF dans le navigateur par défaut
        else:
            print("Erreur : Le fichier GIF n'a pas pu être créé.")
    else :
        return laby



def choix_principal ():
    """"fonction pour l'utilisateur, rien de bien complqué, juste long"""
    affichage_text("Saisissez 1 si vous voulez créer un labyrinthe et l'afficher en interface console.")
    affichage_text("Saisissez 2 si vous voulez créer un labyrinthe et l'afficher en gif.")
    affichage_text("Saisissez 3 si vous voulez quitter.")
    choix = int(input("Votre choix ici : "))


    if choix==1:
        affichage_text("Vous avez choisi de créer un labyrinthe en interface console.")
        affichage_text("Votre labyrinthe est en cours de génération")
        laby = generation(l, h, 0)
        print(laby)
        recommecer()
        

    elif choix==2:
        affichage_text("Vous avez choisi de créer un labyrinthe et l'afficher via un gif.")
        l=demande_largeur()
        h=demande_hauteur()
        affichage_text("Votre labyrinthe est en cours de génération et s'ouvrira une fois terminé")
        laby = generation(l, h, 1)
        recommecer()

    elif choix==3:
        quitter()
    else:
        affichage_text("Veuillez saisir un choix valide")
        choix_principal()


def quitter():
    affichage_text("Voulez vous vraiment quitter ?")
    affichage_text("saisissez 'Y' si vous souhaitez quitter")
    affichage_text("saisissez 'N' si vous souhaitez rester")
    continuite=(input("Y / N : "))
    if continuite == "Y":
        affichage_text("Vous n'auriez jamais du faire ça ...")
        time.sleep(1)
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        webbrowser.open(url)
    elif continuite == "N":
        choix_principal()
    else: 
        affichage_text("Merci de choisir un choix valide")
        quitter()

def recommecer ():
    affichage_text("souhaitez-vous recommencer ?")
    affichage_text("saisissez 'Y' si vous souhaitez rester")
    affichage_text("saisissez 'N' si vous souhaitez quitter")
    continuite=(input("Y / N : "))
    if continuite == "Y":
        choix_principal()
    elif continuite == "N":
        quitter()
    else: 
        affichage_text("Merci de choisir un choix valide")
        recommecer()

def demande_largeur():
    affichage_text("Merci d'indiquer la largeur de votre labyrinthe")
    l=int(input("Largeur de votre labyrinthe : "))
    if l <= 0:
        affichage_text("Merci de rentrer une largeur valide")
        demande_largeur()
    return l

def demande_hauteur():
    affichage_text("Merci d'indiquer la hauteur de votre labyrinthe")
    h=int(input("Hauteur de votre labyrinthe : "))
    if h <= 0:
        affichage_text("Merci de rentrer une hauteur valide")
        demande_hauteur()
    return h
affichage_text("Bienvenue !")
choix_principal()
