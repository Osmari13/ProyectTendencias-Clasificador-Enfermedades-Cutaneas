import sys
import os
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model

import numpy as np
import cv2
import matplotlib.pyplot as plt

width_shape, heigth_shape = 224

names = ['ACNE', 'MELANOMA MALIGNO', 'NEVUS', 'PIE DE ATLETA',
         'PSORIASIS', 'ROSACEA', 'URTICARIA', 'VARICELA', 'VERRUGA', 'VITILIGO']

models = load_model('models/model.json')
print('Modelo Cargado')

imaget_path = 'dataset/test/Acne/images.jpg'
imaget = cv2.resize(cv2.imread(imaget_path), (width_shape,
                    heigth_shape), interpolation=cv2.INTER_AREA)

xt = np.asarray(imaget)
xt = preprocess_input(xt)
xt = np.expand_dims(xt, axis=0)

print("Predicción")
preds = models.predict(xt)

print("Predicción:", names[np.argmax(preds)])
plt.imshow(cv2.cvtColor(np.asarray(imaget), cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
