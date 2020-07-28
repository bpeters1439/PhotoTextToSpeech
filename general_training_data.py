import numpy as np
from PIL import ImageDraw, Image, ImageFont, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
from config import ALPHABET
from bounding_box import bounding_box
from separate_chars import separate_chars

# create our data set
my_train_images = []
my_train_labels = []
my_test_images = []
my_test_labels = []

# TRAINING IMAGES BEGIN

print("creating training images")

fonts = ["cour.ttf"]
font_sizes = [44] # [44,46,48,50,52,54,56,58,60,62,64,66,68,70,72]

for font in fonts:
    print("processing: ", font)
    for font_size in font_sizes:
        print("processing: ", font_size)
        # this 3 character sentence list places is the shortest
        # which places each character everywhere it can be found
        for char1 in ALPHABET:
            for char2 in ALPHABET:
                for char3 in ALPHABET:
                    sentence = char1 + char2 + char3
                    print(sentence)
                    usr_font = ImageFont.truetype(font, font_size)
                    text_width, text_height = usr_font.getsize(sentence)
                    print(text_width, text_height)
                    image = Image.new("RGB", (text_width + 50, text_height + 50), (255, 255, 255))
                    dimage = ImageDraw.Draw(image)
                    dimage = dimage.text((25, 25), sentence, 0, font=usr_font)
                    filename = "training_images/" + font[0:-4] + "_" + str(font_size) + "_sentence_" + sentence + ".PNG"
                    image.save(filename)

                    # use same functions for bounding box and character seperation
                    # as will be used later for pre-processing images of characters
                    # for the neural net
                    bb_image = bounding_box(filename)
                    (character_images, space_indexes) = separate_chars(filename, bb_image)

                    if character_images.shape[0] != 3:
                        # resolution of one of the images was too small
                        # "insufficient detail" was processed instead for size of 19
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print("DETAIL ERROR: IMAGES DON'T MATCH CHARACTERS EXPECTED 3")
                        print("filename: ", filename)
                        print("sentance: ", sentence)
                        print("character images: ", character_images.shape[0])
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        exit(0)

                    character_index = 0
                    for image in character_images:
                        image_array = np.array(image)
                        my_train_images.append(image_array)
                        my_train_labels.append(ALPHABET.find(sentence[character_index]))
                        # print("index: ", character_index)
                        # print("alphabet index: ", ALPHABET.find(nospace_sentence[character_index]))
                        # print("sentence: ", sentence)
                        # print("sentence character index: ", nospace_sentence[character_index])
                        # print("int rep from find: ", ALPHABET.find(nospace_sentence[character_index]))
                        # plt.imshow(image, cmap=plt.get_cmap('gray'))
                        # plt.show()
                        filename = "training_images/" + \
                                   font[0:-4] + "_" + str(font_size) + \
                                   "_s" + sentence + \
                                   "_" + sentence[character_index] + \
                                   "_i" + str(ALPHABET.find(sentence[character_index])) + ".PNG"
                        temp_PIL_image = Image.fromarray(image, "L")
                        temp_PIL_image.save(filename)
                        character_index = character_index + 1

"""
font_index = 0
for font in fonts:
    usr_font = ImageFont.truetype(font, 16)
    for letter in ALPHABET:
        images = []
        text_width, text_height = usr_font.getsize(letter)
        w_adj = 16 - text_width
        h_adj = 24 - text_height
        image = Image.new("L", (text_width + w_adj, text_height + h_adj), 255)
        d_usr = ImageDraw.Draw(image)
        d_usr.text(((16 - text_width) // 2, (24 - text_height) // 2), letter, 0, font=usr_font)
        # save base image
        images.append(image)
        images.append(image.filter(ImageFilter.SHARPEN))
        images.append(image.filter(ImageFilter.SMOOTH))
        images.append(image.filter(ImageFilter.SMOOTH_MORE))
        images.append(image.filter(ImageFilter.DETAIL))
        images.append(image.filter(ImageFilter.GaussianBlur(radius=1)))

        e = ImageEnhance.Contrast(image)
        images.append(e.enhance(150))

        image_index = 0
        for image in images:
            for angle in range(0, 359, 5):
                temp_image = image.rotate(angle, fillcolor=255)
                # the following is needed because windows does not
                # distinguish between upper and lower case in file names
                if letter.isupper():
                    char_modifier = 'u'
                else:
                    char_modifier = 'l'
                filename = "training_images/train_" + \
                           letter + char_modifier + \
                           "_i" + str(image_index) + \
                           "_" + font[0:-4] + \
                           "_a" + str(angle) + ".PNG"
                print(filename)
                temp_image.save(filename)
                temp_image_array = np.array(temp_image)
                my_train_images.append(temp_image_array)
                my_train_labels.append(ALPHABET.find(letter))
            image_index = image_index + 1

    font_index = font_index + 1
    print(image.size)
    plt.show()
"""

