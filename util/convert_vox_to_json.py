# This code converts back and forth between .vox and .json

import struct
import json
import os

SKIP = 5

# Load palette map json data
with open("data/palette_map.json", 'r') as json_file:
    network_color_map = json.load(json_file)

# Load palette json data
with open("data/palette.json", 'r') as json_file:
    network_palette = json.load(json_file)

def rts(n):
    return int(n/SKIP)*SKIP

def rgb_to_index(c):
    # print(c)
    c = (rts(c[0]), rts(c[1]), rts(c[2]))
    index = network_color_map[f"{c[0]},{c[1]},{c[2]}"]
    return index

def index_to_rgb(i):
    return network_palette["colors"][i]

def read_int(file):
    return struct.unpack('<i', file.read(4))[0]

def write_int(file, value):
    file.write(struct.pack('<i', value))

def default_palette():
    palette = [
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (255, 0, 0),
        (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128),
        (128, 128, 0), (0, 128, 128), (128, 0, 128), (128, 0, 128),
    ]
    return [(r, g, b, 255) for r, g, b in palette]

def read_vox_file(filename):
    size_x, size_y, size_z = None, None, None
    voxels = []
    palette = default_palette()

    with open(filename, 'rb') as file:
        if file.read(4) != b'VOX ':
            raise ValueError("Invalid .vox file format")

        if read_int(file) != 150:
            raise ValueError("Unsupported .vox version")

        # Read MAIN chunk header
        main_chunk_id, main_chunk_content_size, main_chunk_children_size = struct.unpack('<4sII', file.read(12))
        assert main_chunk_id == b'MAIN', f"Invalid MAIN chunk ID: {main_chunk_id}"
        main_chunk_end = file.tell() + main_chunk_children_size

        size_x, size_y, size_z = 0, 0, 0
        voxels = []
        palette = default_palette()

        # Process child chunks
        while file.tell() < main_chunk_end:
            chunk_id, chunk_content_size, chunk_children_size = struct.unpack('<4sII', file.read(12))
            if chunk_id == b'SIZE':
                size_x, size_y, size_z = struct.unpack('<3I', file.read(chunk_content_size))
            elif chunk_id == b'XYZI':
                num_voxels, = struct.unpack('<I', file.read(4))
                voxels = [struct.unpack('<4B', file.read(4)) for _ in range(num_voxels)]
            elif chunk_id == b'RGBA':
                palette_data = file.read(chunk_content_size)
                palette = [struct.unpack_from('<4B', palette_data, i * 4) for i in range(256)]
            else:
                # Ignore unsupported chunk and move to the next one
                file.seek(chunk_content_size + chunk_children_size, os.SEEK_CUR)

    return size_x, size_y, size_z, voxels, palette

def write_vox_file(filename, size_x, size_y, size_z, voxels, palette):
    with open(filename, 'wb') as file:
        file.write(b'VOX ')
        write_int(file, 150)

        file.write(b'MAIN')
        write_int(file, 0)
        write_int(file, 12 + 12 + 12 + 4 + len(voxels) * 4 + 12 + 256 * 4)

        file.write(b'SIZE')
        write_int(file, 12)
        write_int(file, 0)
        write_int(file, size_x)
        write_int(file, size_y)
        write_int(file, size_z)

        file.write(b'XYZI')
        write_int(file, 4 + len(voxels) * 4)
        write_int(file, 0)
        write_int(file, len(voxels))
        for x, y, z, color_index in voxels:
            file.write(struct.pack('<BBBB', x, y, z, color_index))

        # Prepare the palette (RGBA) chunk
        palette = palette[:256]  # Truncate the palette if it has more than 256 colors
        while len(palette) < 256:  # Fill the palette with default colors if it has less than 256 colors
            palette.append((0, 0, 0, 0))

        rgba_data = bytearray()
        for color in palette:
            rgba_data.extend(struct.pack('<4B', *color))

        file.write(b'RGBA')
        write_int(file, 256 * 4)
        write_int(file, 0)
        for r, g, b, a in palette:
            file.write(struct.pack('<BBBB', r, g, b, a))

def convert_json_to_vox(input_filename, output_filename):
    def get_color_index(color, palette):
        if len(color) < 4:
            color = (
                color[0],
                color[1],
                color[2],
                255
            )
        if color in palette:
            return palette.index(color) + 1
        else:
            if len(palette) >= 256:
                raise ValueError("Palette size exceeded the limit of 256 colors")
            palette.append(color)
            return len(palette)

    with open(input_filename, 'r') as input_file:
        data = json.load(input_file)

    size_x, size_y, size_z = data['size']['x'], data['size']['y'], data['size']['z']
    palette = []
    voxels = []
    for pos in data['voxels']:
        color_index = data['voxels'][pos]
        pos = tuple(pos.split(','))
        pos = (int(pos[0]), int(pos[1]), int(pos[2]))
        # print(index_to_rgb(color_index))
        ind = get_color_index(tuple(index_to_rgb(color_index)), palette)
        voxels.append(
            (
                pos[0],
                pos[1],
                pos[2],
                ind,
            )
        )

    # voxels2 = [(voxel['x'], voxel['y'], voxel['z'], get_color_index(tuple(voxel['color']), palette)) for voxel in data['voxels']]

    write_vox_file(output_filename, size_x, size_y, size_z, voxels, palette)

def convert_vox_to_json(input_filename, output_filename):
    size_x, size_y, size_z, voxels, palette = read_vox_file(input_filename)
    data = {
        'size': {'x': size_x, 'y': size_y, 'z': size_z},
        'voxels': {}
    }
    for x, y, z, color_index in voxels:
        # Convert vox palette index to rgb, then to an index in the network's palette
        my_palette_index = rgb_to_index(palette[color_index - 1][:3])
        data["voxels"][f"{x},{y},{z}"] = my_palette_index

    with open(output_filename, 'w') as output_file:
        json.dump(data, output_file, indent=2)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 4:
        print(f'Usage: {sys.argv[0]} [to_json | to_vox] input.{sys.argv[1]} output.{sys.argv[1]}')
        sys.exit(1)

    mode, input_filename, output_filename = sys.argv[1], sys.argv[2], sys.argv[3]

    if mode == 'to_json':
        convert_vox_to_json(input_filename, output_filename)
    elif mode == 'to_vox':
        convert_json_to_vox(input_filename, output_filename)
    else:
        print(f"Invalid mode: {mode}. Use 'to_json' or 'to_vox'.")
        sys.exit(1)
