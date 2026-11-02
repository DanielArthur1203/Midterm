import math
import decimal

#Author: Daniel Arthur
def sine(radians):
    """Returns sine of the passed value(must be radians)"""
    return math.sin(radians)

#Author: Daniel Arthur
def cos(radians):
    """Returns cos of the passed value(must be radians)"""
    return math.cos(radians)

#Author: Daniel Arthur
def tan(radians):
    """Returns tan of the passed value(must be radians)"""
    return math.tan(radians)

#Author: Daniel Arthur
def factorial(n):
    """Returns factorial of the given n."""
    if(type(n) != int or n < 0):
       raise ValueError("Domain Error")
    total = 1
    iteration_count = 0
    while(n > 1):
        if(iteration_count >= 400000): #Likely took 2+ seconds to reach this count so just stop
            raise ValueError
        total *= n
        n -= 1
        iteration_count += 1
    return total

#Author: Daniel Arthur
def print_factorial_result(n):
    """Handles issues with printing the result of factorial"""
    num = 0
    try:
       n = int(n)
    except ValueError as e:
       print("Domain Error")
       return

    try:
        num = factorial(n)
        if(num < math.pow(10, 6)):
            print(num) #Number not large enough to justify scientific notation
        else:
            print(f"{num:e}") #Print with scientific notation
    except ValueError as e: 
        msg = str(e)
        if("Domain" in msg):
           print("Domain Error")
        else:
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
  """Checks if a string is a number and returns the appropriate boolean value."""
  try:
    float(s)
    return True
  except ValueError:
    return False

#Author: Piotr Stobierski
def run_command(user_request):
  """Checks if passed string is a menu command. For all commands except \"exit\", the command is ran and True is returned. Passing in \"exit\" returns False. Otherwise returns None."""
  global radian_mode
  command = user_request.strip().lower()
  if command == "help":
    print("Supported binary operations: addition(+), subtraction(-), multiplication(*), division(/) exponentiation(^)")
    print("Supported unary operations: cosine(cos(num)), sine(sin(num)), tangent(tan(num)), factorial(!)")
    print("Calculator can operate in radians or degrees. To change this, enter \"rad\" or \"deg\".")
    print("Current behavior is in radians.") if radian_mode else print("Current behavior is in degrees.")
    return 1
  elif command == "exit":
    return 0
  elif command == "rad":
    radian_mode = True
    print("Input set to radians for trigonometric functions.")
    return 1
  elif command == "deg":
    radian_mode = False
    print("Input set to degrees for trigonometric functions.")
    return 1

def parse_expression(user_request):
  '''Parses user input string and returns a list of form operand, operator, operand (operator, operand for factorial uniquely) or None for strings which fail parsing.'''
  expression = re.split(r"([\+\-\*/\(\^!])", user_request)
  if len(expression) != 3:
    return None
  elif expression[1] == "!":
    return expression[2], expression[1], None
  elif expression[1] == "(":
    expression[2] = expression[2].rstrip(')')
    if is_number(expression[2]):
      return expression[2], expression[0], None
    else:
      return None
  elif not (is_number(expression[0]) and is_number(expression[2])):
      return None
  print(expression)
  return expression

#Author: Piotr Stobierski
radian_mode = True
print("Hello! Welcome to the python terminal calculator.")
while True:
  user_request = input("Enter any two variable operation to see its result (or enter \"help\" to see instructions), or \"exit\".\n")
  command_ran = run_command(user_request)
  if command_ran:
    continue
  elif command_ran == False:
    break
  expression = parse_expression(user_request)
  if expression == None:
    print("Invalid expression.")
    continue
  match expression[1]:
    case "cos":
      if radian_mode:
        print("Your result is:", cos(float(expression[0])))
      else:
        print("Your result is:", cos(calc_radians(float(expression[0]))))
    case "sin":
      if radian_mode:
        print("Your result is:", sine(float(expression[0])))
      else:
        print("Your result is:", sine(calc_radians(float(expression[0]))))
    case "tan":
      if radian_mode:
        print("Your result is:", tan(float(expression[0])))
      else:
        print("Your result is:", tan(calc_radians(float(expression[0]))))
    case "!":
      print("Your result is:", end=" ")
      print_factorial_result(int(expression[0]))
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
      print("Unknown command or format. Make sure expressions are of the form num1+num2 for binary operations, and cos(num) for unary operations.")


