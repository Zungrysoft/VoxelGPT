def rgb_to_hsv(rgb):
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255

    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val

    if max_val == min_val:
        h = 0
    elif max_val == r:
        h = (60 * ((g-b)/diff) + 360) % 360
    elif max_val == g:
        h = (60 * ((b-r)/diff) + 120) % 360
    elif max_val == b:
        h = (60 * ((r-g)/diff) + 240) % 360

    if max_val == 0:
        s = 0
    else:
        s = diff / max_val

    v = max_val

    return (h/360, s, v)

def rgb_to_hsl(rgb):
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255

    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val

    l = (max_val + min_val) / 2

    if max_val == min_val:
        h = 0
        s = 0
    else:
        if l < 0.5:
            s = diff / (max_val + min_val)
        else:
            s = diff / (2 - max_val - min_val)

        if max_val == r:
            h = (g - b) / diff
            if g < b:
                h += 6
        elif max_val == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4

        h /= 6

    return (h, s, l)

def rgb_rescale(rgb):
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255
    return (r, g, b)

def expand_palette(palette):
    ret = []
    for rgb in palette:
        ret.append({
            "rgb": rgb_rescale(rgb),
            "hsv": rgb_to_hsv(rgb),
            "hsl": rgb_to_hsl(rgb),
        })
    return ret