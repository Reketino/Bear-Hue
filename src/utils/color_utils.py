import colorsys


def hue_to_hex( hue, sat, bri):
    h = hue / 65536
    s = sat / 254
    v = bri / 254
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255),int(g * 255),int(b * 255))


def xy_to_hex( x, y, bri):
    if not y:
        return "#888888"
    z = 1.0 - x - y
    Y = bri / 254
    X = (Y / y) * x
    Z = (Y / y) * z
    r = max(0, X * 1.656492 - Y * 0.354851 - Z * 0.255038)
    g = max(0, -X * 0.707196 + Y * 1.655397 + Z * 0.036152)
    b = max(0, X * 0.051713 - Y * 0.121364 + Z * 1.011530)
  
    return "#{:02x}{:02x}{:02x}".format(
        int (min(r * 255, 255)),
        int (min(g * 255, 255)),
        int (min(b * 255, 255)),
        )