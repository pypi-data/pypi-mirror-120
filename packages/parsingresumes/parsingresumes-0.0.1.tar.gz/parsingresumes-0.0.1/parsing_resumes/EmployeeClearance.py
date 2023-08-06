import spacy
from spacy.matcher import PhraseMatcher
from spacy.lang.en import English
import json
#from dotenv import load_dotenv

from clean_dates import find_dates
from final_clearance import get_final_clearance
from clean_fields import CollateralClearance, EligibilityDetermination, SpecialClearance, InvestigationType, ClearanceAgency, Polygraph

#load_dotenv()
nlp = English()


Matchers = {
    'collateral_security_clearance': CollateralClearance,
    'eligibility_determination': EligibilityDetermination,
    'special_clearance_level': SpecialClearance,
    'investigation_type': InvestigationType,
    'clearance_agency': ClearanceAgency,
    'polygraph': Polygraph
}

def create_clearance_string(plain_text_1):
    # loading a model

    # nlp = spacy.load('en_core_web_sm')

    # Add infixes to separate out // and dates in ##(##)/##/##(##) format
    double_slash = [r'''//''', ]
    date = [r'''(?<=[a-zA-Z])([0-9]{2}|[0-9])(/([0-9]{2}|[0-9]))?/([0-9]{4}|[0-9]{2}|[0-9])''', ]

    infixes = nlp.Defaults.infixes + double_slash + date
    infix_regex = spacy.util.compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_regex.finditer

    # creating a Phrasematcher object
    matcher = PhraseMatcher(nlp.vocab)
    plain_text_1 = plain_text_1.lower()

    doc = nlp(plain_text_1)

    phrase_list_collateral = CollateralClearance.keys()

    # for each piece of text in the phase list we are making it into it's own doc object
    # list of a bunch of docs
    collateral_words = [nlp(text) for text in phrase_list_collateral]

    # pass each doc object into the matcher
    matcher.add('collateral_security_clearance', None, *collateral_words)


    d = {}
    found_matches_list = []
    found_matches = matcher(doc)
    # print("matches found: ", found_matches)
    clearances = []

    for match_id, start, end in found_matches:
        # print("inside for loop for going through found_matches")
        string_id = nlp.vocab.strings[match_id]
        clearance_string = doc[start-5:end+15]
        #if string_id == "collateral_security_clearance":
            #found_matches_list.append(clearance_string.text)
        # print(match_id, string_id, start, end, clearance_string.text)

        #d["collateral_security_clearance: "] = found_matches_list
        clearances.append(parse_clearance_string(clearance_string))

    print("the clearances for this are: ", clearances)

    if clearances:
        return clearances[0]
    else:
        return "Uncleared"



def parse_clearance_string(clearance_string):
    matcher = PhraseMatcher(nlp.vocab)
    clearance_string = " ".join(clearance_string.text.split('\n'))
    # print("\nPrinting New Security Clearance String...")
    # print("=" * 140)
    # print(clearance_string)
    # print("=" * 140)

    clearance_string_doc = nlp(clearance_string)

    phrase_list_collateral = CollateralClearance.keys()
    phrase_list_eligibility = EligibilityDetermination.keys()
    phrase_list_special_clearance = SpecialClearance.keys()
    phrase_list_investigation = InvestigationType.keys()
    phrase_list_agency = ClearanceAgency.keys()
    phrase_list_polygraph = Polygraph.keys()

    # for each piece of text in the phase list
    # we are making it into it's own doc object
    # list of a bunch of docs
    collateral_words = [nlp(text) for text in phrase_list_collateral]
    eligibility_words = [nlp(text) for text in phrase_list_eligibility]
    special_clearance_words = [nlp(text) for text in phrase_list_special_clearance]
    investigation_words = [nlp(text) for text in phrase_list_investigation]
    agency_words = [nlp(text) for text in phrase_list_agency]
    polygraph_words = [nlp(text) for text in phrase_list_polygraph]

    matcher = PhraseMatcher(nlp.vocab)
    # pass each doc object into the matcher
    matcher.add('collateral_security_clearance', None, *collateral_words)
    matcher.add('eligibility_determination', None, *eligibility_words)
    matcher.add('special_clearance_level', None, *special_clearance_words)
    matcher.add('investigation_type', None, *investigation_words)
    matcher.add('clearance_agency', None, *agency_words)
    matcher.add('polygraph', None, *polygraph_words)

    found_matches = matcher(clearance_string_doc)
    matches_list = []

    for match_id, start, end in found_matches:
        string_id = nlp.vocab.strings[match_id]
        span = clearance_string_doc[start:end]
        matches_list.append((Matchers[string_id])[span.text])
        # print(match_id, string_id, start, end, (Matchers[string_id])[span.text])

    # calling the get_final_string from final_clearance.py

    final_clearance = get_final_clearance(matches_list)
    print("final_clearance for this employee is: ", final_clearance)
    return final_clearance


# TO DO - be able to pass the clearance string that we create in create_clearance_string to this function
def parse_dates (clearance_string):
    # pull dates out from the clearance string and clean them into a list of [d, m, y]
    dates = find_dates(clearance_string)
    for date in dates:
        if date[2]:
            print_string = "Date: "
            if date[0]:
                print_string += date[0] + " "
            if date[1]:
                print_string += date[1] + " "
            print_string += date[2]
            print(print_string)
        else:
            print("No match found")

    # print()