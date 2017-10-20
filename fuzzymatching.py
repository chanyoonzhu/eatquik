from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def match_fuzzy_string (fuzzy, pool):

    candidate = process.extractOne(fuzzy, pool)[0]
    ratio = fuzz.token_set_ratio(candidate.lower(), fuzzy.lower())
    if ratio > 50:
        return candidate
    else:
        return None
