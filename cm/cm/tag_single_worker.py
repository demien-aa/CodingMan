import nltk
import pprint
import threading
import os
import re
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from collections import defaultdict, OrderedDict
from models import Tag
from django.conf import settings
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import EnglishStemmer

MY_ROOT = settings.ROOT + '/../../'

def get_tag(content, top_n=1000):
    result = defaultdict(int)
    clean = re.sub(r"[^a-zA-Z0-9]+"," ",content.lower())
    text = nltk.word_tokenize(clean)
    # stemmer = LancasterStemmer()
    stemmer = EnglishStemmer()
    material = nltk.pos_tag(text)
    # http://www.monlp.com/2011/11/08/part-of-speech-tags/
    for tag, category in material:   
        # if category in ['NN', 'NNP' 'NNS', 'NNPS']:
        if category in ['NN', 'NNS']:
            # tag = stemmer.stem(tag)
            result[tag] += 1
    ordered_tags = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:top_n])
    return ordered_tags

def single_process(file_index):
    current_app_id = None
    aggregate_comment = ''
    index = 0
    # real_review_file_name = '%stop_n_app_reviews' % (MY_ROOT)
    real_review_file_name = '%sreviews_1000/top_n_app_tag_%s' % (MY_ROOT, file_index)
    app_detail = get_app_detail()
    print real_review_file_name
    with open(real_review_file_name) as f:
        for line in f.readlines():
            if index > 0 and index % 100 == 0:
                print 'The %s hundred line.' % (str(index / 100))
            index += 1
            app_id, title, content = line.split('\t')

            if current_app_id is None:
                current_app_id = app_id
            if app_id != current_app_id and index > 1:
                print 'tag app: %s' % current_app_id
                app_tags = defaultdict(int)
                try:
                    detail = app_detail[current_app_id]
                    material = aggregate_comment + detail
                    create_tag_and_save(material, current_app_id)
                except Exception as e:
                    print 'error here!!!!'
                    print e
                aggregate_comment = ''
                current_app_id = app_id
            aggregate_comment += (title + content)
        try:
            create_tag_and_save(aggregate_comment, current_app_id)
        except Exception as e:
            print e

def get_app_detail():
    result = defaultdict(str)
    review_file_name = '%stop_n_app_details' % (MY_ROOT)
    with open(review_file_name) as f:
        for line in f.readlines():
            app_id, app_name, app_description, app_icon, app_rank = line.split('\t')
            result[app_id] = app_name + app_description
    return result

def create_tag_and_save(aggregate_comment, app_id):
    app_tags = defaultdict(int)
    result = get_tag(aggregate_comment.decode('utf-8'))
    for tag, count in result.iteritems():
        app_tags[tag] += count
    for tag, times in app_tags.iteritems():
        Tag.objects.create(tag=tag, app_id=app_id, times=times)


if __name__ == '__main__':
    single_process(sys.argv[1])
