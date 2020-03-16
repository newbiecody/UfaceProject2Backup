import firebase_admin
import google
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

COLLECTION_COURSES = "courses"

# course = {"id": "", "name": "", "modules": []}
# module = {"index": "", "students": []}
# student = {"matric_num": "", "name": "", "facial_info": {}, "attendance_records": {}}
# facial_matrix_row = {"value": []}
# attendance_records = {"date_time": "isPresent"}


def set_document(collection, document, dic):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(dic)


def get_document(collection, document):
    doc_ref = db.collection(collection).document(document)
    try:
        doc = doc_ref.get()
        # print(u'Document data: {}'.format(doc.to_dict()))
        return doc.to_dict()
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
        return None


def del_document(collection, document):
    doc_ref = db.collection(collection).document(document)
    doc_ref.delete()


def create_course(course_id, course_name):
    course_obj = Course(course_id, course_name)
    set_document(COLLECTION_COURSES, course_id, course_obj.dict())


def set_course(course_id, course_dict):
    set_document(COLLECTION_COURSES, course_id, course_dict)


def del_course(course_id):
    del_document(COLLECTION_COURSES, course_id)


def get_course_dict(course_id):
    return get_document(COLLECTION_COURSES, course_id)


def create_module(course_id, module_index):
    course_dict = get_course_dict(course_id)
    if course_dict is not None:
        modules = course_dict["modules"]
        module_dict = Module(module_index).dict()
        for i in range(len(modules)):
            if modules[i]["index"] == module_index:
                course_dict["modules"][i] = module_dict
                set_course(course_id, course_dict)
                return
        course_dict["modules"].append(module_dict)
        set_course(course_id, course_dict)


def set_module(course_id, module_dict):
    course_dict = get_course_dict(course_id)
    if course_dict is not None:
        modules = course_dict["modules"]
        for i in range(len(modules)):
            if modules[i]["index"] == module_dict["index"]:
                course_dict["modules"][i] = module_dict
                set_course(course_id, course_dict)
                return
        course_dict["modules"].append(module_dict)
        set_course(course_id, course_dict)


def del_module(course_id, module_index):
    course_dict = get_course_dict(course_id)
    if course_dict is not None:
        modules = course_dict["modules"]
        for i in range(len(modules)):
            if modules[i]["index"] == module_index:
                del(course_dict["modules"][i])
                break
    set_course(course_id, course_dict)


def get_module_dict(course_id, module_index):
    course_dict = get_course_dict(course_id)
    if course_dict is not None:
        for i in range(len(course_dict["modules"])):
            if course_dict["modules"][i]["index"] == module_index:
                return course_dict["modules"][i]
    return None


def create_student(course_id, module_index, matric_num, name):
    module_dict = get_module_dict(course_id, module_index)
    if module_dict is not None:
        students = module_dict["students"]
        for i in range(len(students)):
            if students[i]["matric_num"] == matric_num:
                module_dict["students"][i] = Student(matric_num, name).dict()
                set_module(course_id, module_dict)
                return
        module_dict["students"].append(Student(matric_num, name).dict())
        set_module(course_id, module_dict)


def set_student(course_id, module_id, student_dict):
    module_dict = get_module_dict(course_id, module_id)
    if module_dict is not None:
        students = module_dict["students"]
        for i in range(len(students)):
            if students[i]["matric_num"] == student_dict["matric_num"]:
                module_dict["students"][i] = student_dict
                set_module(course_id, module_dict)
                return
        module_dict["students"].append(student_dict)
        set_module(course_id, module_dict)


def del_student(course_id, module_id, matric_num):
    module_dict = get_module_dict(course_id, module_id)
    if module_dict is not None:
        students = module_dict["students"]
        for i in range(len(students)):
            if students[i]["matric_num"] == matric_num:
                del (module_dict["students"][i])
                break
        set_module(course_id, module_dict)


def get_student_obj(course_id, module_index, matric_number):
    module_dict = get_module_dict(course_id, module_index)
    if module_dict is not None:
        for i in range(len(module_dict["students"])):
            if module_dict["students"][i]["matric_num"] == matric_number:
                return Student.init_from_fb_dict(module_dict["students"][i])
    return None


def get_all_student_obj(course_id, module_index):
    module_dict = get_module_dict(course_id, module_index)
    if module_dict is not None:
        students = []
        for i in range(len(module_dict["students"])):
            students.append(Student.init_from_fb_dict(module_dict["students"][i]))
        return students


