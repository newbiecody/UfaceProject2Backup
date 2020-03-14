import numpy as np
import cv2 as cv2
import face_recognition
import os
from django.http import StreamingHttpResponse
from . import FirebaseManager as fb

#Create arrays of known face encodings and their respective names
#Only for Take attendance.
known_face_encodings = []
known_face_names = []

#web cam name
window_name = 'Face Detection Ongoing...'
def registerFace():
    cap = cv2.VideoCapture(0)   
    while True:
        ret,frame = cap.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_face = small_frame[:,:,::-1]
        face_locations = face_recognition.face_locations(rgb_small_face)
            
        #draw bounding box around the face
        for (top,right,bottom,left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame,(left,top),(right,bottom),(0,255,255),2)
        cv2.namedWindow(window_name,flags = cv2.WINDOW_NORMAL)    # removed window to view opencv
        cv2.imshow(window_name,frame)

        key = cv2.waitKey(1)
        #press t to capture an image of face
        if key & 0xFF == ord('t'):
            #get face encoding (facial information) and student name
            face_encoding = face_recognition.face_encodings(rgb_small_face,face_locations)[0]
            face_name = str(input('Please enter your name:\n'))
            #save student name with face encoding in firebase
            fb.write_matrix("facialInfo",face_name,face_encoding)
                

            known_face_names.append(face_name)
            known_face_encodings.append(face_encoding)

            print("Face information of {} has been recorded into database!".format(face_name))
            cap.release()
            return 1
        elif key & 0xFF == ord('q'):
            cap.release()
            return 0
        
    #cap.release()
    


def takeAttendance():

    #Fetch the name list and face encoding list from firebase
    #Store them in known_face_names and known_face_encodings respectively.
        
    #to be added later

    process_this_frame = True
    cap = cv2.VideoCapture(0)   
    while True:
        ret,frame = cap.read()
        small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations,num_jitters=1)

            face_names = []
            for face_encoding in face_encodings:
                name = 'Unknown'
                matches = face_recognition.compare_faces(known_face_encodings,face_encoding)

                #find the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                    name =  known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top,right,bottom,left),name in zip(face_locations,face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame,(left,top),(right,bottom),(0,255,255),2)
            cv2.rectangle(frame,(left,bottom-35),(right,bottom),(128,0,128),2)
            font=cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame,name,(left+6,bottom-6),font,1,(255,255,255),1)
     
            #cv2.namedWindow(window_name,flags =cv2.WINDOW_NORMAL)
            #cv2.imshow(window_name,frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    #    cv2.destroyAllWindows()
