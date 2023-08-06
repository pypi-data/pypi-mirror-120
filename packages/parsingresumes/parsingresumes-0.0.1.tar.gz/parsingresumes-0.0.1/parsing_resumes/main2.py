import json
from Employee import Employee
from EmployeeEducation import EmployeeEducation
from EmployeeWorkHistory import EmployeeWorkHistory
from EmployeeSkills import EmployeeSkills
from pymongo import *
from bson import ObjectId
import pprint

mongo_uri = "mongodb://mshah:sams_best_friend@54.173.181.254:31453/?authSource\\\\=admin"
client = MongoClient(mongo_uri)

'''
Going into the sovern database 
'''
sovern_db = client.sovren

'''
Going into ParsedResume collection in sovern database
'''
parsed_resume_col = sovern_db.ParsedResume

'''
Going into the DemoResumes collection in the sovern database
'''
demo_resumes_col = sovern_db.DemoResumes

'''
Creating a cursor that can be used to retrieve all the documents in the ParsedResume collection
'''
cursor = demo_resumes_col.find()

demo_resumes_ids = []

demo_resume_objects= [i for i in demo_resumes_col.find({})]
parsed_resume_objects = [i for i in parsed_resume_col.find({})]

'''
Connecting to the search database where we will put the parsed jsons into
'''
search_db = client.search

'''
Connecting to the two collections in the search database that we will be inserting the new parsed data into 
- the Resumes and Demo_Resumes collections
'''
search_demo_resumes = search_db.Demo_Resumes
search_resumes = search_db.Resumes

item1 = demo_resume_objects[0]
object_id = None

for key in item1:
    if key == '_id':
        print("type of id: ", type(key)) # the reason this is printed as str is becuase we are gettgin the type of the
        # key ITSELF and not the type of the value that the key represents
        print("_id: ", item1[key])
        object_id = item1[key]

print("\noutside of the for loop: ")
print("object_id: ", object_id, '\n')
print("type of object_id: ", type(object_id), '\n')
object_id_string = ObjectId(object_id).__str__()
print("printing informattion about object_id_string: \n")
print("object_id_string: ", object_id_string)
print("type: ", type(object_id_string))

