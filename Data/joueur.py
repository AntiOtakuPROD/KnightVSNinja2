import pygame
from joueur import *
from boule import *
from niveau import *
from plateforme import *
from menu import *
from ninja import *
from shuriken import *
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
ECRAN_LARGEUR  = 800
ECRAN_HAUTEUR = 600
size = [ECRAN_LARGEUR, ECRAN_HAUTEUR]
screen = pygame.display.set_mode(size)

###################################################

class Joueur(pygame.sprite.Sprite):
    #classe du joueur

    # vitesse de départ

    change_x = 3
    change_y = 0

    # sprites ou on peut rentrer dedans
    niveau = None
    
    def __init__(self, filename):

        super().__init__() 

        # sprite
        self.image = pygame.image.load(filename)

        # la hitbox
        self.rect = self.image.get_rect()
        
        
        self.attack=False


        #la variable pour l'animation après

        self.sautage = -20

        self.vie = 5
        self.bouclier = 10
        
    def update(self):
        """ bouger joueur. """   
        # gravité
        self.calc_grav()

        # mouvement horizontal
        self.rect.x += self.change_x
        self.stop()
        # test de collision
        block_hit_list = pygame.sprite.spritecollide(self, self.niveau.platform_list, False)
        for block in block_hit_list:
            self.rect.right = block.rect.left
            
        enemy_hit_list = pygame.sprite.spritecollide(self, self.niveau.enemy_list, False)
        for ninja in enemy_hit_list:
            self.change_x = 0                        
            
        # mouvement vertical
        self.rect.y += self.change_y

        # test de collision
        block_hit_list = pygame.sprite.spritecollide(self, self.niveau.platform_list, False)
        for block in block_hit_list:

            # change la position si c'est en bas ou en haut qu'on touche
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # arrête le mouvement
            self.change_y = 0
    
        if self.vie <= 0:
            self.vie = 5
           
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1

        # test si on est par terre
        if self.rect.y >= ECRAN_HAUTEUR - self.rect.height - 150 and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = ECRAN_HAUTEUR - self.rect.height - 150

    def saut(self):

        # test de plateforme si on peut sauter
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.niveau.platform_list, False)
        self.rect.y -= 2

        # saut si on peut
        if len(platform_hit_list) > 0 or self.rect.bottom >= ECRAN_HAUTEUR - 150:
            self.change_y = self.sautage

    def stop(self):
	#mouvement vers la droite tout le temps
        self.change_x = 3
	
    def attaque(self):
	#coup d'épée
        self.attack=True
		
class JoueurSprite():
    change_x = 3
    change_y = 0
    def __init__(self):

        super().__init__() 
        self.image = pygame.image.load("art/knight_base.000.png")
        self.rect = self.image.get_rect()
        self.spriteAttack=1
        self.spriteCount = 0
        self.spriteJump = 0
        self.attack = False
        
    def update(self, changex, changey, x, y):
    
        self.change_x = changex
        self.change_y = changey
        self.rect.x = x
        self.rect.y = y-25
     
    def updateAnim(self):
        
        if self.attack == False :
            if self.change_y == 0 :                     
                spriteN = "art/knight_base.00%s.png"%(int(self.spriteCount))
                self.image = pygame.image.load(spriteN)
                self.spriteCount += 1
                if self.spriteCount == 7:
                    self.spriteCount = 0
                self.spriteJump = 0
            else :
                if self.spriteJump == 0:
                    spriteN = "art/knight_saut.000.png"
                    self.image = pygame.image.load(spriteN)
                    self.spriteJump += 1
                elif self.spriteJump < 3 :
                    spriteN = "art/knight_saut.00%s.png"%(int(self.spriteJump))
                    self.image = pygame.image.load(spriteN)
                    self.spriteJump += 1
        else:
            spriteN = "art/knight_attaque.00%s.png"%(int(self.spriteAttack))
            self.image = pygame.image.load(spriteN)
            self.spriteAttack += 1
            if self.spriteAttack == 4:
                self.attack=False
                self.spriteAttack = 1
                
    def attaque(self):
	#coup d'épée
        self.attack=True
        
