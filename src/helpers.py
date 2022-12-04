import os
import re

import nltk.data
import transformers
import logging
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

from dotenv import load_dotenv
from nltk.stem import PorterStemmer

from src.heideltime.python_heideltime import Heideltime

REMOVE_ADDITION_SPACES = re.compile('[\s+]')

load_dotenv()

os.chdir('../..')
current_directory = os.getcwd()
process_description_path = current_directory + os.getenv('PROCESS_DESCRIPTION_PATH')
temporal_expressions_path = current_directory + os.getenv('TEMPORAL_EXPRESSIONS_PATH')
timex3_annotations_path = current_directory + os.getenv('TIMEX3_ANNOTATIONS_PATH')
to_evaluate_path = current_directory + os.getenv('TO_EVALUATE_PATH')

heideltime_parser = Heideltime()
heideltime_parser.set_document_type(os.getenv('DOCUMENT_TYPE'))

REPLACE_BY_SPACE = re.compile('[/(){}\[\]\|@,;]')
REMOVE_SYMBOLS = re.compile('[^0-9a-z #+_]')
REMOVE_NUM = re.compile('[\d+]')
STOPWORDS = set(stopwords.words('english'))

stemmer = PorterStemmer()


def clean_text(txt):
    lemmatizer = WordNetLemmatizer()
    txt = str(txt).lower()
    txt = REMOVE_ADDITION_SPACES.sub(' ', txt)
    txt = REPLACE_BY_SPACE.sub(' ', txt)
    txt = REMOVE_NUM.sub('', txt)
    txt = REMOVE_SYMBOLS.sub('', txt)
    txt = ' '.join(word for word in txt.split() if word not in STOPWORDS)
    txt = ' '.join(word for word in txt.split() if (len(word) >= 2 and len(word) <= 20))
    txt = txt.replace(' not ', ' ')
    txt = ' '.join([lemmatizer.lemmatize(word) for word in txt.split()])
    #txt = ' '.join([stemmer.stem(word) for word in txt.split()])
    return txt


# To get all sentences from a file
def get_all_sentences(file):
    return " ".join(line.strip() for line in file)


# To split text in sentences
def nltk_segmentation(p):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(p, realign_boundaries=False)


def get_sentences(text):
    return nltk_segmentation(text)


def get_temporally_annotated_sentences(text):
    return nltk_segmentation(heideltime_parser.parse(text))


def get_temporally_annotated_text(text):
    return heideltime_parser.parse(text)


def remove_addition_spaces(text):
    return REMOVE_ADDITION_SPACES.sub(' ', text)


# To write all time annotations in a new file
def create_annotated_file(new_file_name, content):
    with open(new_file_name, 'w') as file:
        file.write(content)


def get_unique_values(text):
    used = set()
    unique = [x for x in text if x not in used and (used.add(x) or True)]
    return unique


# To split text in sentences
def nltk_segmentation(p):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(p, realign_boundaries=False)


# It returns only the sentences containing time constraints
def get_sentences_with_time(text):
    sentence_counter = 0
    index_sentences_with_time = []
    sentences_with_time = []
    sentences = nltk_segmentation(text)
    for annotated_sentence in nltk_segmentation(heideltime_parser.parse(text)):
        if "TIMEX3" in annotated_sentence:
            index_sentences_with_time.append(sentence_counter)
        sentence_counter = sentence_counter + 1
    for index in index_sentences_with_time:
        sentences_with_time.append(sentences[index])
    return sentences_with_time

def load_transformers():
    transformers.tokenization_utils.logger.setLevel(logging.ERROR)
    transformers.configuration_utils.logger.setLevel(logging.ERROR)
    transformers.modeling_utils.logger.setLevel(logging.ERROR)

