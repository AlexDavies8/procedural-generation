import random
import os.path

class miner:

    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.steps = 0

    def move(self):
        moveDir = random.randint(1, 4)

        nx = 0
        ny = 0
        
        if moveDir == 1:
            nx = 1
        elif moveDir == 2:
            nx = -1
        elif moveDir == 3:
            ny = 1
        elif moveDir == 4:
            ny = -1

        if inBounds(self.x+nx, self.y+ny):
            self.x += nx
            self.y += ny
            self.steps += 1

    def canDig(self, grid):
        
        if inBounds(self.x+1, self.y):
            if grid[self.x+1][self.y]:
                return True
        if inBounds(self.x-1, self.y):
            if grid[self.x-1][self.y]:
                return True
        if inBounds(self.x, self.y+1):
            if grid[self.x][self.y+1]:
                return True
        if inBounds(self.x, self.y-1):
            if grid[self.x][self.y-1]:
                return True
        return False

def inBounds(x, y):
    return 0 <= x < width and 0 <= y < height

def GenerateCave():
    cave = []
    for x in range(width):
        cave.append([])
        for y in range(height):
            cave[x].append(True)

    miners = []
    miners.append(miner(width//2, height//2))

    totalMiners = 0

    while totalMiners < maxMiners:
        
        for i in range(len(miners)):
            if (not miners[i].canDig(cave)) and len(miners) > 1:
                del miners[i]
                break
            else:
                miners[i].move()
                cave[miners[i].x][miners[i].y] = False
                if random.randint(1, 100) == 8:
                    miners.append(miner(miners[i].x, miners[i].y))
                    totalMiners += 1
                if miners[i].steps > maxSteps:
                    miners[i].x, miners[i].y = width//2, height//2

    return cave

def CleanUp(cave):
    clean = False
    while not clean:
        clean = True
        for x in range(width):
            for y in range(height):
                if not cave[x][y]:
                    continue
                
                ncount = 0
                for nx in range(x-1, x+2):
                    for ny in range(y-1, y+2):
                        if nx == x and ny == y:
                            continue
                        if inBounds(nx, ny):
                            if cave[nx][ny]:
                                ncount += 1
                        else:
                            ncount += 1
                if ncount <= 2:
                    cave[x][y] = False
                    clean = False
    return cave

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

wallChar = input("Enter Wall Character:\n> ") + " "
spaceChar = input("Enter Space Character:\n> ") + " "

maxSteps = int((width+height)//2 * 1.5)
maxMiners = (width+height)//2

cave = GenerateCave()

cave = CleanUp(cave)

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





