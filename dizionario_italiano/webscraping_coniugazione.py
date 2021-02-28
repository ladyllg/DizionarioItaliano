from bs4 import BeautifulSoup
import requests
import lxml
from urllib import parse
import json
import pprint

CONIUGAZIONE_URL = "https://it.bab.la/coniugazione/italiano/{}"

def build_url(base_url):
    scheme, netloc, path, query, fragment = parse.urlsplit(base_url)
    query = parse.quote(query, safe="?=/")
    return parse.urlunsplit((scheme, netloc, path, query, fragment)) 

def get_header_box(soup):
    try:
        header_box = soup.find('div', class_='content')
        header = header_box.find_all('div', class_='quick-result-entry')
        trash = header_box.find('span', class_='flag it')
        trash.extract()
        verbo = header_box.find('h2').get_text()
        dict_header = []
        for h in header:
            try:
                tempo = h.find('div', class_='quick-result-option').get_text()
                coniugazione = h.find('li').get_text()
                dict_header.append({'tempo': tempo, 'coniugazione': coniugazione})
            except Exception as e:
                pass
        header_box.extract()
        return dict_header, verbo
    except Exception as e:
        return [], False

def get_table(soup):
    word_wrap_blocks = soup.find_all('div', class_='conj-tense-wrapper')
    dict_coniugazione = []
    for wrap in word_wrap_blocks:
        modo = wrap.find('div', class_='conj-block container result-block')
        modo_str = modo.find('h3').get_text()
        conj_tente_blocks = wrap.find_all('div', 'conj-tense-block')
        dict_tempi = []
        for c in conj_tente_blocks:
            tempo = c.find('h3', class_='conj-tense-block-header').get_text()
            line = c.find_all('div', class_='conj-item')
            dict_personi = []
            for l in line:
                person = l.find('div', class_='conj-person').get_text()
                result = l.find('div', class_='conj-result').get_text()
                dict_personi.append({'person': person, 'result': result})

            dict_tempi.append({'tempo': tempo, 'personi': dict_personi})

        dict_coniugazione.append({'modo': modo_str, 'tempi': dict_tempi})
    return dict_coniugazione
    

def get_result_coniugazione(parola):
    url = build_url(CONIUGAZIONE_URL.format(parola))
    response = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                                    })
    
    data = response.content
    soup = BeautifulSoup(data, 'lxml')
    header_dict, verbo = get_header_box(soup)
    return {'verbo': verbo, 'header': header_dict, 'coniugazioni': get_table(soup)}

        
