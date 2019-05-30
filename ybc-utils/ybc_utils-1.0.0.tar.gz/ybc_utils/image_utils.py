import os
from PIL import Image

__DEFAULT_PIC_MAX_LENGTH = 500


def resize_if_too_large(filename):

    file = os.path.abspath(filename)
    im = Image.open(file)
    original_width, original_height = im.size
    max_len = max(original_width, original_height)

    if max_len <= __DEFAULT_PIC_MAX_LENGTH:
        return
    ratio = __DEFAULT_PIC_MAX_LENGTH / max_len
    new_size = (original_width * ratio, original_height * ratio)
    im.thumbnail(new_size)
    im.save(filename, 'PNG')


def main():
    resize_if_too_large('Hello world', 42)


if __name__ == '__main__':
    main()
