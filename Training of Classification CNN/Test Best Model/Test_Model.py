import cv2
import numpy as np
from keras.models import model_from_json


def load_model(path):
    json_file = open(path+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path+'.h5')
    return loaded_model


L=['with_mask_2.jpg', 'with_mask_5.jpg', 'with_mask_30.jpg', 'without_mask_11.jpg', 'without_mask_13.jpg', 'without_mask_25.jpg']
Model_Classify=load_model('model__FINAL__RGB')

for path in L:
    img = cv2.imread('some_test_pictures/' + path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(170, 200))
    img = np.array(img)/255.0
    img=np.reshape(img,(1,200, 170,3))
    print('Prediction: ', Model_Classify.predict(img))

# Result: All Classifications are correct
print('FERTIG')
