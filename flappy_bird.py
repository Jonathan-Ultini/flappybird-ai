import pygame
import neat
import time
import os 
import random 

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
  IMGS = BIRD_IMGS
  # quanto il bird si inclinerà per salire
  MAX_ROTATION =  25
  # rotazione ogni volta che si muove
  ROT_VEL = 20
  # qunato durerà ogni animazione
  ANIMATION_TIME = 5

  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.tilt = 0
    self.tick_count = 0
    self.vel = 0
    self.height = self.y
    self.img_count = 0
    self.img = self.IMGS[0]

  def jump(self):
    self.vel = -10.5 # perchè per salire bisogna andare verso lo 0 in su e aumentare per scendere
    self.tick_count = 0 # sapre quando si cambia velocità o direzione
    self.height = self.y # da dove inizia a muoversi il bird

  def move(self):
    self.tick_count += 1 # teniamo conto delle volte che si muove

    # di quanti pixel ci muoviamo, -10.5 + 1.5 = 1.5  continuando a salire o diminuire calcola quanto si muove nel salto
    d = self.vel*self.tick_count + 1.5*self.tick_count**2

    # controlliamo che non vada troppo veloce
    if d >= 16:
      d = 16

    if d < 0:
      d -= 2

    self.y = self.y + d

    if d < 0 or self.y < self.height + 50:
      if self.tilt < self.MAX_ROTATION:
        self.tilt = self.MAX_ROTATION
      else:
        if self.tilt > -90:
          self.tilt -= self.ROT_VEL


  def draaw(self, win):
    self.img_count += 1

    # seleziona quale immagine utilizzare in base a img_count
    if self.img_count < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
    elif self.img_count < self.ANIMATION_TIME*2:
      self.img = self.IMGS[1]
    elif self.img_count < self.ANIMATION_TIME*3:
      self.img = self.IMGS[2]
    elif self.img_count < self.ANIMATION_TIME*4:
      self.img = self.IMGS[1]
    elif self.img_count < self.ANIMATION_TIME*4 + 1:
      self.img = self.IMGS[0]
      self.img_count = 0

    if self.itlt <= -80:
      self.img = self.IMGS[1]
      self.img_count = self.ANIMATION_TIME*2

    # ruota la immgine dal centro
    rotaded_image = pygame.transform.rotate(self.img, self.tilt)
    new_rect = rotaded_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
    win.blit(rotaded_image, new_rect.topleft)