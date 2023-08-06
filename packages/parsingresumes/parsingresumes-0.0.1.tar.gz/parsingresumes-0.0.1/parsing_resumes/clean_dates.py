from spacy.lang.en import English
from spacy.matcher import Matcher
import re

from clean_fields import Month


def find_dates(sec_span):
    dates = []
    nlp = English()

    # If the date is a single token, add it to the list of dates
    for token in sec_span:
        if re.search("([0-9]{2}|[0-9])(/([0-9]{2}|[0-9]))?/([0-9]{4}|[0-9]{2}|[0-9])", token.text) or \
                re.search("([0-9]{4})([0-9]{2})([0-9]{2})", token.text):
            dates.append(nlp(token.text))

    # If the date is multiple tokens, take a span using the year as an anchor
    # and add it to the list of dates
    matcher = Matcher(nlp.vocab)
    matcher.add("date", [[{'TEXT': {'REGEX': "[0-9]{4}"}, 'LENGTH': 4}]])
    matches = matcher(sec_span)
    for match_id, start, end in matches:
        # Potential problem: be careful about overlaps
        if sec_span[start - 1].text == ',':
            dates.append(sec_span[start - 3: end])
        else:
            dates.append(sec_span[start - 2: end + 2])

    # For each date, clean it
    for i in range(len(dates)):
        dates[i] = clean_date(nlp, dates[i])
    return dates


def clean_date(nlp, date_span):
    # Construct matcher patterns
    my_patterns = []
    mdy_patterns = []
    dmy_patterns = []
    ymd_patterns = []
    for month in Month:
        my_patterns.append([{'LOWER': month}, {'LIKE_NUM': True, "LENGTH": 4}])
        mdy_patterns.append([{'LOWER': month},
                             {'LIKE_NUM': True, "LENGTH": {">=": 1, "<=": 2}},
                             {'LIKE_NUM': True, "LENGTH": 4}])
        mdy_patterns.append([{'LOWER': month},
                             {'LIKE_NUM': True, "LENGTH": {">=": 1, "<=": 2}},
                             {'IS_PUNCT': True},
                             {'LIKE_NUM': True, "LENGTH": 4}])
        dmy_patterns.append([{'LIKE_NUM': True, "LENGTH": {">=": 1, "<=": 2}},
                             {'LOWER': month},
                             {'LIKE_NUM': True, "LENGTH": 4}])
        ymd_patterns.append([{'LIKE_NUM': True, "LENGTH": 4},
                             {'LOWER': month},
                             {'LIKE_NUM': True, "LENGTH": {">=": 1, "<=": 2}}])

    matcher = Matcher(nlp.vocab)
    matcher.add("my", my_patterns)
    matcher.add("mdy", mdy_patterns)
    matcher.add("dmy", dmy_patterns)
    matcher.add("ymd", ymd_patterns)

    # Date list of [Day, Month, Year]
    date = [None] * 3

    # Search for single-token date formats
    for token in date_span:
        # Search for full slashed date formats and parse
        date_match = re.search("([0-9]{2}|[0-9])(/([0-9]{2}|[0-9]))?/([0-9]{4}|[0-9]{2})", token.text)
        if date_match:
            if date_match.span() == (0, len(token.text)):
                if date_match.group(2):
                    date[0] = date_match.group(3)
                date[1] = Month[date_match.group(1)]
                date[2] = date_match.group(4)
            else:
                print("Error processing groups")

        # Search for YYYYMMDD format
        else:
            date_match = re.search("([0-9]{4})([0-9]{2})([0-9]{2})", token.text)
            if date_match:
                if date_match.span() == (0, len(token.text)):
                    date[2] = date_match.group(1)
                    date[1] = Month[date_match.group(2)]
                    date[0] = date_match.group(3)
                else:
                    print("Error processing groups")

            # Search for just a year
            date_match = re.search("([0-9]{4})", token.text)
            if date_match and date_match.span() == (0, len(token.text)):
                date[2] = date_match.group(1)

    # Matcher parsing
    matches = matcher(date_span)
    date_formats = {}
    date_format = ""

    # Determine the format of the match
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        date_formats[string_id] = (start, end)
    if "my" in date_formats:
        date_format = "my"
    if "mdy" in date_formats:
        date_format = "mdy"
    if "dmy" in date_formats:
        date_format = "dmy"
    if "ymd" in date_formats:
        date_format = "ymd"

    # Parse matcher formats
    if date_format == "ymd":
        date[0] = date_span[date_formats[date_format][1] - 1].text
        date[1] = Month[date_span[date_formats[date_format][0] + 1].text.lower()]
        date[2] = date_span[date_formats[date_format][0]].text
    if date_format == "mdy":
        date[0] = date_span[date_formats[date_format][0] + 1].text
        date[1] = Month[date_span[date_formats[date_format][0]].text.lower()]
        date[2] = date_span[date_formats[date_format][1] - 1].text
    if date_format == "my" or date_format == "dmy":
        if date_format == "dmy":
            date[0] = date_span[date_formats[date_format][0]].text
        date[1] = Month[date_span[date_formats[date_format][1] - 2].text.lower()]
        date[2] = date_span[date_formats[date_format][1] - 1].text

    # Normalize formats of dates
    if date[0] and len(date[0]) == 1:
        date[0] = "0" + date[0]
    if date[2] and len(date[2]) == 2:
        if int(date[2]) < 30:
            date[2] = "20" + date[2]
        else:
            date[2] = "19" + date[2]

    return date
