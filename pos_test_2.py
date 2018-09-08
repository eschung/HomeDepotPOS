import nltk
import collections

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


def process_text(text):
    tagged_words = collections.OrderedDict()
    tokenized_text = nltk.word_tokenize(text)
    pos_text = nltk.pos_tag(tokenized_text)
    print(pos_text)
    count = 0
    for word in pos_text:
        tagged_words[count] = {'word': word[0], 'pos': word[1], 'pos_simple': pos_tagset[word[1]], 'type': ''}
        count += 1
    return tagged_words

def find_entity(text, pos_graph, type_label):
    current_state = 'Start'
    items = []
    phrase = ''
    word_found = False
    start_index = 0
    index = 0

    for payload in text:
        word = text[payload]
        # if we find a pos that is in our graph
        if word['pos'] in pos_graph[current_state]:
            current_state = word['pos']
            # print(current_state)
            # print('found a proper noun:', word['word'])
            phrase += word['word'] + ' '
            word['type'] = type_label
            if not word_found:
                start_index = index
                word_found = True

        else:
            # if not in graph then add phrase
            if phrase:
                # items.append(phrase.strip())
                end_index = index
                object = {'phrase':phrase.strip(), 'start':start_index, 'end':end_index-1}
                items.append(object)

                word_found = False
                phrase = ''
                current_state = 'Start'


        index += 1

    return text, items

def find_product_attributes(text_payload, product_list):
    brand_graph = {
        'Start': ['NNP'],
        'NNP': ['NNP', 'IN', 'CC'],
        'IN': ['NNP'],
        'CC': ['NNP']
    }

    unit_graph = {
        'Start': ['CD'],
        'CD': []
    }

    modifier_graph = {
        'Start': ['JJ'],
        'JJ': ['JJ',','],
        ',': ['JJ']
    }
    start_index = 0
    product_words_master_list = []
    product_count = 0
    test_ordered_dict = collections.OrderedDict()
    result = {}

    for product in product_list:
        test_ordered_dict = collections.OrderedDict()

        end_index = product['end']
        product_words = []
        # print(start_index,end_index+1)
        # print(text_payload[start_index])
        for i in range(start_index, end_index+1):
            # product_words.append(text_payload[i])
            test_ordered_dict[i] = text_payload[i]
        # print(product_words)
        # product_words_master_list.append([product_words])
        product_words_master_list.append(test_ordered_dict)
        try:
            start_index = end_index + 1
        except:
            print('out of bounds!')

    # go through each product
    for product in product_list:
        end_index = product['end']
        # find brand
        temp, brands = find_entity(product_words_master_list[product_count], brand_graph, 'BRAND')

        # find units
        temp, units = find_entity(product_words_master_list[product_count], unit_graph, 'UNIT')

        # find description
        temp, descriptions = find_entity(product_words_master_list[product_count], modifier_graph, 'MODIFIER')

        product_count += 1

        if brands:
            brand = brands[0]['phrase']
        else:
            brand = None
        if units:
            unit = units[0]['phrase']
        else:
            unit = None
        if descriptions:
            description = descriptions[0]['phrase']
        else:
            description = None

        result[product['phrase']] = {
            'brand': brand,
            'units': unit,
            'description': description
        }
    return result


def main():
    text = "I want 3 hot, pink Black and Decker step ladders, 2 hammers, and blue paint."
    print(text)
    tagged_words = process_text(text)

    brand_graph = {
        'Start': ['NNP'],
        'NNP': ['NNP', 'IN', 'CC'],
        'IN': ['NNP'],
        'CC': ['NNP']
    }

    product_graph = {
        'Start': ['NN', 'NNS'],
        'NN': ['NN', 'NNS'],
        'NNS': []
    }

    unit_graph = {
        'Start': ['CD'],
        'CD': []
    }

    modifier_graph = {
        'Start': ['JJ'],
        'JJ': ['JJ']
    }

    tagged_words, brands = find_entity(tagged_words, brand_graph, 'BRAND')
    tagged_words, products = find_entity(tagged_words, product_graph, 'PRODUCT')
    tagged_words, units = find_entity(tagged_words, unit_graph, 'UNIT')
    tagged_words, description = find_entity(tagged_words, modifier_graph, 'MODIFIER')


    payload = find_product_attributes(tagged_words, products)

    print(payload)
    for product in payload:
        print(product)
        print(payload[product])
        print()

if __name__ == "__main__":
    main()