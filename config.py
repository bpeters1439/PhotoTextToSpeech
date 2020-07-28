from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten

# this file contains initialization data used across this project

# create our label base

ALPHABET = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# ALPHABET = u'fFvVmMQwW'
ALPHABET_SIZE = len(ALPHABET)
# print("alphabet size: ", ALPHABET_SIZE)

# Build the model.
model = Sequential([
    #Dense(64, activation='relu', input_shape=(384,)),
    #Dense(64, activation='relu'),
    #Dense(ALPHABET_SIZE, activation='softmax'),
    Conv2D(32, (3, 3), activation='relu', input_shape=(24,16,1, )),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(ALPHABET_SIZE, activation='softmax')
])

# Compile the model.
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'],
)