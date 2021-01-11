def hex_to_rgb(hex):
    """Convert HEX to RGB

    Args:
        hex (char): like "#ffffff"

    Returns:
        tuple: like (255,255,255)
    """
    hex = hex.lstrip('#')
    lv = len(hex)
    return tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    """Convert RGB to HEX

    Args:
        rgb (tuple): like (255, 255, 255)

    Returns:
        char: like #ffffff
    """
    return '#%02x%02x%02x' % rgb
