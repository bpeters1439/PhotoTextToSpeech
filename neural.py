import numpy as np
from config import ALPHABET, ALPHABET_SIZE, model

# takes an array of images and runs the predictor on each one, returning a string

def neural(images):

    model.load_weights('neuralocr_model_weights.h5')  # from prior training

    input_images = images.reshape((images.shape[0], 24, 16, 1))
    predictions = np.argmax(model.predict(input_images[:]), axis=1)

    # decode our predictions
    characters = [ALPHABET[value] for value in predictions]
    print(characters)
    content_string = ''
    for char in characters:
        content_string = content_string + char

    return content_string