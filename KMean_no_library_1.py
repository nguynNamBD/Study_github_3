
#21120291
# Imports libraries
import numpy as np
import pygame
from sklearn.cluster import KMeans
import random
import math

#import rgb color
BLACK = [0,0,0]
GREY = [96,96,96]
WHITE = [255,255,255]
CREAMGOLD = [255,255,204]

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
YELLOW = [255,255,0]
PURPLE = [204,0,204]
PINK = [255,102,255]
ORANGE = [255,128,0]
BROWN = [102,51,0]
#labels colors 8
COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,PINK,ORANGE,BROWN]

#define variable
k = 0 #number of K point
error = 0 
mouse_click = []
mouse_rand = []
labels = []

# Configuration
pygame.init()
# fps = 60
# fpsClock = pygame.time.Clock()
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Kmean Visualization Pygame')

#font
def create_font(font,size,text,color):
    return  pygame.font.SysFont(font, size).render(text,True,color)
# dialogue_font = pygame.font.SysFont('arial', 25)
# dialogue = dialogue_font.render("Hey there, Beautiful weather today!",True, (0,0,0)) example of font
text_plus = create_font('arial',30,'+','WHITE')
text_minus = create_font('arial',30,'-','WHITE')
text_run = create_font('arial',30,'Run','WHITE')
text_rand = create_font('arial',30,'Random','WHITE')
text_algorithm = create_font('arial',30,'Algorithm','WHITE')
text_reset = create_font('arial',30,'Reset','WHITE')
text_anything = create_font('arial',30,'Anything','WHITE')#you can do everything you like in that box

# Game loop.
while  True:
    screen.fill(GREY)
    #get the mouse
    mouse_px,mouse_py = pygame.mouse.get_pos()    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_px>55 and mouse_px<645 and mouse_py>55 and mouse_py<545:
                mouse_click.append([mouse_px,mouse_py])
            elif mouse_px>700 and mouse_px<750 and mouse_py>50 and mouse_py<100 and k<8:
                k += 1
            elif mouse_px>800 and mouse_px<850 and mouse_py>50 and mouse_py<100 and k>0:
                k -= 1  
            elif mouse_px>700 and mouse_px<850 and mouse_py>150 and mouse_py<200:
                #print('rand')
                error = 0
                mouse_rand = []
                labels = []
                for i in range(k):
                    mouse_rand.append([random.randint(50,650), random.randint(50,550)])
            elif mouse_px>700 and mouse_px<850 and mouse_py>250 and mouse_py<300:
                # print('run')
                #labels != [] --> get the new address of random point in to middle of training point
                if labels != []:
                    for i in range(len(mouse_rand)):
                        x_new_rand = 0
                        y_new_rand = 0
                        times_labels = 0 
                        for j in range(len(mouse_click)):
                            if labels[j] == i:
                                times_labels += 1
                                x_new_rand += mouse_click[j][0]
                                y_new_rand += mouse_click[j][1]
                        if times_labels != 0:
                            mouse_rand[i][0] = x_new_rand/times_labels
                            mouse_rand[i][1] = y_new_rand/times_labels
                #calculate new address of point
                if len(mouse_rand) != 0 :
                    labels = []
                    error = 0
                    for i in range(len(mouse_click)):
                        distance = []
                        for j in range(len(mouse_rand)):
                            distance.append(math.dist(mouse_click[i], mouse_rand[j]))
                        labels.append(distance.index(min(distance)))
                        error += min(distance)

            elif mouse_px>700 and mouse_px<850 and mouse_py>350 and mouse_py<400:
                # print('algorithm')
                kmeans = KMeans(n_clusters=k, random_state=0).fit(mouse_click)
                labels = kmeans.labels_
                print(labels)
            elif mouse_px>700 and mouse_px<850 and mouse_py>450 and mouse_py<500:
                # print('reset')
                labels = []
                mouse_click = []
                mouse_rand = []
                k = 0
                error = 0
            elif mouse_px>700 and mouse_px<850 and mouse_py>550 and mouse_py<600:
                print(mouse_click)
    #Keual and error
    text_Kequal = create_font('arial',30,'K = '+str(k),'WHITE')
    text_error = create_font('arial',40,'Error = '+str(round(error,2)),'WHITE')

    #print some rectangular
    pygame.draw.rect(screen,CREAMGOLD,[50, 50, 600, 500])# border_radius = 100
    pygame.draw.rect(screen,BLACK,[700, 50, 50, 50])# area +
    pygame.draw.rect(screen,BLACK,[800, 50, 50, 50])# area -
    pygame.draw.rect(screen,BLACK,[700, 150, 150, 50])# area rand
    pygame.draw.rect(screen,BLACK,[700, 250, 150, 50])# run
    pygame.draw.rect(screen,BLACK,[700, 350, 150, 50])# area algorithm
    pygame.draw.rect(screen,BLACK,[700, 450, 150, 50])# reset
    pygame.draw.rect(screen,BLACK,[700, 550, 150, 50])# reset

    
    #insert text remember blit after draw.rect()
    screen.blit(text_plus, (710,60))
    screen.blit(text_minus, (810,60))
    screen.blit(text_Kequal, (870,60))
    screen.blit(text_rand, (710,160))
    screen.blit(text_run, (710,260))
    screen.blit(text_algorithm, (710,360))
    screen.blit(text_reset, (710,460))
    screen.blit(text_anything, (710,560))
    screen.blit(text_error, (280,580))
    

    #draw circle
    # pygame.draw.circle(screen, BLACK, (60,60), 10)

    #display position of point in main area
    if mouse_px>50 and mouse_px<650 and mouse_py>50 and mouse_py<550:
        address_point = '('+str(mouse_px-50)+','+str(mouse_py-50)+')'
        text_address_point = create_font('arial', 30, address_point,'BLACK')
        screen.blit(text_address_point, (mouse_px,mouse_py)) 
        # print(address_point)   

    #draw circle (training point Kmean) and random point
    for i in range(len(mouse_click)):
        pygame.draw.circle(screen, BLACK, mouse_click[i], 10)
        if labels == []:
            pygame.draw.circle(screen, WHITE, mouse_click[i], 8)
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], mouse_click[i], 8)
    for i in range(len(mouse_rand)):
        pygame.draw.circle(screen, WHITE, mouse_rand[i], 10)
        pygame.draw.circle(screen,COLORS[i], mouse_rand[i], 8)

    pygame.display.flip() 