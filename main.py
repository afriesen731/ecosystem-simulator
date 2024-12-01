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

WIN_WIDTH = WIDTH * GRID_SIZE + GRID_SIZE
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
BAR_LENGTH = 100
BAR_WIDTH = 20
WARN_ABOUT_WALL = 5
BAR_FONT = pygame.font.SysFont(None, 20)

class SimState:
  _instance = None
  _initialized = False

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super(SimState, cls).__new__(cls, *args, **kwargs)
    return cls._instance

  def __init__(self):
    if self._initialized:
      return

    self.rabbit_instances = []
    self.fox_instances = []
    self.food_instances = []
    self.foods = {}
    self.rabbits = {}
    self.mating_male_rabbits = {}
    self.mating_female_rabbits = {}
    self.foxes = {}
    self.mating_male_foxes = {}
    self.mating_female_foxes = {}

    with open('water.json', 'r') as file:
      self.water = json.load(file)

    self._initialized = True

class Animal:
  """Base class representing an animal in the simulation."""

  GOAL_CUTOFF = 1
  SIM = SimState()

  pythagorean_theorem = lambda a, b: math.sqrt(a ** 2 + b ** 2)

  key = 0

  def __init__(self, x=None, y=None):
    """
    Initialize a new Animal instance.

    Args:
        x (int, optional): X-coordinate of the animal. Default is a random value.
        y (int, optional): Y-coordinate of the animal. Default is a random value.
    """
    Animal.key += 1
    self.KEY = Animal.key

    self.GENDER = random.choice(['male', 'female'])

    if x is None:
      self.x = random.randint(0, WIDTH)
    if y is None:
      self.y = random.randint(0, HEIGHT)
    else:
      self.x = x
      self.y = y

    self.goal = None
    self.state = None

    self.x_direction = 0
    self.y_direction = 0

    self.thirst = 0.0
    self.hunger = 0.01
    self.BASE_REPRODUCTIVE_URGE = 0.6
    self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE

    # Ensure that MATING_BREAK is defined in subclasses
    self.just_mated = random.randint(0, self.__class__.MATING_BREAK)

    self.rest = 1

    self.random_movement_counter = 0

  def set_state(self):
    self.update_needs()
    self.determine_goal()
    self.handle_goal_actions()
    self.avoid_edge()

  def update_needs(self):
    if self.rest > 0:
      return
    self.thirst += self.__class__.THIRST_INCREMENT
    self.hunger += self.__class__.HUNGER_INCREMENT

    if self.just_mated > 0:
      self.reproductive_urge = 0
      self.just_mated -= 1
      if self.just_mated <= 0:
        self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE

  def determine_goal(self):
    if self.state == 'found mate':
      return

    previous_goal = self.goal
    highest_need = max(self.thirst, self.hunger, self.reproductive_urge, self.__class__.BASE_CUTOFF)

    if self.thirst == highest_need and self.thirst > self.__class__.BASE_CUTOFF:
      self.set_goal('water', 'searching for water')
    elif self.hunger == highest_need and self.hunger > self.__class__.BASE_CUTOFF:
      self.set_goal('food', 'searching for food')
    elif self.reproductive_urge == highest_need and self.reproductive_urge > self.__class__.BASE_CUTOFF:
      self.set_goal('reproduce', 'searching for mate')
      self.add_to_mating_pool()
    else:
      self.goal = None
      self.state = None
      self.move_randomly()

    self.remove_from_mating_pool_if_goal_changed(previous_goal)

  def set_goal(self, goal, state):
    if self.goal != goal:
      self.goal = goal
      self.state = state

  def add_to_mating_pool(self):
    mating_pool = self.get_mating_pool()
    mating_pool[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}

  def remove_from_mating_pool_if_goal_changed(self, previous_goal):
    if previous_goal == 'reproduce' and self.goal != 'reproduce':
      mating_pool = self.get_mating_pool(gender=self.GENDER)
      mating_pool.pop(self.KEY, None)

  def get_mating_pool(self, gender=None):
    if gender is None:
      gender = 'female' if self.GENDER == 'male' else 'male'

    if self.__class__.CLASS_TYPE == 'Rabbit':
      if gender == 'female':
        return self.SIM.mating_female_rabbits
      else:
        return self.SIM.mating_male_rabbits
    elif self.__class__.CLASS_TYPE == 'Fox':
      if gender == 'female':
        return self.SIM.mating_female_foxes
      else:
        return self.SIM.mating_male_foxes

  def handle_goal_actions(self):
    if self.goal == 'food':
      self.handle_food_goal()
    elif self.goal == 'water':
      self.handle_water_goal()
    elif self.goal == 'reproduce':
      self.handle_reproduce_goal()

  def handle_food_goal(self):
    if self.state == 'searching for food':
      target_objects = self.SIM.foods if self.__class__.CLASS_TYPE == 'Rabbit' else self.SIM.rabbits
      self.search_for_object(target_objects, 'found food')
      if self.state == 'searching for food':
        self.move_randomly()
    elif self.state == 'found food':
      target_objects = self.SIM.foods if self.__class__.CLASS_TYPE == 'Rabbit' else self.SIM.rabbits
      self.update_target(target_objects, 'searching for food')
      if self.state == 'found food':
        self.point_towards_object()
        if self.target['distance'] <= 1:
          self.state = 'eating'

  def handle_water_goal(self):
    if self.state == 'searching for water':
      self.search_for_object(self.SIM.water, 'found water')
      if self.state == 'searching for water':
        self.move_randomly()
    elif self.state == 'found water':
      self.update_target(self.SIM.water, 'searching for water')
      if self.state == 'found water':
        self.point_towards_object()
        if self.target['distance'] <= 1:
          self.state = 'drinking'

  def handle_reproduce_goal(self):
    mating_pool = self.get_mating_pool()
    if self.state == 'searching for mate':
      self.search_for_object(mating_pool, 'found mate', self.__class__.MATING_VIEW_RANGE)
      if self.state == 'found mate':
        self.find_mate_in_pool(mating_pool)
      if self.state == 'searching for mate':
        self.move_randomly()
    elif self.state == 'found mate':
      self.update_target(mating_pool, 'searching for mate', self.__class__.MATING_VIEW_RANGE)
      if self.state == 'found mate':
        self.point_towards_object()
        if self.target.get('distance') is not None and self.target['distance'] <= 1:
          self.state = 'mating'
          mate = mating_pool[self.target['key']]['self']
          mate.state = 'mating'
          mate.target = {'key': self.KEY}

  def find_mate_in_pool(self, mating_pool):
    for mate in self.visible_items:
      potential_mate = mating_pool[mate['key']]['self']
      if potential_mate.state == 'searching for mate':
        self.target = mate
        potential_mate.state = 'found mate'
        potential_mate.target = {'key': self.KEY}
        break
    else:
      self.state = 'searching for mate'

  def search_for_object(self, list_of_items, state_if_found, VIEW_RANGE=None):
    if VIEW_RANGE is None:
      VIEW_RANGE = self.__class__.VIEW_RANGE
    self.visible_items = []
    calculate_distance_cutoff = (math.sqrt(2)/2) * VIEW_RANGE * 2
    for item in list_of_items:
      current_item = list_of_items[item]
      x_distance = current_item['x'] - self.x
      positive_x_distance = abs(x_distance)
      y_distance = current_item['y'] - self.y
      positive_y_distance = abs(y_distance)
      total_positive_distance = positive_x_distance + positive_y_distance
      if total_positive_distance < calculate_distance_cutoff:
        distance = Animal.pythagorean_theorem(positive_x_distance, positive_y_distance)
        if distance <= VIEW_RANGE:
          self.visible_items.append({
            'key': item,
            'distance': distance,
            'x_distance': x_distance,
            'y_distance': y_distance,
            'positive_x_distance': positive_x_distance,
            'positive_y_distance': positive_y_distance
          })
    if self.visible_items:
      self.visible_items.sort(key=lambda x: x['distance'])
      self.target = self.visible_items[0]
      self.state = state_if_found

  def point_towards_object(self):
    x_dist = self.target.get('x_distance', 0)
    y_dist = self.target.get('y_distance', 0)
    self.x_direction = (x_dist > 0) - (x_dist < 0)
    self.y_direction = (y_dist > 0) - (y_dist < 0)

  def update_target(self, list_of_items, state_if_out_of_range, VIEW_RANGE=None):
    item = list_of_items.get(self.target.get('key'))
    if VIEW_RANGE is None:
      VIEW_RANGE = self.__class__.VIEW_RANGE
    if item is None:
      self.state = state_if_out_of_range
      return
    x_distance = item['x'] - self.x
    positive_x_distance = abs(x_distance)
    y_distance = item['y'] - self.y
    positive_y_distance = abs(y_distance)
    distance = Animal.pythagorean_theorem(positive_x_distance, positive_y_distance)
    if distance >= VIEW_RANGE:
      self.state = state_if_out_of_range
      return
    self.target = {
      'key': self.target['key'],
      'distance': distance,
      'x_distance': x_distance,
      'y_distance': y_distance,
      'positive_x_distance': positive_x_distance,
      'positive_y_distance': positive_y_distance
    }

  def move_randomly(self):
    self.random_movement_counter += 1
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
    elif self.random_movement_counter >= 2 and self.random_movement_counter <= self.__class__.MAX_RANDOM_MOVES:
      self.random_direction = random.random()
      if self.x_direction == 0:
        if self.random_direction >= 0.6:
          self.x_direction = random.choice([-1, 1])
          if self.random_direction >= 0.8:
            self.y_direction = 0
      elif self.y_direction == 0:
        if self.random_direction >= 0.6:
          self.y_direction = random.choice([-1, 1])
          if self.random_direction >= 0.8:
            self.x_direction = 0
      if self.y_direction != 0 and self.x_direction != 0:
        if self.random_direction >= 0.6:
          if random.choice(['x', 'y']) == 'x':
            self.x_direction = 0
          else:
            self.y_direction = 0
      if self.random_movement_counter == self.__class__.MAX_RANDOM_MOVES:
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

  def check_rest(self):
    if self.rest > 0:
      self.rest -= 1
      return True
    return False

  def move(self):
    if self.check_rest():
      return

    if self.state == 'eating':
      self.handle_eating()
    elif self.state == 'drinking':
      self.handle_drinking()
    elif self.state == 'mating':
      self.handle_mating()
    else:
      self.handle_movement()

  def handle_drinking(self):
    self.thirst = 0
    self.rest = self.REST_AFTER_DRINKING

  def handle_movement(self):
    self.rest = self.REST_AFTER_MOVING
    self.x += self.x_direction
    self.y += self.y_direction
    self.update_position_in_sim()
    if self.goal == 'reproduce':
      self.update_mating_pool_position()

  def update_position_in_sim(self):
    pass  # To be implemented in subclasses

  def update_mating_pool_position(self):
    mating_pool = self.get_mating_pool(gender=self.GENDER)
    mating_pool[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}

