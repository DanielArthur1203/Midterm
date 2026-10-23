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

