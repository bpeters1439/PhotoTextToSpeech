from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from pathlib import Path
from letter_gap_analysis import gap_analysis


def separate_chars(filename, image):
    gray_scale_image = ImageOps.grayscale(image)
    gray_scale_image = gray_scale_image.filter(ImageFilter.SHARPEN)
    # gray_scale_image.show()

    # preprocess -> remove as much gray as possible before processing further
    # gray_scale_image = gray_scale_image.filter(ImageFilter.SHARPEN)
    # e = ImageEnhance.Contrast(gray_scale_image)
    # gray_scale_image = e.enhance(100)
    # gray_scale_image.show()

    gs_img_array = np.array(gray_scale_image)
    # take the sum of each column, the vertical sum
    # print(gs_img_array)
    # remove very light pixels which confuse character separation
    gs_img_array[gs_img_array >= 128] = 255
    gs_img_array[gs_img_array <= 96] = 0
    # remove this debug
    image_path = Path(filename)
    tempPILimage = Image.fromarray(gs_img_array)
    tempPILimage.save("log_images/" + "cropped_limit_" + image_path.name)

    vsum = gs_img_array.sum(0)

    # a white column of 24 pixels with a value of 255 has a sum of 6120
    # print(vsum)
    detected_content_columns = []
    MAX_SUM_VALUE = 6120 # - 170  # almost 24 lit pixels but not 1 completely dark one
    for index in range(0, len(vsum.tolist())-1):
        if vsum[index] < MAX_SUM_VALUE:
            detected_content_columns.append(index)

    detected_content_columns = gap_analysis(detected_content_columns)

    # print(detected_content_columns)
    dcc_len = len(detected_content_columns)
    # print(dcc_len)

    # create a draw image for the red line separators
    # needs to be original for red to show up
    local_image_copy = image.copy()
    draw_image = ImageDraw.ImageDraw(local_image_copy)

    image_path = Path(filename)
    character_images = []

    space_locations = []
    character_index = 0
    for index in range(dcc_len):
        value = detected_content_columns[index]
        if (value - 1) not in detected_content_columns:
            min_col = value
            draw_image.line([(min_col - 1,0), (min_col - 1,23)], fill="red", width=0)

        if (value + 1) not in detected_content_columns:
            max_col = value
            # box=(left, upper, right, lower)
            # include white column boundary on each side
            # print("r: ", min_col - 1, max_col + 1)
            letter_image = gray_scale_image.crop((min_col - 1, 0, max_col + 1, 23))
            letter_image = letter_image.resize((16, 24))
            # letter_image.show()
            letter_image.save("log_images/" + str(index) + "_" + image_path.name)
            draw_image.line([(max_col+1,0),(max_col+1,23)], fill="red", width=0)
            character_images.append(np.array(letter_image))
            character_index = character_index + 1

            # only do a space check if not at end of array
        if index != dcc_len - 1:
            next_value = detected_content_columns[index + 1]
            MIN_CHAR_WIDTH = 11
            if (next_value - value >= MIN_CHAR_WIDTH):
                # exclude pixels near other characters
                # print("n: ", value-1, next_value+1, character_index)
                #letter_image = gray_scale_image.crop((value + 1, 0, next_value, 23))
                #letter_image = letter_image.resize((16, 24))
                #letter_image.show()
                #letter_image.save("log_images/" + str(index) + "s_" + image_path.name)
                #character_images.append(np.array(letter_image))
                space_locations.append(character_index)
                character_index = character_index + 1

    #local_image_copy.show()
    local_image_copy.save("log_images/" + "chars_" + image_path.name)

    return (np.array(character_images), space_locations)

# image = Image.open("Insufficient_Detail.PNG")
# separate_chars("Insufficient_Detail.PNG", image)