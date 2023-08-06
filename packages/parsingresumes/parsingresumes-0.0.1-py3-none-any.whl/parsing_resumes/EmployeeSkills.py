import json

class EmployeeSkills():

    def __init__(self, employee_json):
        # options for this dictionary:
        # 1. key = skillName, value = years experience rounded to the tenth place
        # 2. Have multiple keys and dictionaries
        self.employee_skills = []
        try:
            self.employee_json = employee_json
            self.raw_skills_data = self.employee_json['SkillsData'][0]
            self.unique_skills = set()
        except:
            print("Please ensure you pass in an accurate employee data json.")


    ########################################################################################################################
    # Get Skills
    #
    # Written: Sam Caplan
    #
    # Des: Recursively extracts base skills from parsed resume. Yields the skills information back to the formatSkills
    # function
    #
    # Input: Parsed Resume Taxonomy dictionary
    # Output: Yields Skills found in the taxonomy
    #
    # BUGS: None
    # Notes: None

    def getSkills(self, taxonomy, pSkill="No Parent"):

        # checks every single key, goes further and further into skills to
        # Checks to make sure the taxonomy entered is a dict
        if isinstance(taxonomy, dict):
            # If we find the key @whereFound then we know this is a base skill we want to extract
            for key, value in taxonomy.items():
                if key == "FoundIn":  # this is a skills they had in their resume
                    try:
                        # Skill could potentially not have Total Months key because it is a parent skill
                        # yield taxonomy["Name"], taxonomy["MonthsExperience"]['Value'], pSkill
                        yield taxonomy['Name'], taxonomy['MonthsExperience']['Value'], pSkill

                    except KeyError:

                        try:
                            if taxonomy["Variations"]:
                                pass
                        # or skill was not found in users work history description so no time frame was found
                        except KeyError:
                            yield taxonomy["Name"], pSkill
                # if Where Found key was not found then recursively call the function again to continue through this
                # level of the taxonomy
                else:
                    try:
                        yield from self.getSkills(value, taxonomy["Name"])
                    except KeyError:
                        if isinstance(value, list):
                            yield from self.getSkills(value)
                        else:
                            pass
        # If the skill is a list then the skill is a parent skill and we must explore the next depth of the taxonomy
        elif isinstance(taxonomy, list):
            # should jump through sub taxonomy here
            for item in taxonomy:
                yield from self.getSkills(item, pSkill)


    def format_skill(self, skill):
        if skill[0] in self.unique_skills:
            return
        else:
            skill_dict = {}
            skill_dict['Skill_Name'] = skill[0]
            self.unique_skills.add(skill[0])
            if type(skill[1]) == int:
                skill_dict['Years_Experience'] = round((skill[1]/12))
            else:
                skill_dict['Years_Experience'] = 0
            self.employee_skills.append(skill_dict)


    def parse_skills(self):
        taxonomies = self.raw_skills_data['Taxonomies']
        for one_dict in taxonomies:
            for skills_dict in self.getSkills(one_dict['SubTaxonomies']):
                self.format_skill(skills_dict)

        return self.employee_skills