import pygame
import random
import time

pygame.init()

#print text to screen
class Text:
    def __init__(self,text,size,color,x,y):
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        font = pygame.font.Font(None, self.size)
        txt = font.render(self.text, 1, self.color)
        text_rect = txt.get_rect(center = (self.x, self.y))
        game_display.blit(txt, text_rect)
        
#enemy size
large = 30
medium = 20
small = 10
size = [large, medium, small]

#   difficult[  large,  medium, small   ] ->  easy[40,30,20]    ,   normal[30,20,10]    ,   hard[20,10,5]
enemy_size = None

#screen size
frame_x = 1080
frame_y = 800
half_x = frame_x/2
half_y = frame_y/2

#colors
red = 50
green = 100
blue = 100
white = (250,250,250)

#screens
menu = True
game = False
gameover = False

#create frame
game_display = pygame.display.set_mode((frame_x,frame_y))
pygame.display.set_caption("game")
fps_controller = pygame.time.Clock() #fps controller

#crosshair
ch_pos = [frame_x/2,frame_y/2]
crosshair = pygame.image.load("crosshair.png")
crosshair_width = 10 
crosshair_height = 10

#enemy
enemy_spawn = True
enemies = []
enemy_amount = 3 #amount of enemies

score = 0

def spawn_enemy():
    global enemy_spawn, enemy_size, red
    if enemy_spawn:
        for _ in range(enemy_amount): #amount of enemies
            if len(enemies)<enemy_amount:
                enemy_size = random.choice(size) #random enemy size
                enemy_x = random.randrange(1, frame_x - enemy_size)    #random enemy x position
                enemy_y = random.randrange(1, frame_y - enemy_size)   #random enemy y position
                enemies.append([enemy_x,enemy_y, enemy_size, time.time(), [red,green,blue]])    #include enemy into list
        enemy_spawn = False

def explode_enemy(enemy):
    global score, enemy_amount
    enemies.remove(enemy) #remove exploded enemy
    score -= 1
    enemy_amount -= 1 #decrease amount of enemies

#control
def control():
    global score, enemy_spawn, enemy_size, enemy_amount, menu, size, game, gameover
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit event
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:    #KEY EVENTS
            if event.key == pygame.K_ESCAPE: #press esc to quit
                pygame.quit()
                quit()
            if menu:    #menu screen options:   difficult and enemy amount
                if event.key == ord('e'):
                    size = [x + 10 for x in size]
                    menu = 0
                    game = 1
                elif event.key == ord('n'):
                    menu = 0
                    game = 1
                elif event.key == ord('h'):
                    size = [x-5 for x in size]
                    menu = 0
                    game = 1
                if event.key == pygame.K_1: #decide how many enemies will be
                    enemy_amount = 1
                elif event.key == pygame.K_2:
                    enemy_amount = 2
                elif event.key == pygame.K_3:
                    enemy_amount = 3
                elif event.key == pygame.K_4:
                    enemy_amount = 4
                elif event.key == pygame.K_5:
                    enemy_amount = 5
                elif event.key == pygame.K_6:
                    enemy_amount = 6
                elif event.key == pygame.K_7:
                    enemy_amount = 7

        #enemy select
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()   
            mouse_rect = pygame.Rect(mouse_x,mouse_y,1,1)
            for pos in list(enemies):
                enemy_rect = pygame.Rect(pos[0],pos[1], pos[2],pos[2])
                if mouse_rect.colliderect(enemy_rect):  #hit an enemy event
                    if pos[2] == large: #killing large enemies gives 1 score
                        score += 1
                    elif pos[2] == medium:  #killing medium enemies gives 2 score
                        score += 2
                    elif pos[2] == small:   #killing small enemies gives 3 score
                        score += 3
                    enemies.remove(pos) #remove killed enemy
                    enemy_spawn = True  #spawn new enemy

def show_score():
    global score
    font = pygame.font.Font(None ,50)
    score_text = font.render(f"Score:    {score}", 1, (220,200,200))
    text_rect = score_text.get_rect(center = (frame_x/2, frame_y/2+90))
    game_display.blit(score_text, text_rect)

#home screen
while menu:
    control()
    game_display.fill((0,0,0))
    menu_font = Text("GGGGAME",100,(50,180,250),half_x,half_y/2)    #name of the game
    select_difficult = Text("(E) EASY",30,white,half_x,half_y*0.85) #easy
    select_difficult = Text("(N) NORMAL",30,white,half_x,half_y)    #normal
    select_difficult = Text("(H) HARD",30,white,half_x,half_y*1.15) #hard
    enemy_amount_font = Text("press a number to select how many enemies will be. (1-7)", 30, (180,180,180), half_x, half_y*1.75)
    enemy_am = Text(f"{enemy_amount} enemies",30,(180,180,180),half_x,half_y*1.82)    #enemy amount
    pygame.display.update()

#main loop
print("game started")
while game:
    control()
    pygame.mouse.set_visible(False)
    ch_pos = pygame.mouse.get_pos()
    explosion_time = enemy_amount + 0.5
    t = (28 - 3*enemy_amount)/20 #enemies' color change speed

    game_display.fill((0,0,0))
    font = pygame.font.Font(None,30)
    score_txt = font.render(f"score: {score}",1,(120,120,120))
    text_rect = score_txt.get_rect(center = (frame_x/2,75))
    game_display.blit(score_txt, text_rect)

    spawn_enemy()
    for e in enemies:   #draw enemies
        pygame.draw.rect(game_display, e[4], pygame.Rect(e[0], e[1], e[2],e[2]))

    for enemy in enemies:   #enemy color generator
        if enemy[4][0] < 250:
            enemy[4][0] += t
            
        if enemy[4][1]  > 1:
            enemy[4][1] -= t/2

        if  enemy[4][2] > 1:
            enemy[4][2] -= t

    current_time = time.time()
    for e in list(enemies): #   exploding enemy 
        if current_time - e[3] >= explosion_time:
            explode_enemy(e)
    
    if enemy_amount == 0:   #game over
        gameover = 1
        game = 0

    game_display.blit(crosshair, (ch_pos[0] - crosshair_width / 1.6 , ch_pos[1] - crosshair_height / 1.6))  #   draw crosshair
    fps_controller.tick(60) #fps
    pygame.display.update()

#game over screen
print(f"score:  {score}")
while gameover:
    control()
    pygame.mouse.set_visible(1) #set mouse to visible
    game_display.fill((0,0,0))
    font = pygame.font.Font(None ,90)
    game_over_text = font.render("GAME OVER", 1, (255,0,0))
    text_rect = game_over_text.get_rect(center = (frame_x/2, frame_y/2))
    game_display.blit(game_over_text, text_rect)
    show_score()
    pygame.display.update()