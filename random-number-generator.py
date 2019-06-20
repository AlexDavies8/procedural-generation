from random import randint

try:
    min = int(input("Enter minimum:\n> "))
except:
    min = 0

try:
    max = int(input("Enter maximum:\n> "))
except:
    max = 10

print("Enter '0' to exit, press Return/Enter for a new number")

while True:
    print(randint(min, max), end='')
    
    if input(' ') == '0':
        break
