import pygame
import os
import random
import math
import threading
import matplotlib.pyplot as plt
import json
from time import time








# the idea for this project came from this video by Sebastian Lague https://youtu.be/r_It_X7v-1E
pygame.init()
WIDTH = 128 
HEIGHT = 64 


GRID_SIZE = 10

WIN_WIDTH = WIDTH * GRID_SIZE +  GRID_SIZE
WIN_HEIGHT = HEIGHT * GRID_SIZE + GRID_SIZE

FPS = 60
speed = [FPS]

BACKGROUND = pygame.image.load(os.path.join('background.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (1290, 660))



GREEN = (73, 163, 90)
DARK_GREEN = (0, 163, 24)
GREY = (214, 214, 214)
DARK_GREY = (150, 150, 150)
ORANGE = (255, 128, 0)
YELLOW = (224, 219, 49)
RED = (201, 6, 6)
BLUE = (3, 28, 252)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


WHITE_RECT_Y = 140
YELLOW_BAR_X = 20
YELLOW_BAR_Y = WHITE_RECT_Y + 100
BAR_LENGHT = 100
BAR_WIDTH = 20
WARN_ABOUT_WALL = 5
BAR_FONT = pygame.font.SysFont(None, 20)










class SimState:

  _instance = None  # Class variable to hold the single instance

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super(SimState, cls).__new__(cls, *args, **kwargs)
    return cls._instance
  
  def __init__(self):
    
    rabbit_instances = [] 
    fox_instances = []
    food_instances = []
    foods = {}
    rabbits = {}
    mating_male_rabbits = {} 
    mating_female_rabbits = {}
    foxes = {}
    mating_male_foxes = {}
    mating_female_foxes = {}
    with open('water.json', 'r') as file:
      water = json.load(file)



class Animal:
  """Base class representing an animal in the simulation."""

  GOAL_CUTOFF = 1
  SIM = SimState()

  pythagorean_theorem = lambda a, b: math.sqrt(a ** 2 + b ** 2)

  key = 0
  def __init__(self, dict_to_append_to, Animal_Class, x=None, y=None):
    """
    Initialize a new Animal instance.

    Args:
        dict_to_append_to (dict): Dictionary to add this animal to.
        Animal_Class (class): The class of the animal.
        x (int, optional): X-coordinate of the animal. Default is a random value.
        y (int, optional): Y-coordinate of the animal. Default is a random value.
    """
    Animal.key += 1
    self.KEY = Animal.key
    self.Animal_Class = Animal_Class

    self.GENDER = random.choice(['male', 'female'])

    self.x = x
    self.y = y
    
    if self.x is None and self.y is None:
      self.x = random.randint(0, WIDTH)
      self.y = random.randint(0, HEIGHT)
 
    else:
      self.x = x
      self.y = y
    dict_to_append_to.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
    
    self.goal = None
    self.state = None
    
    self.x_direction = None
    self.y_direction = None

    self.thirst = 0.
    self.hunger = 0.01
    self.BASE_REPRODUCTIVE_URGE = 0.6
    self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE

    self.just_mated = random.randint(0, self.Animal_Class.MATING_BREAK)
    

    self.rest = 1

    self.random_movement_counter = 0



  def set_state(self):
    """
    Determine the animal's current state based on its needs and surroundings.

    Args:
        dict_of_male_mates (dict): Dictionary of potential male mates.
        dict_of_female_mates (dict): Dictionary of potential female mates.
        dict_of_food (dict): Dictionary of available food sources.
        water (dict, optional): Dictionary of water sources. Defaults to water.
    """
    if self.rest > 0:
      return

    self.thirst += self.Animal_Class.THIRST_INCRIMENT
    self.hunger += self.Animal_Class.HUNGER_INCRIMENT
    

    if self.just_mated > 0:
      self.reproductive_urge = 0
      self.just_mated -= 1
      if self.just_mated <= 0: self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE
      
    
    previous_goal = self.goal
    
    if self.state != 'found mate':
        
      if self.thirst > max(self.hunger, self.reproductive_urge, self.Animal_Class.BASE_CUTOFF):
        if self.goal != 'water':
          self.goal = 'water'
          self.state = 'searching for water'
      elif self.hunger > max(self.thirst, self.reproductive_urge, self.Animal_Class.BASE_CUTOFF):
        if self.goal != 'food':
          self.goal = 'food'
          self.state = 'searching for food'
      elif self.reproductive_urge > max(self.thirst, self.hunger, self.Animal_Class.BASE_CUTOFF):
        if self.goal != 'reproduce':
          self.goal = 'reproduce'
          self.state = 'searching for mate'

          if self.GENDER == 'male':
            dict_of_male_mates.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})

          if self.GENDER == 'female':
            dict_of_female_mates.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
      
      else:
        self.goal = None
        self.state = None
        self.move_randomly()
      

      if previous_goal == 'reproduce' and self.goal != 'reproduce':  
          
        if self.GENDER == 'male':
          try:
            del dict_of_male_mates[self.KEY]
          except KeyError:
            pass
        if self.GENDER == 'female':
          try:
            del dict_of_female_mates[self.KEY]
          except KeyError:
            pass

      
        

    if self.goal == 'food':
      if self.state == 'searching for food':
        self.search_for_object(dict_of_food, 'found food')
        
        if self.state == 'searching for food':
          self.move_randomly()

      if self.state == 'found food':
        self.update_target(dict_of_food, 'searching for food')
        self.point_towards_object()
        
        if self.target['distance'] <= 1:
          self.state = 'eating'
          

    elif self.goal == 'water':
      if self.state == 'searching for water':
        self.search_for_object(self.SIM.water, 'found water')
        
        if self.state == 'searching for water':
          self.move_randomly()

      if self.state == 'found water':
        self.update_target(self.SIM.water, 'searching for water')
        self.point_towards_object()
        
        if self.target['distance'] <= 1:
          self.state = 'drinking'


          
    elif self.goal == 'reproduce' and self.GENDER == 'male':

      dict_of_male_mates.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})

      
      if self.state == 'searching for mate':
        self.search_for_object(dict_of_female_mates, 'found mate', self.Animal_Class.MATING_VIEW_RANGE)
        if self.state == 'found mate':
          for mate in self.visible_items:
            female = dict_of_female_mates[mate['key']] ['self']
            if female.state == 'searching for mate':
              self.target = mate
              
              break
          if female.state != 'searching for mate':
            self.state = 'searching for mate'
          else:
            mate = dict_of_female_mates[self.target['key']] ['self']
            mate.state = 'found mate'
            mate.target = {'key': self.KEY}
          
          
        
        if self.state == 'searching for mate':
          self.move_randomly()

      if self.state == 'found mate':
        
        self.update_target(dict_of_female_mates, 'searching for mate', self.Animal_Class.MATING_VIEW_RANGE)
        self.point_towards_object()
        
        if self.target.get('distance') <= 1:
          self.state = 'mating'
          mate = dict_of_female_mates[self.target['key']]['self']
          mate.state = 'mating'
          mate.target = {'key': self.KEY}



    elif self.goal == 'reproduce' and self.GENDER == 'female':
      dict_of_female_mates.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
      if self.state == 'searching for mate':
        self.move_randomly()

      elif self.state == 'found mate':
        
        self.update_target(dict_of_male_mates, 'searching for mate', self.Animal_Class.MATING_VIEW_RANGE)
        if self.state == 'found mate':
          self.point_towards_object()
      

    self.avoid_edge()

      
      
          







  def search_for_object(self, list_of_items, state_if_found, VIEW_RANGE=None):
    if VIEW_RANGE == None:
      VIEW_RANGE = self.Animal_Class.VIEW_RANGE
    self.visible_items = []
    calculate_distance_cutoff = (math.sqrt(2)/2) * VIEW_RANGE * 2
    for item in list_of_items:
      #calculating total distance between self.x and the objects x cordinate
      #then they are converted to a positive number

      current_item = list_of_items[item]
      x_distance = current_item['x'] - self.x
      positive_x_distance = abs(x_distance)
      
      y_distance = current_item['y'] - self.y
      positive_y_distance = abs(y_distance)

      total_positive_distance =  positive_x_distance + positive_y_distance

      #using pythagorean theorem to find the exact distance

      if total_positive_distance < calculate_distance_cutoff:
        distance =  Animal.pythagorean_theorem(positive_x_distance, positive_y_distance)
      
        #if the distance is 15 or less the item gets added to a list based on what type it is
        
        if distance <= VIEW_RANGE:
          self.visible_items.append({'key': item, 'distance': distance, 'x_distance': x_distance, 'y_distance': y_distance,
                                    'positive_x_distance': positive_x_distance, 'positive_y_distance': positive_y_distance})
    if len(self.visible_items) > 0:
      self.visible_items.sort(key=lambda x: x['distance'])
      self.target = self.visible_items[0]
    

      self.state = state_if_found

  def point_towards_object(self):
    if self.target.get('x_distance') > 0: self.x_direction = 1
    elif self.target.get('x_distance') < 0: self.x_direction = -1
    elif self.target.get('x_distance') == 0: self.x_direction = 0

    if self.target.get('y_distance') > 0: self.y_direction = 1
    elif self.target.get('y_distance') < 0: self.y_direction = -1
    elif self.target.get('y_distance') == 0: self.y_direction = 0

  def update_target(self, list_of_items, state_if_out_of_range, VIEW_RANGE= None):
    item = list_of_items.get(self.target.get('key'))
    if VIEW_RANGE == None:
      VIEW_RANGE = self.Animal_Class.VIEW_RANGE
    if item == None:
      self.goal = state_if_out_of_range
      return
      
    x_distance = item['x'] - self.x
    positive_x_distance = abs(x_distance)
    
    y_distance = item['y'] - self.y
    positive_y_distance = abs(y_distance)

    total_positive_distance =  positive_x_distance + positive_y_distance

    #using pythagorean theorem to find the exact distance
    distance =  Animal.pythagorean_theorem(positive_x_distance, positive_y_distance)
    
    #if the distance is 15 or less the item gets added to a list based on what type it is
    if distance >= VIEW_RANGE:
      self.state = state_if_out_of_range
      return

    self.target = {'key': self.target['key'], 'distance': distance, 'x_distance': x_distance, 'y_distance': y_distance, 'positive_x_distance': positive_x_distance, 'positive_y_distance': positive_y_distance}
    
    


  def move_randomly(self):
    self.random_movement_counter += 1
    
    #whenever the random movement is at the begining of its sequence
    if self.random_movement_counter == 1:
      
      self.x_direction = random.randint(-1, 1)
      self.y_direction = random.randint(-1, 1)
      

      while self.x_direction == 0 and self.y_direction == 0:
        self.x_direction = random.randint(-1, 1)
        self.y_direction = random.randint(-1, 1)
      

    if self.x <= 0 and self.x_direction == -1: 
      self.x_direction = 1
      
    elif self.x >= WIDTH and self.x_direction == 1:
      self.x_direction = -1

    
    if self.y == 0 and self.y_direction == -1:
      self.y_direction = 1
    
    elif self.y == WIDTH and self.y_direction == 1:
      self.y_direction = -1


    #if the sequence has run more than once
    elif self.random_movement_counter >= 2 and self.random_movement_counter <= self.Animal_Class.MAX_RANDOM_MOVES:

      
      self.random_direction = random.random()
      
      #this has a random chance of turning the object 45 or 90 degrees to the side
      if self.x_direction == 0:

        #40% of the time the object will turn 45 degrees, 20% of the time it will turn 90 degrees
        if self.random_direction >= 0.6:
          self.x_direction = random.choice([-1, 1])

          
          if self.random_direction >= 0.8:
            self.y_direction = 0



      #this has a random chance of turning the object 45 or 90 degrees to the side
      elif self.y_direction == 0:
        
        
        #40% of the time the object will turn 45 degrees, 20% of the time it will turn 90 degrees
        if self.random_direction >= 0.6:
          #determines direction
          self.y_direction = random.randrange(-1, 2, 2)

        
          if self.random_direction >= 0.8:
            self.x_direction = 0
        
      if self.y_direction != 0 and self.x_direction != 0:
          
          if self.random_direction >= 0.6:
            
            self.random_x_or_y_direction = random.choice(['x', 'y'])
            
            if self.random_x_or_y_direction == 'x': self.x_direction = 0
            if self.random_x_or_y_direction == 'y': self.y_direction = 0

  
      #this resets the counter if it has reached its max random moves
      if self.random_movement_counter == self.Animal_Class.MAX_RANDOM_MOVES:
        self.random_movement_counter = 0

  def avoid_edge(self):
    if self.x == 0 and self.x_direction == -1:
      self.x_direction = 0
      
    if self.x >= WIDTH and self.x_direction == 1:
      self.x_direction = 0

    
    if self.y == 0 and self.y_direction == -1:
      self.y_direction = 0
    
    
    if self.y >= HEIGHT and self.y_direction == 1:
      self.y_direction = 0
    