class Rabbit(Animal):
  CLASS_TYPE = 'Rabbit'
  HUNGER_INCREMENT = 0.005
  THIRST_INCREMENT = 0.01
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
  FOX_RANGE = 8

  def __init__(self, x=None, y=None):
    super().__init__(x, y)
    self.SIM.rabbits[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}
    self.SIM.rabbit_instances.append(self)

  def move(self):
    super().move()

  def handle_eating(self):
    try:
      self.hunger -= self.FOOD_RESTORATION
      if self.hunger < 0:
        self.hunger = 0
      key = self.target['key']
      target_food = self.SIM.foods[key]['self']
      target_food.times_eaten += 1
      self.rest = self.REST_AFTER_EATING
    except KeyError:
      self.state = 'searching for food'

  def handle_mating(self):
    if self.GENDER == 'female':
      self.SIM.mating_female_rabbits.pop(self.KEY, None)
      try:
        mate = self.SIM.mating_male_rabbits[self.target['key']]['self']
        mate.just_mated = self.MATING_BREAK
        mate.rest = self.REST_AFTER_MATING
        self.create_offspring()
        self.just_mated = self.MATING_BREAK
        self.rest = self.REST_AFTER_MATING
        self.SIM.mating_male_rabbits.pop(mate.KEY, None)
      except KeyError:
        self.state = 'searching for mate'

  def create_offspring(self):
    Rabbit(self.x, self.y)
    Rabbit(self.x, self.y)

  def update_position_in_sim(self):
    self.SIM.rabbits[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}

  def detect_predators(self):
    if self.rest > 0:
      return False

    self.search_for_object(self.SIM.foxes, 'running', self.FOX_RANGE)
    if self.visible_items:
      self.goal = 'running'
      self.escape_predator()
      return True
    return False

  def escape_predator(self):
    self.point_towards_object()
    self.x_direction *= -1
    self.y_direction *= -1
    self.adjust_to_avoid_walls()
    self.avoid_edge()

  def adjust_to_avoid_walls(self):
    if self.x <= WARN_ABOUT_WALL and self.y_direction == 0:
      self.y_direction = -1 if self.y >= WIDTH / 2 else 1
    elif self.x >= (WIDTH - WARN_ABOUT_WALL) and self.y_direction == 0:
      self.y_direction = -1 if self.y >= WIDTH / 2 else 1
    if self.y <= WARN_ABOUT_WALL and self.x_direction == 0:
      self.x_direction = -1 if self.x >= WIDTH / 2 else 1
    elif self.y >= (HEIGHT - WARN_ABOUT_WALL) and self.x_direction == 0:
      self.x_direction = -1 if self.x >= WIDTH / 2 else 1

