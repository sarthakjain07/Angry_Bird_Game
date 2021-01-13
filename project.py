import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
from pygame import mixer # used to play some audios use in game

# Global Variables for the game
fps = 32
screen_width = 289 
screen_height = 511
screen = pygame.display.set_mode((screen_width, screen_height))
ground = screen_height * 0.8
game_images = {}
game_audios = {}
player_angry_bird = 'images/bird.png'
bg = 'images/7.jpg'
pipe = 'images/pipe.png'

def firstDisplay():
    ''' This is the first screen user will see when the game starts '''

    player_x = int(screen_width/5)
    player_y = int((screen_height - game_images['player'].get_height())/2)
    message_x = int((screen_width - game_images['message'].get_width())/2)
    message_y = int(screen_height*0.13)
    base_x = 0
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
                screen.blit(game_images['background'], (0, 0))    
                screen.blit(game_images['player'], (player_x, player_y))    
                screen.blit(game_images['message'], (message_x,message_y ))    
                screen.blit(game_images['base'], (base_x, ground))    
                pygame.display.update()
                FPSCLOCK.tick(fps)

def mainGame():
    score = 0
    player_x = int(screen_width/5)
    player_y = int(screen_width/2)
    base_x = 0

    # Create 2 pipes for blitting on the screen
    Pipe_1 = getRandomPipe()
    Pipe_2 = getRandomPipe()

    # my List of upper pipes
    upper_pipes = [
        {'x': screen_width+200, 'y':Pipe_1[0]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':Pipe_2[0]['y']},
    ]
    # my List of lower pipes
    lower_pipes = [
        {'x': screen_width+200, 'y':Pipe_1[1]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':Pipe_2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    game_audios['wing'].play()


        crashTest = isCollide(player_x, player_y, upper_pipes, lower_pipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = player_x + game_images['player'].get_width()/2
        for pipe in upper_pipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                game_audios['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = game_images['player'].get_height()
        player_y = player_y + min(playerVelY, ground - player_y - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upper_pipes, lower_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upper_pipes[0]['x']<5:
            newpipe = getRandomPipe()
            upper_pipes.append(newpipe[0])
            lower_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upper_pipes[0]['x'] < -game_images['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
        
        # Lets blit our sprites now
        screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_images['base'], (base_x, ground))
        screen.blit(game_images['player'], (player_x, player_y))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (screen_width - width)/2

        for digit in myDigits:
            screen.blit(game_images['numbers'][digit], (Xoffset, screen_height*0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(fps)

def isCollide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y> ground - 25  or player_y<0:
        game_audios['hit'].play()
        return True
    
    for pipe in upper_pipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if(player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < game_images['pipe'][0].get_width()):
            game_audios['hit'].play()
            return True

    for pipe in lower_pipes:
        if (player_y + game_images['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < game_images['pipe'][0].get_width():
            game_audios['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = game_images['pipe'][0].get_height()
    offset = screen_height/3
    y2 = offset + random.randrange(0, int(screen_height - game_images['base'].get_height()  - 1.2 *offset))
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('ANGRY_BIRD_GAME')
    game_images['numbers'] = ( 
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )

    game_images['message'] =pygame.image.load('images/11.jpg').convert_alpha()
    game_images['base'] =pygame.image.load('images/base.png').convert_alpha()
    game_images['pipe'] =(pygame.transform.rotate(pygame.image.load( pipe).convert_alpha(), 180), 
    pygame.image.load(pipe).convert_alpha()
    )

    # Game sounds
    game_audios['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audios['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    game_audios['point'] = pygame.mixer.Sound('sounds/point.wav')
    game_audios['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    game_audios['wing'] = pygame.mixer.Sound('sounds/wing.wav')
    # game_audios['bgmusic'] = pygame.mixer.Sound('sounds/bgmusic.mp3')

    game_images['background'] = pygame.image.load(bg).convert()
    game_images['player'] = pygame.image.load(player_angry_bird).convert_alpha()

    while True:
        mixer.music.stop()
        firstDisplay() # Welcome screen for user
        mixer.music.load("sounds/bgmusic.mp3")
        mixer.music.play() 
        mainGame() # This function controls the entire game
