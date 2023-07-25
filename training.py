import os
import json
import random
import math
import numpy as np

AIR = 1
UNDECIDED = 0

SIZE = (8, 8, 8)

def encode(pos, i, size):
    if i % 2 == 0:
        return math.sin(pos/(10000**((2*i)/size)))
    else:
        return math.cos(pos/(10000**((2*(i-1))/size)))

# Define embedding function
COLOR_EMBEDDING_LENGTH = 9
# red, green, blue, hue, saturation (hsv), value, saturation (hsl), lightness, transparent
def embed(index, position, color_index, palette, embedding_size):
    # Get rgb value
    if color_index <= 1:
        embedding = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
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

    # for i in range(embedding_size-4):
    #     embedding.append(encode(index, i, embedding_size-4))

    # repeat = math.ceil(embedding_size/4)
    # embedding = (embedding * repeat)[0 : embedding_size]

    # for i in range(embedding_size):
    #     embedding[i] += encode(index, i, embedding_size-4)

    # return embedding

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

def add(v1, v2):
    return (
        v1[0] + v2[0],
        v1[1] + v2[1],
        v1[2] + v2[2],
    )

def get(voxels, key, all_decided=False):
    # If the key is in tuple form, convert it
    if type(key) is tuple:
        key = ttos(key)

    if key in voxels:
        # Return the value of the voxel coords
        return voxels[key]
    else:
        # If it's not in the voxels dictionary, return UNDECIDED
        # all_decided mode makes this return AIR instead, since training example
        # models should act as if every voxel is decided
        return AIR if all_decided else UNDECIDED

def stot(s):
    try:
        spl = s.split(',')
        return (int(spl[0]), int(spl[1]), int(spl[2]))
    except:
        return (0, 0, 0)

def ttos(t):
    try:
        return f'{int(t[0])},{int(t[1])},{int(t[2])}'
    except:
        return '0,0,0'

# Gets the euclidean distance between two points
def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

# Given a voxel and context, determine how much context this voxel will have and score it accordingly
# This method wants to be as close as possible to nearby voxels
# It also adds a random amount of variance to the resulting score, so different voxel pick orders will happen.
def get_voxel_score(pos, context):
    total = 0
    for voxel in context:
        total += 1/(dist(pos, voxel[0]) + 0.01)
    total += len(context)/(dist(pos, (63, 63, 63)) + 0.01)
    return total * (random.random() + 1)

# Decide the coordinates of the next voxel to pick
def pick_next_voxel_old(built_voxels, context):
    cur_pos = context[-1][0]
    best_score = 0
    best_voxel = None

    # Check all voxels within 2 spaces
    for x in range(-2, 3):
        for y in range(-2, 3):
            for z in range(-2, 3):
                voxel = add((x, y, z), cur_pos)
                # Make sure this voxel hasn't already been built
                if get(built_voxels, voxel) == UNDECIDED:
                    score = get_voxel_score(voxel, context)
                    if score > best_score:
                        best_score = score
                        best_voxel = voxel

    # Check some random voxels farther away
    check_count = 15
    check_radius = 5
    while check_count > 0 or best_voxel == None:
        x = int((random.random() - 0.5) * check_radius * 2)
        y = int((random.random() - 0.5) * check_radius * 2)
        z = int((random.random() - 0.5) * check_radius * 2)

        voxel = add((x, y, z), cur_pos)
        # Make sure this voxel hasn't already been built
        if get(built_voxels, voxel) == UNDECIDED:
            score = get_voxel_score(voxel, context)
            if score > best_score:
                best_score = score
                best_voxel = voxel

        check_count -= 1
        check_radius += 0.5

    return best_voxel

# Decide the coordinates of the next voxel to pick
def pick_next_voxel(built_voxels, context):
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



# Generate one training example
def generate_examples(voxels, context_size):
    # Pick starter voxel at random
    keys = list(voxels.keys())
    # starter_voxel = (0, 0, 0)
    # starter_voxel = stot(keys[int(random.random()*len(keys))])
    starter_voxel = (int(random.random()*SIZE[0]), int(random.random()*SIZE[1]), int(random.random()*SIZE[2]-1))

    # Set up dict for voxels that have already been built
    built_voxels = {}
    built_voxels[ttos(starter_voxel)] = get(voxels, starter_voxel, True)

    # Build context list
    context = []
    context.append((starter_voxel, get(voxels, starter_voxel, True)))

    # Generate examples
    ret = []
    for i in range(context_size):
        # Determine the next voxel
        next_voxel = pick_next_voxel(built_voxels, context)

        # Add it to built voxels map
        index_at_position = get(voxels, next_voxel, True)
        built_voxels[ttos(next_voxel)] = index_at_position

        # Add it to context window
        context.append((next_voxel, index_at_position))
        # if len(context) > context_size+1:
        #     context.pop(0)

    ret.append(context)
    return ret

# Generate n training examples, sampled from all of the json files in the training data
def generate_training_examples(num_examples, context_size):
    # Get filenames of all voxel files in training corpus
    filenames = os.listdir('training/json')
    filenames = list(filter(lambda f : "sorpok" in f, filenames))

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
