import os
import cv2
import logging
import numpy as np
from PIL import Image
from mtcnn.mtcnn import MTCNN
from keras.models import model_from_json
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


""" This code snipped detects all the faces in every 30th frame of the input video, classifies whether
 the face wears a mask or not and finally stores the detected face in the folder 'Store_detected_faces/' """


def calssification_with_mask(image):
    global Model_Classify
    image = np.array(image)/255.0
    image = np.reshape(image,(1,200, 170,3))
    pred = Model_Classify.predict(image)
    if pred>0.5:
        return True
    return False

 
def extract_face(pixels, frame_ind, video_ind, required_size=(170, 200), fak=3):
    global detector
    results = detector.detect_faces(pixels)

    for i in range(len(results)):
        x1_f, y1_f, width, height = results[i]['box']
        x1 = max(x1_f - int(width / fak), 0)
        y1 = max(y1_f - int(height / fak), 0)
        x2, y2 = min(x1_f + int(width + width / fak), pixels.shape[1]), min(y1_f + int(height + height / fak), pixels.shape[0])
        face = pixels[y1:y2, x1:x2]
        
        image = Image.fromarray(face)                         
        image = image.resize(required_size)
        if calssification_with_mask(image):
            image.save('Store_detected_faces/With Mask/' + video_ind + '--' + frame_ind + "--Face_" + str(i) + ".jpg")
        else:
            image.save('Store_detected_faces/Without Mask/' + video_ind + '--' + frame_ind + "--Face_" + str(i) + ".jpg")


def load_model(path):
    json_file = open(path + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path + '.h5')
    return loaded_model


Model_Classify=load_model('model_final')
detector = MTCNN()
framerate=30

for fold_p in os.listdir('Input Video'):
    print('In Bearbeitung: ', fold_p)
    Video = cv2.VideoCapture('Input Video/'+fold_p)
    z = 0
    while True:
        ret,frame = Video.read() 
        if ret:
            if z % framerate==0:
                print('Frame ' + str(z))
                Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                extract_face(Frame, str(z), fold_p[0:len(fold_p) - 4])
                # cv2.imwrite('TestFRame.jpg', frame)
            z += 1
        else: 
            break
    Video.release() 
    cv2.destroyAllWindows()


print('Finished, all faces extracted from input video')



