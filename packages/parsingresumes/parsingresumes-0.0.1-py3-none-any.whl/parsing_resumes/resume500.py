import json
from Employee import Employee
from pymongo import *
from bson import ObjectId
import pprint
import EmployeeClearance

mongo_uri = "mongodb://mshah:sams_best_friend@54.173.181.254:31453/?authSource\\\\=admin"
client = MongoClient(mongo_uri)

'''
Going into the sovern database 
'''
sovern_db = client.sovren

'''
Going into DemoResumes collection in sovern database
'''
demo_resume_col = sovern_db.DemoResumes


demo_resume_objects = [i for i in demo_resume_col.find({})]

'''
Connecting to the search database where we will put the parsed jsons into
'''
search_db = client.search

'''
Connecting to the collection in the search database that we will be inserting the new parsed data into 
- the NewResumes collection
'''
search_demo_resumes = search_db.Demo_Resumes

counter = 0
for item in demo_resume_objects:
    test_resume = Employee(item)
    test_resume_search_json = test_resume.get_search_json()
    search_demo_resumes.insert_one(test_resume_search_json)
    print("inserted in mmondo db\n")
    counter = counter + 1

print("counter at the end of loop: ", counter, '\n')
