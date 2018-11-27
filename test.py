import pygame
from player import Player

#tirar depois  
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCORE1=0
SCORE2=0

 
class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		super().__init__()
 		#self.image = pygame.image.load("terra.png")	
		self.image = pygame.Surface([width, height])
		self.image.fill(GREEN)
 
		self.rect = self.image.get_rect()
 




class Level(object):
	def __init__(self, player1,player2):
		self.platform_list = pygame.sprite.Group()
		self.player1 = player1
		self.player2 = player2
		 
		#BG
		self.background = None

	def update(self):
		self.platform_list.update()
 
	def draw(self, screen):
 		#desenha oque falta
		screen.fill(BLUE)
		#screen.fill("ceu.png")
		#screen.fill([255, 255, 255])
		#screen.blit(BackGround.image, BackGround.rect)
		self.platform_list.draw(screen)
 




class Level_01(Level):
	def __init__(self, player1,player2):
		Level.__init__(self, player1,player2)
		#largura,altura,x,y
		level = [[600, 35, 300, 320], #0 main
				 [200, 35, 0, 440],   #1 esqurda baixo
				 [200, 35, 1000, 440],#2 direita baixo
				 [200, 35, 100, 200], #3 esquerda medio 
				 [200, 35, 900, 200], #4 direita medio
				 [400, 35, 400, 90],   #5 cima
				 [35, 350, 0, 0],  #6 parede
				 [35, 350, 1165, 0],  #7 parede
				 [500, 35, 0, 565],  #8 piso esquerda
				 [500, 35, 700, 565],  #9 piso direita
				 ]
 
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			self.platform_list.add(block)



 
def main():

	pygame.init()
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("TowerFall Ascencions da Deep Web")


 	#nasce player
	player1= Player("branco.png")
	player2= Player("preto.png")
 
	#Adiciona Level
	level_list = []
	level_list.append( Level_01(player1,player2) )
 
	#Seta o level
	level_num = 0
	level_atual = level_list[level_num]
 
	sprite_jogo = pygame.sprite.Group()
	player1.level = level_atual
	player2.level = level_atual

	player1.rect.x = 350
	player1.rect.y = SCREEN_HEIGHT - (player1.rect.height) * 2
	player2.rect.x = 850
	player2.rect.y = SCREEN_HEIGHT - (player2.rect.height) * 2
	sprite_jogo.add(player1)
	sprite_jogo.add(player2)
 
	#Loopa até fechar
	done = False
	clock = pygame.time.Clock()#FPS

	# -------- Main Loop -----------
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#Famoso fechar
				done = True
 
 			#SE MEXE,PORRA
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player1.go_left()
				if event.key == pygame.K_RIGHT:
					player1.go_right()
				if event.key == pygame.K_UP:
					player1.jump()
				if event.key == pygame.K_a:
					player2.go_left()
				if event.key == pygame.K_d:
					player2.go_right()
				if event.key == pygame.K_w:
					player2.jump()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player1.change_x < 0:
					player1.stop()
				if event.key == pygame.K_RIGHT and player1.change_x > 0:
					player1.stop()
				if event.key == pygame.K_a and player2.change_x < 0:
					player2.stop()
				if event.key == pygame.K_d and player2.change_x > 0:
					player2.stop()

		#colisão entre eles
		collision = pygame.sprite.collide_rect(player1, player2)

		
		#Eu não confio nesse sistema que eu achei
		if collision == True: #margem de erro and player1.rect.x>=(player2.rect.x-30) and player1.rect.x<=(player2.rect.x+30) and player1.rect.y>=player2.rect.y-38:
			sprite_jogo.remove(player2,player1)
			SCORE1+=1
			player1.jump()
			sprite_jogo.update()
			#pressione espaço
		if event.type == pygame.KEYDOWN and pygame.KEYDOWN == pygame.K_SPACE:
			sprite_jogo.remove(player1)
			sprite_jogo.add(player1, player2)

		if SCORE2>=3 or SCORE1>=3:
			sprite_jogo.add(player1, player2)

		#if SCORE2 or SCORE1 >=3: #???
		#	level_num = 1
		#	SCORE2=0
		#	SCORE1=0

		#if SCORE2 or SCORE1 >=3 and level_num==1:
		#	done = True



		#Tem que dar update pra mexer, maldito
		sprite_jogo.update()
 
		# caso coisas se mexam no level, plataformas, elevadores etc.
		#level_atual.update()
 
		# Bater nas parede
		if player1.rect.right > SCREEN_WIDTH:
			player1.rect.right = player1.rect.width
		if player1.rect.left < 0:
			player1.rect.left = SCREEN_WIDTH - player1.rect.width
		if player1.rect.bottom > SCREEN_HEIGHT:
			player1.rect.bottom = player1.rect.height
		if player1.rect.top < 0:
			player1.rect.top = SCREEN_HEIGHT - player1.rect.height

		if player2.rect.right > SCREEN_WIDTH:
			player2.rect.right = player1.rect.width 
		if player2.rect.left < 0:
			player2.rect.left = SCREEN_WIDTH - player2.rect.width
		if player2.rect.bottom > SCREEN_HEIGHT:
			player2.rect.bottom = player2.rect.height
		if player2.rect.top < 0:
			player2.rect.top = SCREEN_HEIGHT - player2.rect.height


		level_atual.draw(screen)
		sprite_jogo.draw(screen)

		clock.tick(60)	
 
		#Atualiza a tela
		pygame.display.flip()
	pygame.quit()
 
if __name__ == "__main__":
	main()