from opensimplex import OpenSimplex
import os

heightRanges = [(0.00, (0, 50, 255)),
                (0.35, (50, 100, 255)),
                (0.40, (255, 255, 110)),
                (0.55, (50, 200, 50)),
                (0.65, (0, 140, 0)),
                (0.75, (100, 50, 20)),
                (0.90, (230, 230, 255)),
                (0.92, (255, 255, 255))]

def GenerateNoiseMap(width, height, octaves=4, lacunarity=2.0, gain=0.5, xoffset=0, yoffset=0, xscale=1, yscale=1, seed=0):

    #Create map array
    map = []
    for x in range(width):
        map.append([])
        for y in range(height):
            map[x].append(0.0)

    #Get Noise Generator
    noiseGen = OpenSimplex(seed=seed)

    minNoise = 999.9
    maxNoise = -999.9
    
    #Loop over cells and get noise
    for x in range(width):
        for y in range(height):
            amplitude = 1.0
            frequency = 1.0
            n = 0
            for i in range(octaves):
                n += noiseGen.noise2d(x=x*xscale*frequency+xoffset,
                                      y=y*yscale*frequency+yoffset) * amplitude

                amplitude *= gain
                frequency *= lacunarity
            if n < minNoise:
                minNoise = n
            if n > maxNoise:
                maxNoise = n
            map[x][y] = n

    #Normalize noise to between 0 and 1
    for x in range(width):
        for y in range(height):
            map[x][y] = (map[x][y]-minNoise) / (maxNoise-minNoise)
    
    return map

def OutputToImage(grid, path):
    from PIL import Image
    
    img = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            col = heightRanges[len(heightRanges)-1][1]
            for c in heightRanges:
                 if c[0] >= grid[x][y]:
                     col = c[1]
                     break
            img.putpixel((x, y), col)
    img.save(path)

width, height = [int(x) for x in input("Enter Noise Map Dimensions(x y):\n> ").split()]
xscale, yscale, xoffset, yoffset = 0.02, 0.02, 0, 0
seed = 0
octaves = 8
lacunarity, gain = 2.0, 0.5
if input("Fractal Options?(y/n)\n> ") == "y":
    octaves = int(input("Enter Noise Octaves\n> "))
    lacunarity = float(input("Enter Noise Lacunarity\n> "))
    gain = float(input("Enter Noise Gain\n> "))
if input("Advanced Options?(y/n)\n> ") == "y":
    xscale, yscale = [float(x) for x in input("Enter Noise Scale(x y):\n> ").split()]
    xoffset, yoffset = [float(x) for x in input("Enter Noise Offset(x y):\n> ").split()]
    seed = int(input("Enter Noise Seed:\n> "))

map = GenerateNoiseMap(width, height,
                       xoffset=xoffset, yoffset=yoffset,
                       xscale=xscale, yscale=yscale,
                       seed=seed,
                       octaves=octaves,
                       lacunarity=lacunarity, gain=gain)

filepath = input("Filename to save to (leave blank if not saving):\n> ")

if filepath != "":
    ext = os.path.splitext(filepath)[1]

    if ext == ".png" or ext == ".jpg":
        OutputToImage(map, filepath)
