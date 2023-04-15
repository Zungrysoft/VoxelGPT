# This code converts back and forth between .vox and .json

import struct
import json

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

        main_chunk_id = file.read(4)
        if main_chunk_id != b'MAIN':
            raise ValueError("Missing 'MAIN' chunk")

        read_int(file)  # num_bytes_in_main
        read_int(file)  # num_bytes_in_child_chunks

        while True:
            chunk_id = file.read(4)
            if not chunk_id:
                break

            chunk_size = read_int(file)
            _ = read_int(file)  # num_bytes_in_child_chunks

            if chunk_id == b'SIZE':
                size_x, size_y, size_z = read_int(file), read_int(file), read_int(file)
            elif chunk_id == b'XYZI':
                num_voxels = read_int(file)
                for _ in range(num_voxels):
                    x, y, z, color_index = struct.unpack('<BBBB', file.read(4))
                    voxels.append((x, y, z, color_index))
            elif chunk_id == b'RGBA':
                palette = []
                for _ in range(256):
                    r, g, b, a = struct.unpack('<BBBB', file.read(4))
                    palette.append((r, g, b))
            else:
                file.read(chunk_size - 4)  # skip unknown chunk

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
    voxels = [(voxel['x'], voxel['y'], voxel['z'], get_color_index(tuple(voxel['color']), palette)) for voxel in data['voxels']]

    write_vox_file(output_filename, size_x, size_y, size_z, voxels, palette)

def convert_vox_to_json(input_filename, output_filename):
    size_x, size_y, size_z, voxels, palette = read_vox_file(input_filename)
    data = {
        'size': {'x': size_x, 'y': size_y, 'z': size_z},
        'voxels': {}
    }
    for x, y, z, color_index in voxels:
        data["voxels"][f"{x},{y},{z}"] = palette[color_index - 1][:3]

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
