#################################################################################
#   Class main from Bomberman                                                   #
#   Created by Vincent : 24/01/2020                                             #
#                                                                               #
#   Cette classe est la classe principale du jeu, elle permet de definir le     #
#   le decor, et contient la boucle du jeu                                      #
#                                                                               #
#################################################################################

#################################################################################
##
## Import

import pygame
from pygame import *
import os
import random
from random import randrange
import copy
from copy import deepcopy
import time
from Player import Player
from Bombe import Bombe
from Player import IA
from Bonus import Bonus
pygame.init()


#################################################################################
##
##  Importation des images et musiques:

# Decor
BLOCK = pygame.image.load("images/blocks/stone.png")
BLOCK_MIDDLE = pygame.image.load("images/blocks/stone2.png")
GRASS = pygame.image.load("images/blocks/grass.png")
BLOCK_BRICK = pygame.image.load("images/blocks/brick.png")
arrow_sprite = pygame.image.load("images/menu/arrow.png")
fond = pygame.image.load("images/menu/menu2.png")


# Sprites
BLEU = pygame.image.load("images/ia/Bleu/sprite.png")
ROUGE = pygame.image.load("images/ia/Rouge/sprite.png")
JAUNE = pygame.image.load("images/ia/Jaune/sprite.png")
ORANGE = pygame.image.load("images/ia/Orange/sprite.png")
BOMBES = pygame.image.load("images/bombe/bomb.png")
FIRE =pygame.image.load("images/fire/explosion2.png")

# Musique
pygame.mixer.init()
SON_FOND = pygame.mixer.Sound("son/bomberman.wav")
SON_BOMBE = pygame.mixer.Sound("son/bombe.wav")
SON_MORT = pygame.mixer.Sound("son/mort.wav")
SON_VICTOIRE = pygame.mixer.Sound("son/victory.wav")
SON_DEFEAT = pygame.mixer.Sound("son/defeat.wav")


#################################################################################
##
##  Variables globales

SCREEN_WIDTH = pygame.display.Info().current_w      # L'ecran de jeu s'ajuste à la taille de l'ecran de l'ordinateur
SCREEN_HEIGHT = pygame.display.Info().current_h - 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), RESIZABLE)
scrrec = SCREEN.get_rect()
fond = pygame.image.load("images/menu/menu2.png").convert()
VICTOIRE = pygame.image.load("images/menu/VICTOIRE.png").convert()
arrow_sprite = pygame.image.load("images/menu/arrow.png")
COMMANDES = pygame.image.load("images/menu/commandes.png").convert()
VICTOIRE = pygame.transform.scale(VICTOIRE, (scrrec.right, scrrec.bottom))
fond = pygame.transform.scale(fond, (scrrec.right, scrrec.bottom))
COMMANDES = pygame.transform.scale(COMMANDES,(scrrec.right, scrrec.bottom))
#arrow_sprite = pygame.transform.scale(arrow_sprite, (scrrec.right, scrrec.bottom))
ZOOM = int((64/1920)*SCREEN_WIDTH)   # Taille d'une case en pixels
jeu_fini = False
clock = pygame.time.Clock()
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
TIME_START = time.time()# Temps depuis le lancement du jeu
GAME_OVER = pygame.image.load("images/menu/gameover.png").convert()
VIT =ZOOM //16 # Vitesse de deplacement des joueurs


FONT = pygame.font.SysFont("arial", 25)     # Definition de la police d'écriture
CLOCK = pygame.time.Clock()                 # Mise en place de l'horloge interne


LAST_DIRECTION = 0
LIST_BOMB = []      # Liste contenant les bombes
LIST_IA = []        # Liste contenant les IA en vie
LIST_JOUEUR = []    # Liste contennant les joueurs en vie
LIST_BONUS = []     # Liste contennant les bonus

