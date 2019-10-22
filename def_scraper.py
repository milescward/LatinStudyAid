from bs4 import BeautifulSoup
import json
import sys
import time
import random
import requests
from requests.exceptions import RequestException

WORD_LIST = {}

def parse_word(word):
    URL = "http://www.perseus.tufts.edu/hopper/morph?l=" + word + "&la=la"
    try:
        response = requests.get(URL)
    except requests.exceptions.RequestException as e:
        return

    if not response.status_code == 200:
        # print("Word '{}' failed.".format(word))
        return
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    lemmas = soup.find_all(class_="lemma")
    definition = soup.find_all(class_="lemma_definition")
    word_list = []
    index = 0
    for lemma in lemmas:
        word = {}
        try:
            # this was failing for me w/ beautifulsoup4 4.4.1 and lxml 3.6.0 (latest vers.)
            # @suheb you should make sure this works
            word['headword'] = lemma.find(class_="lemma_header").find(class_="la").text.strip()
        except AttributeError:
            pass
        word['definition'] = lemma.find(class_="lemma_definition").text.strip()
        word['pos'] = lemma.find("table").find("tr").find_all("td")[1].text.strip()
        word_list.insert(index, word)
        index += 1

    return word_list


def add_word_to_list(word):
    # check if already in there
    if word in WORD_LIST:
        return
    WORD_LIST[word] = parse_word(word)
    return

