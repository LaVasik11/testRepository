import pygame as p


clock = p.time.Clock()

p.init()
screen = p.display.set_mode((612, 344))
p.display.set_caption("Симулятор СФа(начало)")
icon = p.image.load('../инструменты/фотокарточки/DotaИконка.png').convert_alpha()
p.display.set_icon(icon)

bg = p.image.load('../инструменты/фотокарточки/МИДдота2.png').convert()

walk_left = p.image.load('../инструменты/фотокарточки/СФ_лево.png')
walk_right = p.image.load('../инструменты/фотокарточки/СФ_право.png')
stand_SF = p.image.load('../инструменты/фотокарточки/СФ_стоит.png')
give_coil_anim = p.image.load('../инструменты/фотокарточки/СФ_руки_вверх.png')

Spirit_Breaker = p.image.load('../инструменты/фотокарточки/Бара.png').convert_alpha()

ghost_list_in_game = []




bg_x = 0
player_speed = 5
player_x = 153
player_y = 150

is_jump = False
jump_count = 8

# bg_sound = p.mixer.Sound('../инструменты/Sound/y2mate.com - Sewerslvt  Lexapro Delirium.mp3')
# bg_sound.play()

ghost_timer = p.USEREVENT + 1
p.time.set_timer(ghost_timer, 7000)


label = p.font.Font('../инструменты/Шрифты/sfns-display-bold.ttf', 40)
lose_label = label.render('Вы проиграли', False, (193, 196, 199))
restart_label = label.render('Играть заново', True, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(170, 200))

continue_label = label.render('Продолжить', False, (255, 255, 255))
pause_label = label.render('Пауза', False, (230, 71, 71))
win_label = label.render('Вы победили!', False, (255, 255, 255))

coil_icon = p.imag
e.load('../инструменты/фотокарточки/imgonline-com-ua-Resize-N7OfOJ17iCHh9XPK.jpg')
coil_count = 10
speed_bara = 10
count_enemies_killed = 0
old_count_enemies_killed = 0
coil = p.image.load('../инструменты/фотокарточки/coil2.png').convert_alpha()
bullets = []
t = 0


win = False
gameplay = True
pause = False

def restart():
    global gameplay, player_x, coil_count, count_enemies_killed, speed_bara, win
    gameplay = True
    player_x = 150
    ghost_list_in_game.clear()
    bullets.clear()
    coil_count = 10
    count_enemies_killed = 0
    speed_bara = 10
    win = False

def draw_text(surface, text, x, y, color, font_size):
    font = p.font.Font(None, font_size)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

raning = True
while raning:
    keys = p.key.get_pressed()
    screen.blit(bg, (bg_x, 0))


    if gameplay and not win and not pause:
        if keys[p.K_ESCAPE]:
            pause = True

        if count_enemies_killed == 5:
            win = True
        draw_text(screen, str(coil_count), 10, 10, (255, 255, 255), 36)
        screen.blit(coil_icon, (40, 5))
        draw_text(screen, str(count_enemies_killed), 550, 10, (255, 255, 255), 36)

        player_rect = walk_left.get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game and count_enemies_killed != old_count_enemies_killed:
            speed_bara += 5
            old_count_enemies_killed = count_enemies_killed

        if ghost_list_in_game:

            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(Spirit_Breaker, el)
                el.x -= speed_bara

                if el.x <= -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False


        if keys[p.K_LEFT] and not is_jump:
            screen.blit(walk_left, (player_x, player_y))
        elif keys[p.K_RIGHT] and not is_jump:
            screen.blit(walk_right, (player_x, player_y))
        elif not keys[p.K_RIGHT] and not keys[p.K_LEFT] and is_jump:
            screen.blit(give_coil_anim, (player_x, player_y))
        elif not is_jump:
            screen.blit(stand_SF, (player_x + 20, player_y))


        if keys[p.K_LEFT] and player_x > 10:
            player_x -= player_speed
        elif keys[p.K_RIGHT] and player_x < 550:
            player_x += player_speed

        if not is_jump:
            if keys[p.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                screen.blit(give_coil_anim, (player_x, player_y))
                if jump_count > 0:
                    player_y -= (jump_count**2)/2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8



        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(coil, (el.x, el.y))
                t += 1

                if t >= 15:
                    t = 0
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
                            count_enemies_killed += 1

    elif pause:
        screen.fill((0, 0, 0))
        screen.blit(pause_label, (230, 80))
        screen.blit(continue_label, restart_label_rect)

        mouse = p.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and p.mouse.get_pressed()[0]:
            pause = False

    elif win:
        screen.fill((4, 255, 0))
        screen.blit(win_label, (170, 80))
        screen.blit(restart_label, restart_label_rect)

        mouse = p.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and p.mouse.get_pressed()[0]:
            restart()


    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (170, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = p.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and p.mouse.get_pressed()[0]:
            restart()

    p.display.update()

    for event in p.event.get():
        if event.type == p.QUIT:
            raning = False
            p.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(Spirit_Breaker.get_rect(topleft=(620, 150)))

        if gameplay and event.type == p.KEYUP and event.key == p.K_z and coil_count > 0:
            bullets.append(coil.get_rect(topleft=(player_x + 80, player_y)))
            coil_count -= 1
            coil_track = True
        if gameplay and event.type == p.KEYUP and event.key == p.K_x and coil_count > 0:
            bullets.append(coil.get_rect(topleft=(player_x + 160, player_y)))
            coil_count -= 1
            coil_track = True
        if gameplay and event.type == p.KEYUP and event.key == p.K_c and coil_count > 0:
            bullets.append(coil.get_rect(topleft=(player_x + 240, player_y)))
            coil_count -= 1
            coil_track = True


    clock.tick(25)