def init_jeu():
    global TAB, LIST_BOMB, LIST_IA,LIST_JOUEUR, JOUEUR_BLEU,JOUEUR_JAUNE,JOUEUR_ORANGE,JOUEUR_ROUGE,HAUTEUR,LARGEUR,LIST_BONUS
    SON_FOND.play(loops=-1, maxtime = 0, fade_ms=0)
    TAB = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    HAUTEUR = len(TAB)     # Nombre de cases en hauteur
    LARGEUR = len(TAB[0])  # Nombre de cases en largeur
    LIST_JOUEUR.clear()
    LIST_IA.clear()
    LIST_BOMB.clear()
    LIST_BONUS.clear()
    POS_IA = [(HAUTEUR-2, LARGEUR-2), (HAUTEUR-2, 1), (1, LARGEUR-2)]
    JOUEUR_BLEU = Player(1, 1,1, BLEU,int(ZOOM*(102/64)), ZOOM)
    JOUEUR_JAUNE = IA(POS_IA[0][0], POS_IA[0][1],1, JAUNE,int(ZOOM*(102/64)), ZOOM, (0,-1))
    JOUEUR_ORANGE = IA(POS_IA[1][0], POS_IA[1][1],1, ORANGE,int(ZOOM*(102/64)), ZOOM,(1,0))
    JOUEUR_ROUGE = IA(POS_IA[2][0], POS_IA[2][1],1, ROUGE,int(ZOOM*(102/64)), ZOOM, (-1,0))

init_jeu()
TIME = time.time()

DONE = False                                # Variable qui indique si le jeu est terminé

GRILLE_BOMBE = None     # Grille contenant les distances aux bombes sur la map

#################################################################################
##
##  Fonctions principales

## draw():
#   Parcourt TAB et place les images aux coordonnees donnees
#   en fonction de la valeur des cases du tableau
#   Puis place les joueurs
def draw():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 0 or TAB[j][i] == 4 or TAB[j][i] ==  5 or TAB[j][i] == 6): SCREEN.blit(GRASS,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 1): SCREEN.blit(BLOCK,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 2): SCREEN.blit(BLOCK_MIDDLE,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 3): SCREEN.blit(BLOCK_BRICK,(i*ZOOM,j*ZOOM))

    for bonus in LIST_BONUS:
        bonus.draw(SCREEN, ZOOM)

    for bomb in LIST_BOMB:
        bomb.anim(TIME)
        bomb.draw(SCREEN)
        removeBomb()
        for i in range(bomb.rayon):
            bomb.drawExplo(SCREEN,TAB,LIST_BOMB, i,(1+i),ZOOM, LIST_BONUS)
            bomb.drawExplo(SCREEN,TAB, LIST_BOMB, i,-(1+i),ZOOM, LIST_BONUS)

    for joueur in LIST_JOUEUR:

        joueur.draw(SCREEN, ZOOM//2, int(ZOOM*(102/ZOOM)), ZOOM)

    SCREEN.blit(FONT.render("Temps : " + str(int(TIME- TIME_START)), True, BLACK), (900,15))

    pygame.display.flip()       # Rafraichis l'affichage de Pygame


## generate():
#   Genere les cases destructibles aleatoirement
#   Les maps changent donc à chaque jeux
def generate():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 0 and random.randrange(2)): TAB[j][i] = 3
    TAB[1][1] = 0; TAB[1][2] = 0; TAB[2][1] = 0
    TAB[HAUTEUR-2][1] = 0; TAB[HAUTEUR-2][2] = 0; TAB[HAUTEUR-3][1] = 0
    TAB[1][LARGEUR-2] = 0; TAB[1][LARGEUR-3] = 0; TAB[2][LARGEUR-2] = 0
    TAB[HAUTEUR-2][LARGEUR-2] = 0; TAB[HAUTEUR-3][LARGEUR-2] = 0; TAB[HAUTEUR-2][LARGEUR-3] = 0


## removeBomb():
#   Regarde chaque bombe de la liste
#   On l'enleve de la liste des bombes si elle explose
def removeBomb():
    for Bomb in LIST_BOMB:
        if (Bomb.Explode() == True):
            Bomb.spriteCount = 0
            Bomb.spriteDir=0
            Bomb.sprite= Bomb.getSpriteExplo(FIRE, ZOOM)
            #SON_BOMBE.play()       # Mise en commentaire car ca fais beuguer l'ordi de Quentin
            TAB[Bomb.caseY][Bomb.caseX] = 5
            Bomb.explode = False
            Bomb.player.nbBombe -= 1

        if(Bomb.exploFin):
            TAB[Bomb.caseY][Bomb.caseX] = 0
            LIST_BOMB.remove(Bomb)


## poseBombe(player):
#   Verifie si le joueur peut poser une bombe
#   Pose une bombe sur une case
#   Mise à jour du tableau
def poseBombe(player):
    caseX = player.caseY
    caseY = player.caseX
    if(TAB[caseY][caseX] == 0 and player.nbBombe < player.nbBombeMax):
        LIST_BOMB.append(Bombe(caseX*ZOOM+100,caseY*ZOOM+96,BOMBES, ZOOM, TIME,player))
        TAB[caseY][caseX] = 4
        player.nbBombe += 1


