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
import copy
import time
from Player import Player
from Bombe import Bombe
#from Sprite import Sprite

#################################################################################
##
##  Variables globales

# TAB est la matrice permettant de former la carte
# 0 vide
# 1 mur exterieur
# 2 mur interieur
# 3 briques destructibles
pygame.init()
TAB = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,3,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
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
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
actualTime = 0
#################################################################################
##
##  Importation des images :

# de la carte
Block = pygame.image.load("images/blocks/stone.png")
BlockMiddle = pygame.image.load("images/blocks/stone2.png")
Grass = pygame.image.load("images/blocks/grass.png")
Brick = pygame.image.load("images/blocks/brick.png")

# des sprites des differents personnages
Bleu = pygame.image.load("images/ia/Bleu/sprite.png")
Rouge = pygame.image.load("images/ia/Rouge/sprite.png")
Jaune = pygame.image.load("images/ia/Jaune/sprite.png")
Orange = pygame.image.load("images/ia/Orange/sprite.png")
Vert = pygame.image.load("images/ia/Vert/sprite.png")

#du sprite de la bombe
Bombe = pygame.image.load("images/bombe/bomb.png")


#################################################################################
##
##  Importation des musiques :

#importation de la musique du jeu

pygame.mixer.music.load("son/bomberman_stage_theme.mp3")





#################################################################################
##
##  Fonctions principales

# getSprite(Color):
#   Decoupe l'image Color en sprite
#   Met les sprite a l'echelle de la carte
#   Les rajoute dans un tableau en 2D tel que :
#   Tab = [[SpriteAvant_1, SpriteAvant_2, ...],[SpriteDroit_1, SpriteDroit_2, ...]]
def getSprite(Color,hauteur):
    Tab = []
    for j in range(4):
        tabTemp = []
        for i in range(4):
            imTemp = Color.subsurface((i*29) + (3*i) + 3,0 + (j*48),29,46)
            imTemp = pygame.transform.scale(imTemp,(ZOOM,hauteur))
            tabTemp.append(imTemp)
        Tab.append(tabTemp)
    return Tab

