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

print(multiply(5, 3))
print(multiply(-2, 4))
print(multiply(2.5, 3))

print(divide(10, 2))
print(divide(10, 0))
print(divide(-9, 3))

print(power(2, 3))
print(power(2, -1))
print(power(0, -1))
print(power(0, 0))