## Meurt(player):
#   Regarde si la position du joueur correspond à une cases en explosion
#   Enleve une vie au joueur
#   Si le joueur n'a plus de vie, on enleve le joueur de la liste des joueurs/IA
def Meurt(player):
    x = player.caseY
    y = player.caseX
    if(TAB[y][x]==5):
        player.lives -= 1
        if player.lives >= 1:
            player.invincible = int(TIME- TIME_START) + 5
        if player.lives <= 0:
            if(player in LIST_JOUEUR):
                LIST_JOUEUR.remove(player)
            if(player in LIST_IA):
                LIST_IA.remove(player)
                player.nbBombeMax = 0
                #SON_MORT.play()

def Invinciblility(player):
    if player.invincible >= int(TIME- TIME_START):
        player.lives = 999999999999999
    elif player.invincible > 0:
        player.lives = 1
        player.invincible = 0



## iaDanger(ia):
#   Regarde la position de l'IA
#   Retourne si elle se trouve dans une zone de danger = le rayon de l'explosion de la bombe
def iaDanger(ia): return GRILLE_BOMBE[ia.caseX][ia.caseY] <= 4


## getCloserPlayer(Player):
#   Retourne la position du joueur le plus proche
#
def getCloserPlayer(player):
    dist_min = 1000
    coordonnees_min = (0,0)
    for joueur in LIST_JOUEUR:
        if joueur.carteDist[player.caseX][player.caseY] < dist_min:
            dist_min = joueur.carteDist[player.caseX][player.caseY]
            coordonnees_min = (joueur.caseX,joueur.caseY)

    return coordonnees_min

def MenuScreen():
    global screen,DONE,clock, arrow_sprite
    done2 = False
    done = False
    start = 1
    commandes = 2
    yes = True
    no = False
    arrow = {}
    arrow['x']= 150
    arrow['y']= 430
    arrow['sprite'] = arrow_sprite
    arrow['choice'] = yes

    last_time = 0

    while not done2:

        time = int( pygame.time.get_ticks() / 100 )

        event = pygame.event.Event(pygame.USEREVENT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                DONE = True
                done2 = True

        KeysPressed = pygame.key.get_pressed() # User did something



        if KeysPressed[pygame.K_DOWN] and time - last_time > 3:
            last_time = time
            if arrow['y'] == 430:
                arrow['y']= 560
                arrow['choice'] = no
            else:
                arrow['y']= 430
                arrow['choice'] = yes

        if KeysPressed[pygame.K_UP] and time - last_time > 3:
            last_time = time
            if arrow['y'] == 430:
                arrow['y']= 560
                arrow['choice'] = no
            else:
                arrow['y']= 430
                arrow['choice'] = yes

        if KeysPressed[pygame.K_RETURN]:

            if arrow['choice'] == yes:
                done2 = True


            if arrow['choice'] == no:
                while not done:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # If user clicked close
                            DONE = True
                            done2 = True
                            done = True

                    KeysPressed = pygame.key.get_pressed()
                    if KeysPressed[pygame.K_ESCAPE]:
                        done = True
                    SCREEN.blit(COMMANDES,(0,0))
                    pygame.display.flip()



        SCREEN.blit(fond ,(0,0))
        SCREEN.blit(arrow['sprite'],(arrow['x'],arrow['y']))

        done = False
        pygame.display.flip()
        clock.tick(30)

def GameOver():
    global DONE
    done2 = False
    pressed = False
    press_time = 0
    press_speed = 5
    jeu_fini = False
    SON_FOND.stop()
    #SON_DEFEAT.play()
    while not done2:

        event = pygame.event.Event(pygame.USEREVENT)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                DONE = True
                done2 = True


        KeysPressed = pygame.key.get_pressed()

        if KeysPressed[pygame.K_RETURN]:
            pressed = True
            press_time = int( pygame.time.get_ticks() / 100 )

        if pressed and int( pygame.time.get_ticks() / 100 ) - press_time >= press_speed:
            done2 = True
            jeu_fini = True
            return jeu_fini

        SCREEN.blit(GAME_OVER,(0,0))
        pygame.display.flip()

        with open("scores.txt","w") as fichier :
            fichier.write(str(TIME) + "\n")

def victory():
    global DONE
    done2 = False
    pressed = False
    press_time = 0
    press_speed = 5
    jeu_fini = False
    SON_FOND.stop()
    #SON_VICTOIRE.play()

    while not done2:
        event = pygame.event.Event(pygame.USEREVENT)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                DONE = True
                done2 = True

        KeysPressed = pygame.key.get_pressed()

        if KeysPressed[pygame.K_RETURN]:
            pressed = True
            press_time = int( pygame.time.get_ticks() / 100 )

        if pressed and int( pygame.time.get_ticks() / 100 ) - press_time >= press_speed:
            done2 = True
            jeu_fini = True
            return jeu_fini

        SCREEN.blit(VICTOIRE,(0,0))
        pygame.display.flip()

## iaFuite(ia):
#   Regarde les deplacement possible de l'IA
#   Se deplace sur la case la plus grande = le plus loin de la bombe
def iaFuite(ia) :
    if(ia.x != 0 or ia.y !=0): ia.needToGoCenter = True
    else:ia.needToGoCenter = False

    possibleMove = getPossibleMove(ia)
    posIA = (ia.caseY,ia.caseX)
    max = 0
    caseMax = None
    for case in possibleMove :
        if GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]] > max and GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]] < 100:
            max = GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]]
            caseMax = case
    if(caseMax != None and not ia.needToGoCenter):
        ia.dir = caseMax
        ia.move(ia.dir[0]*VIT, ia.dir[1]*VIT,ZOOM)
        ia.setRightDir()
    else:
        ia.move(ia.dir[0]*VIT, ia.dir[1]*VIT,ZOOM)



