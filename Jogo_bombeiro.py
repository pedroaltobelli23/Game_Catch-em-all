import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 800
HEIGHT = 400
janela_jogo = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Catch em` all ')

white = (255,255,255)
color_dark = (0,0,0)

#===TELA DE INICIO===
tela_inicio=False
instrucoes = True
game = True
while (tela_inicio==False):

    for event in pygame.event.get():
        # ----- Verifica consequências
        
        if event.type == pygame.QUIT:
            tela_inicio = True
            game = False

        if event.type== pygame.KEYDOWN:
            tela_inicio=True

    janela_jogo.fill(color_dark)
    titulo_na_tela = pygame.image.load('tela_de_inicio.png')
    titulo_na_tela = pygame.transform.scale(titulo_na_tela, (WIDTH,HEIGHT))
    janela_jogo.blit(titulo_na_tela,(0,0))
    pygame.display.flip()


# ----- Inicia estruturas de dados


cama_elastica_imagem = pygame.image.load('bombeiros.png')
resgatado_imagem = pygame.image.load('RESGATADO.png')
ambulancia_imagem = pygame.image.load('Ambulancia.png')
predio_imagem = pygame.image.load('images.jpg') #Precisa ser trocada pela imagem de um predio
cama_elastica_imagem = pygame.transform.scale(cama_elastica_imagem, (150,150))
resgatado_imagem = pygame.transform.scale(resgatado_imagem, (30,30))
ambulancia_imagem = pygame.transform.scale(ambulancia_imagem, (175,175))
predio_imagem = pygame.transform.scale(predio_imagem,(100,300))
tela_final = "#" #tela do game over
#Criando a classe do jogador

class Jogador(pygame.sprite.Sprite):
     def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 150
        self.rect.centery = HEIGHT - 50
        self.speedx = 0
        self.mask = pygame.mask.from_surface(self.image)

     def update(self):
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH - 120:       
            self.rect.right = WIDTH - 120
        if self.rect.left < 70:
            self.rect.left = 70

#Criando a classe do resgatado
class Resgatado(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = -25
        self.rect.centery = 400
        self.speedx = 2
        self.speedy = 4.5
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.y == 110 :
            self.speedy = - 5
        elif self.rect.centerx == 700 :
            self.rect.x -= self.speedx
            self.rect.y -= self.speedy
        
    def quicar(self):
        self.speedy = 4.5

#Criando classe da Ambulancia
class Ambulance(pygame.sprite.Sprite) :
    def __init__(self,img) :
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 150
        self.rect.y = 300
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y



class Perigo(pygame.sprite.Sprite) :
    def __init__(self,img) :
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 400
        self.rect.y = 300
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y


# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# Criando um grupo para todos os sprites
all_sprites = pygame.sprite.Group()
all_resgatados = pygame.sprite.Group()

# Criando sprites
player = Jogador(cama_elastica_imagem)
all_sprites.add(player)
rescue = Resgatado(resgatado_imagem)
all_sprites.add(rescue)
all_resgatados.add(rescue)
ambulancia = Ambulance(ambulancia_imagem)
all_sprites.add(ambulancia)

#criando evento para ir adicionando resgatados

ADDRESCUE = pygame.USEREVENT + 1
CHANGE_VEL = pygame.USEREVENT + 2
pygame.time.set_timer(ADDRESCUE,10000)


        

    


#pontuacao inicial do placar
Score = 0
#numero de vidas
Lifes = 3

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        
        if event.type == pygame.QUIT:
            game = False   
        

        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx -= 16
            if event.key == pygame.K_RIGHT:
                player.speedx += 16
        
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx += 16
            if event.key == pygame.K_RIGHT:
                player.speedx -= 16

        

        if event.type == ADDRESCUE :
            rescue = Resgatado(resgatado_imagem)
            all_sprites.add(rescue)
            all_resgatados.add(rescue)
            Random_vel=(random.randint(4,7))*1000
            pygame.time.set_timer(ADDRESCUE,Random_vel)
            print(Random_vel)
            print(len(all_resgatados))
            print(rescue.speedx)

    #Fica mais dificil em funcao da pontuacao do player
    
    if Score//2 == 0:
        rescue.speedx = 2.7
    
        

    #verifica se houve ou nao colisao do resgatado com cama elastica
    for elemento in all_resgatados :
        if pygame.sprite.collide_mask(elemento,player) :   #Houve colisao
            elemento.quicar()
        if pygame.sprite.collide_mask(elemento,ambulancia) :
            elemento.kill()
            Score += 1
        if elemento.rect.y == HEIGHT - 10 :   #ira tirar uma vida quando o rescue cair no chao,nao houve colisao
            Lifes -= 1
            elemento.kill()

    # ----- Gera saídas
    janela_jogo.fill((255, 255, 0))  #Preenche background da tela do jogo
    all_sprites.draw(janela_jogo)
    vertices_ambulancia = ((WIDTH - 150,350),(WIDTH,350),(WIDTH,400),(WIDTH - 150,400))
    janela_jogo.blit(predio_imagem,(0,100)) #blit da imagem do predio

    # ----- Gerando saida da pontucao
    font = pygame.font.Font(None, 30)
    text_pontos = font.render(str(Score), 1, color_dark)
    text_pontuacao = font.render('pontuacao :',1,color_dark)
    janela_jogo.blit(text_pontos, (600,10))
    janela_jogo.blit(text_pontuacao, (450,10))

    # ----- Gerando saida da vida
    text_life = font.render(str(Lifes),1,color_dark)
    text_lifes = font.render('vidas :',1,color_dark)
    janela_jogo.blit(text_life, (750,10))
    janela_jogo.blit(text_lifes,(650,10))

    if Lifes == 0:
            game = False
    
    all_sprites.update()  #Atualizando posicao das sprites
    pygame.display.update()  # Mostra o novo frame para o jogador

#===== Tela de Game Over =====
aa=False
instrucoes = True
game = True
while (aa==False):

    for event in pygame.event.get():
        # ----- Verifica consequências
        
        if event.type == pygame.QUIT:
            aa = True
            

        if event.type== pygame.KEYDOWN:
            aa=True

    janela_jogo.fill(color_dark)
    titulo_na_tela = pygame.image.load('tela_de_inicio.png')
    titulo_na_tela = pygame.transform.scale(titulo_na_tela, (WIDTH,HEIGHT))
    janela_jogo.blit(titulo_na_tela,(0,0))
    pygame.display.flip()


# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

