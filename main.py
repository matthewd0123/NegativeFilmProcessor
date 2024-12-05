import os

from PIL import Image

input_dir_str = "./input/"
output_dir_str = "./output/"

input_dir = os.fsencode(input_dir_str)


def open_image(filename):
    with Image.open(input_dir_str + filename) as input_photo:
        R, G, B = 0, 1, 2
        source = input_photo.split()
        red_out = source[R].point(lambda i: abs(i - 255))
        source[R].paste(red_out)
        green_out = source[G].point(lambda i: abs(i - 255))
        source[G].paste(green_out)
        blue_out = source[B].point(lambda i: abs(i - 255))
        source[B].paste(blue_out)
        output_photo = Image.merge(input_photo.mode, source)
        output_photo.save(output_dir_str + filename)


for file in os.listdir(input_dir):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        print(filename)
        open_image(filename)
