from opensimplex import OpenSimplex
import os

def GenerateNoiseMap(width, height, xoffset=0, yoffset=0, xscale=1, yscale=1, seed=0):

    #Create map array
    map = []
    for x in range(width):
        map.append([])
        for y in range(height):
            map[x].append(0.0)

    #Get Noise Generator
    noiseGen = OpenSimplex(seed=seed)
    
    #Loop over cells and get noise
    for x in range(width):
        for y in range(height):
            map[x][y] = noiseGen.noise2d(x=x*xscale+xoffset, y=y*yscale+yoffset)
            map[x][y] = (map[x][y]+1)/2 #Map from (-1 to 1) to (0 to 1)

    return map

def OutputToImage(grid, path):
    from PIL import Image
    
    img = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            img.putpixel((x, y), (int(grid[x][y]*255), int(grid[x][y]*255), int(grid[x][y]*255)))
    img.save(path)

width, height = [int(x) for x in input("Enter Noise Map Dimensions(x y):\n> ").split()]
xscale, yscale, xoffset, yoffset = 0.2, 0.2, 0, 0
seed = 0
if input("Advanced Options?(y/n)\n> ") == "y":
    xscale, yscale = [float(x) for x in input("Enter Noise Scale(x y):\n> ").split()]
    xoffset, yoffset = [float(x) for x in input("Enter Noise Offset(x y):\n> ").split()]
    seed = int(input("Enter Noise Seed:\n> "))

map = GenerateNoiseMap(width, height,
                       xoffset=xoffset, yoffset=yoffset,
                       xscale=xscale, yscale=yscale,
                       seed=seed)

filepath = input("Filename to save to (leave blank if not saving):\n> ")

if filepath != "":
    ext = os.path.splitext(filepath)[1]

    if ext == ".png" or ext == ".jpg":
        OutputToImage(map, filepath)
