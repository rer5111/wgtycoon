import pygame
import sys
import math
import random
import pickle
from stats import citizens, tiles, costs, inflation, upgrades, description_boxes

try:
    open("Save_file.txt", "r")
    new_file = False
except:
    open("Save_file.txt", "x")
    new_file = True
# Loading save data, unless not present
if new_file:
    matrix = [[3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [3, 0, 0, 0, 0, 0, 1, 1, 1, 1],
              [3, 0, 0, 0, 0, 0, 1, 2, 2, 1],
              [3, 0, 0, 0, 0, 0, 1, 1, 1, 1],
              [3, 3, 0, 0, 0, 0, 0, 0, 1, 1],
              [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
              [3, 3, 0, 0, 0, 0, 0, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 0, 0, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 0, 0, 0, 0]]
    Citizens = 1
    Diamonds = 5
    HouseMultiplier = 1
    HousesBought = 0
    GeneratorMultiplier = 1
    GeneratorsBought = 0
    MinesMultiplier = 1
    MinesBought = 0
    MhousesMultiplier = 1
    MhousesBought = 0
else:
    old_data = open("Save_file.txt", "r")
    old_data = old_data.readlines()
    matrix = []
    data4 = []
    data1 = old_data[1].replace("\n", "")
    data1 = data1.split("|")
    for data2 in data1:
        data2_int = []
        data2 = str(data2)
        data2 = data2.split(",")
        for data3 in data2:
            data2_int.append(round(float(data3),2))
        matrix.append(data2_int)
    Citizens = int(old_data[2])
    Diamonds = int(old_data[3])
    HouseMultiplier = int(old_data[4])
    HousesBought = int(old_data[5])
    GeneratorMultiplier = int(old_data[6])
    GeneratorsBought = int(old_data[7])
    MinesMultiplier = int(old_data[8])
    MinesBought = int(old_data[9])
    MhousesMultiplier = int(old_data[10])
    MhousesBought = int(old_data[11])

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.set_endevent(pygame.USEREVENT)
# window and other baseline stuff
screen = pygame.display.set_mode((1200, 1000), pygame.SRCALPHA)
UI = pygame.Surface((1200, 1000), pygame.SRCALPHA)
icon = pygame.image.load("sprites/icon.png").convert()
pygame.display.set_caption("Watergrad tycoon")
pygame.display.set_icon(icon)
running = True
clock = pygame.time.Clock()
pygame.mixer.music.load("main_song.mp3")
Menu0 = pygame.image.load("sprites/Buy_panel.png").convert()
Menu1 = pygame.image.load("sprites/Upgrade_panel.png").convert()
Grass = pygame.image.load("sprites/0Grass.png").convert()
Stone = pygame.image.load("sprites/1Stone.png").convert()
Mountain = pygame.image.load("sprites/2Mountain.png").convert()
Water = pygame.image.load("sprites/3Water.png").convert()
GHouse1 = pygame.image.load("sprites/4GHouse.png").convert()
GHouse2 = pygame.image.load("sprites/4GHouse2.png").convert()
SHouse1 = pygame.image.load("sprites/4SHouse.png").convert()
SHouse2 = pygame.image.load("sprites/4SHouse2.png").convert()
GGenerator1 = pygame.image.load("sprites/5GGenerator.png").convert()
GGenerator2 = pygame.image.load("sprites/5GGenerator2.png").convert()
SGenerator1 = pygame.image.load("sprites/5SGenerator.png").convert()
SGenerator2 = pygame.image.load("sprites/5SGenerator2.png").convert()
SMineshaft1 = pygame.image.load("sprites/6SMineshaft.png").convert()
SMineshaft2 = pygame.image.load("sprites/6SMineshaft2.png").convert()
MMineshaft1 = pygame.image.load("sprites/6MMineshaft.png").convert()
MMineshaft2 = pygame.image.load("sprites/6MMineshaft2.png").convert()
GMhouse1 = pygame.image.load("sprites/7GMhouse.png").convert()
GMhouse2 = pygame.image.load("sprites/7GMhouse2.png").convert()
SMhouse1 = pygame.image.load("sprites/7SMhouse.png").convert()
SMhouse2 = pygame.image.load("sprites/7SMhouse2.png").convert()


game_timer = 0
Panel_state = True
build_mode = False
music_ended = True
selected_building = 0
sell_timer = 0

# no variable making past this point
number_names = {
    0: "",
    1: "K",
    2: "M",
    3: "T",
    4: "Qd",
    5: "Qn",
}


Bought_amount = {
    4.1: HousesBought,
    5.1: GeneratorsBought,
    6.1: MinesBought,
    7.1: MhousesBought
}

Multiplier_amount = {
    4.1: HouseMultiplier,
    5.1: GeneratorMultiplier,
    6.1: MinesMultiplier,
    7.1: MhousesMultiplier
}


def text_draw(surface, text, font, text_clr, text_pos, centered):
    img = font.render(f"{text}", True, text_clr)
    if not centered:
        surface.blit(img, text_pos)
    else:
        surface.blit(img, img.get_rect(center=text_pos))


def diamond_format(number):
    power = 0
    while len("{:.1f}".format(number)) > 5:
        number /= 1000
        power += 1
    if "{:.1f}".format(number)[-1] != "0" and len("{:.1f}".format(number)) <= 3:
        number = "{:.1f}".format(number)
    else:
        number = int(number)
    return f"{number}{number_names.get(power)}"


def create_ui(coordinates_topleft, coordinates_bottomright, colour1, colour2):  # the legendary square creator
    x, y = coordinates_topleft
    x2, y2 = coordinates_bottomright
    pygame.draw.rect(UI, colour2, pygame.Rect(x, y, abs(x2 - x), abs(y2 - y)))
    pygame.draw.rect(UI, colour1, pygame.Rect(x+5, y+5, abs(x2-x-10), abs(y2-y-10)))


def place_building(tile, building):
    global Citizens, Diamonds, HousesBought, HouseMultiplier, GeneratorsBought, GeneratorMultiplier, MinesBought, \
        MinesMultiplier, MhousesBought, MhousesMultiplier
    tileY, tileX = tile
    if matrix[tileX][tileY] < 4 and matrix[tileX][tileY] in tiles.get(building):
        if building == 4.1 and Diamonds - (costs.get(building)+inflation.get(selected_building)*HousesBought) >= 0:  # house code
            matrix[tileX][tileY] = round(building + (matrix[tileX][tileY]) / 100 + 0.01, 2)
            Citizens += citizens.get(building)*HouseMultiplier
            Diamonds -= costs.get(building)+inflation.get(building)*HousesBought
            HousesBought += 1
        elif building == 5.1 and Citizens + citizens.get(building)*GeneratorMultiplier >= 0 and Diamonds - (costs.get(building)+inflation.get(building)*GeneratorsBought) >= 0:  # Generator code
            matrix[tileX][tileY] = round(building + (matrix[tileX][tileY]) / 100 + 0.01, 2)
            Citizens += citizens.get(building)*GeneratorMultiplier
            Diamonds -= costs.get(building)+inflation.get(building)*GeneratorsBought
            GeneratorsBought += 1
        elif building == 6.1 and Citizens + citizens.get(building)*MinesMultiplier >= 0 and Diamonds - (costs.get(building)+inflation.get(building)*MinesBought) >= 0:  # Mines code
            matrix[tileX][tileY] = round(building + (matrix[tileX][tileY]) / 100 + 0.01, 2)
            Citizens += citizens.get(building)*MinesMultiplier
            Diamonds -= costs.get(building)+inflation.get(building)*MinesBought
            MinesBought += 1
        elif building == 7.1 and Diamonds - (costs.get(building)+inflation.get(selected_building)*MhousesBought) >= 0:  # Mhouse code
            matrix[tileX][tileY] = round(building + (matrix[tileX][tileY]) / 100 + 0.01, 2)
            Citizens += citizens.get(building)*MhousesMultiplier
            Diamonds -= costs.get(building)+inflation.get(building)*MhousesBought
            MhousesBought += 1


def sell_building(tile):
    global Citizens, Diamonds, HousesBought, HouseMultiplier, GeneratorsBought, GeneratorMultiplier, MinesBought, \
        MinesMultiplier, MhousesBought, MhousesMultiplier
    tileY, tileX = tile
    building_del = round(int(matrix[tileY][tileX])+0.1, 1)
    if matrix[tileY][tileX] > 4:
        if building_del == 4.1 and Citizens - (citizens.get(building_del)*HouseMultiplier) >= 0:
            Diamonds += costs.get(building_del)+(inflation.get(building_del)*(HousesBought-1))
            Citizens -= (citizens.get(building_del)*HouseMultiplier)
            HousesBought -= 1
            matrix[tileY][tileX] = round(((matrix[tileY][tileX] - round(matrix[tileY][tileX], 1))*100)-1)
        if building_del == 5.1:
            Diamonds += costs.get(building_del) + (inflation.get(building_del) * (GeneratorsBought - 1))
            Citizens -= (citizens.get(building_del) * GeneratorMultiplier)
            GeneratorsBought -= 1
            matrix[tileY][tileX] = round(((matrix[tileY][tileX] - round(matrix[tileY][tileX], 1)) * 100) - 1)
        if building_del == 6.1:
            Diamonds += costs.get(building_del) + (inflation.get(building_del) * (MinesBought - 1))
            Citizens -= (citizens.get(building_del) * MinesMultiplier)
            MinesBought -= 1
            matrix[tileY][tileX] = round(((matrix[tileY][tileX] - round(matrix[tileY][tileX], 1)) * 100) - 1)
        if building_del == 7.1 and Citizens - (citizens.get(building_del)*MhousesMultiplier) >= 0:
            Diamonds += costs.get(building_del)+(inflation.get(building_del)*(MhousesBought-1))
            Citizens -= (citizens.get(building_del)*MhousesMultiplier)
            MhousesBought -= 1
            matrix[tileY][tileX] = round(((matrix[tileY][tileX] - round(matrix[tileY][tileX], 1))*100)-1)


while running:
    screen.fill((255, 0, 0))
    UI.fill((0, 0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Closing code
            running = False

        if event.type == pygame.USEREVENT:
            music_ended = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # god had no place in the creation of this code
            x_pressed, y_pressed = pygame.mouse.get_pos()
            if x_pressed < 1000 and build_mode and selected_building > 4:
                place_building((x_pressed//100, y_pressed//100), selected_building)
            if x_pressed > 1000 and 960 > y_pressed > 110 and Panel_state:
                selected_building = (y_pressed - 109)//50 + 4.1
                build_mode = True
            elif 1100 > x_pressed > 1000 and 110 > y_pressed > 60:
                Panel_state = True
            elif 110 > y_pressed > 60 and x_pressed > 1100:
                Panel_state = False
            elif x_pressed > 1000 and 960 > y_pressed > 110 and not Panel_state:
                selected_building = (y_pressed - 109) // 50 + 4.1
                if selected_building == 4.1 and Diamonds - math.floor(upgrades.get(selected_building)*(1.75**(HouseMultiplier-1))) >= 0:
                    Diamonds -= math.floor(upgrades.get(selected_building)*(1.75**(HouseMultiplier-1)))
                    Citizens += HousesBought * citizens.get(selected_building)
                    HouseMultiplier += 1
                if selected_building == 5.1 and Diamonds - math.floor(upgrades.get(selected_building)*(1.75**(GeneratorMultiplier-1)))>= 0 and Citizens + citizens.get(selected_building) * GeneratorsBought >= 0:
                    Diamonds -= math.floor(upgrades.get(selected_building)*(1.75**(GeneratorMultiplier-1)))
                    Citizens += citizens.get(selected_building) * GeneratorsBought
                    GeneratorMultiplier += 1
                if selected_building == 6.1 and Diamonds - math.floor(upgrades.get(selected_building)*(1.75**(MinesMultiplier-1)))>= 0 and Citizens + citizens.get(selected_building) * MinesBought >= 0:
                    Diamonds -= math.floor(upgrades.get(selected_building)*(1.75**(MinesMultiplier-1)))
                    Citizens += citizens.get(selected_building) * MinesBought
                    MinesMultiplier += 1
                if selected_building == 7.1 and Diamonds - math.floor(upgrades.get(selected_building)*(1.75**(MhousesMultiplier-1))) >= 0:
                    Diamonds -= math.floor(upgrades.get(selected_building)*(1.75**(MhousesMultiplier-1)))
                    Citizens += MhousesBought * citizens.get(selected_building)
                    MhousesMultiplier += 1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x_pressed, y_pressed = pygame.mouse.get_pos()
            if build_mode:
                selected_building = 0
                build_mode = False
            elif x_pressed < 1000 and matrix[y_pressed // 100][x_pressed // 100] > 4:
                if sell_timer >= 0:
                    sell_building((y_pressed//100, x_pressed//100))
                sell_timer = 60

    XMouse, YMouse = pygame.mouse.get_pos()
    if XMouse > 1000 and 960 > YMouse > 110:
        Building_commented = (YMouse - 109)//50 + 4.1
        NameDescribed = description_boxes.get(Building_commented).get("Name")
        DescriptionDescribed = description_boxes.get(Building_commented).get("Description")
        SizeDescribed = description_boxes.get(Building_commented).get("Size")
        Alt_Size = (0, 0)
        if YMouse+SizeDescribed[1] > 1000:
            Alt_Size = (SizeDescribed[0], -SizeDescribed[1])
            print(SizeDescribed)
        create_ui((XMouse-SizeDescribed[0], YMouse+Alt_Size[1]), (XMouse, YMouse+SizeDescribed[1]+Alt_Size[1]), (195, 195, 195, 255), (0, 0, 0, 255))
        text_draw(UI, NameDescribed, pygame.sysfont.SysFont("FixedSys", 35), (0, 0, 0), (XMouse - SizeDescribed[0]/2, YMouse + 20 + Alt_Size[1]), True)
        DescriptionLines = DescriptionDescribed.split("N")
        for n, i in enumerate(DescriptionLines):
            text_draw(UI, i, pygame.sysfont.SysFont("FixedSys", 25), (0, 0, 0),(XMouse - SizeDescribed[0]/2, YMouse + 50 + (n*20) + Alt_Size[1]), True)
        if Panel_state:
            text_draw(UI, 12, pygame.sysfont.SysFont("FixedSys", 25), (0, 0, 0),(XMouse - SizeDescribed[0] + 15, YMouse + SizeDescribed[1] + Alt_Size[1] -25), False)



    if Panel_state:
        screen.blit(Menu0, (1000, 0))
        text_draw(screen, f"{diamond_format(costs.get(4.1)+inflation.get(4.1)*HousesBought)}", pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1147, 122), False)
        text_draw(screen, f"{diamond_format(citizens.get(4.1)*HouseMultiplier)}", pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1063, 132), False)
        text_draw(screen, f"{diamond_format(costs.get(5.1) + inflation.get(5.1) * GeneratorsBought)}",pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1147, 172), False)
        text_draw(screen, f"{diamond_format(citizens.get(5.1) * GeneratorMultiplier)}", pygame.font.SysFont("Fixedsys", 32),(136, 0, 21), (1063, 182), False)
        text_draw(screen, f"{diamond_format(costs.get(6.1) + inflation.get(6.1) * MinesBought)}",pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1147, 222), False)
        text_draw(screen, f"{diamond_format(citizens.get(6.1) * MinesMultiplier)}", pygame.font.SysFont("Fixedsys", 32),(136, 0, 21), (1063, 232), False)
        text_draw(screen, f"{diamond_format(costs.get(7.1) + inflation.get(7.1) * MhousesBought)}", pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1147, 272), False)
        text_draw(screen, f"{diamond_format(citizens.get(7.1) * MhousesMultiplier)}", pygame.font.SysFont("Fixedsys", 32),(0, 0, 0), (1063, 282), False)
    else:
        screen.blit(Menu1, (1000, 0))
        text_draw(screen, f"{diamond_format(math.floor(upgrades.get(4.1)*(1.75**(HouseMultiplier-1))))}",pygame.font.SysFont("Fixedsys", 26), (0, 0, 0), (1147, 124), False)
        text_draw(screen, f"{diamond_format(citizens.get(4.1) * HouseMultiplier)}+1", pygame.font.SysFont("Fixedsys", 26),(0, 0, 0), (1063, 134), False)
        text_draw(screen, f"{diamond_format(math.floor(upgrades.get(5.1)*(1.75**(GeneratorMultiplier-1))))}",pygame.font.SysFont("Fixedsys", 26), (0, 0, 0), (1147, 175), False)
        text_draw(screen, f"{diamond_format(citizens.get(5.1) * GeneratorMultiplier)}-1", pygame.font.SysFont("Fixedsys", 26),(136, 0, 21), (1063, 184), False)
        text_draw(screen, f"{diamond_format(math.floor(upgrades.get(6.1) * (1.75 ** (MinesMultiplier - 1))))}",pygame.font.SysFont("Fixedsys", 26), (0, 0, 0), (1147, 224), False)
        text_draw(screen, f"{diamond_format(citizens.get(6.1) * MinesMultiplier)}-5", pygame.font.SysFont("Fixedsys", 26),(136, 0, 21), (1063, 234), False)
        text_draw(screen, f"{diamond_format(math.floor(upgrades.get(7.1) * (1.75 ** (MhousesMultiplier - 1))))}",  pygame.font.SysFont("Fixedsys", 26), (0, 0, 0), (1147, 275), False)
        text_draw(screen, f"{diamond_format(citizens.get(7.1) * MhousesMultiplier)}+5", pygame.font.SysFont("Fixedsys", 26),(0, 0, 0), (1063, 284), False)

    if ((round(selected_building) == 4 or round(selected_building) == 5) or round(selected_building) == 7) and build_mode:
        Water.set_alpha(150)
        Mountain.set_alpha(150)
    elif (round(selected_building) == 6) and build_mode:
        Grass.set_alpha(150)
        Water.set_alpha(150)
    elif not build_mode:
        Grass.set_alpha(255)
        Stone.set_alpha(255)
        Mountain.set_alpha(255)
        Water.set_alpha(255)
    game_timer += 1
    sell_timer -= 1
    for i, p in enumerate(matrix):
        for i2, p2 in enumerate(p):
            if matrix[i][i2] == 0:
                screen.blit(Grass, (i2*100, i*100))
            elif matrix[i][i2] == 1:
                screen.blit(Stone, (i2*100, i*100))
            elif matrix[i][i2] == 2:
                screen.blit(Mountain, (i2*100, i*100))
            elif matrix[i][i2] == 3:
                screen.blit(Water, (i2*100, i*100))
            elif matrix[i][i2] == 4.11:
                screen.blit(GHouse1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 4.21
            elif matrix[i][i2] == 4.21:
                screen.blit(GHouse2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 4.11
            elif matrix[i][i2] == 4.12:
                screen.blit(SHouse1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 4.22
            elif matrix[i][i2] == 4.22:
                screen.blit(SHouse2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 4.12
            elif matrix[i][i2] == 5.11:
                screen.blit(GGenerator1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 5.21
                if game_timer % 60 == 0:
                    Diamonds += 1*GeneratorMultiplier
            elif matrix[i][i2] == 5.21:
                screen.blit(GGenerator2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 5.11
                if game_timer % 60 == 0:
                    Diamonds += 1*GeneratorMultiplier
            elif matrix[i][i2] == 5.12:
                screen.blit(SGenerator1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 5.22
                if game_timer % 60 == 0:
                    Diamonds += 1*GeneratorMultiplier
            elif matrix[i][i2] == 5.22:
                screen.blit(SGenerator2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 5.12
                if game_timer % 60 == 0:
                    Diamonds += 1*GeneratorMultiplier
            elif matrix[i][i2] == 6.12:
                screen.blit(SMineshaft1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 6.22
                if game_timer % 60 == 0:
                    Diamonds += 25*MinesMultiplier
            elif matrix[i][i2] == 6.22:
                screen.blit(SMineshaft2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 6.12
                if game_timer % 60 == 0:
                    Diamonds += 25*MinesMultiplier
            elif matrix[i][i2] == 6.13:
                screen.blit(MMineshaft1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 6.23
                if game_timer % 60 == 0:
                    Diamonds += 25*MinesMultiplier
            elif matrix[i][i2] == 6.23:
                screen.blit(MMineshaft2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 6.13
                if game_timer % 60 == 0:
                    Diamonds += 25*MinesMultiplier
            elif matrix[i][i2] == 7.11:
                screen.blit(GMhouse1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 7.21
            elif matrix[i][i2] == 7.21:
                screen.blit(GMhouse2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 7.11
            elif matrix[i][i2] == 7.12:
                screen.blit(SMhouse1, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 7.22
            elif matrix[i][i2] == 7.22:
                screen.blit(SMhouse2, (i2 * 100, i * 100))
                if game_timer % 30 == 0:
                    matrix[i][i2] = 7.12
    if music_ended:
        if random.randint(1, 3000) == 1:
            pygame.mixer.music.play(1)
            print("music started")
            music_ended = False
    text_draw(screen, Citizens, pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1130, 967), False)
    text_draw(screen, diamond_format(Diamonds), pygame.font.SysFont("Fixedsys", 32), (0, 0, 0), (1035, 967), False)
    create_ui((0, 0), (800, 100), (195, 195, 195, 200), (0, 0, 0, 200))
    screen.blit(UI, (0, 0))
    pygame.display.flip()   # Also the base of everything
    clock.tick(60)
# the closing sequence (who would have thought)
new_data = open("Save_file.txt", "w")
save_data = "Секретные разработки нейрорера не трогать\n"
for n, data1 in enumerate(matrix):
    if n != 0:
        save_data += "|"
    for n, data2 in enumerate(data1):
        if n != 9:
            save_data += (str(data2) + ",")
        else:
            save_data += (str(data2))
save_data += (f"\n{Citizens}\n{Diamonds}\n{HouseMultiplier}\n{HousesBought}\n{GeneratorMultiplier}\n{GeneratorsBought}\n"
              f"{MinesMultiplier}\n{MinesBought}\n{MhousesMultiplier}\n{MhousesBought}")
print(save_data)
new_data.writelines(save_data)
pygame.quit()