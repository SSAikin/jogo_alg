import pygame
from player import Player

#tirar depois
GREEN = (30, 220, 30)
BLUE = (50, 70, 255)
 
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
		self.platform_list.draw(screen)

	def draw_black(self, screen, myfont, text):
		screen.fill(GREEN)
		textsurface = myfont.render(text, False, (255,255,255)) 
		screen.blit(textsurface, (50, 200))



class Level_01(Level):
	def __init__(self, player1,player2):
		Level.__init__(self, player1,player2)
		#largura,altura,x,y
		level = [[600, 35, 300, 320],	#0 main
				 [200, 35, 0, 440],		#1 esqurda baixo
				 [200, 35, 1000, 440],	#2 direita baixo
				 [200, 35, 100, 200],	#3 esquerda medio 
				 [200, 35, 900, 200],	#4 direita medio
				 [400, 35, 400, 90],	#5 cima
				 #[35, 320, 0, 0],		#6 parede
				 #[35, 320, 1165, 0],	#7 parede
				 [500, 35, 0, 565],		#8 piso esquerda
				 [500, 35, 700, 565],	#9 piso direita
				 [500, 35, 0, -34], 	#10 teto esq
				 [500, 35, 700, -34],	#11 teto dir
				 ]
 
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			self.platform_list.add(block)



def set_players(player1, player2, level_atual):
	player1.rect.x = 350
	player2.rect.x = 850
	set_player(player1, level_atual)
	set_player(player2, level_atual)

def set_player(player, level_atual):
	player.level = level_atual
	player.rect.y = SCREEN_HEIGHT - (player.rect.height) * 2



def main():
	pygame.init()
	#print(pygame.font.get_fonts())
	myfont = pygame.font.SysFont("monospace", 120)
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("SeMatano")
 	
 	#nasce player
	player1= Player("branco.png",0)
	player2= Player("preto.png",0)
 
	#Adiciona Level,é só tem um, mas dá pra almentar 
	level_list = []
	level_list.append( Level_01(player1,player2) )
 
	#Seta o level
	level_num = 0
	level_atual = level_list[level_num]
	sprite_jogo = pygame.sprite.Group()
	set_players(player1, player2, level_atual)
	sprite_jogo.add(player1)
	sprite_jogo.add(player2)
 
	#Loopa até fechar
	done = False
	clock = pygame.time.Clock()#FPS

	print("WASD para Preto")
	print("SETAS para Branco")
	print("Q para preto renascer, P para Branco")
	print()
	print("ESPAÇO para Novo Jogo")


	# -------- Löop -----------
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#Famoso fechar
				done = True
 
			keys = pygame.key.get_pressed()
			"""for x in range(0,323):
				if keys[x]==1:
					print(x,keys[x])"""

 			#SE MEXE,PORRA

			if keys[303] and keys[275]:
				player1.dash_r()
			if keys[303] and keys[276]:
				player1.dash_l()
			if keys[304] and keys[100]:
				player2.dash_r()
			if keys[304] and keys[97]:
				player2.dash_l()

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
		if player2 in sprite_jogo and player1 in sprite_jogo:
			if (player2.rect.bottom > player1.rect.bottom >= player2.rect.top) and ((player2.rect.right > player1.rect.right-10 > player2.rect.left) or (player2.rect.left < player1.rect.left+10 < player2.rect.right)):
				sprite_jogo.remove(player2)
				player1.pontuacao += 1
				player1.jump()
				sprite_jogo.update()
			if (player1.rect.bottom > player2.rect.bottom >= player1.rect.top) and ((player1.rect.right > player2.rect.right-10 > player1.rect.left) or (player1.rect.left < player2.rect.left+10 < player1.rect.right)):
				sprite_jogo.remove(player1)
				player2.pontuacao += 1
				player2.jump()
				sprite_jogo.update()
		#print("player1: " + str(player1.pontuacao))
		#print("player2: " + str(player2.pontuacao))
		
		#pressione espaço pra começar de novo
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			sprite_jogo.remove(player2)
			sprite_jogo.remove(player1)
			sprite_jogo.update()
			player1= Player("branco.png",0)
			player2= Player("preto.png",0)
			set_players(player1, player2, level_atual)
			sprite_jogo.add(player1)
			sprite_jogo.add(player2)
			sprite_jogo.update()

		#renasce o preto
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q and not player2 in sprite_jogo:
			sprite_jogo.remove(player2)
			sprite_jogo.update()
			player2= Player("preto.png",player2.pontuacao)
			player2.rect.x = 850
			set_player(player2, level_atual)
			sprite_jogo.add(player2)
			sprite_jogo.update()

		#renasce o branco
		if event.type == pygame.KEYDOWN and event.key == pygame.K_p and not player1 in sprite_jogo:
			sprite_jogo.remove(player1)
			sprite_jogo.update()
			player1= Player("branco.png",player1.pontuacao)
			player1.rect.x = 350
			set_player(player1, level_atual)
			sprite_jogo.add(player1)
			sprite_jogo.update()

		if player1.pontuacao>=3 or player2.pontuacao>=3:
			if player1.pontuacao>=3:
				level_atual.draw_black(screen, myfont, "Branco ganhou")
			elif player2.pontuacao>=3:
				level_atual.draw_black(screen, myfont, "O Preto Venceu")
			sprite_jogo.remove(player2)
			sprite_jogo.remove(player1)
			sprite_jogo.update()
		else:
			level_atual.draw(screen)
			sprite_jogo.draw(screen)


		#Tem que dar update pra mexer, maldito
		sprite_jogo.update()
 
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
		

		clock.tick(60)	
 
		#Atualiza a tela
		pygame.display.flip()
	pygame.quit()
 
if __name__ == "__main__":
	main()