from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse, JsonResponse
from django.conf import settings
import numpy as np
import cv2
import face_recognition
import os
#import subprocess
from . import uface
from . import FirebaseManager as fb
import base64
from io import BytesIO
from PIL import Image


def index(request):
    return render(request,'Uface2/login.html')

def logout(request):
    return render(request, 'Uface2/logout.html')

def SelectModule(request):
    data=fb.get_all_course_dict()
    courses=[]
    indexes=[]
    
    for subdata in data:
        for x in subdata.get("modules",""):
            indexes.append(x.get("index",""))
    for subdata in data:
        courses.append(subdata.get("id",""))

    print(courses)
    print(indexes)

    zip_courses_indexes = zip(courses,indexes)
    context = {'zip_courses_indexes':zip_courses_indexes}

    return render(request, 'pages/SelectModule.html', context)

def ViewNameList(request):
    data = fb.get_course_dict("cz3002").get("modules","")
    index_module_data = []

#    for item in data:
#        index_module_data.append(item.get("index","")
    for item in data:
        if item["students"] != None:
            index_module_data.append(item.get("index", ""))

    counter = 1
    index_list=[]
    name_list=[]
    matric_list=[]
    email_list=[]

    for item in data:
        if item["students"] != None and (item.get("index","")!="sp2"):
            for x in item["students"]:
                index_list.append(counter)
                name_list.append(x.get("name",""))
                matric_list.append(x["matric_num"])
                email_list.append(x["email"])
                counter+=1

    zipped_list=zip(index_list,name_list,matric_list,email_list)

    context_dict= {'zipped_list':zipped_list}



    return render(request, 'pages/ViewNamelist.html', context_dict)

def ViewReport(request):
    return render(request, 'pages/ViewReport.html')

#def RegisterFace(request):         latest previous original 17/3/2020
#    if(uface.registerFace()):
#        return render(request, 'pages/RegisterFace.html')
#    else:
#        return render(request, 'pages/error.html')

def TakeAttendance(request):
#    uface.registerFace()
    return render(request, 'pages/TakeAttendance.html')


#testing opencv

#def ViewNameList(request):
#    if request.method =='POST':
#        form = 
#    return HttpResponseRedirect("pages/ViewNamelist.html")


#JH webcam

#face recognition with face_recognition API
def checkFace(request):
    # #json to be sent back to front end
    # #including name, check-in time, face bbox of any student matched in the database 
    backJsonInfo = []

    course_code = "course_code_test"
    course_index = "course_index_test"
    checkInTime = "202003010830"
    if request.method == "POST" and request.is_ajax():
        #get the base64 image sent from the request
        faceImage = request.POST.get('webcam')
        index = faceImage.find('base64,')
        base64Str = faceImage[index+6:]
        byte_data = base64.b64decode(base64Str)
        img_data = BytesIO(byte_data)
        img = np.asarray(Image.open(img_data).convert('RGB'))
        file = open(os.path.join(settings.BASE_DIR,'static/face.png'),'wb')
        file.write(byte_data)
        file.close()
        #resize the frame for faster face detection

        #load known faces from database
        known_student_objects = fb.get_all_student_obj(course_code,course_index)
        known_face_encodings = fb.get_all_facial_info(course_code,course_index)

        #detect faces in the request image
        #may contain more than one face
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img,face_locations,num_jitters=1)

        #list of names for all faces detected 
        face_names = []
        #check all the faces detected in the image with known faces from database
        for i in range(len(face_encodings)):
            face_encoding = face_encodings[i]
            #default name is unknown for each face
            name = 'Unknown'
            signed = False
            matric = ''
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding)

            #calculate distances between the detected face and each known face.
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            #find the index of the best matched face which has the smallest distance      
            best_match_index = np.argmin(face_distances)
            #set the face distance threshold to be 0.4
            if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                #name of matched face
                name =  known_student_objects[best_match_index].dict()["name"]
                matric = known_student_objects[best_match_index].dict()["matric_num"]
                # check if the student has already signed in
                signed = fb.get_attendance_record(course_code,course_index,matric,checkInTime)
                #update the attendance record in the database if the student hasn't signed in 
                if not signed:
                    fb.set_attendance_record(course_code,course_index,matric,checkInTime,True)


            #get bbox coordinates of the face
            top,right,bottom,left = face_locations[i]
            backJsonInfo.append([name,matric,top,right,bottom,left,signed])
    
    return JsonResponse(backJsonInfo,safe=False)


def RegisterFace(request):
    course_code = "course_code_test"
    course_index = "course_index_test"

    backInfo={"list":[]}
    all_student_objects = fb.get_all_student_obj(course_code,course_index)
    for student in all_student_objects:
        name = student.dict()["name"]
        matric = student.dict()["matric_num"]
        registered= "No"
        if bool(student.dict()["facial_info"]):
            registered = "Yes"
        student_info = [matric,name,registered]
        backInfo["list"].append(student_info)

    return render(request,'pages/RegisterFace.html',backInfo)

def faceRegistration(request):
    course_code = "course_code_test"
    course_index = "course_index_test"
    #get student matric number and face image from request
    if request.method == "POST" and request.is_ajax():
        #get the base64 image sent from the request
        faceImage = request.POST.get('webcam')
        matric = request.POST.get('matric')
        #get image from ajax
        index = faceImage.find('base64,')
        base64Str = faceImage[index+6:]
        byte_data = base64.b64decode(base64Str)
        img_data = BytesIO(byte_data)
        img = np.asarray(Image.open(img_data).convert('RGB'))
        #detect faces in the image   
        face_locations = face_recognition.face_locations(img)
        #multiple faces are not allowed
        if len(face_locations) > 1:
            return JsonResponse({"sucess":0})
        #when no face is detected 
        if len(face_locations) < 1:
            return JsonResponse({"success":1})
        #get the face encoding of the face in the image
        face_encodings = face_recognition.face_encodings(img,face_locations)
        #save the student's facial information in firebase
        fb.set_facial_info(course_code,course_index,matric,face_encodings[0]) 
        return JsonResponse({"success":2})