class Fox(Animal):
  CLASS_TYPE = 'Fox'
  MAX_RANDOM_MOVES = 10
  HUNGER_INCREMENT = 0.003
  THIRST_INCREMENT = 0.01
  BASE_CUTOFF = 0.4
  FOOD_RESTORATION = 0.75
  VIEW_RANGE = 15
  MATING_VIEW_RANGE = 1000

  REST_AFTER_EATING = 40
  REST_AFTER_DRINKING = 40
  REST_AFTER_MATING = 100
  REST_AFTER_MOVING = 4

  MATING_BREAK = 500

  def __init__(self, x=None, y=None):
    super().__init__(x, y)
    self.SIM.foxes[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}
    self.SIM.fox_instances.append(self)
    self.BASE_REPRODUCTIVE_URGE = 0.6
    self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE

  def move(self):
    super().move()

  def handle_eating(self):
    try:
      target_rabbit = self.SIM.rabbits[self.target['key']]['self']
      self.SIM.rabbits.pop(target_rabbit.KEY, None)
      self.SIM.rabbit_instances.remove(target_rabbit)
      self.hunger -= self.FOOD_RESTORATION
      if self.hunger < 0:
        self.hunger = 0
      self.rest = self.REST_AFTER_EATING
      self.remove_rabbit_from_mating_pools(target_rabbit)
    except KeyError:
      self.state = 'searching for food'

  def remove_rabbit_from_mating_pools(self, rabbit):
    self.SIM.mating_female_rabbits.pop(rabbit.KEY, None)
    self.SIM.mating_male_rabbits.pop(rabbit.KEY, None)

  def handle_mating(self):
    if self.GENDER == 'female':
      try:
        mate_entry = self.SIM.mating_male_foxes.get(self.target.get('key'))
        if mate_entry:
          mate = mate_entry['self']
          if self.is_adjacent(mate):
            self.rest = self.REST_AFTER_MOVING  # Wait for mating
          else:
            mate.just_mated = self.MATING_BREAK
            mate.rest = self.REST_AFTER_MATING
            self.SIM.mating_male_foxes.pop(mate.KEY, None)
            self.create_offspring()
      except KeyError:
        self.state = 'searching for mate'
        return
      self.just_mated = self.MATING_BREAK
      self.rest = self.REST_AFTER_MATING
      self.SIM.mating_female_foxes.pop(self.KEY, None)

  def is_adjacent(self, other):
    return abs(other.x - self.x) == 1 and abs(other.y - self.y) == 1

  def create_offspring(self):
    Fox(self.x, self.y)

  def update_position_in_sim(self):
    self.SIM.foxes[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}

