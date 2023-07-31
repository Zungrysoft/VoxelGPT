from PIL import Image
import sys

def create_palette(image_path, output_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    width, height = img.size
    colors = set()
    for y in range(height):
        for x in range(width):
            colors.add(img.getpixel((x, y)))

    palette_name = image_path.split('/')[-1].split('.')[0]
    gpl_file = open(output_path, 'w')
    gpl_file.write(f"GIMP Palette\nName: VoxelGPT\nColumns: 3\n#\n")

    for color in colors:
        gpl_file.write(f"{color[0]} {color[1]} {color[2]}\n")

    gpl_file.close()

if __name__ == "__main__":
    # Read in command line arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [source.png] [output.json]")
        exit()

    source_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    create_palette(source_file_name, output_file_name)