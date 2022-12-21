import os
import shutil
import logging
import sqlite3
import matplotlib.pyplot as plt
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


""" This code snipped looks for each detedted face from the folder 'Store_detected_face/Without_Mask' whether the person with
 this face already exists in the database. That means is calculates via a neuronal network a embedding of the face and compares
 it with all the embeddings from the profile_pictures from the database. When the embeddings are closer than a specific threshold,
 the faces velong to the same person. All faces of one person are maped and stored in a folder in the directory
 'Compare_detected_faces_with_database/Face Verification'. Persons which are new to the database get a new entry in the database
  and are labeled with the folder name 'ID_Fremd_NEU' """


def extract_face(filename, required_size=(224, 224)):
    global detector
    pixels = plt.imread(filename)
    results = detector.detect_faces(pixels)
    if len(results)!=0:
        x1, y1, width, height = results[0]['box']
        x2, y2 = x1 + width, y1 + height
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
    else:  # no face found
        return [0, 0]
    return [face_array, 'Found']

 
def get_embeddings(path):
    global model
    extraction = extract_face(path)
    if extraction[1]=='Found':
        face = [extraction[0]]
        samples = asarray(face, 'float32')
        samples = preprocess_input(samples, version=2)
        embedding = model.predict(samples)
    else:
        print('NO EMBEDDING FOUND, no face detected')
        return [0,0]
    return [embedding, 'Found']


def eveluate(path_1, embedding_2):
    embedding_1=get_embeddings(path_1)
    if embedding_1[1]=='Found':
        score = round(cosine(embedding_1[0], embedding_2), 2)
        if score > 0.45:
            return [False, 0]
        return [True, 0]
    else:
        return [True, 'Not Found']


def get_embeddings_database(record):
    l_data_embeddings = []
    for row in record:
        pic_path = 'Compare_detected_faces_with_database/Database/Temp.jpg'
        with open(pic_path, 'wb') as file:
            file.write(row[3])
        l_data_embeddings += [[row[0], row[1], row[2], get_embeddings(pic_path)[0], row[4]]]
    if len(record)!=0:
        os.remove('Compare_detected_faces_with_database/Database/Temp.jpg')
    return l_data_embeddings


def update_embeddings(l_data_embeddings, data_tuple):
    pic_path = 'Compare_detected_faces_with_database/Database/Temp.jpg'
    with open(pic_path, 'wb') as file:
        file.write(data_tuple[3])
    l_data_embeddings += [[data_tuple[0], data_tuple[1], data_tuple[2], get_embeddings(pic_path)[0], data_tuple[4]]]
    os.remove('Compare_detected_faces_with_database/Database/Temp.jpg')
    return l_data_embeddings
    



detector = MTCNN()
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
connection = sqlite3.connect("Compare_detected_faces_with_database/Database/Profil_Datenbank.db")
cursor = connection.cursor()
cursor.execute("""SELECT * from Profile""")
record = cursor.fetchall()
L_Database_Embeddings = get_embeddings_database(record)

for path_pic in os.listdir('Store_detected_faces/Without Mask'):
    print('path_pic: ', path_pic)
    Already_Exist=False
    for row in L_Database_Embeddings:
        # print("Person_ID:", row[0], " Vorname:", row[1], " Nachname:", row[2], " Anzahl_Verstöße:", row[4])
        Eveluation = eveluate('Store_detected_faces/Without Mask/' + path_pic, row[3])
        if Eveluation[0] and Eveluation[1]==0:
            # Found an already exiting person in the database by comparison with the profile picture
            try:
                os.mkdir('Compare_detected_faces_with_database/Face Verification/'+str(row[0])+'_'+row[1]+'_'+row[2])
            except:
                pass
            shutil.copy('Store_detected_faces/Without Mask/'+path_pic, 'Compare_detected_faces_with_database/Face Verification/'+
                        str(row[0])+'_'+row[1]+'_'+row[2])
            cursor.execute(""" UPDATE Profile SET Anzahl_Verstöße=? WHERE Person_ID=? """, (row[4]+1, row[0]))
            row[4] += 1
            print('Found Match (with person from database) with ID: ', row[0])
            Already_Exist=True
            break
        elif Eveluation[0] and Eveluation[1]=='Not Found':
            print('Person not in database')
            Already_Exist=True
            break

    if not Already_Exist:
        # New personen is created/inserted to database
        with open('Store_detected_faces/Without Mask/'+path_pic, 'rb') as file:
            blobData = file.read()
        cursor.execute("""SELECT * from Profile""")
        record_new = cursor.fetchall()
        New_ID = record_new[len(record_new)-1][0]+1
        data_tuple = (New_ID, 'Fremd', 'NEU', blobData, 1)
        query = """ INSERT INTO Profile (Person_ID, Vorname, Nachname, Profilbild, Anzahl_Verstöße) VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(query, data_tuple)
        try:
            os.mkdir('Compare_detected_faces_with_database/Face Verification/'+str(New_ID)+'_Fremd_NEU')
        except:
            pass
        shutil.copy('Store_detected_faces/Without Mask/'+path_pic, 'Compare_detected_faces_with_database/Face Verification/'+str(New_ID)+
                    '_Fremd_NEU')
        print('No Match, New Person Created in folder Face Verification')
        L_Database_Embeddings = update_embeddings(L_Database_Embeddings, data_tuple)  # Remeber new person
            

connection.commit()  # save changes
connection.close()
