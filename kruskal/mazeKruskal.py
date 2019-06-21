import random
import os.path

class cell:
    def __init__(self, pos):
        self.parent = None
        self.position = pos
        self.N = False
        self.E = False

    def getRoot(self):
        return (self.parent.getRoot() if self.parent else self)

def MergeCells(a, b):
    if a.getRoot() != b.getRoot():
        b.getRoot().parent = a
        return True
    return False

def GenerateMaze():

    #Create cells
    cells = []
    for x in range(width):
        cells.append([])
        for y in range(height):
            cells[x].append(cell((x, y)))

    #Create edges
    edges = []
    for x in range(width):
        for y in range(height):
            if y < width-1:
                edges.append((x, y, 'N'))
            if x < height-1:
                edges.append((x, y, 'E'))
    random.shuffle(edges)

    dirs = {'N' : (0, 1), 'E' : (1, 0)}

    while len(edges) > 0:

        x, y, dir = edges.pop()
        nx, ny = x + dirs[dir][0], y + dirs[dir][1]

        cella, cellb = cells[x][y], cells[nx][ny]

        if MergeCells(cella, cellb):
            if dir == 'N':
                cella.N = True
            elif dir == 'E':
                cella.E = True

    return cells

def ConvertToText(cells):
    string = wallChar * (width * 2 + 1) + "\n"
    for y in range(height):
        h = wallChar
        v = wallChar
        for x in range(width):
            h += spaceChar + spaceChar if cells[x][y].E else spaceChar + wallChar
            v += spaceChar + wallChar if cells[x][y].N else wallChar + wallChar
        string += h + "\n" + v + "\n"
    return string

def OutputToImage(cells, path):
    from PIL import Image
    
    img = Image.new('RGB', (width*2+1, height*2+1))
    for x in range(width):
        for y in range(height):
            img.putpixel((x*2+1, y*2+1), (255, 255, 255))
            img.putpixel((x*2+2, y*2+2), (0, 0, 0))
            img.putpixel((x*2+2, y*2+1), ((255, 255, 255) if cells[x][y].E else (0, 0, 0)))
            img.putpixel((x*2+1, y*2+2), ((255, 255, 255) if cells[x][y].N else (0, 0, 0)))
    img.save(path)

def OutputToTxt(string, path):
    file = open(path, "w")
    file.write(string)
    file.close()

width, height = [int(x) for x in input("Enter Maze Dimensions:\n> ").split()]

wallChar = input("Enter Wall Character:\n> ") + " "
spaceChar = input("Enter Space Character:\n> ") + " "

maze = GenerateMaze()

mazeStr = ConvertToText(maze)

if width <= 30 and height <= 30:
    print(mazeStr)
    
filepath = input("Filename to save to (leave blank if not saving):\n> ")

if filepath != "":
    ext = os.path.splitext(filepath)[1]

    if ext == ".txt":
        OutputToTxt(mazeStr, filepath)
    elif ext == ".png" or ext == ".jpg":
        OutputToImage(maze, filepath)







    
