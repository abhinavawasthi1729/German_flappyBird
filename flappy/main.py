import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
question_answer = {
    'Du siehst __________ Baum' : 'B',
    'Sie schickt __________ Information' : 'R',
    'Ich öffne _________ Tür' : 'R',
    'Ich höre ________ Song' : 'B',
    'Er kennt ________ Weg' : 'B', 
    'Wir brauchen __________ Geld' : 'G',
    'Wer macht _________ Übung' : 'R',
    'Ich frage __________ Kollegen' : 'B', 
    'Sie kocht __________ Mittagessen' : 'G', 
}
question_set = list(question_answer.keys())
answer_set = list(question_answer.values())
circle_count = 0
total_circle_height = SCREENHEIGHT * 0.8
rgbValue = {
    'R' : [30, (1/3)*total_circle_height],
    'G' : [(1/3)*total_circle_height, (2/3)*total_circle_height],
    'B' : [(2/3)*total_circle_height, total_circle_height]
}

question_selected = []                  #list of questions that are alredy displayed

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int((SCREENWIDTH - GAME_SPRITES['player'].get_width())/2)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    global circle_count

    # Create 2 pipes for blitting on the screen
    newCircle1 = getRandomCircle()
    
    newCircle2 = getRandomCircle()


    

    # my List of circles
    circle_list = [
        {'x': SCREENWIDTH+200, 'y':newCircle1['y']},
        {'x': SCREENWIDTH+200+newCircle2['x'], 'y':newCircle2['y']},
    ]
   
    circleVelX = -3

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping

    font_color=(0,0,0)
    font_obj=pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf",14)

    question_selected.append(random.randint(0, len(question_set)-1))    #appending a question index in empty list

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<circle_list[0]['x']<3:
            newCircle = getRandomCircle()
            
            circle_list.append(newCircle)

        # if the pipe is out of the screen, remove it
        if circle_list[0]['x'] < -GAME_SPRITES['circles'].get_width():
            circle_list.pop(0)
            circle_count+=1 
            if (len(question_selected) == len(question_set) ):
                question_selected.clear()                    #clear list if full so that game continues
            index = random.randint(0, len(question_set)-1)
            while( index in question_selected ):
                index = random.randint(0, len(question_set)-1)
            question_selected.append(index)

        crashTest = isCollide(playerx, playery, circle_list) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        #check if mid point of player(bird) passes the mid point of circle
        playerMid = int((playerx +GAME_SPRITES['player'].get_width())/2)
        for circle in circle_list:
            circleMid = int((circle['x'] +GAME_SPRITES['circles'].get_width())/2)
            if (circleMid < playerMid-8  <= circleMid + 1) and (crashTest==False):     # playerMid-9 is hit and try value
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for circle in circle_list:
            circle['x'] += circleVelX
            

        # # Add a new pipe when the first is about to cross the leftmost part of the screen
        # if 0<circle_list[0]['x']<3:
        #     newpipe = getRandomCircle()
            
        #     circle_list.append(newpipe)

        # # if the pipe is out of the screen, remove it
        # if circle_list[0]['x'] < -GAME_SPRITES['circles'].get_width():
        #     circle_list.pop(0)
        #     circle_count+=1                             #circle count is the ith circle player is going to pass
            
            
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        # text_obj=font_obj.render(question_set[circle_count % len(question_set)] + "  Answer :"+answer_set[circle_count % len(question_set)],True,font_color)
        text_obj=font_obj.render(question_set[question_selected[len(question_selected)-1]] + f' ({answer_set[question_selected[len(question_selected)-1]]})',True,font_color)
              
        SCREEN.blit(text_obj,(22,5))
        for circle in circle_list:
            SCREEN.blit(GAME_SPRITES['circles'], (circle['x'], circle['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, circle_list):
    # global circle_count  
    # index = circle_count % len(question_answer)
    

    # print(f" index {index}")
    #hits ground or upper part
    if ( playery < 5 or playery > GROUNDY - 25):
        GAME_SOUNDS['hit'].play()
        return True
    # print(f'questions selected {question_selected}')
    # print(f'index in iscollide {len(question_selected)-1}')
    index = question_selected[len(question_selected)-1]
    for circle in circle_list:
        if (circle['x'] <= playerx <= circle['x'] + GAME_SPRITES['circles'].get_width()):    #if player is within the width of circle
            answer = answer_set[index]
            # print(f"answer {answer}")
            if not(rgbValue[answer][0] <= playery < rgbValue[answer][1]):
                # print(f"range {rgbValue[answer][0]} - {rgbValue[answer][1]}")
                # print(f"playery {playery}")
                GAME_SOUNDS['hit'].play()
                return True
            else:
                return False       
    return False

def getRandomCircle():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    
    offset = 2*SCREENWIDTH
    
    return {'x' : offset, 'y' : 30}






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('German Chidiya')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['circles'] =pygame.image.load('gallery/sprites/circles.png').convert_alpha()
   

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
        circle_count = 0 
        question_selected.clear()