class Rabbit(Animal):
  CLASS_TYPE = 'Rabbit'
  HUNGER_INCRIMENT = 0.005
  THIRST_INCRIMENT = 0.01
  BASE_CUTOFF = 0.2
  FOOD_RESTORATION = Animal.GOAL_CUTOFF
  
  REST_AFTER_EATING = 60
  REST_AFTER_DRINKING = 60
  REST_AFTER_MATING = 60
  REST_AFTER_MOVING = 7

  MATING_BREAK = 300
  
  MAX_RANDOM_MOVES = 10
  VIEW_RANGE = 15
  MATING_VIEW_RANGE = 35
  FOX_RANGE = 8#10

  
  def move(self):

    if self.rest > 0:
      self.rest -= 1

      return
    #print(self.state)
    

    if self.state == 'eating':

      try:
        self.hunger -= Rabbit.FOOD_RESTORATION
        if self.hunger < 0:
          self.hunger = 0
        key = self.target['key']
        target_food = self.SIM.foods[key]['self']
        target_food.times_eaten += 1
        self.rest = Rabbit.REST_AFTER_EATING

        #self.goal = None
        #self.state = None
      except KeyError:
        self.state = 'searching for food'
        
    elif self.state == 'drinking':
      self.thirst = 0
      self.rest = Rabbit.REST_AFTER_DRINKING
      #self.goal = None
      #self.state = None


    elif self.state == 'mating' and self.GENDER == 'female':
      try:
        del self.SIM.mating_female_rabbits[self.KEY]
      except KeyError:
        pass
      try:
        mate = self.SIM.mating_male_rabbits[self.target['key']]['self']

        mate.just_mated =Rabbit.MATING_BREAK
        mate.rest = Rabbit.REST_AFTER_MATING

        self.SIM.rabbit_instances.append(Rabbit(self.SIM.rabbits, Rabbit, self.x, self.y))
        
        self.SIM.rabbit_instances.append(Rabbit(self.SIM.rabbits, Rabbit, self.x, self.y))

        self.just_mated = Rabbit.MATING_BREAK
        self.rest = Rabbit.REST_AFTER_MATING
        del self.SIM.mating_male_rabbits[mate.KEY]
      except KeyError:
        self.state = 'searching for mate'




    else:
      self.rest = Rabbit.REST_AFTER_MOVING
      
      self.x += self.x_direction
      self.y += self.y_direction
      
      self.SIM.rabbits.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
      if self.goal == 'mating' and self.GENDER == 'female':
        self.SIM.mating_female_rabbits.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
        
      elif self.goal == 'mating' and self.GENDER == 'male':
        self.SIM.mating_male_rabbits.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
  



  def check_for_fox(self):
    if self.rest > 0:
      return

    
    self.search_for_object('running', Rabbit.FOX_RANGE)

    if len(self.visible_items) > 0:
      self.goal = 'running'

      self.point_towards_object()
      self.x_direction = self.x_direction * -1
      self.y_direction = self.y_direction * -1

      if self.x <= WARN_ABOUT_WALL and self.y_direction == 0:
        if self.y >= WIDTH/2: self.y_direction = -1
        elif self.y < WIDTH/2: self.y_direction = 1
        
      elif self.x >= (WIDTH - WARN_ABOUT_WALL) and self.y_direction == 0:
        if self.y >= WIDTH/2: self.y_direction = -1
        elif self.y < WIDTH/2: self.y_direction = 1

      
      if self.y <= WARN_ABOUT_WALL and self.x_direction == 0:
        if self.x >= WIDTH/2: self.x_direction = -1
        elif self.x < WIDTH/2: self.x_direction = 1
      
      
      elif self.y >= (WIDTH - WARN_ABOUT_WALL) and self.x_direction == 0:
        if self.x >= WIDTH/2: self.x_direction = -1
        elif self.x < WIDTH/2: self.x_direction = 1
      
      self.avoid_edge()
      return True
    
    else:
      return False










