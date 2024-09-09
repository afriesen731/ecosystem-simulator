import pygame
import os
import random
import math
import threading
import matplotlib.pyplot as plt
from time import time








# the idea for this project came from this video by Sebastian Lague https://youtu.be/r_It_X7v-1E
pygame.init()
WIDTH = 128 #128
HEIGHT = 64 #64


GRID_SIZE = 10

WIN_WIDTH = WIDTH * GRID_SIZE +  GRID_SIZE
WIN_HEIGHT = HEIGHT * GRID_SIZE + GRID_SIZE

FPS = 60 #60
speed = [FPS]

BACKGROUND = pygame.image.load(os.path.join('background.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (1290, 660))

#HEART = pygame.image.load(os.path.join('Heart.png'))
#HEART =  pygame.transform.scale(HEART, (6, 6))

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
bar_font = pygame.font.SysFont(None, 20)


rabbit_instances = [] 
fox_instances = []
food_instances = []


foods = {}
water = {1: {'x': 63, 'y': 0}, 2: {'x': 64, 'y': 0}, 3: {'x': 83, 'y': 0}, 4: {'x': 84, 'y': 0}, 5: {'x': 85, 'y': 0}, 6: {'x': 64, 'y': 1}, 7: {'x': 65, 'y': 1}, 8: {'x': 85, 'y': 1}, 9: {'x': 86, 'y': 1}, 10: {'x': 11, 'y': 2}, 11: {'x': 12, 'y': 2}, 12: {'x': 64, 'y': 2}, 13: {'x': 65, 'y': 2}, 14: {'x': 86, 'y': 2}, 15: {'x': 
87, 'y': 2}, 16: {'x': 10, 'y': 3}, 17: {'x': 11, 'y': 3}, 18: {'x': 13, 'y': 3}, 19: {'x': 14, 'y': 3}, 20: {'x': 65, 'y': 3}, 21: {'x': 87, 'y': 3}, 22: {'x': 88, 'y': 3}, 23: {'x': 8, 'y': 4}, 24: {'x': 9, 'y': 4}, 25: {'x': 10, 'y': 4}, 26: {'x': 11, 'y': 4}, 27: {'x': 12, 'y': 4}, 28: {'x': 13, 'y': 4}, 29: {'x': 14, 
'y': 4}, 30: {'x': 65, 'y': 4}, 31: {'x': 66, 'y': 4}, 32: {'x': 88, 'y': 4}, 33: {'x': 89, 'y': 4}, 34: {'x': 6, 'y': 5}, 35: {'x': 7, 'y': 5}, 36: {'x': 8, 'y': 5}, 37: {'x': 9, 'y': 5}, 38: {'x': 10, 'y': 5}, 39: {'x': 11, 'y': 5}, 40: {'x': 12, 'y': 5}, 41: {'x': 13, 'y': 5}, 42: {'x': 65, 'y': 5}, 43: {'x': 66, 'y': 5}, 44: {'x': 88, 'y': 5}, 45: {'x': 89, 'y': 5}, 46: {'x': 5, 'y': 6}, 47: {'x': 6, 'y': 6}, 48: {'x': 7, 'y': 6}, 49: {'x': 8, 'y': 6}, 50: {'x': 9, 'y': 6}, 51: {'x': 64, 'y': 6}, 52: {'x': 65, 'y': 6}, 53: {'x': 66, 'y': 6}, 54: {'x': 88, 'y': 6}, 55: {'x': 89, 'y': 6}, 56: {'x': 5, 'y': 7}, 57: {'x': 6, 'y': 7}, 58: {'x': 7, 'y': 7}, 59: {'x': 8, 'y': 7}, 60: {'x': 9, 'y': 7}, 61: {'x': 64, 'y': 7}, 62: {'x': 65, 'y': 7}, 63: {'x': 66, 'y': 7}, 64: {'x': 88, 'y': 7}, 65: {'x': 
89, 'y': 7}, 66: {'x': 5, 'y': 8}, 67: {'x': 6, 'y': 8}, 68: {'x': 7, 'y': 8}, 69: {'x': 8, 'y': 8}, 70: {'x': 63, 'y': 8}, 71: {'x': 64, 'y': 8}, 72: {'x': 65, 'y': 8}, 73: {'x': 88, 'y': 8}, 74: {'x': 89, 'y': 8}, 75: {'x': 5, 'y': 9}, 76: {'x': 61, 'y': 9}, 77: {'x': 62, 'y': 9}, 78: {'x': 63, 'y': 9}, 79: {'x': 88, 'y': 9}, 80: {'x': 89, 'y': 9}, 81: {'x': 90, 'y': 9}, 82: {'x': 59, 'y': 10}, 83: {'x': 60, 'y': 10}, 84: {'x': 88, 'y': 10}, 85: {'x': 89, 'y': 10}, 86: {'x': 3, 'y': 11}, 87: {'x': 4, 'y': 11}, 88: {'x': 57, 'y': 11}, 89: {'x': 58, 'y': 11}, 90: {'x': 87, 'y': 11}, 91: {'x': 88, 'y': 11}, 92: {'x': 89, 'y': 11}, 93: {'x': 
3, 'y': 12}, 94: {'x': 4, 'y': 12}, 95: {'x': 55, 'y': 12}, 96: {'x': 56, 'y': 12}, 97: {'x': 87, 'y': 12}, 98: {'x': 3, 'y': 13}, 99: {'x': 4, 'y': 13}, 100: {'x': 53, 'y': 13}, 101: {'x': 86, 'y': 13}, 102: {'x': 87, 'y': 13}, 103: {'x': 52, 'y': 14}, 104: {'x': 53, 'y': 14}, 105: {'x': 85, 'y': 14}, 106: {'x': 86, 'y': 
14}, 107: {'x': 51, 'y': 15}, 108: {'x': 85, 'y': 15}, 109: {'x': 86, 'y': 15}, 110: {'x': 50, 'y': 16}, 111: {'x': 84, 'y': 16}, 112: {'x': 85, 'y': 16}, 113: {'x': 48, 'y': 17}, 114: {'x': 49, 'y': 17}, 115: {'x': 83, 'y': 17}, 116: {'x': 84, 'y': 17}, 117: {'x': 85, 'y': 17}, 118: {'x': 48, 'y': 18}, 119: {'x': 49, 'y': 18}, 120: {'x': 83, 'y': 18}, 121: {'x': 84, 'y': 18}, 122: {'x': 85, 'y': 18}, 123: {'x': 47, 'y': 19}, 124: {'x': 48, 'y': 19}, 125: {'x': 83, 'y': 19}, 126: {'x': 84, 'y': 19}, 127: {'x': 47, 'y': 20}, 128: {'x': 48, 'y': 20}, 129: {'x': 83, 'y': 20}, 130: {'x': 84, 'y': 20}, 131: {'x': 46, 'y': 21}, 132: {'x': 47, 'y': 21}, 133: {'x': 83, 'y': 21}, 134: {'x': 84, 'y': 21}, 135: {'x': 46, 'y': 22}, 136: {'x': 47, 'y': 22}, 137: {'x': 83, 'y': 22}, 138: {'x': 84, 'y': 22}, 139: 
{'x': 46, 'y': 23}, 140: {'x': 47, 'y': 23}, 141: {'x': 83, 'y': 23}, 142: {'x': 84, 'y': 23}, 143: {'x': 47, 'y': 24}, 144: {'x': 83, 'y': 24}, 145: {'x': 84, 'y': 24}, 146: {'x': 85, 'y': 24}, 147: {'x': 47, 'y': 25}, 148: {'x': 48, 'y': 25}, 149: {'x': 84, 'y': 25}, 150: {'x': 85, 'y': 25}, 151: {'x': 86, 'y': 25}, 152: {'x': 47, 'y': 26}, 153: {'x': 48, 'y': 26}, 154: {'x': 49, 'y': 26}, 155: {'x': 85, 'y': 26}, 156: {'x': 86, 'y': 26}, 157: {'x': 48, 'y': 27}, 158: {'x': 49, 'y': 27}, 159: {'x': 85, 'y': 27}, 160: {'x': 86, 'y': 27}, 161: {'x': 49, 'y': 28}, 162: {'x': 50, 'y': 28}, 163: {'x': 84, 'y': 28}, 164: {'x': 85, 'y': 28}, 165: {'x': 86, 'y': 28}, 166: {'x': 49, 'y': 29}, 167: {'x': 50, 'y': 29}, 168: {'x': 51, 'y': 29}, 169: {'x': 69, 'y': 29}, 170: {'x': 70, 'y': 29}, 171: {'x': 71, 
'y': 29}, 172: {'x': 72, 'y': 29}, 173: {'x': 73, 'y': 29}, 174: {'x': 74, 'y': 29}, 175: {'x': 75, 'y': 29}, 176: {'x': 76, 'y': 29}, 177: {'x': 84, 'y': 29}, 178: {'x': 85, 'y': 29}, 179: {'x': 50, 'y': 30}, 180: {'x': 51, 'y': 30}, 181: {'x': 52, 'y': 30}, 182: {'x': 62, 'y': 30}, 183: {'x': 63, 'y': 30}, 184: {'x': 64, 'y': 30}, 185: {'x': 65, 'y': 30}, 186: {'x': 67, 'y': 30}, 187: {'x': 78, 'y': 30}, 188: {'x': 79, 'y': 30}, 189: {'x': 80, 'y': 30}, 190: {'x': 81, 'y': 30}, 191: {'x': 82, 'y': 30}, 192: {'x': 83, 'y': 30}, 193: {'x': 50, 'y': 31}, 194: {'x': 51, 'y': 31}, 195: {'x': 52, 'y': 31}, 196: {'x': 53, 'y': 31}, 197: {'x': 61, 'y': 31}, 198: {'x': 51, 'y': 32}, 199: {'x': 52, 'y': 32}, 200: {'x': 53, 'y': 32}, 201: {'x': 61, 'y': 32}, 202: {'x': 51, 'y': 33}, 203: {'x': 52, 'y': 33}, 
204: {'x': 53, 'y': 33}, 205: {'x': 60, 'y': 33}, 206: {'x': 61, 'y': 33}, 207: {'x': 52, 'y': 34}, 208: {'x': 53, 'y': 34}, 209: {'x': 58, 'y': 34}, 210: {'x': 59, 'y': 34}, 211: {'x': 60, 'y': 34}, 212: {'x': 61, 'y': 34}, 213: {'x': 52, 'y': 35}, 214: {'x': 53, 'y': 35}, 215: {'x': 54, 'y': 35}, 216: {'x': 57, 'y': 35}, 217: {'x': 58, 'y': 35}, 218: {'x': 59, 'y': 35}, 219: {'x': 53, 'y': 36}, 220: {'x': 55, 'y': 36}, 221: {'x': 57, 'y': 36}, 222: {'x': 53, 'y': 37}, 223: {'x': 
54, 'y': 37}, 224: {'x': 53, 'y': 38}, 225: {'x': 51, 'y': 39}, 226: {'x': 52, 'y': 39}, 227: {'x': 46, 'y': 40}, 228: {'x': 47, 'y': 40}, 229: {'x': 48, 'y': 40}, 230: {'x': 49, 'y': 40}, 231: {'x': 50, 'y': 40}, 232: {'x': 51, 'y': 40}, 233: {'x': 124, 'y': 40}, 234: {'x': 125, 'y': 40}, 235: {'x': 126, 'y': 40}, 236: {'x': 127, 'y': 40}, 237: {'x': 18, 'y': 41}, 238: {'x': 19, 'y': 41}, 239: {'x': 20, 'y': 41}, 240: {'x': 21, 'y': 41}, 241: {'x': 22, 'y': 41}, 242: {'x': 24, 'y': 41}, 243: {'x': 25, 'y': 41}, 244: {'x': 26, 'y': 41}, 245: {'x': 27, 'y': 41}, 246: {'x': 28, 'y': 41}, 247: {'x': 29, 'y': 41}, 248: {'x': 30, 'y': 41}, 249: 
{'x': 31, 'y': 41}, 250: {'x': 32, 'y': 41}, 251: {'x': 33, 'y': 41}, 252: {'x': 34, 'y': 41}, 253: {'x': 35, 'y': 41}, 254: {'x': 36, 'y': 41}, 255: {'x': 37, 'y': 41}, 256: {'x': 38, 'y': 41}, 257: {'x': 39, 'y': 41}, 258: {'x': 40, 'y': 41}, 259: {'x': 41, 'y': 41}, 260: {'x': 42, 'y': 41}, 261: {'x': 43, 'y': 41}, 262: {'x': 44, 'y': 41}, 263: {'x': 45, 'y': 41}, 264: {'x': 46, 'y': 41}, 265: {'x': 47, 'y': 41}, 266: {'x': 49, 'y': 41}, 267: {'x': 121, 'y': 41}, 268: {'x': 122, 'y': 41}, 269: {'x': 123, 'y': 41}, 270: {'x': 124, 'y': 41}, 271: {'x': 9, 'y': 42}, 272: {'x': 10, 'y': 42}, 273: {'x': 11, 'y': 42}, 274: {'x': 12, 'y': 42}, 
275: {'x': 13, 'y': 42}, 276: {'x': 14, 'y': 42}, 277: {'x': 15, 'y': 42}, 278: {'x': 16, 'y': 42}, 279: {'x': 17, 'y': 42}, 280: {'x': 18, 'y': 42}, 281: {'x': 19, 'y': 42}, 282: {'x': 20, 'y': 42}, 283: {'x': 21, 'y': 42}, 284: {'x': 34, 'y': 42}, 285: {'x': 35, 'y': 42}, 286: {'x': 36, 'y': 42}, 287: {'x': 37, 'y': 42}, 288: {'x': 38, 'y': 42}, 289: {'x': 39, 'y': 42}, 290: {'x': 40, 'y': 42}, 291: {'x': 41, 'y': 42}, 292: {'x': 42, 'y': 42}, 293: {'x': 121, 'y': 42}, 294: {'x': 122, 'y': 42}, 295: {'x': 3, 'y': 43}, 296: {'x': 4, 'y': 43}, 297: {'x': 5, 'y': 43}, 298: {'x': 6, 'y': 43}, 299: {'x': 7, 'y': 43}, 300: {'x': 8, 'y': 43}, 301: {'x': 9, 'y': 43}, 302: {'x': 10, 'y': 43}, 303: {'x': 11, 'y': 43}, 304: {'x': 120, 'y': 43}, 305: {'x': 121, 'y': 43}, 306: {'x': 122, 'y': 43}, 307: {'x': 0, 'y': 44}, 308: {'x': 1, 'y': 44}, 309: {'x': 2, 'y': 44}, 310: {'x': 3, 'y': 44}, 311: {'x': 119, 'y': 44}, 312: {'x': 120, 'y': 44}, 313: {'x': 121, 'y': 44}, 
314: {'x': 122, 'y': 44}, 315: {'x': 119, 'y': 45}, 316: {'x': 121, 'y': 45}, 317: {'x': 119, 'y': 46}, 318: {'x': 120, 'y': 46}, 319: {'x': 121, 'y': 46}, 320: {'x': 119, 'y': 47}, 321: {'x': 120, 'y': 47}, 322: {'x': 121, 'y': 47}, 323: {'x': 119, 'y': 48}, 324: {'x': 120, 'y': 48}, 325: {'x': 118, 'y': 49}, 326: {'x': 116, 'y': 50}, 327: {'x': 117, 'y': 50}, 328: {'x': 118, 'y': 50}, 329: {'x': 119, 'y': 50}, 330: {'x': 115, 'y': 51}, 331: {'x': 116, 'y': 51}, 332: {'x': 117, 'y': 51}, 333: {'x': 118, 'y': 51}, 334: {'x': 113, 'y': 52}, 335: {'x': 114, 'y': 52}, 336: {'x': 115, 'y': 52}, 337: {'x': 116, 'y': 52}, 338: {'x': 111, 'y': 53}, 339: {'x': 112, 'y': 53}, 340: {'x': 113, 'y': 53}, 341: {'x': 114, 'y': 53}, 342: {'x': 110, 'y': 54}, 343: {'x': 111, 'y': 54}, 344: {'x': 112, 'y': 54}, 345: {'x': 109, 'y': 55}, 346: {'x': 110, 'y': 55}, 347: {'x': 109, 'y': 56}, 348: {'x': 110, 'y': 56}, 349: {'x': 108, 'y': 57}, 350: {'x': 109, 'y': 57}, 351: {'x': 108, 'y': 58}, 352: {'x': 109, 'y': 58}, 353: {'x': 107, 'y': 59}, 354: {'x': 108, 'y': 59}, 355: {'x': 105, 'y': 60}, 356: {'x': 106, 'y': 60}, 357: {'x': 107, 
'y': 60}, 358: {'x': 104, 'y': 61}, 359: {'x': 105, 'y': 61}, 360: {'x': 106, 'y': 61}, 361: {'x': 101, 'y': 62}, 362: {'x': 102, 'y': 62}, 363: {'x': 103, 'y': 62}, 364: {'x': 98, 'y': 63}, 365: {'x': 100, 'y': 63}, 366: {'x': 101, 'y': 63}, 367: {'x': 96, 'y': 64}, 368: {'x': 97, 'y': 64}, 369: {'x': 98, 'y': 64}, 370: {'x': 99, 'y': 64}}
rabbits = {}
mating_male_rabbits = {} 
mating_female_rabbits = {}
foxes = {}
mating_male_foxes = {}
mating_female_foxes = {}


WARN_ABOUT_WALL = 5




class Animal:
  GOAL_CUTOFF = 1

  pythagorean_theorem = lambda a, b: math.sqrt(a ** 2 + b ** 2)

  key = 0
  def __init__(self, dict_to_append_to, Animal_Class, x=None, y=None):
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



  def set_state(self, dict_of_male_mates, dict_of_female_mates, dict_of_food, water=water):
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
        self.search_for_object(water, 'found water')
        
        if self.state == 'searching for water':
          self.move_randomly()

      if self.state == 'found water':
        self.update_target(water, 'searching for water')
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

  
  def move(self, rabbit_instances):

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
        target_food = foods[key]['self']
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
        del mating_female_rabbits[self.KEY]
      except KeyError:
        pass
      try:
        mate = mating_male_rabbits[self.target['key']]['self']

        mate.just_mated =Rabbit.MATING_BREAK
        mate.rest = Rabbit.REST_AFTER_MATING

        rabbit_instances.append(Rabbit(rabbits, Rabbit, self.x, self.y))
        
        rabbit_instances.append(Rabbit(rabbits, Rabbit, self.x, self.y))

        self.just_mated = Rabbit.MATING_BREAK
        self.rest = Rabbit.REST_AFTER_MATING
        del mating_male_rabbits[mate.KEY]
      except KeyError:
        self.state = 'searching for mate'




    else:
      self.rest = Rabbit.REST_AFTER_MOVING
      
      self.x += self.x_direction
      self.y += self.y_direction
      
      rabbits.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
      if self.goal == 'mating' and self.GENDER == 'female':
        mating_female_rabbits.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
        
      elif self.goal == 'mating' and self.GENDER == 'male':
        mating_male_rabbits.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
  



  def check_for_fox(self):
    if self.rest > 0:
      return

    
    self.search_for_object(foxes, 'running', Rabbit.FOX_RANGE)

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
  

  def __init__(self, foxes, Fox, x=None, y=None):
    self.x = x
    self.y = y
    super().__init__(foxes, Fox, self.x, self.y)
    
    
    #foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
    
    self.BASE_REPRODUCTIVE_URGE = 0.6
    self.reproductive_urge = self.BASE_REPRODUCTIVE_URGE

  def move(self, fox_instances, rabbit_instances):
    if self.rest > 0:
      self.rest -= 1
      return
    
    if self.state == 'eating':
      
      try:
        target_food = rabbits[self.target['key']] ['self']
        rabbits.pop(target_food.KEY)
        self.hunger -= Fox.FOOD_RESTORATION
        if self.hunger < 0:
          self.hunger = 0

      except KeyError:

        self.state = 'searching for food'
        return
      try:
        mating_female_rabbits.pop(target_food.KEY)
      except KeyError:
        pass
      try:
        mating_male_rabbits.pop(target_food.KEY)
      except KeyError:
        pass

      rabbit_instances.remove(target_food)
      self.rest = Fox.REST_AFTER_EATING

      #self.goal = None
      #self.state = None
        
    elif self.state == 'drinking':
      self.thirst = 0
      self.rest = Fox.REST_AFTER_DRINKING

      #self.goal = None
      #self.state = None

    elif self.state == 'mating' and self.GENDER == 'female':
      fox_instances.append(Fox(foxes, Fox, self.x, self.y))
      
      self.just_mated = Fox.MATING_BREAK
      self.rest = Fox.REST_AFTER_MATING
      #self.goal = None
      #self.state = None
      del mating_female_foxes[self.KEY]

      mate = mating_male_foxes[self.target['key']]['self']

      mate.just_mated = Fox.MATING_BREAK
      mate.rest = Fox.REST_AFTER_MATING
      #mate.goal = None
      #mate.state = None
      del mating_male_foxes[mate.KEY]

    else:
      self.rest = Fox.REST_AFTER_MOVING
      self.x += self.x_direction
      self.y += self.y_direction
      
      foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
      if self.goal == 'mating' and self.GENDER == 'female':
        mating_female_foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
        
      elif self.goal == 'mating' and self.GENDER == 'male':
        mating_male_foxes.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})

    

