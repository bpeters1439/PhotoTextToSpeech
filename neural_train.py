import numpy as np
from keras.utils import plot_model, to_categorical
import matplotlib.pyplot as plt
from config import ALPHABET, ALPHABET_SIZE, model
from PIL import Image

# the following code trains our neural network

# load training data
train_images = np.load("training_data/train_images.npy")
print ("loading training data: ", train_images.shape)
# show first image - debug
#i=Image.fromarray(train_images[0],"L")
#i.show()
train_labels = np.load("training_data/train_labels.npy")
print ("loading training labels: ", train_labels.shape)
test_images = np.load("training_data/test_images.npy")
print ("loading testing data: " , test_images.shape)
test_labels = np.load("training_data/test_labels.npy")
print ("loading testing labels: ", test_labels.shape)

# Normalize the images.
#train_images = (train_images / 255) - 0.5
#test_images = (test_images / 255) - 0.5

# Flatten the images.
#train_images = train_images.reshape((-1, 384))
#test_images = test_images.reshape((-1, 384))
train_images = train_images.reshape(train_images.shape[0], 24, 16, 1)
test_images = test_images.reshape(test_images.shape[0], 24, 16, 1)
train_images = train_images.astype('float32')
test_images = test_images.astype('float32')
train_images = train_images / 255
test_images = test_images / 255

# Train the model.
history = model.fit(
  train_images,
  to_categorical(train_labels),
  epochs=1,
  batch_size=4,
  verbose=1,
  workers=2,
  use_multiprocessing=True
)

# Evaluate the model.
score = model.evaluate(
  test_images,
  to_categorical(test_labels)
)

print("                        ", model.metrics_names)
print("model evaluation score: ", score)


# plot model shape to file
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)


# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
# plt.plot(history.history['mse'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
# plt.plot(history.history['mse'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Save the model to disk.
model.save_weights('neuralocr_model_weights.h5')

# Predict on the first 10 test images.
# predictions = model.predict(test_images[:10])
predictions = model.predict(train_images[:100])
# print(predictions)

# Print our model's predictions.
print(np.argmax(predictions, axis=1))

# decode our predictions
characters = [ALPHABET[value] for value in np.argmax(predictions, axis=1)]
print(characters)
content_string = ''
for char in characters:
    content_string = content_string + char
print(content_string)


# Check our predictions against the ground truths.
print(train_labels[:100])

# decode test labels
characters = [ALPHABET[value] for value in train_labels[:100] ]
print(characters)
content_string = ''
for char in characters:
    content_string = content_string + char
print(content_string)