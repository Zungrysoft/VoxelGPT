import os
import json
import random
import math
import vector as vec
import numpy as np

AIR = 1
UNDECIDED = 0

SIZE = (20, 20, 20)

def encode(pos, i, size):
    if i % 2 == 0:
        return math.sin(pos/(10000**((2*i)/size)))
    else:
        return math.cos(pos/(10000**((2*(i-1))/size)))

# Define embedding function
COLOR_EMBEDDING_LENGTH = 10
# red, green, blue, hue, saturation (hsv), value, saturation (hsl), lightness, transparent, next
def embed(index, position, color_index, palette, embedding_size):
    # Get rgb value
    # Next voxel's positional encoding
    if color_index == -1:
        embedding = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    # Air voxel
    elif color_index == 0 or color_index == 1:
        embedding = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    # Solid voxel
    else:
        # Set up values
        color = palette[color_index]
        embedding = []

        # rgb
        embedding.append(color["rgb"][0])
        embedding.append(color["rgb"][1])
        embedding.append(color["rgb"][2])

        # hsv
        embedding.append(color["hsv"][0])
        embedding.append(color["hsv"][1])
        embedding.append(color["hsv"][2])

        # hsl
        embedding.append(color["hsl"][1])
        embedding.append(color["hsl"][2])

        # not transparent
        embedding.append(0.0)

        # not the next voxel
        embedding.append(1.0)

    # Add positional encoding
    dimension_length = int((embedding_size - COLOR_EMBEDDING_LENGTH) / 3)
    for coord in position:
        for i in range(dimension_length):
            embedding.append(encode(coord, i, dimension_length))

    # Add index-positional encoding for the remainder of the embedding-size
    index_dimension_length = embedding_size - len(embedding)
    for i in range(index_dimension_length):
        embedding.append(encode(index, i, index_dimension_length))

    # Return
    return embedding

def embed_nptest(index, position, color_index, palette, embedding_size):
    pos_index = position[0] + (position[1] * SIZE[0]) + (position[2] * SIZE[0] * SIZE[1])

    embedding = []
    for i in range(embedding_size):
        embedding.append(1 if i == pos_index else 0)

    return embedding


# Encode a palette index into a one-hot-encoded output vector
def encode_one_hot(index, length):
    # Change UNDECIDED into AIR
    if index < 1:
        index = 1

    # Create the zeros vector
    ret = np.zeros((length-1,))

    # Add the one at the right index
    # We remove the zero index because the sculptures should never output UNDECIDED
    ret[index-1] = 1.0
    return ret

def remove_farthest(context, pos):
    # Find which context element is the farthest away
    farthest_index = 0
    farthest_dist = 0
    for i in range(len(context)):
        cur_dist = vec.dist(context[i][0], pos)
        if cur_dist > farthest_dist:
            farthest_dist = cur_dist
            farthest_index = i

    # Delete that context element and return
    del context[farthest_index]
    return context

def get(voxels, key, all_decided=False):
    # If the key is in tuple form, convert it
    if type(key) is tuple:
        key = vec.ttos(key)

    if key in voxels:
        # Return the value of the voxel coords
        return voxels[key]
    else:
        # If it's not in the voxels dictionary, return UNDECIDED
        # all_decided mode makes this return AIR instead, since training example
        # models should act as if every voxel is decided
        return AIR if all_decided else UNDECIDED

# Given a voxel and context, determine how much context this voxel will have and score it accordingly
# This method wants to be as close as possible to nearby voxels
# It also adds a little bit of variance to the resulting score, so different voxel pick orders will happen.
def get_voxel_score(pos, context):
    total = 0
    center_pos = (int(SIZE[0]/2), int(SIZE[1]/2), int(SIZE[2]/2))
    for voxel in context:
        total += 1/(vec.dist(pos, voxel[0]) + 0.01)
    total += len(context)/(vec.dist(pos, center_pos) + 0.01)
    return total * (random.random() + 1)