# TRAINING IMAGES END

# TEST IMAGES BEGIN

sentances = []
# never use 19 characters bc that is the number in the error string insufficient detail
# sentances.append(u'the uick brown fox ums over the laz do')   # no below the line lower case
# sentances.append(u'the quick brown fox jumps over the lazy dog')
# sentances.append(u'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG')
# sentances.append(u'tHe QuIcK bRoWn FoX jUmPs OvEr ThE lAzY dOg')
# sentances.append(u'ThE qUiCk BrOwN fOx JuMpS oVeR tHe LaZy DoG')
sentances.append(u'1234567890')
sentances.append(u'1 2 3 4 5 6 7 8 9 0')
sentances.append(u'12 34 56 78 90')
sentances.append(u'123 456 789')

font_sizes = [36, 72] # 38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72]
# fonts = ["cour.ttf", "lucon.ttf"]

for font in fonts:
    print("processing: ", font)
    for font_size in font_sizes:
        print("processing: ", font_size)
        sentence_index = 0
        for sentence in sentances:
            print("processing: ", sentence)
            nospace_sentence = sentence.replace(' ', '')
            print("no space: ", nospace_sentence)
            num_chars = len(sentence)
            usr_font = ImageFont.truetype(font, font_size)
            text_width, text_height = usr_font.getsize(sentence)
            print(text_width, text_height)
            image = Image.new("RGB", (text_width + 50, text_height + 50), (255,255,255))
            dimage = ImageDraw.Draw(image)
            dimage = dimage.text((25, 25), sentence, 0, font=usr_font)
            filename = "test_images/" + font[0:-4] + "_" + str(font_size) + "_sentence_" + str(sentence_index) + ".PNG"
            image.save(filename)

            # use same functions for bounding box and character seperation
            # as will be used later for pre-processing images of characters
            # for the neural net
            bb_image = bounding_box(filename)
            (character_images, space_indexes) = separate_chars(filename, bb_image)

            # check characters printed equal images produced
            if (character_images.shape[0] != num_chars - len(space_indexes)):
                # resolution of one of the images was too small
                # "insufficient detail" was processed instead for size of 19
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("DETAIL ERROR: IMAGES DON'T MATCH CHARACTERS EXPECTED")
                print("filename: ", filename)
                print("sentance: ", sentence)
                print("character images: ", character_images.shape[0])
                print("characters in sentance: ", num_chars)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                exit(0)

            character_index = 0
            for image in character_images:
                image_array = np.array(image)
                my_test_images.append(image_array)
                my_test_labels.append(ALPHABET.find(nospace_sentence[character_index]))
                # print("index: ", character_index)
                # print("alphabet index: ", ALPHABET.find(nospace_sentence[character_index]))
                # print("sentence: ", sentence)
                # print("sentence character index: ", nospace_sentence[character_index])
                # print("int rep from find: ", ALPHABET.find(nospace_sentence[character_index]))
                # plt.imshow(image, cmap=plt.get_cmap('gray'))
                # plt.show()
                filename = "test_images/" + \
                           font[0:-4] + "_" + str(font_size) + \
                           "_s" + str(sentence_index) + \
                           "_" + sentence[character_index] +\
                           "_i" + str(ALPHABET.find(nospace_sentence[character_index])) + ".PNG"
                temp_PIL_image = Image.fromarray(image, "L")
                temp_PIL_image.save(filename)
                character_index = character_index + 1

            sentence_index = sentence_index + 1


print("end sentence processing")

# TEST IMAGES END

# convert to numpy arrays
train_images = np.array(my_train_images)
train_labels = np.array(my_train_labels)
test_images = np.array(my_test_images)
test_labels = np.array(my_test_labels)

print("saving training data")
print("training images: ", train_images.shape)
print("training data size :", train_images.size)
np.save("training_data/train_images.npy", train_images)
np.save("training_data/train_labels.npy", train_labels)
print("testing images: ", test_images.shape)
print("testing data size :", test_images.size)
np.save("training_data/test_images.npy", test_images)
np.save("training_data/test_labels.npy", test_labels)

print("completed")