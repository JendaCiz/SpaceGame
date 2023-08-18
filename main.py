import pygame
import random

def draw_background():
    # Zde se vykreslí dvě kopie pozadí vedle sebe
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos + 1024, 0)) ## Druhe pozadi

def position():
    alien_img_rect.x = width + alien_behind_border
    alien_img_rect.y = random.randint(60, height-48)

pygame.init()
floor_x_pos = 0  ###### Pozice pro zem #######


#obrazovka
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch 'em all")


### NASTAVENI HRY  ####
player_start_lives = 5        ## Menime v prubehu hry     
player_speed = 5               ## Nemenime                
alien_speed = 5                  ## Menime                  
alien_speed_acceleration = 0.0009   ## Nemenime               
alien_behind_border = 100         ## Nemenime                
score = 0                       ## Menime                                                                
player_lives = player_start_lives ## Menime                 
alien_current_speed = alien_speed 
bg_x_pos = 0                             


#FPS a hodiny 
fps = 60
clock = pygame.time.Clock()

#Barvy
dark_yellow = pygame.Color("#d9aa2d")
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Fonty
space_font_big = pygame.font.Font("fonts/font1.ttf", 30)
space_font_middle = pygame.font.Font("fonts/font1.ttf", 30)

#Text
game_name = space_font_big.render("Defences of Planet Earth", True, dark_yellow)
game_name_rect = game_name.get_rect()
game_name_rect.center = (width//2, 30)



lives_text = space_font_middle.render(f"Lives : {player_lives}", True, dark_yellow)
lives_text_rect = lives_text.get_rect()
lives_text_rect.center = (width -70, 30)

game_over_text = space_font_big.render("Game Over", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width//2, height//2)

continue_text = space_font_middle.render("Play Again = Press Any Button", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 40)



# Tvary
pygame.draw.line(screen, dark_yellow, (0, 60), (width, 60), 2)

#Zvuky a muzika v pozadi
pygame.mixer.music.load("media/background%music.mp3.")
pygame.mixer.music.play(-1)
lose_life_sound = pygame.mixer.Sound("media/lose.wav")
lose_life_sound.set_volume(1.2)
take_alien_sound = pygame.mixer.Sound("media/level_up.wav")
take_alien_sound.set_volume(0.9)




#Obrazky
bg_surface = pygame.image.load("img/02.jpg").convert()


ship_img = pygame.image.load("img/space_ship3.png")
ship_img_rect = ship_img.get_rect()
ship_img_rect.center = (200, height//2)

alien_img = pygame.image.load("img/alien4.png")
alien_img_rect = alien_img.get_rect()
alien_img_rect.x = width + alien_behind_border
alien_img_rect.y = random.randint(60, height - 48)


earth_img = pygame.image.load("img/earth1.png")
earth_img_rect = earth_img.get_rect()
earth_img_rect.center = (-50, height -220)



#Hlavni cyklus
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False


    # Pohyb
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and ship_img_rect.top > 60:
        ship_img_rect.y -= player_speed
    elif(keys[pygame.K_DOWN] or keys[pygame.K_s]) and ship_img_rect.bottom < height:
        ship_img_rect.y += player_speed


    # Pohyb aliena
    if alien_img_rect.x < 0:
        player_lives -= 1
        position()
        lose_life_sound.play()
    else:
        # alien se pohybuje do leva
        alien_img_rect.x -= alien_current_speed

    # Kontrola kolize
    if ship_img_rect.colliderect(alien_img_rect):
        score += 1
        alien_current_speed += alien_speed_acceleration
        position()
        take_alien_sound.play()
    else:
        alien_current_speed += alien_speed_acceleration


    #if score == 5:
        #alien_speed += alien_speed_acceleration
    #elif score > 5 and score <= 10:
        #alien_speed += alien_speed_acceleration
    #elif score > 10:
        #alien_speed += alien_speed_acceleration



    lives_text = space_font_middle.render(f"Lives : {player_lives}", True, dark_yellow)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.center = (width -70, 30)

    scoree_text = space_font_middle.render(f"Score : {score}", True, dark_yellow)
    score_text_rect = scoree_text.get_rect()
    score_text_rect.left = 15
    score_text_rect.top = 17

    

    screen.blit(bg_surface, (0, 0))
    
    # Pohyb pozadí - snížení hodnoty x pozice, aby se zdálo, že se pozadí pohybuje doleva
    bg_x_pos -= 1
    # Vykreslení pozadí
    draw_background()
     # Pokud první kopie pozadí "odjede" zleva, vrátím ji zpět na pravou stranu
    if bg_x_pos <= -1024:
        bg_x_pos = 0


    screen.blit(game_name, game_name_rect)
    screen.blit(scoree_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    screen.blit(ship_img, ship_img_rect)
    screen.blit(alien_img, alien_img_rect)
    screen.blit(earth_img, earth_img_rect)


    # Kontrola konce hry
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer_music.stop()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_start_lives
                    alien_current_speed = alien_speed
                    ship_img_rect.y = height//2
                    pause =False
                    pygame.mixer_music.play(-1, 0.0)

                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False



    
    pygame.display.update()
    
    clock.tick(fps)
pygame.quit()


