from main import demo_resume_objects
from Employee import Employee

for item in demo_resume_objects[:10]:
    employee_obj = Employee(item)
    skills = employee_obj.get_employee_skills()

    print("skills: \n", skills)

print("inside test_skills.py")