# Using two-layered dictionaries to ensure consistency and make it easier
# to change labels if desired

# To change a label, change it in the enumerated dictionary
# To change/add how the matcher picks up a phrase, change/add it in the complete dictionary

# Note: For 'green badge' => TS/SCI with unknown poly

Months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

Month = {
    "01": Months[1],
    "1": Months[1],
    "jan": Months[1],
    "january": Months[1],
    "02": Months[2],
    "2": Months[2],
    "feb": Months[2],
    "february": Months[2],
    "03": Months[3],
    "3": Months[3],
    "mar": Months[3],
    "march": Months[3],
    "04": Months[4],
    "4": Months[4],
    "apr": Months[4],
    "april": Months[4],
    "05": Months[5],
    "5": Months[5],
    "may": Months[5],
    "06": Months[6],
    "6": Months[6],
    "jun": Months[6],
    "june": Months[6],
    "07": Months[7],
    "7": Months[7],
    "jul": Months[7],
    "july": Months[7],
    "08": Months[8],
    "8": Months[8],
    "aug": Months[8],
    "august": Months[8],
    "09": Months[9],
    "9": Months[9],
    "sep": Months[9],
    "sept": Months[9],
    "september": Months[9],
    "10": Months[10],
    "oct": Months[10],
    "october": Months[10],
    "11": Months[11],
    "nov": Months[11],
    "november": Months[11],
    "12": Months[12],
    "dec": Months[12],
    "december": Months[12]
}

CollateralClearances = {
    1: "Uncleared",
    2: "Confidential",
    3: "Secret",
    4: "Top Secret"
}

CollateralClearance = {
    "confidential": CollateralClearances[2],
    "secret": CollateralClearances[3],
    "top secret": CollateralClearances[4],
    "ts": CollateralClearances[4]
}

EligibilityDeterminations = {
    1: "Public Trust"
}

EligibilityDetermination = {
    "public trust": EligibilityDeterminations[1],
    "pt": EligibilityDeterminations[1]
}

SpecialClearances = {
    1: "SCI",
    2: "SAP",
    3: "NATO"
}

SpecialClearance = {
    "sci": SpecialClearances[1],
    "secret compartmented information": SpecialClearances[1],
    "sap": SpecialClearances[2],
    "special access program": SpecialClearances[2],
    "nato": SpecialClearances[3],
    "north atlantic treaty organization": SpecialClearances[3]
}

InvestigationTypes = {
    1: "NAC",
    2: "NACLC",
    3: "SSBI",
}

InvestigationType = {
    "nac": InvestigationTypes[1],
    "national agency check": InvestigationTypes[1],
    "tier 1": InvestigationTypes[1],
    "naclc": InvestigationTypes[2],
    "national agency check with local agency checks and credit check": InvestigationTypes[2],
    "tier 3": InvestigationTypes[2],
    "ssbi": InvestigationTypes[3],
    "single scope background investigation": InvestigationTypes[3],
    "sbi": InvestigationTypes[3],
    "tier 5": InvestigationTypes[3],
    "ssbi-pr": InvestigationTypes[3]
}

ClearanceAgencys = {
    1: "NSA",
    2: "DCSA",
    3: "DHS",
    4: "FBI",
    5: "DOD",
    6: "OPM",
    7: "Army",
    8: "NRO"
}

ClearanceAgency = {
    "nsa": ClearanceAgencys[1],
    "national security agency": ClearanceAgencys[1],
    "dcsa": ClearanceAgencys[2],
    "defense counterintelligence and security agency": ClearanceAgencys[2],
    "defense counterintelligence security agency": ClearanceAgencys[2],
    "dhs": ClearanceAgencys[3],
    "homeland security": ClearanceAgencys[3],
    "fbi": ClearanceAgencys[4],
    "federal bureau of investigation": ClearanceAgencys[4],
    "dod": ClearanceAgencys[5],
    "department of defense": ClearanceAgencys[5],
    "opm": ClearanceAgencys[6],
    "office of personnel management": ClearanceAgencys[6],
    "army": ClearanceAgencys[7],
    "nro": ClearanceAgencys[8],
    "national reconnaissance office": ClearanceAgencys[8]
}

Polygraphs = {
    1: "FS Polygraph",
    2: "CI Polygraph",
    3: "LS Polygraph",
    4: "Unknown Polygraph"
}

# for strings like "fs polygraph", it would still be picked up by picking up 'fs'
# need to be careful not to confuse counterintelligence with an agency, can be done when matched
# unknown polygraph is for a person who just writes 'polygraph' without designating a type
Polygraph = {
    "fs": Polygraphs[1],
    "fsp": Polygraphs[1],
    "full scope": Polygraphs[1],
    "full-scope": Polygraphs[1],
    "ci": Polygraphs[2],
    "counterintelligence": Polygraphs[2],
    "ls": Polygraphs[3],
    "lifestyle": Polygraphs[3],
    "polygraph": Polygraphs[4],
    "polygraphed": Polygraphs[4]
}
