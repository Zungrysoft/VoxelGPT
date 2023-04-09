from PIL import Image
import math
import json
import sys

# Read in command line arguments
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} [source.png] [output.json]")
    exit()

source_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Open image
im = Image.open(source_file_name,)
pixels = im.load()

# Get all pixels
colors = []
for y in range(im.height):
    for x in range(im.width):
        colors.append(pixels[x, y][:3])

result = {
    "colors": colors
}

# Write output file
with open(output_file_name, 'w') as output_file:
    json.dump(result, output_file)
