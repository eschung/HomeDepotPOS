import nltk
import collections


text = "Along the way, we'll cover some fundamental techniques in NLP, including sequence labeling, n-gram models, backoff, and evaluation. These techniques are useful in many areas, and tagging gives us a simple context in which to present them. We will also see how tagging is the second step in the typical NLP pipeline, following tokenization."
text = "This is a Wellington Manufacturing hammer."
text = "I want 3 Black and Decker step ladders, 2 hammers, and blue paint."
tokenized_text = nltk.word_tokenize(text)
pos_text = nltk.pos_tag(tokenized_text)
# print(pos_text)

pos_tagset = {
    "$":"dollar",
    "''":"closing quotation mark",
    "(":"opening parenthesis",
    ")":"closing parenthesis",
    ",":"comma",
    "--":"dash",
    ".":"sentence terminator",
    "":": colon or ellipsis",
    "CC":"conjunction, coordinating",
    "CD":"numeral, cardinal",
    "DT":"determiner",
    "EX":"existential there",
    "FW":"foreign word",
    "IN":"preposition or conjunction, subordinating",
    "JJ":"adjective or numeral, ordinal",
    "JJR":"adjective, comparative",
    "JJS":"adjective, superlative",
    "LS":"list item marker",
    "MD":"modal auxiliary",
    "NN":"noun, common, singular or mass",
    "NNP":"noun, proper, singular",
    "NNPS":"noun, proper, plural",
    "NNS":"noun, common, plural",
    "PDT":"pre-determiner",
    "POS":"genitive marker",
    "PRP":"pronoun, personal",
    "PRP$":"pronoun, possessive",
    "RB":"adverb",
    "RBR":"adverb, comparative",
    "RBS":"adverb, superlative",
    "RP":"particle",
    "SYM":"symbol",
    "TO":"'to' as preposition or infinitive marker",
    "UH":"interjection",
    "VB":"verb, base form",
    "VBD":"verb, past tense",
    "VBG":"verb, present participle or gerund",
    "VBN":"verb, past participle",
    "VBP":"verb, present tense, not 3rd person singular",
    "VBZ":"verb, present tense, 3rd person singular",
    "WDT":"WH-determiner",
    "WP":"WH-pronoun",
    "WP$":"WH-pronoun, possessive",
    "WRB":"Wh-adverb",
    "``":"opening quotation mark"
}
# for tag in pos_tagset:
#     print(tag)

# filepath = 'test.txt'
# with open(filepath) as fp:
#    line = fp.readline()
#    while line:
#        if ':' in line:
#            colon_pos = line.find(':')
#            print('"'+line[:colon_pos]+'":"'+line[colon_pos+1:].strip()+'",')
#        line = fp.readline()

tagged_words = collections.OrderedDict()

count = 0
for word in pos_text:
    # print(word[0]+' : '+pos_tagset[word[1]])
    tagged_words[count] = {'word':word[0], 'pos':word[1], 'pos_simple':pos_tagset[word[1]], 'type':''}
    count += 1


def find_entity(text, brand_graph, type_label):
    current_state = 'Start'
    brands = []
    phrase = ''
    word_found = False
    start_index = 0

    for payload in text:
        word = text[payload]
        # if we find a pos that is in our graph
        if word['pos'] in brand_graph[current_state]:
            current_state = word['pos']
            # print(current_state)
            # print('found a proper noun:', word['word'])
            phrase += word['word'] + ' '
            word['type'] = type_label
            if word_found:


        else:
            # if not in graph then add phrase
            if phrase:
                brands.append(phrase.strip())
                phrase = ''
                current_state = 'Start'

    return text, brands



brand_graph = {
    'Start':['NNP'],
    'NNP':['NNP','IN','CC'],
    'IN':['NNP'],
    'CC':['NNP']
}

product_graph = {
    'Start':['NN','NNS'],
    'NN':['NN','NNS'],
    'NNS':[]
}

unit_graph = {
    'Start':['CD'],
    'CD':[]
}

print(text)
print(pos_text,'\n')

tagged_words, brands = find_entity(tagged_words, brand_graph, 'BRAND')
tagged_words, products = find_entity(tagged_words, product_graph, 'PRODUCT')
tagged_words, units = find_entity(tagged_words, unit_graph, 'UNIT')

print('Brands:',brands)
print('Products:',products)
print('Units:',units)

'''
{
    'step ladders': {
                    'brand':'Black and Decker',
                    'units': 3
                    }
    'hammers': {
                'units': 2
                }
    'paint':{
            'color': 'blue'
            }
}
'''

# {'word':'step ladder', 'start':3, 'end':4}