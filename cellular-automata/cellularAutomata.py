import random
import os.path

def GenerateCave():
    grid = []
    for x in range(width):
        grid.append([])
        for y in range(height):
            grid[x].append(random.uniform(0, 100) <= wallPercentage)

    for i in range(iterations):
        grid = IterateCave(grid)

    return grid 
    
def IterateCave(grid):
    new = list(map(list, grid))#Copy grid

    for x in range(width):
        for y in range(height):
            count = GetNeighbourCount(grid, x, y)
            if grid[x][y] and count < 3: #If alive and too few neighbours, kill it
                new[x][y] = False
            elif (not grid[x][y]) and count > 4: #If dead and enough neighbours, make it alive
                new[x][y] = True
                
    return new

def GetNeighbourCount(grid, x, y):
    count = 0
    for fx in range(-1, 2):
        for fy in range(-1, 2):
            if fx == 0 and fy == 0: #Ignore itself when counting neighbours
                continue
            nx = x+fx
            ny = y+fy

            if 0 <= nx < width and 0 <= ny < height:
                count += 1 if grid[nx][ny] else 0 #Add 1 if neighbour is solid
            else:
                count += 1 #Treat edges as solid
    return count

def ConvertToText(grid):
    string = ""
    for y in range(height):
        ln = ""
        for x in range(width):
            ln += wallChar if grid[x][y] else spaceChar
        string += ln + "\n"
    return string

def OutputToImage(grid, path):
    from PIL import Image
    
    img = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            img.putpixel((x, y), (0, 0, 0) if grid[x][y] else (255, 255, 255))
    img.save(path)

def OutputToTxt(string, path):
    file = open(path, "w")
    file.write(string)
    file.close()

width, height = [int(x) for x in input("Enter Maze Dimensions:\n> ").split()]

wallPercentage = float(input("Enter Percentage Starting Walls (recommended 45):\n> "))
iterations = int(input("Enter Generation Iterations (recommended 4):\n> "))

wallChar = input("Enter Wall Character:\n> ") + " "
spaceChar = input("Enter Space Character:\n> ") + " "

cave = GenerateCave()

caveStr = ConvertToText(cave)

if width <= 60 and height <= 60:
    print(caveStr)

filepath = input("Filename to save to (leave blank if not saving):\n> ")

if filepath != "":
    ext = os.path.splitext(filepath)[1]

    if ext == ".txt":
        OutputToTxt(caveStr, filepath)
    elif ext == ".png" or ext == ".jpg":
        OutputToImage(cave, filepath)

