import pygame
import neat
import time
import os 
import random 
pygame.font.init() # init font

# Dimensioni della finestra di gioco
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Caricamento e ridimensionamento delle immagini degli uccelli
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]

# Caricamento e ridimensionamento delle altre immagini di gioco
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    """
    Classe che rappresenta l'uccello nel gioco.
    Gestisce il movimento, l'animazione e la rotazione.
    """
    IMGS = BIRD_IMGS  # Immagini per l'animazione
    MAX_ROTATION = 25  # Massima inclinazione verso l'alto
    ROT_VEL = 20  # Velocità di rotazione verso il basso
    ANIMATION_TIME = 5  # Tempo tra un frame dell'animazione e il successivo

    def __init__(self, x, y):
        """Inizializza l'uccello con la posizione di partenza."""
        self.x = x
        self.y = y
        self.tilt = 0  # Inclinazione iniziale
        self.tick_count = 0  # Conta i frame dall'ultimo salto
        self.vel = 0  # Velocità verticale
        self.height = self.y  # Altezza iniziale
        self.img_count = 0  # Conta i frame per l'animazione
        self.img = self.IMGS[0]  # Immagine iniziale

    def jump(self):
        """Fa saltare l'uccello."""
        self.vel = -10.5  # Velocità negativa per salire (coordinate decrescono verso l'alto)
        self.tick_count = 0  # Reset del conteggio per calcolare il movimento
        self.height = self.y  # Registra l'altezza da cui è partito il salto

    def move(self):
        """Gestisce il movimento dell'uccello tenendo conto della gravità."""
        self.tick_count += 1  # Aumenta il conteggio dei frame
        
        # Calcola il movimento usando una formula per la fisica del salto
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # Limita la velocità massima di discesa
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2  # Aggiunge un piccolo boost per il salto

        self.y = self.y + d  # Aggiorna la posizione verticale

        # Controlla se l'uccello sta ancora salendo o ha raggiunto un certo punto
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION  # Inclina verso l'alto
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL  # Ruota verso il basso simulando la caduta

    def draw(self, win):
        """Disegna l'uccello nella finestra di gioco."""
        self.img_count += 1  # Aumenta il conteggio per l'animazione

        # Cambia l'immagine in base al conteggio per simulare il battito delle ali
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0  # Reset dell'animazione

        # Se l'uccello è in picchiata, mantieni un'immagine fissa
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Ruota l'immagine in base alla tilt
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)  # Disegna l'immagine ruotata

    def get_mask(self):
        """Restituisce la maschera dell'uccello per la collisione pixel-perfect."""
        return pygame.mask.from_surface(self.img)



class Pipe:
    """Classe che rappresenta un tubo nel gioco."""
    GAP = 200  # Spazio tra i tubi
    VEL = 5  # Velocità di movimento dei tubi

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False  # Flag per controllare se l'uccello ha superato il tubo
        self.set_height()
    
    def set_height(self):
        """Imposta l'altezza del tubo in modo casuale."""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Muove il tubo verso sinistra."""
        self.x -= self.VEL

    def draw(self, win):
        """Disegna il tubo nella finestra di gioco."""
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self,bird):
        """Restituisce True se l'uccello collide con il tubo."""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False



class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Muove la base verso sinistra."""
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Se il primo sprite è fuori dalla finestra, sposta il secondo sprite
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        # Se il secondo sprite è fuori dalla finestra, sposta il primo sprite
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """Disegna la base nella finestra di gioco."""
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, bird, pipes, base, score):
    # Disegna lo sfondo
    win.blit(BG_IMG, (0,0))

    # Disegna i tubi
    for pipe in pipes:
        pipe.draw(win)

    # Disegna il punteggio
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
                    
    # Disegna la base
    base.draw(win)

    # Disegna l'uccello
    bird.draw(win)

    # Aggiorna la finestra
    pygame.display.update()



def main(genomes, config):
    # Inizializza il bird e la finestra di gioco
    nets = []
    birds = []
    ge = []

    for g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0
    

    run = True
    while run:
        clock.tick(30)  # Limita il gioco a 30 frame al secondo

        # Controlla gli eventi nella finestra di gioco
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #bird.move()  # Muovi l'uccello

        rem = []  # Tubi da rimuovere
        add_pipe = False  # Flag per aggiungere un nuovo tubo

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                  ge[x].fitness -= 1
                  birds.pop(x)
                  nets.pop(x)
                  ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True # Attiviamo il flag per aggiungere un tubo


            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe) # Aggiungiamo i tubi alla lista di rimozione

            
            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600)) # Aggiungiamo un nuovo tubo


        for r in rem:
            pipes.remove(r) # Rimuoviamo i tubi che sono usciti dallo schermo


        for x, bird in enumerate(birds):
        # nel caso in cui tocchi il suolo
            if bird.y + bird.img.get_height() >= 730:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        # muove la base
        base.move()

        # Disegna la finestra ad ogni iterazione
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()


main()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p =  neat.Population(config)

    # Statistiche di output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Numero di generazioni
    winner = p.run(main, 50)



# Esegui il gioco se il file viene eseguito direttamente
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
