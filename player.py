import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self,cor):
		super().__init__()

		width = 35
		height = 35
		self.image = pygame.image.load(cor)
		self.rect = self.image.get_rect()
		self.double = 0
		self.pontuacao = 0
		self.name = cor.split(".")[0]
 
 		#Ele pede
		self.change_x = 0
		self.change_y = 0
 
	def update(self): ###ESSSSSSSSEEEEEEEEEEEEEEEEEEE AQUI
			
		self.calc_grav()
 
		# dir/esq
		self.rect.x += self.change_x
 
		# Colisão lateral
		# spritecollide(sprite, group, dokill, collided = None)
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list,False)
		for block in block_hit_list:
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				self.rect.left = block.rect.right
 
		# Cima/baixo
		self.rect.y += self.change_y
 
		# Check
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom
			#Pra quando bate a cabeça
			self.change_y = 0

		#all_sprites_list = pygame.sprite.Group()

		#if pygame.sprite.spritecollideany(player1,player2) != None:
		#	print('collision')
		#	return True
		#return False

	def calc_grav(self):
		if self.change_y == 0: #se não sobe é 1
			self.change_y = 1
		else:
			self.change_y += .35
 
	def jump(self):
		# ele vai pra baixo pra conferir se tem plataforma em baixo
		self.rect.y += 2
		tem_plataforma = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 2
		if len(tem_plataforma) == True:
			self.double = 0
 
		if len(tem_plataforma)==True or self.double == 1:
			self.change_y = -10
			self.double += 1
 
	# movimento
	dire=0
	def go_left(self):
		self.change_x = -6
		dire=1
		if self.dire==0:
			self.image = pygame.transform.flip(self.image,True,False)
			self.dire=1

	def go_right(self):
		self.change_x = 6
		dire=0
		if self.dire==1:
			self.image = pygame.transform.flip(self.image,True,False)
			self.dire=0

	def stop(self):
		self.change_x = 0

	def dash_l(self):
		self.change_x = -12

	def dash_r(self):
		self.change_x = 12

	#def shoot(self):