import json
from Employee import Employee
from EmployeeEducation import EmployeeEducation
from EmployeeWorkHistory import EmployeeWorkHistory
from EmployeeSkills import EmployeeSkills
import pymongo

# right now the jsons are coming out of a file so using the below functions to open
# those files and load the json. Ultimately they will be coming straight from the
# MongoDB database

file = open('EmployeeJSONs/Lauren_Hale.json')
test1 = json.load(file)

employee_test1 = Employee(test1)
print(employee_test1.final_employee_data)
search_json = {}

search_json['_id'] = employee_test1.get_object_id()
search_json['Name'] = employee_test1.get_employee_name()
search_json['Resume'] = employee_test1.get_employee_resume_location()
search_json['Clearance'] = employee_test1.get_security_clearance()
search_json['Years Experience'] = employee_test1.get_work_experience_years()
search_json['Education'] = employee_test1.get_employee_education()
search_json['Certifications'] = employee_test1.get_employee_certifications()
search_json['Skills'] = employee_test1.get_employee_skills()
search_json['Work History'] = employee_test1.get_employee_work_history()


for key in search_json:
    print(key, ": ", search_json[key], '\n')

print('\n\n\n\n')

print("tesing out get_search_json : \n")

print(employee_test1.get_search_json())