# keep time format consistent
def set_attendance_record(course_id, module_index, matric_number, time, is_present):
    student_obj = get_student_obj(course_id, module_index, matric_number)
    student_obj.attendance_records[time] = is_present
    set_student(course_id, module_index, student_obj.dict())


def get_attendance_record(course_id, module_index, matric_number, time):
    student_obj = get_student_obj(course_id, module_index, matric_number)
    if student_obj.attendance_records[time] is None:
        return False
    else:
        return student_obj.attendance_records[time]


def get_all_facial_info(course_id, module_index):
    student_objs = get_all_student_obj(course_id, module_index)
    if student_objs is None:
        return
    facial_matrices = []
    for x in range(len(student_objs)):
        facial_matrices.append(student_objs[x].facial_info)
    return facial_matrices


def set_facial_info(course_id, module_index, matric_number, matrix):
    student_obj = get_student_obj(course_id, module_index, matric_number)
    student_obj.facial_info = matrix
    set_student(course_id, module_index, student_obj.dict())


class Course:
    def __init__(self, course_id, name):
        self.id = course_id
        self.name = name
        self.modules = []

    def add_module(self, module_obj):
        self.modules.append(module_obj)

    def dict(self):
        return {"id": self.id, "name": self.name, "modules": self.modules}


class Module:
    def __init__(self, index):
        self.index = index
        self.students = []

    def add_student(self, student_obj):
        self.students.append(student_obj)

    def dict(self):
        return {"index": self.index, "students": self.students}


class Student:
    # student = {"matric_num": "", "name": "", "facial_info": [], "attendance_records": {}}
    def __init__(self, matric_num, name):
        self.matric_num = matric_num
        self.name = name
        self.facial_info = []
        self.attendance_records = {}

    @classmethod
    def init_from_fb_dict(cls, student_dict):
        student = Student(student_dict["matric_num"], student_dict["name"])
        fb_facial_info = student_dict["facial_info"]
        for x in range(len(fb_facial_info)):
            student.facial_info.append(fb_facial_info[x]["value"])
        student.attendance_records = student_dict["attendance_records"]
        return student

    def dict(self):
        fb_facial_info = []
        for x in range(len(self.facial_info)):
            fb_facial_info.append({"value": self.facial_info[x]})
        return {"matric_num": self.matric_num, "name": self.name,
                "facial_info": fb_facial_info, "attendance_records": self.attendance_records}


def test():
    set_course("cz3002", {"empty": None})
    print(get_course_dict("cz3002") == {"empty": None})

    create_course("cz3002", "ASE")
    print(get_course_dict("cz3002") == {'id': 'cz3002', 'modules': [], 'name': 'ASE'})

    set_module("cz3002", {"index": "sp1"})
    print(get_module_dict("cz3002", "sp1") == {"index": "sp1"})

    create_module("cz3002", "sp1")
    print(get_module_dict("cz3002", "sp1") == {'students': [], 'index': 'sp1'})

    set_student("cz3002", "sp1", {"matric_num": "0", "name": None,
                                  "facial_info": [{"value": [0, 1]}], "attendance_records": {}})
    print(get_student_obj("cz3002", "sp1", "0").dict() ==
          {'matric_num': '0', 'name': None, 'facial_info': [{'value': [0, 1]}], 'attendance_records': {}})

    create_student("cz3002", "sp1", "0", "Jason")
    print(get_student_obj("cz3002", "sp1", "0").dict() ==
          {'matric_num': '0', 'name': 'Jason', 'facial_info': [], 'attendance_records': {}})

    set_attendance_record("cz3002", "sp1", "0", "20200313", True)
    print(get_attendance_record("cz3002", "sp1", "0", "20200313"))

    create_student("cz3002", "sp1", "1", "Jason2")
    print(get_all_student_obj("cz3002", "sp1")[0].name == "Jason"
          and get_all_student_obj("cz3002", "sp1")[1].name == "Jason2")

    set_facial_info("cz3002", "sp1", "0",
                    [[0, 0, 1, 1],
                     [1, 1, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0]])
    print(get_all_facial_info("cz3002", "sp1") == [[[0, 0, 1, 1], [1, 1, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]], []])

    # del_student("cz3002", "sp1", "0")
    # print(get_student_obj("cz3002", "sp1", "0") is None)
    #
    # del_module("cz3002", "sp1")
    # print(get_module_dict("cz3002", "sp1") is None)
    #
    # del_course("cz3002")
    # print(get_course_dict("cz3002") is None)


# test()