class Food:
  SIM = SimState()
  total_food = 0
  key = 0
  MAX_TIMES_EATEN = 10
  MAX_FOOD = 600
  STARTING_FOOD = round(MAX_FOOD / 2)
  wait_to_add_food = 0
  FOOD_WAIT = 10

  @classmethod
  def del_and_create_food(cls):
    # Remove food that has been eaten too many times
    to_remove = []
    for food in cls.SIM.food_instances:
      if food.times_eaten >= cls.MAX_TIMES_EATEN:
        cls.SIM.foods.pop(food.KEY, None)
        to_remove.append(food)
    for food in to_remove:
      cls.SIM.food_instances.remove(food)

    # Add new food if below MAX_FOOD
    if len(cls.SIM.food_instances) < cls.MAX_FOOD:
      cls.wait_to_add_food += 1
      if cls.wait_to_add_food >= cls.FOOD_WAIT:
        cls.wait_to_add_food = 0
        Food()

  def __init__(self, original=False):
    Food.total_food += 1
    Food.key += 1
    self.KEY = Food.key
    self.times_eaten = 0

    if not original:
      self.x = random.randint(0, WIDTH)
      self.y = random.randint(0, HEIGHT)
      # Ensure food is not placed on water
      while any(self.x == w['x'] and self.y == w['y'] for w in self.SIM.water.values()):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

      self.SIM.foods[self.KEY] = {'x': self.x, 'y': self.y, 'self': self}
      self.SIM.food_instances.append(self)

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
  RECT = pygame.Surface((need * BAR_LENGTH, BAR_WIDTH))
  RECT.set_alpha(200)
  RECT.fill(COLOUR)
  win.blit(RECT, (BAR_X, BAR_Y))

  RECT = pygame.Surface((BAR_LENGTH, BAR_WIDTH))
  RECT.set_alpha(100)
  RECT.fill(COLOUR)
  win.blit(RECT, (BAR_X, BAR_Y))

  bar_name = BAR_FONT.render(name, True, BLACK)
  win.blit(bar_name, (BAR_X + 5, BAR_Y + 5))

