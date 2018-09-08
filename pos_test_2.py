import nltk



# tokenized_text = nltk.word_tokenize(text)
# pos_text = nltk.pos_tag(tokenized_text)
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
#
# for word in pos_text:
#     print(word[0]+' : '+pos_tagset[word[1]])

with open('company-data.txt') as f:
    read_data = f.readlines()
f.closed

for line in read_data:
    tokenized_text = nltk.word_tokenize(line)
    pos_text = nltk.pos_tag(tokenized_text)
    print(pos_text)
    for word in pos_text:
        print(word[0]+' : '+pos_tagset[word[1]])
    print()


brand_graph = {
    'NNP':['NNP','IN'],
    'IN':['NNP']
}

noun_phrase_graph = {
    'NN':['NN','JJ','IN'],
    'IN':['NN','JJ']
}