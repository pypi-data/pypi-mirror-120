import json
from EmployeeEducation import EmployeeEducation
from EmployeeSkills import EmployeeSkills
from EmployeeWorkHistory import EmployeeWorkHistory
import EmployeeClearance
import logging
import boto3
from botocore.exceptions import ClientError
from presigned import create_presigned_url
from bson import ObjectId

class Employee:
    def __init__(self, employee_json):
        print("inside Employee constructor")
        self.sovern_employee_json = employee_json
        self.employee_name = None
        self.employee_education = None
        self.employee_work_history = None
        self.employee_skills = None
        self.employee_security_credentials = None
        # called just employee_data in the UML diagram but changed it here because there is 2 employee data jsons:
        # 1. The raw json taken in from Sovern
        # 2. The formatted json that will be used to complete the SPT and will be stored in the database
        self.final_employee_data = {}
        self.get_object_id()
        self.get_employee_name()
        self.get_employee_resume_location()
        self.get_work_experience_years()
        self.get_security_clearance()
        self.get_employee_education()
        self.get_employee_certifications()
        self.get_employee_skills()
        self.get_employee_work_history()
        self.get_resume_plain_text()
        self.get_resume_uri()

    def get_object_id(self):
        original_id = self.sovern_employee_json['_id']
        string_id = ObjectId(original_id).__str__()
        self.build_final_employee_data('doc_id', string_id)
        '''
        The try-except block below was giving me issues when this function was called
        '''
        # try:
        #     original_id = self.sovern_employee_json['_id']
        #     string_id = original_id.toString()
        #     self.build_final_employee_data('_id', string_id)
        # except:
        #     None

    '''
    Getting the location of this candidate's resume in AWS S3
    '''
    def get_resume_uri(self):
        try:
            uri = self.sovern_employee_json['uri']
            uri_pieces = uri.split('/')
            presigned_url = create_presigned_url('resume-test-bucket-fcg', uri_pieces[-1])
            self.build_final_employee_data('presigned_url', presigned_url)
        except:
            self.build_final_employee_data('presigned_url', None)
            return None

    def get_employee_name(self):
        try:
            self.employee_name = self.sovern_employee_json['ContactInformation']['CandidateName']['FormattedName'].title()
            self.build_final_employee_data('Name', self.employee_name)
            print("Name from Employee.py is: ", self.employee_name)
            return self.employee_name
        except:
            self.build_final_employee_data('Name', None)
            return None

    def get_employee_resume_location(self):
        self.build_final_employee_data('Resume', None)
        return None

    def get_security_clearance(self):
        try:
            plain_text = self.sovern_employee_json['ResumeMetadata']['PlainText']
            employee_clearance = EmployeeClearance.create_clearance_string(plain_text)

            # my old code that just took the clearance from what the Sovern picked up in the

            # security_clearance = self.sovern_employee_json['SecurityCredentials'][0]['Name']
            # self.build_final_employee_data('Clearance', security_clearance)
            # return security_clearance

            self.build_final_employee_data('Clearance', employee_clearance)
            print("final clearance in Employee.py is: ", self.final_employee_data['Clearance'])
        except KeyError:
            self.build_final_employee_data('Clearance', 'Uncleared')
            return 'Uncleared'

    def get_work_experience_years(self):
        months_experience = self.sovern_employee_json['EmploymentHistory']['ExperienceSummary']['MonthsOfWorkExperience']
        years = int(months_experience/12)
        self.build_final_employee_data('Years_Experience', years)

    def get_employee_education(self):
        try:
            employee = EmployeeEducation(self.sovern_employee_json)
            # in order to get all the degrees that an employee has we have to run get_degree() on the
            # instance of EmployeeEducation first which creates and returns employee_degrees - an
            # attribute which is a list of dictionaries containing information about all the degrees
            # an employee holds
            degrees = employee.get_degrees()
            self.build_final_employee_data('Education', degrees)
            # or we could return degrees since both are the same thing
            # returning things in case in the future these functions are run just to print out their own information and
            # not to build the JSON object
            return employee.employee_degrees
        except:
            # because we still want the Education field for the JSON object
            self.build_final_employee_data('Education', None)
            return None

    def get_employee_certifications(self):
        employee = EmployeeEducation(self.sovern_employee_json)
        certifications = employee.get_certifications()
        self.build_final_employee_data('Certs', certifications)
        return certifications

    def get_employee_skills(self):
        employee = EmployeeSkills(self.sovern_employee_json)
        skills = employee.parse_skills()
        self.build_final_employee_data('Skills', skills)
        return skills

    def get_employee_work_history(self):
        print("inside get_employee_work_history in Employee.py")
        employee = EmployeeWorkHistory(self.sovern_employee_json)
        work_history = employee.get_work_history()
        if work_history == None:
            print("No work history for this one")
        self.build_final_employee_data('Work_History', work_history)
        return work_history

    def get_resume_plain_text(self):
        plain_text = self.sovern_employee_json['ResumeMetadata']['PlainText']
        self.build_final_employee_data('plain_text', plain_text)

    def get_search_json(self):
        '''
        We go through all the steps necessary to build up the final_employee_data dictionary in the init
        function itself so with this function we just have to return the class variable
        '''
        return self.final_employee_data

    def build_final_employee_data(self, key, value):
        self.final_employee_data[key] = value

    '''
    To be implemented later
    '''
    def build_SPT(self):
        pass