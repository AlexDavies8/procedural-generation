import random
import os.path

class cell:

    def __init__(self, x, y):
        self.N = False
        self.E = False
        self.S = False
        self.W = False

        self.x = x
        self.y = y

    def HasUncarved(self):
        return self.N and self.E and self.S and self.W

def ConnectCells(start, end, dir):
    if dir == 'N':
        start.N = True
        end.S = True
    elif dir == 'E':
        start.E = True
        end.W = True
    elif dir == 'S':
        start.S = True
        end.N = True
    elif dir == 'W':
        start.W = True
        end.E = True

def AddDirection(pos, dir):
    if dir == 'N':
        return (pos[0], pos[1]+1)
    elif dir == 'E':
        return (pos[0]+1, pos[1])
    elif dir == 'S':
        return (pos[0], pos[1]-1)
    elif dir == 'W':
        return (pos[0]-1, pos[1])

def Carve(grid, currPos, visited):
    visited.append(currPos)
    
    dirs = ['N', 'E', 'S', 'W']
    for tries in range(4):
        dir = random.choice(dirs)
        newPos = AddDirection(currPos, dir)
        if newPos not in visited and 0 <= newPos[0] < width and 0 <= newPos[1] < height:
            ConnectCells(grid[currPos[0]][currPos[1]], grid[newPos[0]][newPos[1]], dir)
            grid, visited = Carve(grid, newPos, visited)
        dirs.remove(dir)
    
    return grid, visited

def RenderToString(grid):
    str = ""
    str += ((wallChar+" ")*(width*2+1)) + "\n"
    for y in range(height):
        h = wallChar+" "
        v = wallChar+" "
        for x in range(width):
            h += (spaceChar+" "+spaceChar+" ") if grid[x][y].E else (spaceChar+" "+wallChar+" ")
            v += (spaceChar+" "+wallChar+" ") if grid[x][y].N else (wallChar+" "+wallChar+" ")
        str += h + "\n"
        if y < width-1:
            str += (v) + "\n"
    str += ((wallChar+" ")*(width*2+1)) + "\n"

    return str

width, height = [int(x) for x in input("Enter Maze Dimensions:\n> ").split()]
wallChar = input("Enter Wall Character:\n> ")
spaceChar = input("Enter Space Character:\n> ")
gr = []
for x in range(width):
    gr.append([cell(x, y) for y in range(height)])

gr, _ = Carve(gr, (0, 0), [])

mapStr = RenderToString(gr)

if width <= 30 and height <= 30:
    print(mapStr)

filepath = input("Filename to save to (leave blank if not saving):\n> ")
if filepath != "":
    ext = os.path.splitext(filepath)[1]

    if ext == ".txt":
        file = open(filepath, "w")
        file.write(mapStr)
        file.close()
    elif ext == ".png" or ext == ".jpg":
        from PIL import Image
        img = Image.new('RGB', (width*2+1, height*2+1))
        for x in range(width):
            for y in range(height):
                img.putpixel((x*2+1, y*2+1), (255, 255, 255))
                img.putpixel((x*2+2, y*2+2), (0, 0, 0))
                img.putpixel((x*2+2, y*2+1), ((255, 255, 255) if gr[x][y].E else (0, 0, 0)))
                img.putpixel((x*2+1, y*2+2), ((255, 255, 255) if gr[x][y].N else (0, 0, 0)))
        img.save(filepath)
    else:
        print("File extension not recognised\nOnly .txt, .png and .jpg files are supported")
    

