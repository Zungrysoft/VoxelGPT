import os
import json
import random
import math

AIR = 1
UNDECIDED = 0

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
    for c in context:
        total += 1/(dist(pos, c[0]) + 0.01)
    return total * (random.random() + 1)

# Decide the coordinates of the next voxel to pick
def pick_next_voxel(built_voxels, context):
    cur_pos = context[-1][0]
    best_score = 0
    best_voxel = cur_pos

    # Check all voxels within 2 spaces
    for x in range(-2, 3):
        for y in range(-2, 3):
            for z in range(-2, 3):
                voxel = (x, y, z)
                # Make sure this voxel hasn't already been built
                if get(built_voxels, voxel) == UNDECIDED:
                    score = get_voxel_score(voxel, context)
                    if score > best_score:
                        best_score = score
                        best_voxel = voxel

    # Check some random voxels farther away
    CHECK_COUNT = 15
    CHECK_RADIUS = 10
    for i in range(CHECK_COUNT):
        x = int((random.random() - 0.5) * CHECK_RADIUS * 2)
        y = int((random.random() - 0.5) * CHECK_RADIUS * 2)
        z = int((random.random() - 0.5) * CHECK_RADIUS * 2)

        voxel = (x, y, z)
        # Make sure this voxel hasn't already been built
        if get(built_voxels, voxel) == UNDECIDED:
            score = get_voxel_score(voxel, context)
            if score > best_score:
                best_score = score
                best_voxel = voxel

    return best_voxel

# Generate one training example
def generate_examples(voxels, context_size):
    # Pick starter voxel at random
    keys = list(voxels.keys())
    i = int(random.random()*len(keys))
    starter_voxel = keys[i]

    # Set up dict for voxels that have already been built
    built_voxels = {}
    built_voxels[starter_voxel] = get(voxels, starter_voxel, True)

    # Build context list
    context = []
    context.append((stot(starter_voxel), voxels[starter_voxel]))

    # Generate examples
    ret = []
    for i in range(context_size):
        # Determine the next voxel
        next_voxel = pick_next_voxel(built_voxels, context)

        # Add it to built voxels map
        nvs = ttos(next_voxel)
        built_voxels[nvs] = get(voxels, nvs, True)

        # Add it to context window
        context.append((next_voxel, voxels[starter_voxel]))
        # if len(context) > context_size+1:
        #     context.pop(0)

    ret.append(context)
    return ret

# Generate n training examples, sampled from all of the json files in the training data
def generate_training_examples(num_examples, context_size):
    # Get filenames of all voxel files in training corpus
    filenames = os.listdir('training/json')

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