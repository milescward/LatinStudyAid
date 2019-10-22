import os
from collections import Counter
from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.readers import get_corpus_reader
from cltk.corpus.latin.latin_library_corpus_types import corpus_directories_by_type
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.stop.latin import STOPS_LIST
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from cltk.lemmatize.latin.backoff import *
from cltk.semantics.latin.lookup import *
import string
import re
import def_scraper


# See available texts

# Import the corpus
latin_importer = CorpusImporter('latin')
latin_importer.import_corpus('latin_models_cltk')
latin_importer.import_corpus('latin_text_latin_library')

latin_corpus = get_corpus_reader(corpus_name = 'latin_text_latin_library', language = 'latin')
#print(len(list(latin_corpus.docs())))
#print(corpus_directories_by_type)

# print(len(list(latin_corpus.paras())))
# print(len(list(latin_corpus.sents())))
# print(len(list(latin_corpus.words())))
# text = os.path.expanduser('~/cltk_data/latin/text/latin_text_latin_library/caesar/')
# with open(text) as fo:
#     text = fo.read()
#
# print(text[500:1500])
#text_lowered = text.lower()


# Import the text
cae = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. 2 Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. 3 Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, 4 proximique sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut ipsi in eorum finibus bellum gerunt. 5 Eorum una pars, quam Gallos obtinere dictum est, initium capit a flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et Helvetiis flumen Rhenum, vergit ad septentriones. 6 Belgae ab extremis Galliae finibus oriuntur, pertinent ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. 7 Aquitania a Garumna flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum solis et septentriones."
cae_text_lowered = cae.lower()

latin_sentence_tokenizer = TokenizeSentence('latin')
latin_word_tokenizer = WordTokenizer('latin')
alphabetized_list = []
lemmatizer = LemmaReplacer('latin')
backoff_lemmatizer = BackoffLatinLemmatizer()

# Tokenize into sentence tokens
def tokenize_sentences(text):
    return latin_sentence_tokenizer.tokenize(text)

# Tokenize the text into word tokens
# I think the tokenize method may have
# a parameter where you pass the string



# Strip the punctuation
def strip_punctuation(text):
    tokens = latin_word_tokenizer.tokenize(text)
    word_tokens_wo_punctuation = [token for token in tokens if token not in ['.', ',', ':', ';']]
    return word_tokens_wo_punctuation


# Get a unique set of the word tokens
def unique_words(text):
    uniques = set(strip_punctuation(text))
    return uniques

# Print number of sentences and words

# Alphabetize the list

# def alphabetize_words():
#     for word in cae_word_tokens_WO_punc_unique:
#         alphabetized_list.append(word)
#     return alphabetized_list

# Show Word frequency
# cae_word_counter = Counter(cae_word_tokens_WO_punc)
# print(cae_word_counter)


def remove_stops(text):
    no_stops = [w for w in strip_punctuation(text) if w not in STOPS_LIST]
    return no_stops


# Lemmatize
def lemmatize(text):
    lemmata_orig = lemmatizer.lemmatize(strip_punctuation(remove_stops(text)), return_raw=True)
    return lemmata_orig


def get_POS(text):
    unique_vocab = set()
    tagger = POSTag('latin')
    tagged = tagger.tag_crf(text)
    for item in tagged:
        if item in ['.', ',', ':', ';', "'", "',"]:
            continue
        unique_vocab.add(item)

    return sorted(list(unique_vocab))


def get_text_vocab(text):
    translator = Synonyms(dictionary='translations', language='latin')
    lemmas = lemmatizer.lemmatize(strip_punctuation(text), return_raw=True)
    translations = translator.lookup(lemmas)
    just_translations = Lemmata.isolate(translations)
    tr = set(just_translations)
    roots = []
    for item in tr:
        x = item.split('/')
        word = x[1]
        word = re.sub("\d+", "", word)
        roots.append(word)
    return sorted(set(roots))

WORD_LIST = {}

def add_word_to_list(word):
    # check if already in there
    if word in WORD_LIST:
        return
    WORD_LIST[word] = def_scraper.parse_word(word)
    return

def get_definitions(text):
    roots = get_text_vocab(text)
    for item in roots:
        add_word_to_list(item)
    return WORD_LIST

definitions = get_definitions(cae)
for item in definitions.items():
    print(item)
