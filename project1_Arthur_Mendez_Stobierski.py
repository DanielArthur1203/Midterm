import math
import decimal

def sine(radians):
    """Returns sine of the passed value(must be radians)"""
    return math.sin(radians)

def cos(radians):
    """Returns cos of the passed value(must be radians)"""
    return math.cos(radians)

def tan(radians):
    """Returns tan of the passed value(must be radians)"""
    return math.tan(radians)

def factorial(n):
    """Returns factorial of the given n."""
    total = 1
    iteration_count = 0
    while(n > 1):
        if(iteration_count >= 400000): #Likely took 2+ seconds to reach this count so just stop
            raise ValueError
        total *= n
        n -= 1
        iteration_count += 1
    return total

def print_factorial_result(n):
    """Handles issues with printing the result of factorial"""
    num = 0
    try:
        num = factorial(n)
        if(num < math.pow(10, 6)):
            print(num) #Number not large enough to justify scientific notation
        else:
            print(f"{num:e}") #Print with scientific notation
    except ValueError as e: 
        print("Value too large") #Happens when num has too many digits to be converted to a str
    except OverflowError as e:
        d = decimal.Decimal(num) #OverflowError happens when num is too large to convert through f print so decimal is needed
        print(f"{d:.2e}")
    except:
        print("Unknown Error")

#Author: Joel Mendez
def multiply(a,b):
    """ Multiply two numbers and return the result. """
    return a * b

#Author: Joel Mendez
def divide(a,b):
    """ Divide two numbers and return an error if the divisor is zero. """
    if b == 0:
        return "Error: Division by zero"
    return a / b

#Author: Joel Mendez
def power(a,b):
    """ Raise a number to a power, checking for undefined zero-base cases."""
    if a == 0 and b <= 0:
        return "Error: Undefined result for 0 raised to a non-positive power"
    result = a ** b
    return result

#Author: Piotr Stobierski
def add(a,b):
  """Add two numbers and return the result."""
  return a + b

#Author: Piotr Stobierski
def subtract(a,b):
  """Subtract two numbers and return the result."""
  return a - b
#Author: Piotr Stobierski
def calc_degrees(radians):
    """Converts and returns a value from radians to degrees"""
    return radians * (180/math.pi)

#Author: Piotr Stobierski
def calc_radians(degrees):
    """Converts and returns a value from degrees to radians"""
    return degrees * (math.pi/180)

#Author: Piotr Stobierski
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#Author: Piotr Stobierski

radian_mode = True

print("Hello! Welcome to the python terminal calculator.")
while True:
  user_request = input("Enter any two variable operation to see its result (or enter \"help\" to see instructions), or \"exit\".\n")
  if user_request.strip().lower() == "help":
    print("Supported binary operations: addition(+), subtraction(-), multiplication(*), division(/) exponentiation(^)")
    print("Supported unary operations: cosine(cos(num)), sine(sin(num)), tangent(tan(num)), factorial(!)")
    print("Calculator can operate in radians or degrees. To change this, enter \"rad\" or \"deg\".")
    print("Current behavior is in radians.") if radian_mode else print("Current behavior is in degrees.")
    continue
  elif user_request.strip().lower() == "exit":
    break
  elif user_request.strip().lower() == "rad":
    radian_mode = True
    print("Input set to radians for trigonometric functions.")
    continue
  elif user_request.strip().lower() == "deg":
    radian_mode = False
    print("Input set to degrees for trigonometric functions.")
    continue
  expression = user_request.split()
  if len(expression) != 3:
    if "(" in user_request and ")" in user_request and len(expression) == 1:
      command, argument = user_request.split("(", 1)
      command = command.strip().lower()
      argument = argument.rstrip(")").strip()
      try: 
        match command:
          case "cos":
            if radian_mode:
              print("Your result is:", cos(float(argument)))
            else:
              print("Your result is:", cos(calc_radians(float(argument))))
          case "sin":
            if radian_mode:
              print("Your result is:", sine(float(argument)))
            else:
              print("Your result is:", sine(calc_radians(float(argument))))
          case "tan":
            if radian_mode:
              print("Your result is:", tan(float(argument)))
            else:
              print("Your result is:", tan(calc_radians(float(argument))))
          case "!":
            print("Your result is:", end=" ")
            print_factorial_result(int(argument))
          case _:
            print("Unknown command. Make sure commands are written with a space between all expressions for binary commands, and no spaces for unary commands.")
      except ValueError:
        print("Invalid argument. Make sure you provide a number within the parenthesis.")
    else:
      print("Unknown command. Make sure commands are written with a space between all expressions for binary commands, and no spaces for unary commands.")
  else:
    try:
      if is_number(expression[0]) and is_number(expression[2]):
        match expression[1]:
          case "+":
            print("Your result is:", add(float(expression[0]), float(expression[2])))
          case "-":
            print("Your result is:", subtract(float(expression[0]), float(expression[2])))
          case "*":
            print("Your result is:", multiply(float(expression[0]), float(expression[2])))
          case "/":
            print("Your result is:", divide(float(expression[0]), float(expression[2])))
          case "^":
            print("Your result is:", power(float(expression[0]), float(expression[2])))
          case _:
            print("Unknown command. Make sure commands are written with a space between all expressions for binary commands, and no spaces for unary commands3.")
      else: print("Invalid arguments. Make sure you are entering numbers for your operands.")
    except ValueError: 
      print("Unknown operator.")