## moveIA(ia):
#   S'occupe du deplacement principal des IA
#   Regarde en premiere si l'IA est en danger = dans le rayon d'explosion de la bombe
#   Si non, elle se dirige dans une direction jusqu'à rencontrer un mur
def moveIA(ia):
    if iaDanger(ia) :  iaFuite(ia)
    else :
        possibleMove = getPossibleMove(ia)
        if((0,0) in possibleMove): possibleMove.remove((0,0))
        if (ia.dir in possibleMove): ia.move(ia.dir[0]*VIT, ia.dir[1]*VIT,ZOOM)
        else:
            poseBombe(ia)
            if(len(possibleMove) !=0 ):
                deplacement_ia = random.randrange(len(possibleMove))
                ia.dir = possibleMove[deplacement_ia]
                ia.setRightDir()
            else:
                ia.dir = (0,0)

## getTabPos(x,y):
#   Prendre la position en pixels du joueur
#   Regarde en fonction du zoom (taille de la fenetre) sur quelle case le joueur se trouve
#   Retourne la case du joueur
def getTabPos(x,y):
    posX = x // ZOOM
    posY = y // ZOOM
    return (posX,posY)


## getPossibleMovePlayer(player):
#   En focntion de la position du joueur
#   On regarde les cases tout autour pour connaitre leurs valeurs
#   Retourne les deplacements possibles du joueur
def getPossibleMove(player):
    possibleMove = []
    tab = []

    tab.append(TAB[player.caseX+1][player.caseY])
    tab.append(TAB[player.caseX-1][player.caseY])
    tab.append(TAB[player.caseX][player.caseY+1])
    tab.append(TAB[player.caseX][player.caseY-1])
    tab.append(TAB[player.caseX][player.caseY])

    if((tab[0]  == 0 or tab[0]  == 5 or tab[0]  == 6 or player.y != 0) and player.x == 0): possibleMove.append((0,1))
    if((tab[1]  == 0 or tab[1]  == 5 or tab[1]  == 6 or player.y != 0) and player.x == 0): possibleMove.append((0,-1))
    if((tab[2]  == 0 or tab[2]  == 5 or tab[2]  == 6 or player.x != 0) and player.y == 0): possibleMove.append((1,0))
    if((tab[3]  == 0 or tab[3]  == 5 or tab[3]  == 6 or player.x != 0) and player.y == 0): possibleMove.append((-1,0))
    if((tab[4]  == 0 or tab[4]  == 5 or tab[4]  == 6 or player.x != 0) and player.y == 0): possibleMove.append((0,0))


    return possibleMove