class Fox(Animal):

  CLASS_TYPE = 'Fox'
  MAX_RANDOM_MOVES = 10
  HUNGER_INCRIMENT = 0.003
  THIRST_INCRIMENT = 0.01
  BASE_CUTOFF = 0.4 #0.2
  FOOD_RESTORATION = 0.75 #1
  VIEW_RANGE = 15
  MATING_VIEW_RANGE = 1000
  
  REST_AFTER_EATING = 40
  REST_AFTER_DRINKING = 40 #was 40
  REST_AFTER_MATING = 100
  REST_AFTER_MOVING = 4 #5

  MATING_BREAK = 500
  

  def __init__(self, Fox, x=None, y=None):
    self.x = x
    self.y = y
    super().__init__(Fox, self.x, self.y)
    
    
    
    self.BASE_REPRODUCTIVE_URGE = 0.6
    self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE

  def move(self):
    if self.rest > 0:
      self.rest -= 1
      return
    
    if self.state == 'eating':
      
      try:
        target_food = self.SIM.rabbits[self.target['key']] ['self']
        self.SIM.rabbits.pop(target_food.KEY)
        self.hunger -= Fox.FOOD_RESTORATION
        if self.hunger < 0:
          self.hunger = 0

      except KeyError:

        self.state = 'searching for food'
        return
      try:
        self.SIM.mating_female_rabbits.pop(target_food.KEY)
      except KeyError:
        pass
      try:
        self.SIM.mating_male_rabbits.pop(target_food.KEY)
      except KeyError:
        pass

      self.SIM.rabbit_instances.remove(target_food)
      self.rest = Fox.REST_AFTER_EATING

      #self.goal = None
      #self.state = None
        
    elif self.state == 'drinking':
      self.thirst = 0
      self.rest = Fox.REST_AFTER_DRINKING

      #self.goal = None
      #self.state = None

    elif self.state == 'mating' and self.GENDER == 'female':
      self.SIM.fox_instances.append(Fox(self.SIM.foxes, Fox, self.x, self.y))
      
      self.just_mated = Fox.MATING_BREAK
      self.rest = Fox.REST_AFTER_MATING
      #self.goal = None
      #self.state = None
      del self.SIM.mating_female_foxes[self.KEY]

      mate = self.SIM.mating_male_foxes[self.target['key']]['self']

      mate.just_mated = Fox.MATING_BREAK
      mate.rest = Fox.REST_AFTER_MATING
      #mate.goal = None
      #mate.state = None
      del self.SIM.mating_male_foxes[mate.KEY]

    else:
      self.rest = Fox.REST_AFTER_MOVING
      self.x += self.x_direction
      self.y += self.y_direction
      
      self.SIM.foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
      if self.goal == 'mating' and self.GENDER == 'female':
        self.SIM.mating_female_foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
        
      elif self.goal == 'mating' and self.GENDER == 'male':
        self.SIM.mating_male_foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})

    

