import firebase_admin
import google
from firebase_admin import credentials, firestore

cred = credentials.Certificate('UfaceInterface/ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

COLLECTION_COURSES = "courses"
COLLECTION_FACIAL = "facialInfo"


def test():
    collection = "courses"
    document = "cz3002"
    course = {"id": "cz3002", "name": "ASE", "au": 3, "modules": []}
    module = {"index": "sp1", "students": []}
    for x in range(6):
        module["students"].append({"name": "student" + str(x), "id": str(x)})
    for x in range(3):
        module["index"] = "sp" + str(x)
        course["modules"].append(module.copy())

    write(collection, document, course)
    course = read(collection, document)

    collection = "facialInfo"
    facial_matrix = [[0, 0, 1, 1],
                     [1, 1, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0]]
    # facial_data_obj = {"data": []}
    # for x in range(len(facial_matrix)):
    #     facial_data_obj["data"].append({"value": facial_matrix[x]})
    # for y in range(6):
    #     write(collection, "studentId:" + str(y), facial_data_obj)
    # facial_data_obj = read(collection, "studentId:0")
    # facial_matrix = []
    # for x in range(len(facial_data_obj["data"])):
    #     facial_matrix.append(facial_data_obj["data"][x]["value"])
    # print(facial_matrix)

    for y in range(6):
        write_matrix(collection, "studentId:" + str(y), facial_matrix)
    facial_matrix = read_matrix(collection, "studentId:0")
    print(facial_matrix)


def write(collection, document, obj):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(obj)


def read(collection, document):
    doc_ref = db.collection(collection).document(document)
    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
        return doc.to_dict()
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')


def write_matrix(collection, document, matrix):
    matrix_obj = {"data": []}
    for x in range(len(matrix)):
        matrix_obj["data"].append({"value": matrix[x]})
    write(collection, document, matrix_obj)


def read_matrix(collection, document):
    matrix_obj = read(collection, document)
    matrix = []
    for x in range(len(matrix_obj["data"])):
        matrix.append(matrix_obj["data"][x]["value"])
    return matrix


# test()