## grilleBombe():
#   Grille contenantles murs et les bombes
#   Elle permet ensuite de savoir si les ia sont en danger ou non
def grilleBombe():
    global GRILLE_BOMBE
    GRILLE_BOMBE = copy.deepcopy(TAB)
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TAB[y][x] == 4 or TAB[y][x] == 5): GRILLE_BOMBE[y][x] = 0
            if (TAB[y][x] == 1 or TAB[y][x] == 2 or TAB[y][x] == 3): GRILLE_BOMBE[y][x] = 1000
            if (TAB[y][x] == 0): GRILLE_BOMBE[y][x] = 100


## miseDistance():
#   Fonction qui permet de mettre à distance les cases de la grille bombe
#   Si la case se trouve à cote de la bombe elle sera mise à 1 (etc)
def miseDistance():
    global GRILLE_BOMBE
    done = True
    while done:
        done = False
        for y in range(HAUTEUR):
            for x in range(LARGEUR):
                if (GRILLE_BOMBE[y][x] == 1000): continue
                if (GRILLE_BOMBE[y][x] >= 0):
                    mini = min(GRILLE_BOMBE[y][x+1], GRILLE_BOMBE[y][x-1], GRILLE_BOMBE[y+1][x], GRILLE_BOMBE[y-1][x])
                    if (mini +1 < GRILLE_BOMBE[y][x]):
                        GRILLE_BOMBE[y][x] = mini +1
                        done = True

def takeBonus(player):
    global TAB
    for bonus in LIST_BONUS:
        if(bonus.caseY == player.caseX and bonus.caseX == player.caseY):
            bonus.effect(player)
            LIST_BONUS.remove(bonus)
            TAB[player.caseX][player.caseY]=0

def interactionJoueur():
    global JOUEUR_BLEU

    keysPressed = pygame.key.get_pressed()  # On retient les touches pressees

    ############################ Pose Bombe ############################
    if(keysPressed[pygame.K_SPACE]):
        if JOUEUR_BLEU in LIST_JOUEUR :
            poseBombe(JOUEUR_BLEU)

    ############################ Deplacement ############################
    ## Mouvements du joueur:
    #   On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
    #   On fait appelle a la fonction move pour changer les coordonnees et les sprites

    possibleMove = getPossibleMove(JOUEUR_BLEU)

    ## Si deux touches sont pressees en meme temps on priorise le changement de direction :
    if(keysPressed[pygame.K_UP] and keysPressed[pygame.K_RIGHT] and JOUEUR_BLEU.dir == (0,-1) and (1,0) in possibleMove): JOUEUR_BLEU.dir = (1,0)
    elif(keysPressed[pygame.K_UP] and keysPressed[pygame.K_RIGHT] and JOUEUR_BLEU.dir == (1,0) and (0,-1) in possibleMove): JOUEUR_BLEU.dir = (0,-1)
    elif(keysPressed[pygame.K_UP] and keysPressed[pygame.K_LEFT] and JOUEUR_BLEU.dir == (-1,0) and (0,-1) in possibleMove): JOUEUR_BLEU.dir = (0,-1)
    elif(keysPressed[pygame.K_UP] and keysPressed[pygame.K_LEFT] and JOUEUR_BLEU.dir == (0,-1) and (-1,0) in possibleMove): JOUEUR_BLEU.dir = (-1,0)
    elif(keysPressed[pygame.K_DOWN] and keysPressed[pygame.K_RIGHT] and JOUEUR_BLEU.dir == (1,0) and (0,1) in possibleMove): JOUEUR_BLEU.dir = (0,1)
    elif(keysPressed[pygame.K_DOWN] and keysPressed[pygame.K_RIGHT] and JOUEUR_BLEU.dir == (0,1) and (1,0) in possibleMove): JOUEUR_BLEU.dir = (1,0)
    elif(keysPressed[pygame.K_DOWN] and keysPressed[pygame.K_LEFT] and JOUEUR_BLEU.dir == (0,1) and (-1,0) in possibleMove): JOUEUR_BLEU.dir = (-1,0)
    elif(keysPressed[pygame.K_DOWN] and keysPressed[pygame.K_LEFT] and JOUEUR_BLEU.dir == (-1,0) and (0,1) in possibleMove): JOUEUR_BLEU.dir = (0,1)
    ## Si une seule touche est pressees on prend la direction idoine
    elif(keysPressed[pygame.K_DOWN] and (0,1) in possibleMove): JOUEUR_BLEU.dir = (0,1)
    elif(keysPressed[pygame.K_UP] and (0,-1) in possibleMove): JOUEUR_BLEU.dir = (0,-1)
    elif(keysPressed[pygame.K_RIGHT] and (1,0) in possibleMove): JOUEUR_BLEU.dir = (1,0)
    elif(keysPressed[pygame.K_LEFT] and (-1,0) in possibleMove): JOUEUR_BLEU.dir = (-1,0)
    ## Si aucunes touches n'est pressees on quitte la fonction
    else: return

    ## Si la fonction n'a pas ete quitte jusqu'ici, c'est qu'un deplacement a ete valide, on procede donc au deplacement du joueur par rapport a sa direction
    JOUEUR_BLEU.setRightDir()
    JOUEUR_BLEU.move(JOUEUR_BLEU.dir[0]*VIT,JOUEUR_BLEU.dir[1]*VIT,ZOOM)