# dessine():
#   Parcourt TAB et place les images aux coordonnees idoines
#   en fonction de la valeur des cases du tableau
#   Puis place les joueurs
def dessine():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 4):
                screen.blit(Bombe,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 3):
                screen.blit(Brick,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 2):
                screen.blit(BlockMiddle,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 1):
                screen.blit(Block,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 0):
                screen.blit(Grass,(i*ZOOM,j*ZOOM))

    JoueurBleu.draw(screen)
    JoueurVert.draw(screen)
    JoueurJaune.draw(screen)
    JoueurRouge.draw(screen)
    JoueurOrange.draw(screen)
    screen.blit(font.render(str(actualTime // 1), True, WHITE), ((1920 // 2) - 25 , 64*HAUTEUR + 32))
    pygame.display.flip() # Rafraichis l'affichage de Pygame

## move():
#   On change les coordonnees du joueur selon son deplacement
#   On regarde la retenu de sprite est complete ou non:
#       * Si oui on change de sprite (+1 %Nombre de sprite pour ne pas sortir du tableau) et et on reset la retenu de sprite
#       * Si non on augmente la retenu
#   (permet d'eviter un changement de sprite trop rapide par rapport a sa vitesse)
def move(player, posX, posY):
    player.y += posY
    player.x += posX
    if(player.spriteOffset == 2):
        player.spriteCount = (player.spriteCount + 1) % 4
        player.spriteOffset = 0
    else:
        player.spriteOffset += 1

def poseBombe(player):
    caseX = int(player.x/ZOOM)
    caseY = int(player.y/ZOOM)
    if(TAB[caseY][caseX] == 0):
        TAB[caseY][caseX] = 4

def getTabPos(player):
    posX = player.x // ZOOM
    posY = player.y // ZOOM
    return (posX,posY)

def getPossibleMove(player):
    possibleMove = []
    posTabX = getTabPos(player)[1]
    posTabY = getTabPos(player)[0]
    if(TAB[posTabX+1][posTabY] == 0 or TAB[posTabX+1][posTabY] == 5): possibleMove.append((0,1))
    if(TAB[posTabX-1][posTabY] == 0 or TAB[posTabX-1][posTabY] == 5): possibleMove.append((0,-1))
    if(TAB[posTabX][posTabY+1] == 0 or TAB[posTabX][posTabY+1] == 5): possibleMove.append((1,0))
    if(TAB[posTabX][posTabY-1] == 0 or TAB[posTabX][posTabY-1] == 5): possibleMove.append((-1,0))
    return possibleMove


#################################################################################
##
##  Initialisation


police = pygame.font.SysFont("arial", 22)
font = pygame.font.SysFont("arial", 50)
screenInfo = pygame.display.Info()
screeenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h - 100
screen = pygame.display.set_mode((screeenWidth,screenHeight), RESIZABLE)
pygame.display.set_caption("ESIEE - BOMBERMAN")
done = False
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
temps = time.time()
pygame.mixer.music.play()#activation de la musique
ZOOM = int((64/1920)*screeenWidth)   # Taille d'une case en pixels
JoueurBleu = Player(96,102,getSprite(Bleu,int(ZOOM*(102/64))))
liste_ia = []
JoueurJaune = Player(720,350,getSprite(Jaune,int(ZOOM*(102/64))))
JoueurOrange = Player(1450,102,getSprite(Orange,int(ZOOM*(102/64))))
JoueurRouge = Player(1450,700,getSprite(Rouge,int(ZOOM*(102/64))))
JoueurVert= Player(96,700,getSprite(Vert,int(ZOOM*(102/64))))


liste_ia.append(JoueurJaune)
liste_ia.append(JoueurOrange)
liste_ia.append(JoueurRouge)
liste_ia.append(JoueurVert)

JoueurBleu = Player(96,102,getSprite(Bleu,int(ZOOM*(102/64))))

#Deplacement aléatoire des personnages
dep = [(0,4), (0,-4), (4,0),(-4,0)]





#################################################################################
##
##   Boucle principale


# --------  Main -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.VIDEORESIZE:
            screenHeight = event.h
            screeenWidth = event.w
            ZOOM = int((64/1920)*screeenWidth)

            JoueurBleu.sprite = getSprite(Bleu,int(ZOOM*(102/64)))
            JoueurJaune.sprite = getSprite(Jaune,int(ZOOM*(102/64)))
            JoueurOrange.sprite = getSprite(Orange,int(ZOOM*(102/64)))
            JoueurRouge.sprite = getSprite(Rouge,int(ZOOM*(102/64)))
            JoueurVert.sprite = getSprite(Vert,int(ZOOM*(102/64)))
            Grass = pygame.transform.scale(Grass,(ZOOM,ZOOM))
            Brick = pygame.transform.scale(Brick,(ZOOM,ZOOM))
            Block = pygame.transform.scale(Block,(ZOOM,ZOOM))
            BlockMiddle = pygame.transform.scale(BlockMiddle,(ZOOM,ZOOM))

            pygame.display.flip()
            dessine()

    for ia in liste_ia:
        deplacement_ia = []
        deplacement_ia = random.randrange(len(dep))
        if deplacement_ia == 0:
            ia.spriteDir = 0
        if deplacement_ia == 1:
            ia.spriteDir = 3
        if deplacement_ia == 2:
            ia.spriteDir = 2
        if deplacement_ia == 3:
            ia.spriteDir = 1
        move(ia,dep[deplacement_ia][0], dep[deplacement_ia][1])
        time.sleep(0.00001)
    keysPressed = pygame.key.get_pressed()  # On retient les touches pressees

    ## Mouvements du Joueur
    #   On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
    #   On fait appelle a la fonction move pour changer les coordonnees et les sprites
    possibleMove = getPossibleMove(JoueurBleu)
    print(possibleMove)
    if(keysPressed[pygame.K_DOWN]  and (0,1) in possibleMove):
        JoueurBleu.spriteDir = 0
        move(JoueurBleu,0,ZOOM)
    if(keysPressed[pygame.K_UP] and (0,-1) in possibleMove):
        move(JoueurBleu,0,-ZOOM)
        JoueurBleu.spriteDir = 3
    if(keysPressed[pygame.K_RIGHT] and (1,0) in possibleMove):
        move(JoueurBleu,ZOOM,0)
        JoueurBleu.spriteDir = 2
    if(keysPressed[pygame.K_LEFT] and (-1,0) in possibleMove):
        move(JoueurBleu,-ZOOM,0)
        JoueurBleu.spriteDir = 1
    if(keysPressed[pygame.K_SPACE]):
        poseBombe(JoueurBleu)

    actualTime = time.time() - temps
    screen.fill(BLACK)
    dessine()   # On redessine l'affichage et on actualise
    clock.tick(30) # Limite d'image par seconde
    #a mettre quand le personnage est mort : pygame.mixer.music.stop()
pygame.quit() # Ferme la fenetre et quitte.
