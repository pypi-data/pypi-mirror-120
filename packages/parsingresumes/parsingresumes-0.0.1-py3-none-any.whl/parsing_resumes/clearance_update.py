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


counter_2 = 0
# inserting 100 resumes into search.NewResumes
# for item in demo_resume_objects:
#     test_resume2 = Employee(item)
#     print("type of test_resume2: ", type(test_resume2))
#     print("sovern_employee_json: ", test_resume2.sovern_employee_json)
#     test_resume_search_json2 = test_resume2.get_search_json()
#     print("name of emoloyee: ", test_resume_search_json2['Name'])
#     try:
#         print("original id of employee: ", test_resume2['_id']) # for looking them up in the original mongo db
#     except:
#         print("test_resume2 for the employee: ", test_resume2.final_employee_data, '\n')
#     search_demo_resumes.insert_one(test_resume_search_json2)
#     counter_2 = counter_2 + 1
#
# print("counter)2 at the end of second for loop: ", counter_2, '\n')

# testing out only the clearance output for all

# counter3 = 0
# for item in demo_resume_objects:
#     plain_text = item['ResumeMetadata']['PlainText']
#     print("new employee:")
#     test = EmployeeClearance.create_clearance_string(plain_text)
#     print("clearance in clearance_update.py main file: ", test, '\n\n')
#     counter3 = counter3 + 1
#
# print("counter3 is: ", counter3, '\n')

# testing for just Adeshina Bright Adebayo:
for item in demo_resume_objects:
    if item['_id'] == ObjectId('6140a66813a3d1a52a358e80'):
        print("found Adeshina")
        test_employee = Employee(item)
        test_employee_search_json = test_employee.get_search_json()
        print("final json is: ", test_employee_search_json)

print("--------------------------------------------------------------------------------------------------------------\n")

counter = 0
for item in demo_resume_objects:
    if item['_id'] == ObjectId('6140a66813a3d1a52a358e80'):
        print("wanting to pass this object id for: ", item['ContactInformation']['CandidateName']['FormattedName'].title())
    else:
        test_resume = Employee(item)
        test_resume_search_json = test_resume.get_search_json()
        # search_demo_resumes.insert_one(test_resume_search_json)
        print("inserted in mmondo db\n")
        counter = counter + 1

print("counter at the end of loop: ", counter, '\n')
