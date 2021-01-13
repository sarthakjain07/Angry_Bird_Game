# Angry_Bird_Game
A super cool angry birds mini game using python language.

1.Random:
We can generate random numbers in Python by using random module.

Why we used this module?
It is used to generate random number of pipes which are the hurdles in our game. When our bird hits one of the pipe the game is over.

2.Sys:
The sys module provides information about constants, functions and methods of the Python interpreter. dir(system) gives a summary of the available constants, functions and methods. Another possibility is the help() function. Using help(sys) provides valuable detail information.

Why we used this module?
It is used to close the program of our game using sys.exit() command after pygame.quit() command. Without this module our program would not end.

3.Pygame:
Pygame is a cross-platform set of Python modules designed for writing video games. It includes computer graphics and sound libraries designed to be used with the Python programming language.

Why we used this module?
It is the main and most important module of our game. All the images, audio clips, game background, base, background music is controlled by this module only. Also from pygame.locals import* and from pygame import mixer are used to import all local basic functionalities of pygame and mixer is imported to play the music and audio clips in the game according to their events.
