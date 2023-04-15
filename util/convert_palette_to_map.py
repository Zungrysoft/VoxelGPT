from PIL import Image
import math
import json
import sys
import colorsys
import datetime

WEIGHT_HUE = 1.1
WEIGHT_SAT = 0.9
WEIGHT_VAL = 1

SCALE_FACTOR_SAT = 0.5
SCALE_FACTOR_VAL = 0.5

CHECK_RATE = 1 # In seconds
SKIP = 5
TOTAL_CALCS = int(256/SKIP + 1)**3

def lerp(a, b, f):
    return (1-f)*a + f*b

def hsv_dist(a, b):
    # Figure out linear distances of each component
    # h_dist = min(min(abs(a[0]-b[0])*WEIGHT_HUE, abs((a[0]+1)-b[0])*WEIGHT_HUE), abs((a[0]-1)-b[0])*WEIGHT_HUE)
    h_dist = (a[0]-b[0])*WEIGHT_HUE
    s_dist = (a[1]-b[1])*WEIGHT_SAT
    v_dist = (a[2]-b[2])*WEIGHT_VAL

    # Scale down hue and saturation when value is low
    # When value is 0, hue and saturation have no effect on the result
    v_scale = lerp(1, ((a[2]+b[2]) / 2), SCALE_FACTOR_VAL)
    h_dist *= v_scale
    s_dist *= v_scale

    # Scale down hue when saturation is low
    s_scale = lerp(1, ((a[1]+b[1]) / 2), SCALE_FACTOR_SAT)
    h_dist *= s_scale

    # Calculate euclidean distance
    dist = h_dist**2 + s_dist**2 + v_dist**2
    return dist

def find_closest(rgb, palette):
    # Convert rgb(0 - 255) to hsv(0.0 - 1.0)
    hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)

    # Iterate over palette colors to find the closest one
    closest_index = 0
    closest_distance = 999999999
    for index, color in enumerate(palette[2:]):
        # Convert rgb(0 - 255) to hsv(0.0 - 1.0)
        palette_hsv = colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)

        # Find the distance between these to colors
        dist = hsv_dist(palette_hsv, hsv)

        # Check if this is the closest color so far
        if dist < closest_distance:
            closest_distance = dist
            closest_index = index + 2 # The +2 is to compensate for skipping the first two (reserved) elements of the list

    # Return closest color
    return closest_index

def convert(input_file_name, output_file_name):
    with open(input_file_name, 'r') as json_file:
        # Load json data
        palette = json.load(json_file)["colors"]

        # For each rgb value, find its closest in palette
        result = {}
        completed = 0
        prev_check = datetime.datetime.now()
        for r in range(0, 256, SKIP):
            for g in range(0, 256, SKIP):
                for b in range(0, 256, SKIP):
                    closest = find_closest((r, g, b), palette)
                    result[f"{r},{g},{b}"] = closest

                    # Every CHECK_RATE seconds, print percent completion
                    completed += 1
                    if (datetime.datetime.now().second - prev_check.second) > CHECK_RATE:
                        prev_check = datetime.datetime.now()
                        percent = int((completed/TOTAL_CALCS)*100)
                        print(f"{completed}/{TOTAL_CALCS} ({percent}%)")

        # Write output file
        with open(output_file_name, 'w') as output_file:
            json.dump(result, output_file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [source.json] [output.png]")
        exit()

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    convert(input_file_name, output_file_name)

    print("Done")
