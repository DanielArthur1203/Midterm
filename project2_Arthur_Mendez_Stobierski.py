import math
import decimal
import re
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

#Author: Daniel Arthur
def numpy_gamma(values):
  """Evaluates the Gamma function for both scalar values and NumPy arrays."""
  scalar_gamma = np.vectorize(math.gamma, otypes=[float])
  return scalar_gamma(values)

#Author: Daniel Arthur
def sample_function(function, x):
  """Returns a new ndarray with resampled y values for the new x range"""

  try: #Everything in the try here handles potential edge cases like zooming out too far
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
      y = function(x)
  except (OverflowError, ValueError, ZeroDivisionError):
    y = np.full(x.shape, np.nan)
    for index, value in enumerate(x):
      try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
          y[index] = function(float(value))
      except (OverflowError, ValueError, ZeroDivisionError):
        continue

  y = np.asarray(y)
  if np.iscomplexobj(y):
    y = np.where(np.isclose(y.imag, 0), y.real, np.nan)
  if y.ndim == 0:
    y = np.full(x.shape, y.item(), dtype=float)
  else:
    y = np.broadcast_to(y, x.shape).astype(float, copy=True)
  y[~np.isfinite(y)] = np.nan
  return y


#Author: Daniel Arthur
def function_from_string(string: str):
  """Returns a tuple containing the simplified function for matplotlib. If syntax is invalid then None is returned"""
  x_sym = sp.Symbol("x")
  x = np.linspace(-10, 10, 100)
  if "x!" in string:
    string = string.replace("x!", "gamma(x+1)")
    x = np.linspace(0, 10, 100)
  try:
    equation = sp.simplify(string)
    f = sp.lambdify(x_sym, equation, modules=[{"gamma": numpy_gamma}, "numpy"],)
    y = sample_function(f, x)
  except (sp.SympifyError, ValueError, TypeError):
    print("Syntax Error(see help for info on syntax)")
    return None
  except KeyError:
     print("Do not divide by 0 or input complex infinites(i.e. zoo)")
     return None
  except IndexError:
     print("Parsing Error. Please make sure you are keeping it to arithmetic operators and trig functions.")
     return None
  except NameError:
     print("Undefined Function Entered. Please make sure you are keeping it to arithmetic operators and trig functions.")
     return None
  except:
    print("Syntax Error(see help for info on syntax)")
    return None
  return y, equation, x

#Author: Daniel Arthur
def graph(function):
  """Plots whatever function of x was inputted provided that the syntax was valid."""
  result = function_from_string(function)
  if result is None: return

  y = result[0]
  equation = result[1]
  x = result[2]

  fig, ax = plt.subplots(num="Graph")
  try:
    line, = ax.plot(x, y, label=f"y = {equation}")
    ax.legend()
    ax.grid(True)

    f = sp.lambdify(sp.Symbol("x"), equation, modules=[{"gamma": numpy_gamma}, "numpy"],)
    previous_x_span = abs(x[-1] - x[0])

    def update_graph(_):
      """Callback function to update graph when the user zooms out"""
      nonlocal previous_x_span #Force use previous_x_span in the scope of graph
      x_min, x_max = ax.get_xlim()
      if not np.isfinite(x_min) or not np.isfinite(x_max) or x_min == x_max:
        return

      visible_x = np.linspace(x_min, x_max, 2000)
      visible_y = sample_function(f, visible_x)
      line.set_data(visible_x, visible_y)
      finite_y = visible_y[np.isfinite(visible_y)]
      current_x_span = abs(x_max - x_min)

      if current_x_span > previous_x_span and finite_y.size:
        if np.max(np.abs(finite_y)) <= np.sqrt(np.finfo(float).max):
          y_min, y_max = np.min(finite_y), np.max(finite_y)
          y_margin = (y_max - y_min) * 0.05
          if y_margin == 0:
            y_margin = max(abs(y_min) * 0.05, 0.5)
          ax.set_ylim(y_min - y_margin, y_max + y_margin)
      previous_x_span = current_x_span
      fig.canvas.draw_idle()

    ax.callbacks.connect("xlim_changed", update_graph)
    plt.show()
  except ValueError:
    print("Syntax Error(see help for info on syntax)")
    return
  except:
     print("Syntax Error(see help for info on syntax)")
     return

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
       return "Domain Error"

    try:
        num = factorial(n)
        if(num < math.pow(10, 6)):
            return num #Number not large enough to justify scientific notation
        else:
            return f"{num:e}" #Print with scientific notation
    except ValueError as e: 
        msg = str(e)
        if("Domain" in msg):
           return "Domain Error"
        else:
            return "Value too large" #Happens when num has too many digits to be converted to a str
    except OverflowError as e:
        d = decimal.Decimal(num) #OverflowError happens when num is too large to convert through f print so decimal is needed
        return f"{d:.2e}"
    except:
        return "Unknown Error"

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