# Pick by building outwards
def pick_next_voxel_clump(built_voxels, context):
    cur_pos = context[-1][0]
    best_score = 0
    best_voxel = None

    # Check all voxels within 2 spaces
    for x in range(-2, 3):
        for y in range(-2, 3):
            for z in range(-2, 3):
                voxel = vec.add((x, y, z), cur_pos)
                # Make sure this voxel hasn't already been built
                if get(built_voxels, voxel) == UNDECIDED:
                    score = get_voxel_score(voxel, context)
                    if score > best_score:
                        best_score = score
                        best_voxel = voxel

    # Check some random voxels farther away
    check_count = 15
    check_radius = 3
    while best_voxel == None:
        # check_count > 0 or

        x = int((random.random() - 0.5) * check_radius * 2)
        y = int((random.random() - 0.5) * check_radius * 2)
        z = int((random.random() - 0.5) * check_radius * 2)

        voxel = vec.add((x, y, z), cur_pos)
        # Make sure this voxel hasn't already been built
        if get(built_voxels, voxel) == UNDECIDED:
            score = get_voxel_score(voxel, context)
            if score > best_score:
                best_score = score
                best_voxel = voxel

        check_count -= 1
        check_radius += 0.5

    return best_voxel

# Pick linearly in size
def pick_next_voxel_linear(built_voxels, context):
    x, y, z = context[-1][0]

    # X axis
    x += 1
    if x >= SIZE[0]:
        x = 0

        # Y axis
        y += 1
        if y >= SIZE[1]:
            y = 0

            # Z axis
            z += 1

    return (x, y, z)

def pick_next_voxel_random(built_voxels, context):
    pick = (math.floor(random.random() * SIZE[0]), math.floor(random.random() * SIZE[1]), math.floor(random.random() * SIZE[2]))
    while (vec.ttos(pick) in built_voxels):
        pick = pick_next_voxel_linear(built_voxels, [(pick, 1)])

    return pick

# Decide the coordinates of the next voxel to pick
def pick_next_voxel(built_voxels, context):
    return pick_next_voxel_linear(built_voxels, context)

# Generate one training example
def generate_examples(voxels, context_size):
    # Pick starter voxel at random
    # start_pos = (0, 0, 0)
    # start_pos = (int(SIZE[0]/2), int(SIZE[1]/2), int(SIZE[2]/2))
    keys = list(voxels.keys())
    start_pos = vec.stot(keys[int(random.random()*len(keys))])
    # start_pos = (int(random.random()*SIZE[0]), int(random.random()*SIZE[1]), int(random.random()*SIZE[2]-1))

    # Set up dict for voxels that have already been built
    built_voxels = {}
    built_voxels[vec.ttos(start_pos)] = get(voxels, start_pos, True)

    # Build context list
    context = []
    context.append((start_pos, get(voxels, start_pos, True)))

    # Generate examples
    ret = []
    for i in range(context_size):
        # Determine the next voxel
        next_voxel = pick_next_voxel(built_voxels, context)

        # Add it to built voxels map
        index_at_position = get(voxels, next_voxel, True)
        built_voxels[vec.ttos(next_voxel)] = index_at_position

        # Add it to context window
        context.append((next_voxel, index_at_position))
        if len(context) > context_size+1:
            context = remove_farthest(context, next_voxel)

    ret.append(context)
    return ret

# Generate n training examples, sampled from all of the json files in the training data
def generate_training_examples(num_examples, context_size):
    # Get filenames of all voxel files in training corpus
    filenames = os.listdir('training/json')
    filenames = list(filter(lambda f : "sor" in f, filenames))

    # Determine how many examples we should generate from each file
    examples_each = int(num_examples / len(filenames))
    examples_remainder = num_examples % len(filenames)

    # For each file...
    examples = []
    for filename in filenames:
        with open("training/json/" + filename, 'r') as json_file:
            # Load json data
            voxels = json.load(json_file)["voxels"]

            # Determine how many examples to generate
            # Any remainder examples are spread across the first few files
            num_examples = examples_each
            if examples_remainder > 0:
                examples_remainder -= 1
                num_examples += 1

            # Generate training examples
            for _ in range(num_examples):
                examples += generate_examples(voxels, context_size)

    return examples
