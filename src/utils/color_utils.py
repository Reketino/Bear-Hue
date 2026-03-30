import colorsys


def hue_to_hex( hue, sat, bri):
    h = hue / 65536
    s = sat / 254
    v = bri / 254
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255),int(g * 255),int(b * 255))