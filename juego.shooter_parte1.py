import pygame, random

#definimos ancho y largo, definimos tambien colores
width=700
height=420
black=(0,0,0)
white=(255,255,255)
green=(0,255,0)

#definimos funciones de inicializacion

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Shooter")
clock=pygame.time.Clock()



#Con esta funcion podemos dibujar un texto como ser el puntajen del juego

def draw_text(surface,text,size,x,y):
	font=pygame.font.SysFont("serif",size)
	text_surface=font.render(text,True,white)
	text_rect=text_surface.get_rect()
	text_rect.midtop=(x,y)
	surface.blit(text_surface,text_rect)


#definimos el escudo:

def draw_escudo_bar(surface,x,y,porcentage):
	bar_lenght=100
	bar_height=10
	fill=(porcentage/100)*bar_lenght
	border=pygame.Rect(x,y,bar_lenght,bar_height)
	fill=pygame.Rect(x,y,fill,bar_height)
	pygame.draw.rect(surface,green,fill)
	pygame.draw.rect(surface,white,border,2)


#Con esta clase le damos forma al Jugador

class jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load("nave_espacial2.jpg").convert()
		#self.image.set_colorkey(white)
		self.rect=self.image.get_rect()
		self.rect.centerx=width//2
		self.rect.bottom=height-10
		self.speed_x=0
		self.escudo=100

	def update(self):
		self.speed_x=0
		keystate=pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x=-5
		if keystate[pygame.K_RIGHT]:
			self.speed_x=5
		self.rect.x+=self.speed_x
		if self.rect.right>width:
			self.rect.right=width
		if self.rect.left<0:
			self.rect.left=0

	def shoot(self):#para los disparos
		bullet=Bullet(self.rect.centerx,self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		#laser_sound.play()

#Con esta clase creamos los disparos de la nava

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		super().__init__()
		self.image=pygame.image.load("laser1.jpg")
		#self.image.set_colorkey()
		self.rect=self.image.get_rect()
		self.rect.y=y
		self.rect.centerx=x
		self.speedy= -10

	def update(self):
		self.rect.y+=self.speedy
		if self.rect.bottom<0:
			self.kill()#Con este metodo eliminamos todas las intancias  de cualquier lista

#Con esta clase podemos darle forma a los meteoritos del juego:

class meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=random.choice(meteoros_imagenes)
		self.image.set_colorkey(black)
		self.image.set_colorkey(white)
		self.rect=self.image.get_rect()
		self.rect.x=random.randrange(width-self.rect.width)
		self.rect.y=random.randrange(-140,-100)
		self.speedy=random.randrange(1,10)
		self.speedx=random.randrange(-5,5)


	def update(self):
		self.rect.y+=self.speedy
		self.rect.x+=self.speedx
		if self.rect.top>height +10 or self.rect.left<-40 or self.rect.right>width+25:
			self.rect.x=random.randrange(width-self.rect.width)
			self.rect.y=random.randrange(-100,-40)
			self.speedy=random.randrange(1,10)

class Explosion(pygame.sprite.Sprite):
	def __init__(self,center):
		super().__init__()
		self.image=explosion_animacion[0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.last_update=pygame.time.get_ticks()
		self.frame_rate=50#velocidad de la explosion

	def update(self):
		now=pygame.time.get_ticks()
		if now - self.last_update>self.frame_rate:
			self.last_update=now
			self.frame+=1
			if self.frame==len(explosion_animacion):
				self.kill()
			else:
				center=self.rect.center
				self.image=explosion_animacion[self.frame]
				self.rect=self.image.get_rect()
				self.rect.center=center


#Cargar imagen de fondo

background=pygame.image.load("fondo2.jpg").convert()

#Cargamos los sonidos del Juego:

#laser_sound=pygame.mixer.Sound("laser5.ogg")
#explosion=pygame.mixer.Sound("explosion.wav")
#pygame.mixer.music.load("music.ogg")
#pygame.mixer.music.set_volume(0.2)

#Creamos una funcion de game_over y la mostramos por pantalla

def show_go_screen():
	screen.blit(background, [0,0])
	draw_text(screen, "Shooter", 65, width//2, height//4)
	draw_text(screen,"Las instrucciones van aqui", 27, width//2,height//2)
	draw_text(screen," Press key",20, width//2, height*3/4)
	pygame.display.flip()
	esperando=True
	while esperando:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
			if event.type==pygame.KEYUP:
				esperando=False


#Creamos una lista para almacenar los meteoros y que aparezcan aleatoriamente

meteoros_imagenes=[]
meteoros_lista=["meteorito2.jpg","meteor1.jpg","meteor2.jpg","meteor3.jpg","meteor4.jpg","meteor5.jpg"]

for img in meteoros_lista:
	meteoros_imagenes.append(pygame.image.load(img).convert())

#####________----------------Explosiones###________________

explosion_animacion=[]

for i in range(9):
	file="imagenes/Explosion{}.jpg".format(i)
	img=pygame.image.load(file).convert()
	img.set_colorkey(black)
	img_scala=pygame.transform.scale(img,(70,70))
	explosion_animacion.append(img_scala)


#aca hacemos que el sonido del juego se genere infinitamente:

#pygame.mixer.music.play(loops=-1)

#Variable para ser utilizada en el while infinito, o bucle principal
game_over=True
running=True

#Bluque Principal del Juego:

while running:
	if game_over:


		show_go_screen()

		game_over=False
		all_sprites=pygame.sprite.Group()#Todos los sprites en grupos diferentes
		meteo_lista=pygame.sprite.Group()	
		bullets=pygame.sprite.Group()
		Jugador=jugador()
		all_sprites.add(Jugador)
		for i in range(8):# For utilizado para lograr que aparezcan los  meteoritos desde muchas direcciones
			meteoro=meteor()
			all_sprites.add(meteoro)
			meteo_lista.add(meteoro)
		puntaje=0#Variable puntaje:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False

		elif event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE:
				Jugador.shoot()


	all_sprites.update()

	#Coliciones meteoros-laser

	hits=pygame.sprite.groupcollide(meteo_lista,bullets,True,True)

	for hit in hits:
		puntaje+=10
		#explosion.play()
		explosion=Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteoro=meteor()
		all_sprites.add(meteoro)
		meteo_lista.add(meteoro)

	#Ver las coliciones jugador-meteoros

	hits=pygame.sprite.spritecollide(Jugador,meteo_lista,True)
	for hit in hits:
		Jugador.escudo -= 25#cada vez que me pegue un meteoro disminuira mi escudo de 100
		meteoro=meteor()
		all_sprites.add(meteoro)
		meteo_lista.add(meteoro)
		if Jugador.escudo<=0:
			game_over=True


	#Draw / rander:

	#Aplicamos el fondo de la pantalla al juego:

	screen.blit(background,[0,0])
	
	#screen.fill(black)

	all_sprites.draw(screen)

	#marcador del juego

	draw_text(screen,str(puntaje),25,width//2,10)

	#Escudo:

	draw_escudo_bar(screen,5,5, Jugador.escudo)

	pygame.display.flip()

pygame.quit()
