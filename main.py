from time import sleep
import tkinter as tk
from Puzzle import Puzzle
import SearchAgent
import pygame
from buttons import Button

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100
SIDES_PADDING = 10
INBTWN_SPACE = 1
PUZZLE_WIDTH = (SCREEN_WIDTH - (2*SIDES_PADDING))

BACK_GRND_COLOR = (255,255,255)
RED = (123,44,130)
bg = pygame.image.load("BG.png")
start_player = False
agent_selected = None
generate_random = False
A_star_type = None
font_size = 50
text_size = 30
padding = 4
def start_window():
    global start_player
    buttons = []
    player_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Play",BACK_GRND_COLOR,font_size)
    player_button.draw(game_screen)
    buttons.append(player_button)
    AI_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"AI",BACK_GRND_COLOR,font_size)
    AI_button.draw(game_screen)
    buttons.append(AI_button)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            start_player = True
                            return
                        if i == 1:
                            return
                
            pygame.display.update()
    pygame.quit()

def AI_window():
    game_screen.blit(bg,(0,0))
    global agent_selected
    buttons = []
    BFS = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"BFS",BACK_GRND_COLOR,font_size)
    BFS.draw(game_screen)
    buttons.append(BFS)
    DFS = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"DFS",BACK_GRND_COLOR,font_size)
    DFS.draw(game_screen)
    buttons.append(DFS)
    a_star = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (2*BUTTON_HEIGHT) + (2*padding), BUTTON_WIDTH,BUTTON_HEIGHT,RED,"A*",BACK_GRND_COLOR,font_size)
    a_star.draw(game_screen)
    buttons.append(a_star)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            agent_selected = 0
                            return
                        if i == 1:
                            agent_selected = 1
                            return
                        if i == 2:
                            agent_selected = 2
                            return
                
            pygame.display.update()
    pygame.quit()

def generating_window():
    game_screen.blit(bg,(0,0))
    global generate_random
    buttons = []
    text = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Generate the puzzle random?",BACK_GRND_COLOR,text_size)
    text.draw(game_screen)
    YES = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (BUTTON_HEIGHT)+padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"YES",BACK_GRND_COLOR,font_size)
    YES.draw(game_screen)
    buttons.append(YES)
    NO = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (2*BUTTON_HEIGHT)+(2*padding), BUTTON_WIDTH,BUTTON_HEIGHT,RED,"NO",BACK_GRND_COLOR,font_size)
    NO.draw(game_screen)
    buttons.append(NO)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            generate_random = True
                            return
                        if i == 1:
                            return
                
            pygame.display.update()
    pygame.quit()

def A_Star_window():
    game_screen.blit(bg,(0,0))
    global A_star_type
    buttons = []
    mnha_type = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Manhaten Type",BACK_GRND_COLOR,text_size)
    mnha_type.draw(game_screen)
    buttons.append(mnha_type)

    eqlid_type = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Ecledian Type",BACK_GRND_COLOR,text_size)
    eqlid_type.draw(game_screen)
    buttons.append(eqlid_type)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            A_star_type = 1
                            return
                        if i == 1:
                            A_star_type = 0
                            return
                
            pygame.display.update()
    pygame.quit()



pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("BG.png")
game_screen.blit(bg,(0,0))
# game_screen.fill(BACK_GRND_COLOR)
pygame.display.set_caption("8-puzzle")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)




start_window()


if start_player:
    generating_window()
    p = Puzzle(game_screen, generate_random, bg)
    while True:
        p.getEvents()
else:
    AI_window()
    generating_window()
    if agent_selected != None:
        
        if agent_selected == 0:
            p = Puzzle(game_screen, generate_random, bg)
            agent = SearchAgent.DFS(p.state)
        elif agent_selected == 1:
            p = Puzzle(game_screen, generate_random, bg)
            agent = SearchAgent.BFS(p.state)
        elif agent_selected == 2:
            A_Star_window()
            p = Puzzle(game_screen, generate_random, bg)
            agent = SearchAgent.AStar(p.state)
        
        c = SearchAgent.timer(agent.search, A_star_type)
        
        res = c[1]
        print("Time: "+str(c[0])+" s")
        print("Max depth: ",res.depth)
        s = "Total number of moves: " + str(len(res.moves)-1)
        time = round(c[0], 5)
        witdth = (PUZZLE_WIDTH-(2*INBTWN_SPACE))//3
        time_text = Button(10, 10, witdth, BUTTON_HEIGHT-60, RED," Time: "+str(time)+ "s",BACK_GRND_COLOR,text_size-10)
        time_text.draw(p.screen)
        Max_depth_text = Button(10+ witdth+INBTWN_SPACE, 10, witdth, BUTTON_HEIGHT-60, RED," Max depth: "+str(res.depth),BACK_GRND_COLOR,text_size-10)
        Max_depth_text.draw(p.screen)
        total_no_moves_text = Button(10+(2*witdth)+(2*INBTWN_SPACE), 10, witdth, BUTTON_HEIGHT-60, RED," # of explored: " + str(res.states),BACK_GRND_COLOR,text_size-10)
        total_no_moves_text.draw(p.screen)
        pygame.display.update()

        root = tk.Tk()
        root.withdraw()
        if tk.messagebox.askyesno("Display moves","Display solution moves?\n"+s):
            i = 0
            while i+1 < len(res.moves):
                p.drawSwap(res.moves[i],res.moves[i+1])
                sleep(1)
                i += 1
                p.checkQuit()
        while True:
            p.checkQuit()

