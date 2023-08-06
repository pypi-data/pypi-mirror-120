__version__ = '0.0.2'

# Imports
import os
from time import sleep
import random
import math as m;

#   classes


# console module
class cons:
    """
    console module
    """

    # log method
    def log(x):
        """
        logs a statement to the console
        """
        if x == None:
            print('\u001b[31m * console.log(x): contains a None value\u001b[37m')
            return
        else:
            return print(f'\u001b[37m{x}\u001b[37m')
    
    def clear():
        os.system('clear')

# static module
class static:
    """
    static module
    """

    # alpha method
    def alpha(x, y):
        """
        takes a string and returns alpha values, and replaces non alpha values with second argument
        static.alpha('1A2B3C', '#') -> '#A#B#C'
        """
        if y == 'none' or y == None or y == 0: y = str('')
        if isinstance(x, str) and isinstance(y, str):
            for i in x:
                if str.isnumeric(i):
                    x = x.replace(i, y)
                else: pass
            return x
        else:
            print('\u001b[31m * color(x, y): argument(s) is not a string value\u001b[37m')
            return

    # num method
    def num(x, y):
        """
        takes a string and returns numeric values, and replaces non numeric values with second argument
        static.num('1A2B3C', '#') -> '1#2#3#'
        """
        if y == 'none' or y == None or y == 0: y = str('')
        if isinstance(x, str):
            for i in x:
                if str.isnumeric(i): pass
                else: x = x.replace(i, y)
            return x
        else:
            print('\u001b[31m * argument is not a string value\u001b[37m')
            return

    # space method
    def space(x, y):
        """
        takes a string and returns character values, and replaces non character values with second argument
        static.space('1 A 2 B', '#') -> '1#A#2#B'
        """
        if y == 'none' or y == None or y == 0: y = str('')
        if isinstance(x, str):
            for i in x:
                if i == ' ':
                    x = x.replace(i, y)
            return x
        else: 
            print('\u001b[31m * argument is not a string value\u001b[37m')
            return

    # replace method
    def replace(x, y, z):
        """
        takes a string and replaces character values in the second argument with character values in the third argument
        static.find('1##2##3##4', '#', '') -> '1234'
        """
        if z == 'none' or z == None or z == 0: z = str('')
        if isinstance(x, str):
            if isinstance(y, str):
                for i in x:
                    if i == y:
                        x = x.replace(i, z)
                return x
            elif isinstance(y, list):
                for i in x:
                    for j in y:
                        if i == j:
                            x = x.replace(i, z)
                return x
            else:
                print('\u001b[31m * argument is not a string value or a list value\u001b[37m')


#   stand-alone functions


# color function
def color(x, y: str):
    """
    changes the color of console.log message
    color('123', 'green') -> 123 (in green text)
    """
    if isinstance(x, str) and isinstance(y, str):
        if y == str('red'):
            return f'\u001b[31m{x}\u001b[37m'
        elif y == str('green') or y == str('gre'):
            return f'\u001b[32m{x}\u001b[37m' 
        elif y == str('yellow') or y == str('yel'):
            return f'\u001b[33m{x}\u001b[37m'
        elif y == str('blue') or y == str('blu'):
            return f'\u001b[34m{x}\u001b[37m'
        elif y == str('magenta') or y == str('mag'):
            return f'\u001b[35m{x}\u001b[37m'
        elif y == str('cyan') or y == str('cya'):
            return f'\u001b[36m{x}\u001b[37m'
        elif y == str('black') or y == str('bla') or y == str('blk'):
            return f'\u001b[30m{x}\u001b[37m'
    else:
        print('\u001b[31m * color(x, y): argument(s) is not a string value\u001b[37m')

# typeof function
def typeof(*data):
    """
    gives the type of inputted argument
    typeof(1.01) -> 'float'
    """
    if len(data) == 1:
        if isinstance(data[0], int):
            return 'integer'
        elif isinstance(data[0], float):
            return 'float'
        elif isinstance(data[0], str):
            return 'string'
        elif callable(data[0]):
            return 'function'
        elif isinstance(data[0], list):
            return 'list'
        elif isinstance(data[0], dict):
            return 'dictionary'
        elif isinstance(data, tuple):
            return 'tuple'
        elif hasattr(data[0], '__class__'):
            return 'class'
        elif isinstance(data[0], None):
            return 'none'
    elif len(data) == 2:
        if data[1] == str('int'):
            if isinstance(data[0], int):
                return True
            else: return False
        elif data[1] == str('float'):
            if isinstance(data[0], float):
                return True
            else: return False
        elif data[1] == str('str'):
            if isinstance(data[0], str):
                return True
            else: return False 
        elif data[1] == str('func') or data[1] == str('function'):
            if callable(data[0]):
                return True
            else: return False
        elif data[1] == str('list'):
            if isinstance(data[0], list):
                return True
            else: return False
        elif data[1] == str('dict') or data[1] == str('dictionary'):
            if isinstance(data[0], dict):
                return True
            else: return False
        elif data[1] == str('class'):
            if hasattr(data[0], '__class__'):
                return True
            else: return False
        elif data[1] == str('null') or data[1] == str('none'):
            if isinstance(data[0], None):
                return True
            else: return False

