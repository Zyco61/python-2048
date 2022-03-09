import pygame
from pygame.locals import *

class GUI2048(object):
    
    def __init__(self, nb):
        """
        Initialise une grille du jeu 2048 de nb*nb cases.
        Les couleurs de cases sont gérées jusqu'à une valeur de 32768.
        """
        
        #des constantes pour le dessin de la grille
        self.nb = nb #la taille de la grille
        self.w = 150 #largeur d'une case
        self.d = 10 #entre deux cases
        #la liste des coordonnées de chaque case de la grille (coordonnées du coin en haut à gauche)
        self.xy0 = [self.d + (self.d + self.w) * x for x in range(self.nb)]

        #initialisation de pygame
        pygame.init()
        #calcul de la taille totale de la fenètre
        self.wFen = self.nb * self.w + (self.nb + 1) * self.d
        #hauteur idem + un bandeau pour le score
        hFen = self.wFen + 100  
        #on définit la fenêtre de base de notre jeu
        self.fond = pygame.display.set_mode((self.wFen, hFen))
        #un titre sur cette fenêtre
        pygame.display.set_caption("2048")

        #une liste contenant les différentes cases possibles de vide à 32768
        self.cases = [self._creerCase(i) for i in range(16)]
        
        self.refresh([[0 for x in range(nb)] for y in range(nb)], 0)
    
    def _creerCase(self, n):
        clrCase = ['#CDC1B3' , '#EEE4DA', '#ECE0C8', '#EFB27C', '#F59562', '#F87A64', '#F86039', '#EDCE71', '#ECCC69', '#EBC852', '#EFC53D', '#EFC130', '#76A136', '#2CB388', '#2D83B4', '#3D3A35']
        clrPolice = ['black', 'black', 'black', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']

        case = pygame.Surface((self.w, self.w))
        case.fill(pygame.Color(clrCase[n]))

        if n > 0:
            if 2**n < 100:
                taille = 125
            elif 2**n < 1000:
                taille = 100
            elif 2**n < 10000:
                taille = 80
            else :
                taille = 60
                
            police = pygame.font.SysFont("Arial Black.ttf",taille)
            texte = police.render(str(2**n), True, clrPolice[n])
            #pour centrer le texte dans la case
            rectTexte = texte.get_rect()
            rectTexte.center = case.get_rect().center
            
            case.blit(texte, rectTexte)
        
        return case
    
    def refresh(self, g, score):
        """
        Cette méthode rafraichie l'affichage du jeu 2048 conformément à la grille passée en argument.
        
        g est une liste de nb listes.
        Par exemple ;
        g[0][0] est la case en haut a gauche,
        g[3][3] est la case en bas à droite dans une grille de 4*4.
        
        Attention : la valeur affichée est la puissance de 2 du contenu de g.
        0 -> case vide
        1 -> affiche 2
        2 -> affiche 4
        3 -> affiche 8
        4 -> affiche 16
        8 -> affiche 256
        11 -> affiche 2048
        ...
        
        score est un entier qui s'afichera en bas de l'écran.
        """

        self.fond.fill(pygame.Color("#BCAF9F"))
        for y in range(self.nb):
            for x in range(self.nb):
                self.fond.blit(self.cases[g[y][x]], (self.xy0[x], self.xy0[y])) 
        #le score :
        police = pygame.font.SysFont("Arial Black.ttf", 100)        
        txtScore = police.render("SCORE :", True, 'white')
        self.fond.blit(txtScore, (2 * self.d, self.wFen + self.d))
        txtScore = police.render(str(score), True, 'white')
        self.fond.blit(txtScore, (self.wFen // 2, self.wFen + self.d))                
                
        #Rafraîchissement de l'écran
        pygame.display.update()
        
    def gameOver(self):
        """
        Cette méthode permet d'afficher GAME OVER plein écran sur fond rouge.
        """
        self.fond.fill("red")
        police = pygame.font.Font("led.ttf",72)
        texte = police.render("GAME OVER", True, pygame.Color("#FFFF00"))
        #pour centrer le texte
        rectTexte = texte.get_rect()
        rectTexte.center = self.fond.get_rect().center
        self.fond.blit(texte,rectTexte)
        #Rafraîchissement de l'écran
        pygame.display.update()
        
    def waitClick(self):
        """
        Cette méthode attend l'action d'un joueur. Elle gère trois type d'actions :
            - demande fermeture de la fenètre : fermeture propre de la fenètre pygame et fin du programme python.
            - click sur la fenetre : retourne un tuple contenant les numéros (x, y) de la case choisie.
            - appui sur des 4 flèches du clavier : retourne un caractère 'U', 'D', 'L', ou 'R'. Quelques autres touches sont également gérées et retourne la lettre saisie.
        Une fois exécutée, on ne peut sortir de cette méthode que par l'une de ces trois actions.

        """        
        while True:
            #Limitation de vitesse de la boucle
            pygame.time.Clock().tick(20)
            
            for event in pygame.event.get():    #Attente des événements
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:   #Si clic gauche
                        if event.pos[1] < self.nb * (self.w + self.d):
                            return (event.pos[0]//(self.w + self.d), event.pos[1]//(self.w + self.d))

                if event.type == KEYDOWN:
                    touches = {K_y : 'y', K_n : 'n', K_s :'s', K_r : 'r', K_c : 'c', K_o : 'o', K_d : 'd', K_RIGHT : 'R', K_LEFT : 'L', K_UP : 'U', K_DOWN : 'D' }
                    touche = event.key
                    if touche in touches:
                        return touches[touche]                          

if __name__ == "__main__":
    import time
    
    GUI = GUI2048(4)
    
    grille = [[0 for i in range(4)] for j in range(4)]
    score = 0
    GUI.refresh(grille, score)
    time.sleep(0.02)
    
    GUI.gameOver()
    
    for i in range(4):
        for j in range(4):
            grille[i][j] = 4*i + j
            score += 2**(4*i+j+1)
            GUI.refresh(grille, score)
            time.sleep(0.025)            

    while True:
        print(GUI.waitClick())