class Food:

  SIM = SimState()
  total_food = 0
  key = 0
  MAX_TIMES_EATEN = 10
  MAX_FOOD = 600
  STARTING_FOOD = round(MAX_FOOD/2)
  
  wait_to_add_food = 0
  FOOD_WAIT = 10

  @staticmethod
  def del_and_create_food():
    for food in self.SIM.food_instances:
      if food.times_eaten >= Food.MAX_TIMES_EATEN:
        del self.SIM.foods[food.KEY]
        self.SIM.food_instances.remove(food)


    if len(self.SIM.food_instances) < Food.MAX_FOOD:
      Food.wait_to_add_food += 1
      if Food.wait_to_add_food >= Food.FOOD_WAIT:
        Food.wait_to_add_food = 0
        self.SIM.food_instances.append(Food())

  
  def __init__(self, original=False):

    Food.total_food += 1
    Food.key += 1
    self.KEY = Food.key

  
    if original is False:
      self.x = random.randint(0, WIDTH)
      self.y = random.randint(0, HEIGHT)
      while True:
        
        for i in self.SIM.water:
          if self.x == self.SIM.water[i]['x'] and self.y == self.SIM.water[i]['y']:
            finished = False
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            continue
        break

      self.SIM.foods.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
    
    self.times_eaten = 0