def contains(x, y):
    """
    contains('Hello, World!', ["H", "W", "!", "m"]) -> {'H': True, 'W': True, '!': True, 'm': False}
    """
        
    returnedDict = {}
    valueList = []

    if isinstance(x, str) and isinstance(y, str):
      if len(x) <= 1:
          for i in x:
              if i == y:
                  return True
              return False
      else:
          results = x.find(y)
          if results < 0:
              return False
          else: return True
    elif isinstance(y, list):
        for j in y:
            if j in x:
                returnedDict[j] = True
                continue
            elif not j in x:
                returnedDict[j] = False
                continue
            
        for i, j in returnedDict.items():
            valueList.append(j)
        if not False in valueList: return True
        if not True in valueList: return False
        else: return returnedDict
    else:
        print('\u001b[31m * argument is not a string value or a list value\u001b[37m')




#   math module

class math:
  """
  math module
  """
  
  def random(*args):
      """
      returns random number between your first and second arguments (
        if no args given uniform number between 0 and 1)

      Math.random() // Math.random(0, 8)
      """

      if len(args) == 0:
          return random.uniform(0, 1)
      elif len(args) == 2:
          if isinstance(args[0], int) and isinstance(args[1], int) or isinstance(args[0], float) and isinstance(args[1], float):
              return random.uniform(args[0], args[1])
          else:
              print('error')
      else:
        print('error')

  def floor(x):
      """
      returns rounded down number
      
      Math.floor(1.9) -> 1
      """
      if isinstance(x, float):
          return m.floor(x)
      elif isinstance(x, int):
          return x
      else:
          return print('error')
  
  def ceil(x):
      """
      returns rounded up number
      
      Math.floor(1.1) -> 2
      """
      if isinstance(x, float):
          return m.ceil(x)
      elif isinstance(x, int):
          return x
      else:
          return print('error')

  def round(x):
      """
      rounds given number up or down accordingly
      
      Math.round(1.9) -> 2
      """
      if isinstance(x, float):
          return round(x)
      elif isinstance(x, int):
          return x
      else:
          return print('error')

  def trunc(x):
      """
      truncates decimal (floating point) values into integers
      
      Math.trunc(2.22) -> 2
      """
      if isinstance(x, float):
          return int(x)
      if isinstance(x, int):
          return x
      else:
          return print('error')
  
  def dec(x):
      """
      converts an integer to a floating point number

      Math.dec(2) -> 2.0
      """
      if isinstance(x, int):
          return float(x);
      elif isinstance(x, float):
          return x
      else:
          return print('error')
  
  def inverse(x):
      """
      returns the inverse of given number
      
      Math.inverse(2) -> -2
      """
      if isinstance(x, int) or isinstance(x, float):
          if x < 0:
              return -abs(x)
          else:
              return abs(x)
      else:
          return print('error')
  
  def pow(x, y):
      """
      returns the given number raised to the given exponent
      
      Math.pow(5, 2) -> 25
      """
      if isinstance(x, int) or isinstance(x, float) and isinstance(y, int) or isinstance(y, float):
          return pow(x, y)
      else:
          return print('error')
  
  def sqrt(x):
      """
      returns square root of given number
      
      Math.sqrt(10) -> 3.16
      """
      if isinstance(x, int) or isinstance(x, float):
          return m.sqrt(x)
      else:
          return print('error')
  
  def sin(x):
      """
      returns the sine of given number

      Math.sin(9) -> 0.41
      """
      if isinstance(x, int) or isinstance(x, float):
          return m.sin(x)
      else: 
          return print('error')
  
  def asin(x):
    """
    returns the arc sine of given number
    """
    return m.asin(x)
  
  def asinh(x):
    """
    returns the hyperbolic arc sine of given number
    """
    return m.asinh(x)
  
  def atan(x):
      """
      returns the arc tangent of given number
      """
      return m.atan(x)
  
  def atan2(x, y):
      """
      returns the arc tangent of given number where x & y are coordinates of the point
      """
      return m.atan2(y, x)
  
  def atanh(x):
      """
      returns hyperbolic arc tangent of given number
      """
      return m.atanh(x)

  def cos(x):
      """
      returns cosine of given number
      
      Math.cos(5) -> 0.28
      """
      if isinstance(x, int) or isinstance(x, float):
          return m.cos(x)
      else:
          return print('error')
  
  def acos(x):
      """
      returns arc cosine of given number
      """
      return m.acos(x)
  
  def acosh(x):
    """
    returns the hyperbolic arc cosine of given number
    """
    return m.acosh(x)

  def max(*args):
      """
      returns largest number in args

      Math.max(5, 20, 500, 6, 87, 1) -> 500
      """
      for i in args:
          if isinstance(i, int) or isinstance(i, float):
              continue
          else:
              return print('error')
      return max(args)

  def min(*args):
      """
      returns smallest number in args

      Math.min(5, 20, 500, 6, 87, 1) -> 1
      """
      for i in args:
          if isinstance(i, int) or isinstance(i, float):
              continue
          else:
              return print('error')
      return min(args)
  
  def sign(x):
      """
      returns if x is negative, positive, or None
      """
      if x < 0:
        return -1
      elif x > 0:
        return 1
      elif x == 0:
        return 0
  
  def log(x):
      """
      returns the natural logarithm of given number
      """
      return m.log(x)
  
  def log2(x):
      """
      returns the base-2 logarithm of given number
      """
      return m.log2(x)

  def log10(x):
      """
      returns the base-10 logarithm of given number
      """
      return m.log10(x)

  def pi():
      """
      returns pi
      
      Math.pi() -> 3.1415926535897
      """
      return 3.1415926535897
  
  def factors(x):
      """
      returns factor list of given number in a list
      
      Math.factors(5) -> [1, 5]
      """
      if isinstance(x, int) or isinstance(x, float):
          factors_list = []
          for i in range(1, x + 1):
            if x % i == 0:
              factors_list.append(i)
          return factors_list
      else:
        print('error')

cons.log(contains('<@!91481y8568912881>', ['M', '!']))