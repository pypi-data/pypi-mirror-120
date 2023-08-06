import json

class EmployeeEducation:
    def __init__(self, employee_json):
        self.sovern_employee_json = employee_json
        self.employee_degrees = []
        self.employee_certifications = []

    '''
    Adding an id to each type of degree for better parsing for the front end
    '''
    def get_degree_id(self, degree_name):
        if degree_name.lower()[0] == 'a':
            return 100
        elif degree_name.lower()[0] == 'b':
            return 200
        elif degree_name.lower()[0] == 'm':
            return 300
        elif degree_name.lower()[0] == 'p':
            return 400
        elif degree_name.lower()[0] == 'd': # doctorate
            return 400
        else:
            return None

    def format_degree_dictionary(self, degree_list):
        for degree in degree_list:
            one_degree = {}
            degree_parts = degree.split(' in ')
            one_degree['Degree'] = degree_parts[0]
            one_degree['Id'] = self.get_degree_id(degree_parts[0])
            major = degree_parts[1]
            one_degree['Type'] = major
            self.employee_degrees.append(one_degree)

        # newly added
        # return self.employee_degrees

    def get_degrees(self):
        education_data = self.sovern_employee_json['Education']
        degree_types = []
        for degree in education_data['EducationDetails']:
            # going up to Type will only result in the title of the degree: bachelors, M.S, M.Sc, PhD
            degree_title = degree['Degree']['Type']
            # Every title will be followed by 'in' which is to be followed by the major name
            degree_title = degree_title.title() + ' in '
            # the 'Majors' key is a list. The line of code below assumes that there is only one value in that list
            # which is what has been observed in all of the examples jsons (under employeeJSONs folder for example)
            major = degree['Majors'][0].title()
            major_one = major.title()
            degree_title = degree_title + major
            degree_types.append(degree_title)

        self.format_degree_dictionary(degree_types)
        # newly added
        return self.employee_degrees

    '''
    Pulling out all the certifications that 
    '''
    def get_certifications(self):
        try:
            cert_dict = self.sovern_employee_json['Certifications']
            certifications_list = []
            for value in cert_dict:
                new_dict = {}
                new_dict['Name'] = value['Name']
                certifications_list.append(new_dict)
                del new_dict
            return certifications_list
        except:
            return None