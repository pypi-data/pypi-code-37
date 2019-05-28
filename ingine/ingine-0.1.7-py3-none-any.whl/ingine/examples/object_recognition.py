import os
import numpy

from keras.datasets import fashion_mnist
from keras import utils
from ingine import ann

os.environ['KERAS_BACKEND'] = 'theano'

# Загружаем данные
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

# Преобразование размерности изображений
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
# Нормализация данных
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

# Преобразуем метки в категории
Y_train = utils.to_categorical(y_train, 10)
Y_test = utils.to_categorical(y_test, 10)

categorizer = ann.get_categorizer(X_train, y_train, 10, epochs = 2)

from PIL import Image, ImageDraw

test_image = X_test[0].reshape(28, 28)

image = Image.new("L", (280, 280), (255,))
draw = ImageDraw.Draw(image)
for i in range(28):  # For every pixel:
    for j in range(28):
        draw.rectangle((i * 10, j * 10, (i + 1) * 10, (j + 1) * 10), fill = (255 - int(test_image[j][i] * 255),))


image.show()

print(categorizer(X_test[0].reshape(1, 784)))