import json
from Employee import Employee
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


# inserting the 27 resumes into Search.Demo_Resumes
for item in demo_resume_objects:
    test = Employee(item)
    test_search_json = test.get_search_json()
    search_demo_resumes.insert_one(test_search_json)

counter_1 = 0

# inserting 27 resumes into just the search.Resumes
for item in demo_resume_objects:
    test_resume = Employee(item)
    test_resume_search_json = test_resume.get_search_json()
    search_resumes.insert_one(test_resume_search_json)
    counter_1 = counter_1 + 1

print("counter_1 at the end of first for loop: ", counter_1, '\n')


counter_2 = 0
# inserting 100 resumes into search.Resumes
for item in parsed_resume_objects:
    test_resume2 = Employee(item)
    test_resume_search_json2 = test_resume2.get_search_json()
    search_resumes.insert_one(test_resume_search_json2)
    counter_2 = counter_2 + 1

print("counter)2 at the end of second for loop: ", counter_2, '\n')