# Ecosystem Simulator
This project is a visually straightforward ecosystem simulator, written in Python, that models an environment with rabbits and foxes. The inspiration for this project comes from Sebastian Lague’s video [Coding Adventure: Simulating an Ecosystem](https://youtu.be/r_It_X7v-1E).

- White Squares: rabbits
- Orange Squares: foxes
- Yellow Squares: rabbit food
- Blue: water
- Red Square: selected animal


## [Video Demonstration](https://afriesen731.github.io/ecosystem-simulator/) 

## How to set up
1. Clone the repo
2. Create a python virtual environment
3. Run "pip install -r requirements.txt"
4. Run main.py with the python interpreter (works with python 3.12)

## How to use

After starting the program, you'll be prompted to enter the initial number of foxes and rabbits (a 1:10 fox-to-rabbit ratio works well). While the simulation is running, you can add more animals or adjust the simulation speed by following the terminal prompts.

Each animal has a state, showing its current goals and needs. You can view an animal's state by clicking on it in the game window or by pressing:

- r to view a random rabbit,
- f to view a random fox.

When you close the window to end the simulation, a graph showing the population trends of foxes and rabbits will appear. The way each rabbit died is also displayed on the terminal.
