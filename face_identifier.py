import cv2
import numpy as np
import face_recognition
import os

path="imgs"
images=[]
classnames=[]
imgs=os.listdir(path)
for cl in imgs:
    img=cv2.imread(f"{path}/{cl}")
    images.append(img)
    classnames.append(cl.split('_')[0])

def get_encodings(images):
    list=[]
    for i in images:
        faceenc=face_recognition.face_encodings(i)[0]
        list.append(faceenc)
    return list

encoding_list=get_encodings(images)

Password=input("Enter the security code (Password=oscorp): ").lower()

if Password=="oscorp":
    print("Keep your Face ready.......")
    cap = cv2.VideoCapture(0)
    camOn=True
    while camOn:
        success,img=cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        faces=face_recognition.face_locations(imgS)
        encode=face_recognition.face_encodings(imgS,faces)

        for encodeface,faceloc in zip(encode,faces):
            matches=face_recognition.compare_faces(encoding_list,encodeface)
            facedis = face_recognition.face_distance(encoding_list, encodeface)

            matchIndex=np.argmin(facedis)
            if matches[matchIndex]:
                name=classnames[matchIndex].upper()
                print(f"Hello {name}")
                camOn=False
            else:
                print("Sorry does not match")

            # Display the resulting frame
            cv2.imshow('video', imgS)
            if cv2.waitKey(1) == ord('q'):
                break

        # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Oops wrong Password")

