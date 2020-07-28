import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
from bounding_box import bounding_box
from separate_chars import separate_chars
from neural import neural

warnings.filterwarnings('ignore')

# main entry point to the application both from GUI and console
# a single argument identifying the image with text is expected
# a tuple with an error/success string and content string is returned
# (<error string|success>, <string found in image>)


def nocr(filename):
    print("nocr:" + filename)
    # bounding box, find and log a box around the characters of interest
    bounded_image = bounding_box(filename)
    # separate characters, placing each in the log_images directory
    (individual_images, space_locations) = separate_chars(filename, bounded_image)
    # return predicted string
    nospace_string = neural(individual_images)
    print(nospace_string)
    final_string = ''
    offset = 0
    for index in range(0, len(nospace_string)):
        if (index + offset) in space_locations:
            final_string = final_string + ' '
            offset = offset + 1
        final_string = final_string + nospace_string[index]

    return final_string


# if this file is run directly, this script should use the console
if __name__ == "__main__":
    # two arguments are expected as the first is the name of the script, 0 index
    # the second is the name of the file to be processed
    if (len(sys.argv) == 2):
        nocr(sys.argv[1])
    else:
        print("\nInsufficient Arguments\n")
        print("\tUsage: python nocr.py <image filename>")