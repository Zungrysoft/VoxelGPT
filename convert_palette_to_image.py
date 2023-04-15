from PIL import Image
import math
import json
import sys

TILE_SIZE = 32

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} [source.json] [output.png]")
    exit()

file_name = sys.argv[1]
output_file_name = sys.argv[2]

with open(file_name, 'r') as json_file:
    # Load json data
    data = json.load(json_file)
    colors = data["colors"]
    colors = [[0, 0, 0], [0, 0, 0]] + colors

    # Figure out image dimensions
    num_colors = len(colors)
    width = int(math.sqrt(num_colors))
    height = int(math.ceil(num_colors/width))
    print(f"Converting palette of {num_colors} colors...")

    # Declare image
    pal = Image.new(mode="RGBA", size=(width, height))
    pixels = pal.load()

    # Iterate over colors and save them to their respective place on the image
    for i, color in enumerate(colors):
        x = i % width
        y = int(i / width)
        pixels[x, y] = tuple(color)
    
    # Scale up the image
    pal = pal.resize((width*TILE_SIZE, height*TILE_SIZE), Image.NEAREST)

    # Save result
    pal.save(output_file_name)

    print("Done")










