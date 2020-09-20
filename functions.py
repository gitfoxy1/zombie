import pygame

def exit_game(event):
    """" Вйти из игры если нажат знак QUIT или кнопка ESCAPE """
    # по умолчанию игра продолжается
    exit_ = False

    # выход если нажат знак QUIT
    if event.type == pygame.QUIT:
        exit_ = True

    # выход если нажата кнопка ESCAPE
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
            exit_ = True

    return exit_


def get_active_hero_id(heroes, hero, hero_id):
    if hero.actions == 0:
        hero.actions = hero.actions_max  # сброс счётчика действий
        hero_id += 1  # активным становится следующий герой
        if hero_id >= len(heroes):  # после последнего героя активным становится первый герой
            hero_id = 0
    return hero_id


def run_turn(map, heroes, character_id, event, keyboard_mode, screen, backpack, charecters):
    """" Обработка хода героя,
        если у героя закончились действия, тогда ход переходит к следующему герою.
        'character_id' - индекс героя """

    hero_ = heroes[character_id]
    while True:
        # управление на карте
        if keyboard_mode == 'map':
            # переключаем управление на рюкзак
            if event.key == pygame.K_i:
                keyboard_mode = 'backpack'
                backpack.clear_item_id()
                break
            # атакуем
            elif event.key == pygame.K_a:
                keyboard_mode = 'attack'
            # Передвижение персонажа по карте
            elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                hero_.move(event, map)
            # герой поднемает вещь на карте
            elif event.key == pygame.K_e:
                hero_.pick_up_item(map)
            elif event.key == pygame.K_d:
                hero_.drop_down_item(map)

        # управление в рюкзаке
        elif keyboard_mode == 'backpack':
            # переключаем управление на карту
            if event.key in [pygame.K_ESCAPE, pygame.K_i]:
                keyboard_mode = 'map'
                break

            # выбираем вещь в рюкзаке
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                backpack.select_item(event, hero_)
            elif event.key == pygame.K_e:
                hero_.get_item_to_hands(backpack)

        elif keyboard_mode == 'attack':
            if event.key in [pygame.K_ESCAPE, pygame.K_a]:
                keyboard_mode = 'map'
            elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                character_id = hero_.attack(event, map, charecters)

        break

    character_id = get_active_hero_id(heroes, hero_, character_id)  # у героя закончились ходы, ход переходит к следующему герою
    return character_id, keyboard_mode
