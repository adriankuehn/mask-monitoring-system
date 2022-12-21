# Mask Monitoring System
Development of a CNN deep learning monitoring system for automatic face detection, classification and identification (comparison to ID-photos) of non-mask wearers in videos

## How does the monitoring system work?

### 1. Pre Setup: 
You can create a new database with the file 'Create and Visualize database.py' based on the profile pictures (ID-photos) in the folder 'profile_pictures/'.

### Face Detection and Classification: 
The file 'Face_Detection and Classification' loads the video from 'Input Video/' and detects in constant intervals all faces from the persons in the video. This detection is based on a MTCNN neuronal network which returns the coordinates of the 'inner' face. For visual purposes we are transforming those coordinates in a way so that we can see and store the entire head. After that we classify all the detected faces in two groups 'mask wearers' and 'non-mask wearers'. This classification is based on a self trained convolutional neuronal network. The development and training of the network can be found in the folder 'Training of Classification CNN/'. The training utilizes a for our purposes modified Kaggle dataset of several thousand face images (see implementation) and achieves a final validation accuracy of 99.6%.

### 2. Face Verificaiton: 
These stored images (1. Step) from the directory 'Without Mask/' are now compared with the ID-photos from the SQLite3 database 'Compare_detected_faces_with_database/Database/Profil_Database.db' by the program 'Face_Verification.py'. This database contains the previously defined people with the values (ID, first name, last name, profile picture (ID-photo), number of mask violations). The comparison is carried out by embedding the detected faces which is a representation at the end of the CNN layers before the cnn classifier starts. It is generated using an imported Resnet50 based on the VGGFace2 data sets. Based on the high-dimensional embeddings of the two images, the cosine distance is calculated (value between 0 and 1). If the value is below 0.45 (threshold, self-optimized), the two images belong to the same person. Depending on the verification results, a folder  for each person is created in the directory “Compare_detected_faces_with_database/Face Verification/”. Each person's folder contains all of the detected facial non-mask wearing images of this specific person. Unknown 'NEW' people are automatically added to the database as strangers (folder name: 'ID_Fremd_NEU/') and will therefore be recognized in the future. Depending on the number of occurrences of mask violations, a counter for each person is calculated. In the end, with the script 'Create and Visualize database.py' you can also plot see the final state of the database after the above steps were completed.


### 3. Conclusion
To challenge the system I gave the monitoring-system a video form the German news TV as input and also added a few pictures from Dwayne Johnson and Leonardo DiCaprio to the detected faces from the video (I also added them to the database before the verification step starts). The face detection and verification works extremely well. All detected facial images can be assigned to the persons in the database without any problems. New persons are detected without any troubles and also the faces of Dwayne and Leonardo are recognized as already existent in the database and mapped in the folders from 'Face Verification/' accordingly. I tried the system with many different videos, persons and database initializations. It always worked reliably.


## Instructions for local deployment:
* Other version combinations may also work but its complicated, so thats the constalation I used...
* install python version 3.6 (Don't forget to add Python to PATH Variables during the installation instructions, otherwise it will be hard to access pip)
* pip install tensorflow==2.4.1
* pip install keras==2.4.1
* pip install keras_vggface
* pip install keras_applications
* pip install mtcnn
* pip uninstall pyparsing
* pip install pyparsing==2.4.7

Finally when you enter "pip list" you should get the following packages and versions:
* google-pasta            0.2.0
* grpcio                  1.32.0
* h5py                    2.10.0
* idna                    3.4
* importlib-metadata      4.8.3
* Keras                   2.4.1
* Keras-Applications      1.0.8
* Keras-Preprocessing     1.1.2
* keras-vggface           0.6
* kiwisolver              1.3.1
* Markdown                3.3.7
* matplotlib              3.0.0
* mtcnn                   0.1.1
* numpy                   1.19.5
* oauthlib                3.2.2
* opencv-python           4.6.0.66
* opt-einsum              3.3.0
* Pillow                  8.4.0
* pip                     21.3.1
* protobuf                3.19.6
* pyasn1                  0.4.8
* pyasn1-modules          0.2.8
* pyparsing               2.4.7
* python-dateutil         2.8.2
* pytz                    2022.7
* PyYAML                  6.0
* requests                2.27.1
* requests-oauthlib       1.3.1
* rsa                     4.9
* scipy                   1.5.4
* setuptools              59.6.0
* six                     1.15.0
* tensorboard             2.10.1
* tensorboard-data-server 0.6.1
* tensorboard-plugin-wit  1.8.1
* tensorflow              2.4.1
* tensorflow-estimator    2.4.0
* termcolor               1.1.0
* typing-extensions       3.7.4.3
* urllib3                 1.26.13
* Werkzeug                2.0.3
* wheel                   0.37.1
* wrapt                   1.12.1
* zipp                    3.6.0
