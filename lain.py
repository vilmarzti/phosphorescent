import numpy as np
import argparse

from os import listdir, path, mkdir, system
from shutil import rmtree
from PIL import Image, ImageEnhance
from math import exp

from multiprocessing import Pool
"""
create the inbetween frames for the phosphorescent pigment to shine

use following command to reconstruct the video
ffmpeg -r 60 -framerat 75 -i black_frames/out%04d.png -vcodec  libx264 -pix_fmt yuv420p out.mp4

"""


#original_dir = 'frames'
#output_dir = 'black_frames'
#black_frame = 'out_black.png'
#number_frames_between = 15


def format_name(pos):
    return "out%04d.png" % pos

def shifted_sigmoid(x, range):
    """ Sigmoid function and shifted for range
    """
    shifted_x = (x - 1 - range/3) 
    return 1/(1 + exp(-shifted_x))

def sigmoid(x):
    return 1/(1 + exp(-x))

def save_adjusted_frame(image_path, brightness, output_path):
    with Image.open(image_path) as im:
        enhancer = ImageEnhance.Brightness(im)
        new_image = enhancer.enhance(brightness)
        new_image.save(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Give n-th extracted frame and the number of frames in between")
    parser.add_argument("-f", "--add", help="The number of darkened frames added", default=15, type=int)
    parser.add_argument("-i", "--input", help="The folder with the extracted frames", default="frames", type=str)
    parser.add_argument("-o", "--output", help="The folder with the extracted frames", default="black_frames",type=str)

    args = parser.parse_args()

    original_dir = args.input
    output_dir = args.output
    frame_names = listdir(original_dir)
    number_frames_between = args.add

    frame_paths = map(
        lambda file_name: path.join(original_dir, file_name),
        frame_names
    )

    frame_paths = np.repeat(
        list(frame_paths),
        number_frames_between
    )

    brightness = [ 
        sigmoid(x  - number_frames_between / 3) 
        for x in range(number_frames_between)
    ]

    brightness = brightness * len(frame_paths)

    output_paths =  [
        path.join(
            output_dir,
            format_name(image_number)
        )
        for image_number in range(len(frame_paths) * number_frames_between)
    ]
    
    function_inputs = list(
        zip(
            frame_paths,
            brightness,
            output_paths
        )
    )


    with Pool() as pool:
        pool.starmap(
            save_adjusted_frame,
            function_inputs 
        )