# Author: Joel Mendez
def add_to_history(history, expression, result):
    """Saves a calculation to the history list."""
    history.append((expression, result))


# Author: Joel Mendez
def show_history(history):
    """Displays all previous calculations."""
    if len(history) == 0:
        print("No history yet.")
    else:
        number = 1

        for entry in history:
            print(f"{number}. {entry[0]} = {entry[1]}")
            number += 1


# Author: Joel Mendez
def clear_history(history):
    """Clears all previous calculations."""
    history.clear()

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
    print("Supported unary operations: cosine(cos(num)), sine(sin(num)), tangent(tan(num)), factorial(!) Note: factorial is entered in postfix notation")
    print("Calculator can operate in radians or degrees. To change this, enter \"rad\" or \"deg\".")
    print("Current behavior is in radians.") if radian_mode else print("Current behavior is in degrees.")
    print("When graphing be sure to input arithmetic operators in Python syntax. Ex: To graph y = 2x simply input 2 * x. For y = x^2 do x ** 2. Do not input any complex values")
    print("Enter \"history\" to see your past calculations, or \"clear\" to erase them.")
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
  elif command == "graph":
    function = input("Enter function: ")
    graph(function)
    return 1
  elif command == "history":
    show_history(history)
    return 1
  elif command == "clear":
    clear_history(history)
    print("History cleared.")
    return 1

def parse_expression(user_request):
  '''Parses user input string and returns a list of form operand, operator, operand (operator, operand for factorial uniquely) or None for strings which fail parsing.'''
  unary_expression = re.fullmatch(
      r"\s*(sin|cos|tan)\s*\(\s*([^()]*)\s*\)\s*",
      user_request,
      re.IGNORECASE,
  )
  if unary_expression and is_number(unary_expression.group(2)):
    return unary_expression.group(2).strip(), unary_expression.group(1).lower(), None

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
  return expression

#Author: Piotr Stobierski
radian_mode = True
history = []
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
  result = None
  match expression[1]:
    case "cos":
      if radian_mode:
        result = cos(float(expression[0]))
      else:
        result = cos(calc_radians(float(expression[0])))
    case "sin":
      if radian_mode:
        result = sine(float(expression[0]))
      else:
        result = sine(calc_radians(float(expression[0])))
    case "tan":
      if radian_mode:
        result = tan(float(expression[0]))
      else:
        result = tan(calc_radians(float(expression[0])))
    case "!":
      result = print_factorial_result(expression[0])
    case "+":
      result = add(float(expression[0]), float(expression[2]))
    case "-":
      result = subtract(float(expression[0]), float(expression[2]))
    case "*":
      result = multiply(float(expression[0]), float(expression[2]))
    case "/":
      result = divide(float(expression[0]), float(expression[2]))
    case "^":
      result = power(float(expression[0]), float(expression[2]))
    case _:
      print("Unknown command or format. Make sure expressions are of the form num1+num2 for binary operations, and cos(num) for unary operations.")
  if result is not None:
    print("Your result is:", result)
    if is_number(str(result)):
      add_to_history(history, user_request.strip(), result)
