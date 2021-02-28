from bs4 import BeautifulSoup
import requests
import lxml
from urllib import parse
import json
import pprint

CAMBRIDGE_URL = "https://dictionary.cambridge.org/dictionary/italian-english/{}"

def build_url(base_url):
    scheme, netloc, path, query, fragment = parse.urlsplit(base_url)
    query = parse.quote(query, safe="?=/")
    return parse.urlunsplit((scheme, netloc, path, query, fragment)) 

def get_header(header):
    try:
        dpos = header.find('span', class_='pos dpos').get_text()
        gram = header.find_all('span', class_='gram dgram')
        part_of_speech = dpos
        for g in gram:
            part_of_speech += g.get_text()
    
    except Exception as e:
        print(e)
        dpos = header.find('span', class_='pos dpos').get_text()
        part_of_speech = '{}'.format(dpos)
    return part_of_speech

def get_examples(block):
    phrase_divs = block.find_all('div', class_='examp dexamp')
    phrase_spans = block.find_all('span', class_='eg deg')
    dict_esempi = []
    for p in phrase_divs:
        esempio = p.find('span', class_='eg deg').get_text()
        trans = p.find('span', class_='trans dtrans hdb').get_text().replace('\n','')
        dict_esempi.append({'esempio': esempio, 'translation': trans})
    
    for p in phrase_divs:
        block.div.extract()
    
    return dict_esempi

def get_definition_block(block):    
    if block: 
        definition_trans = block.find_all('span', 'trans dtrans')
        string_defintion = ''
        for d in definition_trans:
            string_defintion += '{}'.format(d.get_text())

    return {'definition': string_defintion, 'esempi': get_examples(block)}

def get_data_cambridge(soup):
    try:
        dict_prhases = []
        dictionary = soup.find('div', 'dictionary')
        pages = dictionary.find_all('span', class_='link dlink')
        dict_pages = []
        for p in pages:
            dict_parola = []
            definitions = p.find_all('div', class_='sense-block')
            header_obj = p.find('span', 'di-info')
            header_str = get_header(header_obj)
            if header_obj:
                header_str = get_header(header_obj)
                for d in definitions:
                    dict_info = []
                    sense_body = d.find_all('div', 'sense-body dsense_b')
                    for b in sense_body:
                        try:
                            indicator = b.find('span', class_='indicator dindicator').get_text()
                        except:
                            indicator = ''

                        def_block = b.find('div', 'def-body ddef_b ddef_b-t')
                        
                        dict_info.append({'indicator': indicator, 'definitions': get_definition_block(def_block)})
                    
                    dict_parola.append(dict_info)
                dict_pages.append({'header': header_str, 'body': dict_parola})
            else:
                return False
    except Exception as e:
        print(e)
        return False
    return dict_pages

def get_result_cambridge(parola):
    url = build_url(CAMBRIDGE_URL.format(parola))
    response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                                    })    
    data = response.content
    soup = BeautifulSoup(data, 'lxml')
    return get_data_cambridge(soup)
        
