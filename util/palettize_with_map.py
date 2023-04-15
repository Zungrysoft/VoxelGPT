from PIL import Image
import math
import json
import sys

SKIP = 1

def rts(n):
    return int(n/SKIP)*SKIP

def convert(map_file_name, palette_file_name, input_file_name, output_file_name):
    with open(map_file_name, 'r') as json_file:
        with open(palette_file_name, 'r') as json_file2:
            # Load json data
            map = json.load(json_file)
            palette = json.load(json_file2)["colors"]

            f = Image.open(input_file_name,)
            pixels_from = f.load()

            t = Image.new(mode="RGBA", size=(f.width, f.height))
            pixels_to = t.load()

            for y in range(f.height):
                for x in range(f.width):
                    c = pixels_from[x, y]
                    # ROUND TO SKIP
                    c = (rts(c[0]), rts(c[1]), rts(c[2]))
                    index = map[f"{c[0]},{c[1]},{c[2]}"]
                    pixels_to[x, y] = tuple(palette[index])

            t.save(output_file_name)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} [map.json] [palette.json] [input_image.png] [output_image.png]")
        exit()

    map_file_name = sys.argv[1]
    palette_file_name = sys.argv[2]
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    convert(map_file_name, palette_file_name, input_file_name, output_file_name)

    print("Done")
