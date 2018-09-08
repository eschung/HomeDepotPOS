import re

test_companies = ['BLACK AND DECKER']

# given a list of companies and a dictionary of words, return string with capitalised brand names
def capitalise_companies(companies, payload):
    # TODO: optimize
    words = re.findall(r"[\w']+", payload)
    for word in words:
        phrase_length = 1
        start_index = words.index(word)
        while phrase_length <= len(words) - start_index:
            phrase = ""
            for i in range(0, phrase_length):
                if len(phrase) != 0:
                    phrase += " "
                phrase += words[start_index + i]
            if phrase.upper() in companies:
                capitalise_words(words, start_index, phrase_length)
            phrase_length += 1
    return " ".join(words)


def capitalise_words(words, start, length):
    for i in range (0, length):
        words[start + i] = words[start + i].capitalize()