def mark_water(win, water, WIDTH, HEIGHT):
  key = 0
  for y_cord in range(HEIGHT):
    for x_cord in range(WIDTH):
      x = math.floor(x_cord * GRID_SIZE + (GRID_SIZE / 2))
      y = math.ceil(y_cord * GRID_SIZE + (GRID_SIZE / 2))
      pixel = win.get_at((x, y))
      if pixel == (0, 162, 232):
        key += 1
        water.update({key: {'x': x_cord, 'y': y_cord}})
  print(water)
  exit()



def graph(record_fox_instances, record_rabbit_instances):
  len_of_fox_record = len(record_fox_instances)
  len_of_rabbit_record = len(record_rabbit_instances)
  plt.plot(range(len_of_fox_record), record_fox_instances, linestyle='solid', color='red', label='Foxes')
  plt.plot(range(len_of_rabbit_record), record_rabbit_instances, linestyle='solid', color='blue', label='Rabbits')
  plt.title('Foxes and Rabbits over time')
  plt.xlabel('Seconds')
  plt.ylabel('Population')
  plt.legend()
  plt.show()

def loading_bar(win, BAR_X, BAR_Y, COLOUR, need, name):
  RECT = pygame.Surface((need*BAR_LENGHT, BAR_WIDTH))
  RECT.set_alpha(200)
  RECT.fill(COLOUR)
  win.blit(RECT, (BAR_X,BAR_Y))

  RECT = pygame.Surface((BAR_LENGHT, BAR_WIDTH))
  RECT.set_alpha(100)
  RECT.fill(COLOUR)
  win.blit(RECT, (BAR_X,BAR_Y))

  bar_name = BAR_FONT.render(name, True, BLACK)
  win.blit(bar_name, (BAR_X+5, BAR_Y+5))



