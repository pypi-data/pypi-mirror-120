# create sublists for all the final clearances. These are the phrases in
# orange from Matt's JIRA document

'''
The idea is to divide the final clearance title into a list of sub tokens then
check if a list is a sublist of all the phrases picked up by our matcher.

Potential problems that are possible here:

1. More than one list can match. For example if someone has a TS/SCI with FS Poly that
could match the ts_fs_poly list but also the top_secret list since 'Top Secret' will be
one of the phrases that gets picked up
'''

'''
Problems found AFTER running all the code:

1. We COULD take the last list printed out since that seems to be the most detailed one BUT the problem 
arises when we have a Top Secret with an Unknown Polygraph. This results in only Top Secret being selected as 
the final answer

2. This code is heavy and slow! Soo.... efficiency needs works, especially as we move to do this on larger data
sets 
'''

'''
Notes from my meeting with D&A:
1. Unknown polygraph sometimes only comes from the fact that they mention the word 'polygraph' in there
2. Put in a key for the LS poly 
3. Add TS/SCI with Unknown Poly as a key - put unknown poly above ci and fs 
4. Write the resulting data to a json file 
'''

# Should Secret NATO be included with Secret?
# putting 'CI Polygraph' as one phrase instead of 'CI' and 'Polygraph'
# because A&D's code normalizes counterintelligence polygraph to 'CI Polygraph'
# same with full scope poly

clearances = {
    'Confidential': ['Confidential'],
    'Public Trust': ['Public Trust'],
    'Secret': ['Secret'],
    'Top Secret': ['Top Secret'],
    'Top Secret/SCI': ['Top Secret', 'SCI'],
    'Top Secret/SCI with Lifestyle Polygraph': ['Top Secret', 'SCI', 'LS Polygraph'],
    'Top Secret/SCI with CI Polygraph': ['Top Secret', 'SCI', 'CI Polygraph'],
    'Top Secret/SCI with FS Polygraph': ['Top Secret', 'SCI', 'FS Polygraph']
}

clearance_weights = {
    1: 'Confidential',
    2: 'Public Trust',
    3: 'Secret',
    4: 'Top Secret',
    5: 'Top Secret/SCI with CI Polygraph',
    6: 'Top Secret/SCI with FS Polygraph'
}

clearance_weights2 = {
    'Confidential': 1,
    'Public Trust': 2,
    'Secret': 3,
    'Top Secret': 4,
    'Top Secret/SCI with CI Polygraph': 5,
    'Top Secret/SCI with FS Polygraph': 6
}


def get_final_clearance(matches):
    # print("inside get_final_string in final_clearance")
    # print("matches passed in: ", matches)
    all_clearance_keys = []
    for key in clearances:
        # steps taken by this for loop and the if statement in it
        # 1. go to every key in the clearances dict, take its values and put it in a set (so no repetitions),
        # and
        if set(clearances[key]).issubset(set(matches)):
            # print("the key found for this list is: ", key)
            all_clearance_keys.append(key)
    if len(all_clearance_keys) > 0 :
        return all_clearance_keys[-1]
    else:
        return "Uncleared"



def get_final_string2(matches):
    print("inside get_final_string in final_clearance")
    print("matches passed in: ", matches)
    all_clearance_keys = []
    for key in clearances:
        # steps taken by this for loop and the if statement in it
        # 1. go to every key in the clearances dict, take its values and put it in a set (so no repetitions),
        # and
        if set(clearances[key]).issubset(set(matches)):
            print("the key found for this list is: ", key)
            all_clearance_keys.append(key)
    print("final clearance would be: ", all_clearance_keys[-1], '\n')