class Food:

  
  total_food = 0
  key = 0
  MAX_TIMES_EATEN = 10
  MAX_FOOD = 600
  STARTING_FOOD = round(MAX_FOOD/2)
  
  wait_to_add_food = 0
  FOOD_WAIT = 10

  @staticmethod
  def del_and_create_food(food_instances, foods):
    for food in food_instances:
      if food.times_eaten >= Food.MAX_TIMES_EATEN:
        del foods[food.KEY]
        food_instances.remove(food)


    if len(food_instances) < Food.MAX_FOOD:
      Food.wait_to_add_food += 1
      if Food.wait_to_add_food >= Food.FOOD_WAIT:
        Food.wait_to_add_food = 0
        food_instances.append(Food())

  
  def __init__(self, original=False):

    Food.total_food += 1
    Food.key += 1
    self.KEY = Food.key

  
    if original is False:
      self.x = random.randint(0, WIDTH)
      self.y = random.randint(0, HEIGHT)
      while True:
        
        for i in water:
          if self.x == water[i]['x'] and self.y == water[i]['y']:
            finished = False
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            continue
        break

      foods.update({self.KEY: {'x': self.x, 'y': self.y, 'self': self}})
    
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

  bar_name = bar_font.render(name, True, BLACK)
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
  

def main(rabbit_instances, fox_instances, food_instances, mating_female_rabbits, mating_male_rabbits):
  hunger_deaths = 0
  thirst_deaths = 0
  eaten_rabbits = 0



  clock = pygame.time.Clock()
  run = True
  task_running = False
  
  print("\n \033[39;49;1m Welcome to Ecosystem simulator\033[0m")

  starting_rabbits = int(input('rabbits: '))

  starting_foxes = int(input('foxes: '))

  rabbit_instances = [Rabbit(rabbits, Rabbit) for _ in range(starting_rabbits)]
  if starting_rabbits == 2:
    male = rabbit_instances[0]
    male.GENDER = 'male'

    female = rabbit_instances[1]
    female.GENDER = 'female'
  
  fox_instances = [Fox(foxes, Fox) for _ in range(starting_foxes)]
  if starting_foxes == 2:
    male = fox_instances[0]
    male.GENDER = 'male'

    female = fox_instances[1]
    female.GENDER = 'female'

  food_instances = [Food() for _ in range(Food.STARTING_FOOD)]

  original_food = Food(True)
  win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  pygame.display.set_caption('ecosystem simulator')
  
  record_fox_instances = []
  record_rabbit_instances = []
  loop_counter = 0
  tracked_object = None

  task = threading.Thread(target = add_input, args=[fox_instances, rabbit_instances, speed])
  while run:
    clock.tick(speed[0])
    loop_counter += 1
    if loop_counter % FPS == 0:
      record_fox_instances.append(len(fox_instances))
      record_rabbit_instances.append(len(rabbit_instances))
    a = time()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        position = []
        mouse_x = math.floor(pos[0]/GRID_SIZE)
        mouse_y = math.floor(pos[1]/GRID_SIZE)
        clicked_foxes = [fox for fox in fox_instances if fox.x == mouse_x and fox.y == mouse_y]
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
            tracked_object = random.choice(rabbit_instances)
          except IndexError:
            pass
        if event.key == pygame.K_f:
          try:
            tracked_object = random.choice(fox_instances)
          except IndexError:
            pass
    

    if not task.is_alive():
      task = threading.Thread(target = add_input, args=[fox_instances, rabbit_instances, speed])
      task.start()
      


    for fox in fox_instances:
      fox.set_state(mating_male_foxes, mating_female_foxes, rabbits)
      if fox.state == 'eating': eaten_rabbits += 1
      if max(fox.thirst, fox.hunger) > Animal.GOAL_CUTOFF:
        del foxes[fox.KEY]

        try:
          mating_female_foxes.pop(fox.KEY)
        except KeyError:
          pass
        try:
          mating_male_foxes.pop(fox.KEY)
        except KeyError:
          pass

        fox_instances.remove(fox)

    for fox in fox_instances:
      fox.move(fox_instances, rabbit_instances)

    
    for rabbit in rabbit_instances:
      fox_in_range = rabbit.check_for_fox()
      if fox_in_range is False:
        rabbit.set_state(mating_male_rabbits, mating_female_rabbits, foods)
        
    


      if max(rabbit.thirst, rabbit.hunger) > Animal.GOAL_CUTOFF:
        if rabbit.thirst > rabbit.hunger:
          thirst_deaths += 1
        else:
          hunger_deaths += 1


        del rabbits[rabbit.KEY]
        mating_female_rabbits.pop(rabbit.KEY, None)
        mating_male_rabbits.pop(rabbit.KEY, None)
        rabbit_instances.remove(rabbit)


    for rabbit in rabbit_instances:
      rabbit.move(rabbit_instances)

    original_food.del_and_create_food(food_instances, foods)
    
    b = time()
    #print(len(rabbit_instances), test)
    #print(b - a)

    if rabbit_instances == 0 and fox_instances == 0:
      run = False
    draw_window(win, rabbit_instances, fox_instances, food_instances, tracked_object)
  print('\nthirst deaths: ', thirst_deaths)
  print('hunger deaths: ', hunger_deaths)
  print('eaten rabbits: ', round(eaten_rabbits/60))
  pygame.quit()
  graph(record_fox_instances, record_rabbit_instances)
  
if __name__ == '__main__':
  main(rabbit_instances, fox_instances, food_instances, mating_female_rabbits, mating_male_rabbits)

