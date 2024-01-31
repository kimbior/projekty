import pygame, sys
import os

def bouncing_rect(platform):
    global x_speed, y_speed
    moving_rect.x += x_speed
    moving_rect.y += y_speed

    if moving_rect.right >= screen_width or moving_rect.left <= 0:
        x_speed *= -1
    if moving_rect.bottom >= screen_height or moving_rect.top <=0:
        y_speed *= -1

    collision_tollerance = 10
    if moving_rect.colliderect(platform):
        if abs(platform.top - moving_rect.bottom) < collision_tollerance and y_speed >0:
            y_speed *=-1
            if moving_rect.x+15 >= platform.x and moving_rect.x+15 <= platform.x + (platform_width/3)-40:
                print("lewa")
                print(x_speed)
                if x_speed >= 0:
                    x_speed +=1
                elif x_speed <= 0:
                    x_speed -=1
                print(x_speed)

            if moving_rect.x + 15 >= (platform.x+platform_width/2) +40 and moving_rect.x + 15 <= platform.x + platform_width:
                print("prawa")
                print(x_speed)
                if x_speed >= 0:
                    x_speed -= 1
                elif x_speed <= 0:
                    x_speed += 1
                print(x_speed)

        if abs(platform.bottom - moving_rect.top) < collision_tollerance and y_speed <0:
            y_speed *=-1
        if abs(platform.right - moving_rect.left) < collision_tollerance and x_speed <0:
            x_speed *=-1
        if abs(platform.left - moving_rect.right) < collision_tollerance and x_speed >0:
            x_speed *=-1

    pop = -1
    for _ in range(len(lista_przeszkod)):
        if lista_przeszkod[_] in lista_przeszkod:
            if moving_rect.colliderect(lista_przeszkod[_]):
                if abs(lista_przeszkod[_].top - moving_rect.bottom) < collision_tollerance and y_speed > 0:
                    y_speed *= -1
                    pop = _

                if abs(lista_przeszkod[_].bottom - moving_rect.top) < collision_tollerance and y_speed < 0:
                    y_speed *= -1
                    pop =_

                if abs(lista_przeszkod[_].right - moving_rect.left) < collision_tollerance and x_speed < 0:
                    x_speed *= -1
                    pop = _

                if abs(lista_przeszkod[_].left - moving_rect.right) < collision_tollerance and x_speed > 0:
                    x_speed *= -1
                    pop = _

            pygame.draw.rect(screen, (255, 0, 255), lista_przeszkod[_])
            screen.blit(brick_image, (lista_przeszkod[_].x, lista_przeszkod[_].y))


    if pop > -1:
        lista_przeszkod.pop(pop)

def key_handling(platform,VEL):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_a] and platform.x - VEL >0:  # LEFT
        platform.x -= VEL
    if key_pressed[pygame.K_d] and platform.x + VEL + platform.width < screen_width:   # RIGHT
        platform.x += VEL
    if key_pressed[pygame.K_SPACE]:
        return "start"

def draw_winner(text):

    draw_text = WINNER_FONT.render(text, 1, (255,255,255))
    screen.blit(draw_text, (screen_width/2 - draw_text.get_width() /
                         2, screen_width/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_loser(text):

    draw_text = WINNER_FONT.render(text, 1, (255, 255, 255))
    screen.blit(draw_text, (screen_width / 2 - draw_text.get_width() /
                            2, screen_width / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_assets(platform):
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (255, 255, 255), moving_rect)
    screen.blit(platform_trans,(platform.x,platform.y))
    screen.blit(ball_image, (moving_rect.x, moving_rect.y))

def start_position(platform):
    moving_rect.x = platform.x+60
    moving_rect.y = platform.y-50
    for _ in range(len(lista_przeszkod)):
        pygame.draw.rect(screen, (255, 0, 255), lista_przeszkod[_])

def main():
    platform = pygame.Rect(300,600,platform_width,platform_height)
    switch = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        if len(lista_przeszkod) == 0:
            winner_text = "Wygrales!!"
            draw_winner(winner_text)
            break
        elif moving_rect.bottom >= screen_height :
            winner_text = "Przegrales!!"
            draw_loser(winner_text)
            break


        draw_assets(platform)
        if key_handling(platform,VEL) == "start" or switch == True:
            bouncing_rect(platform)
            switch = True
        else:
            start_position(platform)


        key_handling(platform, VEL)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)




pygame.init()

VEL = 5
clock = pygame.time.Clock()
screen_width,screen_height = 800,800
screen = pygame.display.set_mode((screen_width,screen_height))

platform_width,platform_height = 200,100
platform_image = pygame.image.load(os.path.join('assets','platform.png'))
platform_trans = pygame.transform.scale(platform_image,(platform_width,platform_height))

brick_image = pygame.image.load(os.path.join('assets','brick-image.png'))
brick_image = pygame.transform.scale(brick_image,(100,40))

ball_image = pygame.image.load(os.path.join('assets','ball-image.png'))
ball_image = pygame.transform.scale(ball_image,(30,30))

moving_rect = pygame.Rect(350,350,30,30)
x_speed, y_speed = 5,-5

WINNER_FONT = pygame.font.SysFont('comicsans', 100)



lista_przeszkod = []
i=0
for _ in range(0, 2400, 100):
    lista_przeszkod.append(f'przeszkoda{_}')
    if _ <800:
        lista_przeszkod[i] = pygame.Rect(0 + _, 0, 100, 40)
    elif _ <1600:
        lista_przeszkod[i] = pygame.Rect(_ - 800, 40, 100, 40)
    elif _ <2400:
        lista_przeszkod[i] = pygame.Rect(_ - 1600, 80, 100, 40)
    i+=1

if __name__ == "__main__":
    main()