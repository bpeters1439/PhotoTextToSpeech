# this script takes an image file and creates a bounding box around the text
# accuracy is important so that the neural net data and training remains focused and simple
# this is for black text on white backgrounds for monospaced fonts in a noiseless setting
# to make it independent of color, edge detection could be used instead, but this is less accurate
# noise can be addressed with de-speckling the image, and converting to black and white
# a histogram is created of all the rows
# all non-white content has lower values and will be perceived as dips in the histogram
# this method was chosen because it is more exact than finding objects with neural nets or edge detection
# slant can be adjusted for by comparing the ends of the bounding box to the content on each side
# multiple lines can be handled by iterating over the dips
# here we provide the single line of text in the image solution

from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from pathlib import Path

def bounding_box(image_name):
    # open image file and print its shape
    original_image = Image.open(image_name)
    # print("original size: ", original_image.size)
    # original_image.show()

    # convert original image to black and white
    bw_original_image = original_image.convert("1", dither=None)
    # bw_original_image.show()

    bw_img_array = np.array(bw_original_image)  # convert into a np array for easy processing
    # print("shape of image:", bw_img_array.shape)  # pixels vertically and horizontally
    average = np.average(bw_img_array.tolist(), )
    # print("average density: ", average)

    vsum = bw_img_array.sum(0)  # sum vertically
    hsum = bw_img_array.sum(1)  # sum horizontally
    vavg = np.average(vsum.tolist(), )
    havg = np.average(hsum.tolist(), )
    # print("vertical sum average", vavg)
    # print("horizontal sum average", havg)

    # rows and columns of interest contain at least 1 black pixel after image is converted to black and white
    # so should have a value of at least one less than the number of pixels in the image size horizontally or vertically
    cols_of_interest = [index for index in range(0, len(vsum.tolist())) if vsum[index] <= original_image.size[1] - 1]  # vavg]  # white has the highest value of 255
    rows_of_interest = [index for index in range(0, len(hsum.tolist())) if hsum[index] <= original_image.size[0] - 1]  # havg]
    # print("bounding rectangle")
    # print("rows of interest   :", rows_of_interest[0], rows_of_interest[-1])
    # print("columns_of_interest:", cols_of_interest[0], cols_of_interest[-1])

    # place bounding box around text with a 2 pixel border so letters don't touch edges
    # this does a little pre-processing to better match training data which should never touch boundaries
    upperleft = (cols_of_interest[0] - 2, rows_of_interest[0] - 2)
    lowerright = (cols_of_interest[-1] + 2, rows_of_interest[-1] + 2)

    # create an image to draw in, copy data in original image
    # this is necessary because we can't use red to show selection
    # in a black and white image
    # save image in the log directory with slightly modified name
    draw_image = ImageDraw.ImageDraw(original_image)
    draw_image.rectangle([upperleft, lowerright], outline="red")
    # original_image.show()
    image_path = Path(image_name)
    original_image.save("log_images/" + "bb_" + image_path.name)

    # reload original image to remove the red bounding box that was drawn
    original_image = Image.open(image_name)
    # crop to region of interest
    cropped_image = original_image.crop(
        box=(cols_of_interest[0] - 3, rows_of_interest[0] - 3, cols_of_interest[-1] + 3, rows_of_interest[-1] + 3))

    # print("cropped image shape", np.array(cropped_image).shape)

    # get rid of light pixels
    cropped_image_array = np.array(cropped_image)
    cropped_image_array[cropped_image_array >= 112] = 255
    cropped_image = Image.fromarray(cropped_image_array)

    # resize image for 24H and 16W
    # do a ratio of the height we have to the height we want to resize the image to
    height = cropped_image_array.shape[0]
    width = cropped_image_array.shape[1]
    ratio = 24.0 / height
    print("pre crop height: ", height)
    print("pre crop width: ", width)
    print("crop ratio: ", ratio)

    # if the height of the bounding box found is not greater or equal to 24 pixels (the height of the neural net input)
    # we would need to enlarge the image and introduce non-existing detail from the limited pixels
    # abort if the information is too little to analyze
    if height < 24:
        print("*****************************************")
        print("Insufficient Detail for Letter Separation")
        print("*****************************************")
        # returning a known good image prevents lots of edge case errors
        error_image = Image.open("Insufficient_Detail.PNG")
        error_image.save("log_images/" + "cropped_" + image_path.name)
        return error_image

    cropped_resized_image = cropped_image.resize((int(width * ratio), 24))
    # print("result image shape", np.array(cropped_image).shape)

    # resize image for 24H and 16W
    # do a ratio of the height we have to the height we want to resize the image to
    height = np.array(cropped_resized_image).shape[0]
    width = np.array(cropped_resized_image).shape[1]
    print("post crop height: ", height)
    print("post crop width: ", width)
    cropped_resized_image.save("log_images/" + "cropped_" + image_path.name)

    return cropped_resized_image