def add_input(speed):
  SIM = SimState()
  while (True):
    speed_or_animals = input('Change speed or animals(s/a): ')
    if speed_or_animals == 's':
      multiple = int(input('Enter speed(multiples base speed by input): '))
      speed[0] = round(multiple * FPS)
    elif speed_or_animals == 'a':
      rabbits_or_foxes = input('Add foxes or rabbits(r/f): ')
      if rabbits_or_foxes == 'f':
        add_foxes = int(input('Enter number of foxes to add: '))
        for _ in range(add_foxes):
          Fox()
      elif rabbits_or_foxes == 'r':
        add_rabbits = int(input('Enter number of rabbits to add: '))
        for _ in range(add_rabbits):
          Rabbit()

def display_tracked_object(tracked_object, win):
  SIM = SimState()
  instances = SIM.rabbit_instances + SIM.fox_instances
  if tracked_object in instances:
    WHITE_RECT = pygame.Surface((130, 200))
    WHITE_RECT.set_alpha(100)
    WHITE_RECT.fill(WHITE)
    win.blit(WHITE_RECT, (5, WHITE_RECT_Y))
    state_colour = BLACK
    adjusted_font_width = 30
    if tracked_object.state is not None:
      FONT_SIZE = 30
      letters = len(tracked_object.state)
      MAX_LETTERS = 10
      if letters > MAX_LETTERS:
        adjusted_font_width = round(MAX_LETTERS / letters * FONT_SIZE)
      else:
        adjusted_font_width = FONT_SIZE

    tracked_object_state_font = pygame.font.SysFont(None, adjusted_font_width)

    if tracked_object.__class__.CLASS_TYPE == 'Fox':
      instance_colour = ORANGE
    elif tracked_object.__class__.CLASS_TYPE == 'Rabbit':
      instance_colour = BLUE

    instance_type = tracked_object_font.render((tracked_object.__class__.CLASS_TYPE), True, instance_colour)

    if tracked_object.goal == 'water':
      state_colour = BLUE
    elif tracked_object.goal == 'reproduce':
      state_colour = RED
    elif tracked_object.goal == 'food':
      state_colour = YELLOW
    elif tracked_object.goal == 'running':
      state_colour = ORANGE

    word_state = state_font.render('State:', True, BLACK)
    tracked_object_state = tracked_object_state_font.render(tracked_object.state, True, state_colour)

    # Draw a box around the chosen instance
    pygame.draw.rect(win, RED, pygame.Rect(tracked_object.x * GRID_SIZE, tracked_object.y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    loading_bar(win, YELLOW_BAR_X, YELLOW_BAR_Y, YELLOW, tracked_object.hunger, 'hunger')
    loading_bar(win, YELLOW_BAR_X, YELLOW_BAR_Y + 30, BLUE, tracked_object.thirst, 'thirst')
    loading_bar(win, YELLOW_BAR_X, YELLOW_BAR_Y + 60, RED, tracked_object.reproductive_urge, 'reproduce')
    CENTER_OF_WHITE_RECT = instance_type.get_rect(center=(130 / 2, WHITE_RECT_Y + 20))
    win.blit(instance_type, CENTER_OF_WHITE_RECT)
    win.blit(word_state, (10, WHITE_RECT_Y + 40))
    win.blit(tracked_object_state, (20, WHITE_RECT_Y + 60))

tracked_object_font = pygame.font.SysFont(None, 30)
font = pygame.font.SysFont(None, 40)
state_font = pygame.font.SysFont(None, 30)

def draw_window(win, tracked_object):
  SIM = SimState()
  win.blit(BACKGROUND, (0, 0))
  for food in SIM.food_instances:
    x = food.x * GRID_SIZE
    y = food.y * GRID_SIZE
    pygame.draw.rect(win, YELLOW, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))

  for rabbit in SIM.rabbit_instances:
    x = rabbit.x * GRID_SIZE
    y = rabbit.y * GRID_SIZE
    pygame.draw.rect(win, GREY, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))

  for fox in SIM.fox_instances:
    x = fox.x * GRID_SIZE
    y = fox.y * GRID_SIZE
    pygame.draw.rect(win, ORANGE, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))

  if tracked_object is not None:
    display_tracked_object(tracked_object, win)

  rabbit_counter = font.render('Rabbits: {}'.format(len(SIM.rabbit_instances)), True, (0, 0, 0))
  rabbit_counter.set_alpha(172)

  fox_counter = font.render('Foxes: {}'.format(len(SIM.fox_instances)), True, (0, 0, 0))
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

  print("\n \033[39;49;1m Welcome to Ecosystem simulator\033[0m")

  starting_rabbits = int(input('rabbits: '))
  starting_foxes = int(input('foxes: '))

  # Initialize rabbits
  SIM.rabbit_instances = [Rabbit() for _ in range(starting_rabbits)]
  if starting_rabbits >= 2:
    male_rabbit = SIM.rabbit_instances[0]
    male_rabbit.GENDER = 'male'
    female_rabbit = SIM.rabbit_instances[1]
    female_rabbit.GENDER = 'female'

  # Initialize foxes
  SIM.fox_instances = [Fox() for _ in range(starting_foxes)]
  if starting_foxes >= 2:
    male_fox = SIM.fox_instances[0]
    male_fox.GENDER = 'male'
    female_fox = SIM.fox_instances[1]
    female_fox.GENDER = 'female'

  # Initialize food
  SIM.food_instances = [Food() for _ in range(Food.STARTING_FOOD)]

  win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  pygame.display.set_caption('Ecosystem Simulator')

  record_fox_instances = []
  record_rabbit_instances = []
  loop_counter = 0
  tracked_object = None

  # Start the input thread
  task = threading.Thread(target=add_input, args=[speed])
  task.daemon = True
  task.start()

  while run:
    clock.tick(speed[0])
    loop_counter += 1
    if loop_counter % FPS == 0:
      record_fox_instances.append(len(SIM.fox_instances))
      record_rabbit_instances.append(len(SIM.rabbit_instances))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        mouse_x = math.floor(pos[0] / GRID_SIZE)
        mouse_y = math.floor(pos[1] / GRID_SIZE)
        clicked_foxes = [fox for fox in SIM.fox_instances if fox.x == mouse_x and fox.y == mouse_y]
        clicked_rabbits = [rabbit for rabbit in SIM.rabbit_instances if rabbit.x == mouse_x and rabbit.y == mouse_y]
        clicked_instances = clicked_rabbits + clicked_foxes
        if len(clicked_instances) > 0:
          tracked_object = clicked_instances[-1]

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

    # Update foxes
    foxes_to_remove = []
    for fox in SIM.fox_instances:
      fox.set_state()
      if fox.state == 'eating':
        eaten_rabbits += 1
      if max(fox.thirst, fox.hunger) > Animal.GOAL_CUTOFF:
        foxes_to_remove.append(fox)

    for fox in foxes_to_remove:
      SIM.foxes.pop(fox.KEY, None)
      SIM.mating_female_foxes.pop(fox.KEY, None)
      SIM.mating_male_foxes.pop(fox.KEY, None)
      SIM.fox_instances.remove(fox)

    for fox in SIM.fox_instances:
      fox.move()

    # Update rabbits
    rabbits_to_remove = []
    for rabbit in SIM.rabbit_instances:
      predator_detected = rabbit.detect_predators()
      if not predator_detected:
        rabbit.set_state()
      if max(rabbit.thirst, rabbit.hunger) > Animal.GOAL_CUTOFF:
        if rabbit.thirst > rabbit.hunger:
          thirst_deaths += 1
        else:
          hunger_deaths += 1
        rabbits_to_remove.append(rabbit)

    for rabbit in rabbits_to_remove:
      SIM.rabbits.pop(rabbit.KEY, None)
      SIM.mating_female_rabbits.pop(rabbit.KEY, None)
      SIM.mating_male_rabbits.pop(rabbit.KEY, None)
      SIM.rabbit_instances.remove(rabbit)

    for rabbit in SIM.rabbit_instances:
      rabbit.move()

    # Update food
    Food.del_and_create_food()

    # Check for simulation end condition
    if len(SIM.rabbit_instances) == 0 and len(SIM.fox_instances) == 0:
      run = False

    # Draw the window
    draw_window(win, tracked_object)

  print('\nthirst deaths: ', thirst_deaths)
  print('hunger deaths: ', hunger_deaths)
  print('eaten rabbits: ', round(eaten_rabbits / 60))
  pygame.quit()
  graph(record_fox_instances, record_rabbit_instances)

if __name__ == '__main__':
  main()
