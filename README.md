# Pacman Portal
This is a clone of the Pacman game, but with a small change. 
In this game, Pacman can create portals on the walls of the maze to make his escape from the Ghosts.

## Getting Started

### Prerequisites
This game was made using Python 3.7.x and Pygame. 
You can install **Python 3** by downloading the installer [here](https://www.python.org/downloads/).

**Install Pygame using**:

```python3 -m pip install -U pygame --user```. 

To make sure pygame is running correctly, run this command:

```python3 -m pygame.examples.aliens```

If this doesn't work, please refer to the [Pygame Getting Started wiki page](https://www.pygame.org/wiki/GettingStarted).

## Run The Game
To run the game, simply run the command:

```python3 pacman.py```

### Controls
Pacman can be controlled using the **arrow keys**. 
To create the portals, use the **'z'** and **'x'** keys. 
 
 The **'z'** key will create the blue portal while the **'x'** key will create the red portal.
 
## Quiting The Game
To quit the game, simply press the **'q'** key.

## Bugs
- The Ghost AI does not work, they can walk through walls. Cannot find the home base after being eaten.
- Pacman can sometimes clip through walls while moving through the maze.
- Pacman can sometimes get stuck on a wall
