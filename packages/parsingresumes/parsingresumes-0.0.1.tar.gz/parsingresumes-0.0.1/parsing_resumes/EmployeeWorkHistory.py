import json

class EmployeeWorkHistory:

    def __init__(self, employee_json):
        self.sovern_employee_json = employee_json
        self.work_history = []
        self.formatted_work_history = None

    # idea is parse_work_history just parses information out of the json, and format/get work_history would
    # format it in a way that is easily readable and suitable for the big Employee json we are building in
    # Employee
    def parse_work_history(self):
        try:
            employee_data_positions = self.sovern_employee_json['EmploymentHistory']['Positions']
            try:
                for position in employee_data_positions:
                    new_work_dict = {}
                    new_work_dict['Employer'] = position['Employer']['Name']['Normalized']
                    new_work_dict['Job Title'] = position['JobTitle']['Raw']
                    new_work_dict['Start Date'] = position['StartDate']['Date']
                    # how to deal with outputting end date if its chile key 'IsCurrentDate' equal to true ??
                    new_work_dict['End Date'] = position['EndDate']['Date']
                    new_work_dict['Job Duties'] = position['Description'].split('\n')
                    self.work_history.append(new_work_dict)
            except KeyError:
                return None
        except KeyError:
            print("returning None becuase no positions from work history")
            return None

        # print("self.work_history: \n")
        # print(self.work_history, '\n')
        # print("Length of self.work_history: ", len(self.work_history), '\n')

    # change name to format_work_history possibly?
    def get_work_history(self):
        self.parse_work_history()
        return self.work_history # the raw work history - this can be part of the json
        # object I build to send back ot mongo

    def format_work_history(self):
        pass