def add_input(fox_instances, rabbit_instances, speed):
  speed_or_animals = input('Change speed or animals(s/a): ')
  if speed_or_animals == 's':
    multiple = int(input('Enter speed(multiples base speed by input): '))
    del speed[0]
    speed.append(round(multiple*FPS))
    
  if speed_or_animals == 'a':
    rabbits_or_foxes = input('Add foxes or rabbits(r/f): ')
    if rabbits_or_foxes == 'f':
      add_foxes = int(input('Enter number of foxes to add: '))
      for i in range(add_foxes):
        fox_instances.append(Fox(foxes, Fox))
    if rabbits_or_foxes == 'r':
      add_rabbits = int(input('Enter number of rabbits to add: '))
      for i in range(add_rabbits):
        rabbit_instances.append(Rabbit(rabbits, Rabbit))



def display_tracked_object(tracked_object, instances, win):
  if tracked_object in instances:
    WHITE_RECT = pygame.Surface((130, 200))
    WHITE_RECT.set_alpha(100)
    WHITE_RECT.fill(WHITE)
    
    win.blit(WHITE_RECT, (5,WHITE_RECT_Y))
    state_colour = BLACK
    adjusted_font_width = 30
    if tracked_object.state is not None:    
      
      FONT_SIZE = 30
    
      letters = len(tracked_object.state)
      MAX_LETTERS = 10
      if letters > MAX_LETTERS:
        adjusted_font_width = round(MAX_LETTERS/letters*FONT_SIZE)
      else:
        adjusted_font_width = FONT_SIZE



    tracked_object_state_font = pygame.font.SysFont(None, adjusted_font_width)
    
    if tracked_object.Animal_Class.CLASS_TYPE == 'Fox':
      instance_colour = ORANGE
    if tracked_object.Animal_Class.CLASS_TYPE == 'Rabbit':
      instance_colour = BLUE
    
    instance_type = tracked_object_font.render((tracked_object.Animal_Class.CLASS_TYPE), True, instance_colour)

    if tracked_object.goal == 'water':
      state_colour = BLUE
    if tracked_object.goal == 'reproduce':
      state_colour = RED
    if tracked_object.goal == 'food':
      state_colour = YELLOW
    if tracked_object.goal == 'running':
      state_colour = ORANGE

    word_state = state_font.render('State:', True, BLACK)
    tracked_object_state = tracked_object_state_font.render(tracked_object.state, True, state_colour)

    

    #draw a box around the chosen instance###
    pygame.draw.rect(win, RED, pygame.Rect(tracked_object.x*GRID_SIZE, tracked_object.y*GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)


    loading_bar(win, YELLOW_BAR_X, YELLOW_BAR_Y, YELLOW, tracked_object.hunger, 'hunger')
    loading_bar(win, YELLOW_BAR_X, YELLOW_BAR_Y+30, BLUE, tracked_object.thirst, 'thirst')
    loading_bar(win, YELLOW_BAR_X, YELLOW_BAR_Y+60, RED, tracked_object.reproductive_urge, 'reproduce')
    CENTER_OF_WHITE_RECT = instance_type.get_rect(center=(130/2, WHITE_RECT_Y + 20))
    win.blit(instance_type, CENTER_OF_WHITE_RECT)
    win.blit(word_state, (10, WHITE_RECT_Y + 40))
    win.blit(tracked_object_state, (20, WHITE_RECT_Y + 60))



tracked_object_font = pygame.font.SysFont(None, 30)
font = pygame.font.SysFont(None, 40)

state_font = pygame.font.SysFont(None, 30)

def draw_window(win, rabbit_instances, fox_instances, food_instances, tracked_object):
  win.blit(BACKGROUND, (0, 0))
  for food in food_instances:
    x = food.x * GRID_SIZE
    y = food.y * GRID_SIZE
    pygame.draw.rect(win, YELLOW, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))

  for rabbit in rabbit_instances:
    x = rabbit.x * GRID_SIZE
    y = rabbit.y * GRID_SIZE
    pygame.draw.rect(win, GREY, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))

  for fox in fox_instances:
    x = fox.x * GRID_SIZE
    y = fox.y * GRID_SIZE
    pygame.draw.rect(win, ORANGE, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))
  
  instances = rabbit_instances + fox_instances

  
  if tracked_object in instances and tracked_object != None:
    display_tracked_object(tracked_object, instances, win)



      

  
  


  rabbit_counter = font.render('Rabbits: {}'.format(len(rabbit_instances)), True, (0, 0, 0))
  rabbit_counter.set_alpha(172)

  fox_counter = font.render('Foxes: {}'.format(len(fox_instances)), True, (0, 0, 0))
  fox_counter.set_alpha(172)
  win.blit(rabbit_counter, (10, 10))
  win.blit(fox_counter, (10, 40))


  pygame.display.update()
  

