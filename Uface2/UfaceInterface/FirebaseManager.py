import firebase_admin
import google
from firebase_admin import credentials, firestore

cred = credentials.Certificate('UfaceInterface/ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

COLLECTION_COURSES = "courses"

# course = {"id": "", "name": "", "modules": []}
# module = {"index": "", "students": []}
# student = {"matric_num": "", "name": "", "facial_info": {}, "attendance_records": {}}
# facial_matrix_row = {"value": []}
# attendance_records = {"session": "isPresent"}


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


def get_all_course_dict():
    doc_ref_list = db.collection(COLLECTION_COURSES).list_documents()
    doc_dict_list = []
    for doc_ref in doc_ref_list:
        doc_dict_list.append(doc_ref.get().to_dict())
    return doc_dict_list


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


def add_session(course_id, module_id, session_name):
    module_dict = get_module_dict(course_id, module_id)
    if module_dict is None:
        return
    module_dict["sessions"].append(session_name)
    set_module(course_id, module_dict)


def get_sessions(course_id, module_id):
    module_dict = get_module_dict(course_id, module_id)
    if module_dict is None:
        return []
    return module_dict["sessions"]


def create_student(course_id, module_index, matric_num, name):
    module_dict = get_module_dict(course_id, module_index)
    if module_dict is not None:
        students = module_dict["students"]
        for i in range(len(students)):
            if students[i]["matric_num"] == matric_num:
                student = Student(matric_num, name)
                module_dict["students"][i] = student.dict()
                set_module(course_id, module_dict)
                return student
        student = Student(matric_num, name)
        module_dict["students"].append(student.dict())
        set_module(course_id, module_dict)
        return student


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


def get_all_registered_student_obj(course_id, module_index):
    module_dict = get_module_dict(course_id, module_index)
    if module_dict is not None:
        students = []
        for i in range(len(module_dict["students"])):
            student_obj = Student.init_from_fb_dict(module_dict["students"][i])
            if len(student_obj.facial_info) > 0:
                students.append(student_obj)
        return students


def set_attendance_record(course_id, module_index, matric_number, session, is_present):
    student_obj = get_student_obj(course_id, module_index, matric_number)
    student_obj.attendance_records[session] = is_present
    set_student(course_id, module_index, student_obj.dict())


def get_attendance_record(course_id, module_index, matric_number, session):
    student_obj = get_student_obj(course_id, module_index, matric_number)
    if session not in student_obj.attendance_records.keys():
        return False
    else:
        return student_obj.attendance_records[session]


def get_all_facial_info(course_id, module_index):
    student_objs = get_all_student_obj(course_id, module_index)
    if student_objs is None:
        return
    facial_matrices = []
    for x in range(len(student_objs)):
        if len(student_objs[x].facial_info) > 0:
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
        self.sessions = []

    def add_student(self, student_obj):
        self.students.append(student_obj)

    def add_session(self, session_name):
        self.sessions.append(session_name)

    def dict(self):
        return {"index": self.index, "students": self.students, "sessions": self.sessions}


class Student:
    # student = {"matric_num": "", "name": "", "facial_info": [], "attendance_records": {}}
    def __init__(self, matric_num, name):
        self.matric_num = matric_num
        self.name = name
        self.facial_info = []
        self.attendance_records = {}
        self.email = ""

    @classmethod
    def init_from_fb_dict(cls, student_dict):
        student = Student(student_dict["matric_num"], student_dict["name"])
        fb_facial_info = student_dict["facial_info"]
        student.attendance_records = student_dict["attendance_records"]
        if "email" in student_dict.keys():
            student.email = student_dict["email"]
        for x in range(len(fb_facial_info)):
            student.facial_info.append(fb_facial_info[x]["value"])
        return student

    def dict(self):
        fb_facial_info = []
        for x in range(len(self.facial_info)):
            fb_facial_info.append({"value": self.facial_info[x]})
        return {"matric_num": self.matric_num, "name": self.name,
                "facial_info": fb_facial_info, "attendance_records": self.attendance_records,
                "email": self.email}

    def set_email(self, email):
        self.email = email


def test():
    set_course("cz3002", {"empty": None})
    print(get_course_dict("cz3002") == {"empty": None})

    create_course("cz3002", "ASE")
    print(get_course_dict("cz3002") == {'id': 'cz3002', 'modules': [], 'name': 'ASE'})

    set_module("cz3002", {"index": "sp1"})
    print(get_module_dict("cz3002", "sp1") == {"index": "sp1"})

    create_module("cz3002", "sp1")
    print(get_module_dict("cz3002", "sp1") == {'students': [], 'index': 'sp1', 'sessions': []})

    add_session("cz3002", "sp1", "lab1")
    print(get_sessions("cz3002", "sp1") == ["lab1"])

    set_student("cz3002", "sp1", {"matric_num": "0", "name": None,
                                  "facial_info": [{"value": [0, 1]}], "attendance_records": {}})
    print(get_student_obj("cz3002", "sp1", "0").dict() ==
          {'matric_num': '0', 'name': None, 'facial_info': [{'value': [0, 1]}], 'attendance_records': {}, 'email': ''})

    create_student("cz3002", "sp1", "0", "Jason")
    print(get_student_obj("cz3002", "sp1", "0").dict() ==
          {'matric_num': '0', 'name': 'Jason', 'facial_info': [], 'attendance_records': {}, 'email': ''})

    set_attendance_record("cz3002", "sp1", "0", "lab1", True)
    print(get_attendance_record("cz3002", "sp1", "0", "lab1"))

    create_student("cz3002", "sp1", "1", "Jason2")
    print(get_all_student_obj("cz3002", "sp1")[0].name == "Jason"
          and get_all_student_obj("cz3002", "sp1")[1].name == "Jason2")

    print(get_all_course_dict())

    set_facial_info("cz3002", "sp1", "0",
                    [[0, 0, 1, 1],
                     [1, 1, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0]])
    print(get_all_facial_info("cz3002", "sp1") == [[[0, 0, 1, 1], [1, 1, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]])

    print(get_all_registered_student_obj("cz3002", "sp1")[0].matric_num == "0"
          and len(get_all_registered_student_obj("cz3002", "sp1")) == 1)

    del_student("cz3002", "sp1", "0")
    print(get_student_obj("cz3002", "sp1", "0") is None)

    del_module("cz3002", "sp1")
    print(get_module_dict("cz3002", "sp1") is None)

    del_course("cz3002")
    print(get_course_dict("cz3002") is None)


def add_dummy_data():
    create_course("cz3002", "ASE")

    create_module("cz3002", "sp1")

    for x in range(20):
        student = create_student("cz3002", "sp1", "matric_num_" + str(x), "student_name_" + str(x))
        student.set_email(student.name + "@e.ntu.edu.sg")
        set_student("cz3002", "sp1", student.dict())

    for x in range(5):
        add_session("cz3002", "sp1", "lab" + str(x+1))

    create_module("cz3002", "sp2")

    for x in range(20):
        create_student("cz3002", "sp2", "matric_num_" + str(x), "student_name_" + str(x))


# test()
# add_dummy_data()