#################################################################################
##
##  Initialisation

def Init():
    SCREEN.fill(BLACK)
    MenuScreen()
    pygame.mouse.set_visible(True)
    pygame.display.set_caption("ESIEE - BOMB HERMANN")
    #pygame.mixer.music.play()   # Activation de la musique

    LIST_IA.append(JOUEUR_JAUNE)        # Ajout du joueur JAUNE dans la liste IA
    LIST_IA.append(JOUEUR_ORANGE)       # Ajout du joueur ORANGE dans la liste IA
    LIST_IA.append(JOUEUR_ROUGE)        # Ajout du joueur ROUGE dans la liste IA


    for ia in LIST_IA:
        LIST_JOUEUR.append(ia)
        ia.setRightDir()    # Defini la direction des sprites des ia a l'init

    LIST_JOUEUR.append(JOUEUR_BLEU)

    generate()
#################################################################################
##
##   Boucle principale
# --------  Main -----------
Init()
while not DONE:
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True

        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            oldZoom = ZOOM
            ZOOM = int((64/1920)*SCREEN_WIDTH)
            VIT = int(ZOOM / 16)

            for player in LIST_JOUEUR:
                player.x = int(ZOOM * (player.x/oldZoom))
                player.y = int(ZOOM * (player.y/oldZoom))
                player.getSprite(int(ZOOM*(102/64)),ZOOM)

            GRASS = pygame.transform.scale(pygame.image.load("images/blocks/grass.png"),(ZOOM,ZOOM))
            BLOCK_BRICK = pygame.transform.scale(pygame.image.load("images/blocks/brick.png"),(ZOOM,ZOOM))
            BLOCK = pygame.transform.scale(pygame.image.load("images/blocks/stone.png"),(ZOOM,ZOOM))
            BLOCK_MIDDLE = pygame.transform.scale(pygame.image.load("images/blocks/stone2.png"),(ZOOM,ZOOM))
            pygame.display.flip()
            draw()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: LAST_DIRECTION = 1
            if event.key == pygame.K_RIGHT: LAST_DIRECTION = 2
            if event.key == pygame.K_DOWN: LAST_DIRECTION = 3
            if event.key == pygame.K_UP: LAST_DIRECTION = 4

        for joueur in LIST_JOUEUR:
            joueur.generateDist(TAB)



    grilleBombe()
    miseDistance()
    for ia in LIST_IA:
        moveIA(ia)

    interactionJoueur()

    for ia in LIST_IA:
        Meurt(ia)
        Invinciblility(ia)

    #print()
    #for i in range(len(TAB)):
        #print(TAB[i])

    Meurt(JOUEUR_BLEU)
    Invinciblility(JOUEUR_BLEU)
    if (JOUEUR_BLEU not in LIST_JOUEUR):
        SCREEN.fill(BLACK)
        jeu_fini = GameOver()
    if (len(LIST_IA) == 0):
        SCREEN.fill(BLACK)
        jeu_fini = victory()

    for player in LIST_JOUEUR:
        if(TAB[player.caseX][player.caseY] == 6): takeBonus(player)

    SCREEN.fill(BLACK)
    TIME = time.time()
    draw()   # On redessine l'affichage et on actualise
    CLOCK.tick(30) # Limite d'image par seconde
    if jeu_fini == True:
        jeu_fini = False
        init_jeu()
        Init()
        draw()
        continue



    # A mettre quand le personnage est mort : pygame.mixer.music.stop()


pygame.quit() # Ferme la fenetre et quitte le jeu