def main():
  
  SIM = SimState()
  hunger_deaths = 0
  thirst_deaths = 0
  eaten_rabbits = 0



  clock = pygame.time.Clock()
  run = True
  task_running = False
  
  print("\n \033[39;49;1m Welcome to Ecosystem simulator\033[0m")

  starting_rabbits = int(input('rabbits: '))

  starting_foxes = int(input('foxes: '))

  SIM.rabbit_instances = [Rabbit(rabbits, Rabbit) for _ in range(starting_rabbits)]
  if starting_rabbits == 2:
    male = SIM.rabbit_instances[0]
    male.GENDER = 'male'

    female = SIM.rabbit_instances[1]
    female.GENDER = 'female'
  
  SIM.fox_instances = [Fox(SIM.foxes, Fox) for _ in range(starting_foxes)]
  if starting_foxes == 2:
    male = SIM.fox_instances[0]
    male.GENDER = 'male'

    female = SIM.fox_instances[1]
    female.GENDER = 'female'

  SIM.food_instances = [Food() for _ in range(Food.STARTING_FOOD)]

  original_food = Food(True)
  win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  pygame.display.set_caption('ecosystem simulator')
  
  record_fox_instances = []
  record_rabbit_instances = []
  loop_counter = 0
  tracked_object = None

  task = threading.Thread(target = add_input, args=[SIM.fox_instances, SIM.rabbit_instances, speed])
  while run:
    clock.tick(speed[0])
    loop_counter += 1
    if loop_counter % FPS == 0:
      record_fox_instances.append(len(SIM.fox_instances))
      record_rabbit_instances.append(len(SIM.rabbit_instances))
    a = time()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        position = []
        mouse_x = math.floor(pos[0]/GRID_SIZE)
        mouse_y = math.floor(pos[1]/GRID_SIZE)
        clicked_foxes = [fox for fox in SIM.fox_instances if fox.x == mouse_x and fox.y == mouse_y]
        clicked_rabbits = [rabbit for rabbit in rabbit_instances if rabbit.x == mouse_x and rabbit.y == mouse_y]
        clicked_instances =  clicked_rabbits + clicked_foxes
        if len(clicked_instances) > 0:
          tracked_object = clicked_instances[-1]
        clicked_foxes = []
        clicked_rabbits = []
        clicked_instances = []
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          tracked_object = None
        if event.key == pygame.K_r:
          try:
            tracked_object = random.choice(SIM.rabbit_instances)
          except IndexError:
            pass
        if event.key == pygame.K_f:
          try:
            tracked_object = random.choice(SIM.fox_instances)
          except IndexError:
            pass
    

    if not task.is_alive():
      task = threading.Thread(target = add_input, args=[SIM.fox_instances, SIM.rabbit_instances, speed])
      task.start()
      


    for fox in SIM.fox_instances:
      fox.set_state(SIM.mating_male_foxes, SIM.mating_female_foxes, SIM.rabbits)
      if fox.state == 'eating': eaten_rabbits += 1
      if max(fox.thirst, fox.hunger) > Animal.GOAL_CUTOFF:
        del SIM.foxes[fox.KEY]

        try:
          SIM.mating_female_foxes.pop(fox.KEY)
        except KeyError:
          pass
        try:
          SIM.mating_male_foxes.pop(fox.KEY)
        except KeyError:
          pass

        SIM.fox_instances.remove(fox)

    for fox in SIM.fox_instances:
      fox.move(SIM.fox_instances, SIM.rabbit_instances)

    
    for rabbit in SIM.rabbit_instances:
      fox_in_range = rabbit.check_for_fox()
      if fox_in_range is False:
        rabbit.set_state(SIM.mating_male_rabbits, SIM.mating_female_rabbits, SIM.foods)
        
    


      if max(rabbit.thirst, rabbit.hunger) > Animal.GOAL_CUTOFF:
        if rabbit.thirst > rabbit.hunger:
          thirst_deaths += 1
        else:
          hunger_deaths += 1


        del SIM.rabbits[rabbit.KEY]
        SIM.mating_female_rabbits.pop(rabbit.KEY, None)
        SIM.mating_male_rabbits.pop(rabbit.KEY, None)
        SIM.rabbit_instances.remove(rabbit)


    for rabbit in SIM.rabbit_instances:
      rabbit.move(SIM.rabbit_instances)

    original_food.del_and_create_food(SIM.food_instances, SIM.foods)
    
    b = time()


    if SIM.rabbit_instances == 0 and SIM.fox_instances == 0:
      run = False
    draw_window(win, SIM.rabbit_instances, SIM.fox_instances, SIM.food_instances, tracked_object)
  print('\nthirst deaths: ', thirst_deaths)
  print('hunger deaths: ', hunger_deaths)
  print('eaten rabbits: ', round(eaten_rabbits/60))
  pygame.quit()
  graph(record_fox_instances, record_rabbit_instances)
  
if __name__ == '__main__':
  main()

