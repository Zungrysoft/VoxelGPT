import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import color

def plot_voxel(voxels):
    with open('data/palette.json', 'r') as json_file:
        palette = json.load(json_file)['colors']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Iterate over voxels and plot them
    for voxel_pos, color_index in voxels.items():
        if color_index > 1:
            x, y, z = map(int, voxel_pos.split(","))
            r, g, b = palette[color_index]
            ax.scatter(x, y, z, c=[(r/255, g/255, b/255)], marker='s', s=200)

    ax.scatter(-1, -1, -1, c=[(0, 0, 0)], marker='o', s=1)
    ax.scatter(8, 8, 8, c=[(0, 0, 0)], marker='o', s=1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_box_aspect([1, 1, 1])

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [voxel_file.json]")
        exit()

    json_file = sys.argv[1]

    # Parse the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)["voxels"]
    plot_voxel(data)
