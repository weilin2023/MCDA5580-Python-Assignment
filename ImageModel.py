import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

# load data
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
num_classes = 10
input_shape = (28,28,1)

# manipulating the data
x_train = x_train.astype("float32")/255
x_test = x_test.astype("float32")/255

x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)
print(y_train.shape)

model = tf.keras.Sequential(
    [
     tf.keras.Input(shape=input_shape),
     layers.Conv2D(64, kernel_size=(3,3), activation='relu'),
     layers.MaxPooling2D(pool_size=(2,2)),
     layers.Conv2D(128, kernel_size=(3,3), activation='relu'),
     layers.MaxPooling2D(pool_size=(2,2)),
     layers.Flatten(),
     layers.Dense(num_classes, activation='softmax')
    ]
)

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, validation_split=0.2)
model.evaluate(x_test, y_test)

model.save('image_model.keras')
