from PIL import Image

gscale = "⠄⠆⠖⠶⡶⣩⣪⣫⣾⣿"


def rescale(image, height=18):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_width)/float(old_height)
    width = int(aspect_ratio * height * 2)
    dim = (width, height)
    image = image.convert('L').resize(dim)

    initial_pixels = list(image.getdata())
    new_pixels = [gscale[min(int((pixel_value / 255) * len(gscale)), len(gscale) - 1)] for pixel_value in initial_pixels]
    pixels = ''.join(new_pixels)
    new_image = [pixels[index:index + width] for index in range(0, len(pixels), width)]
    return '\n'.join(new_image)


def runner(path):
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in", path)
        return
    image = rescale(image)

    return image
