import nltk
import pprint
import threading
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from collections import defaultdict, OrderedDict
from models import Tag
from django.conf import settings
from nltk.stem.lancaster import LancasterStemmer

MY_ROOT = settings.ROOT + '/../../'

def get_tag(content, top_n=1000):
    result = defaultdict(int)
    text = nltk.word_tokenize(content.lower())
    stemmer = LancasterStemmer()
    for tag, category in nltk.pos_tag(text):
        if category in ['NN', 'NNP', 'NNS', 'NNPS']:  # http://www.monlp.com/2011/11/08/part-of-speech-tags/
            # tag = stemmer.stem(tag)
            result[tag] += 1
    ordered_tags = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:top_n])
    return ordered_tags

def single_process():
    current_app_id = None
    aggregate_comment = ''
    index = 0
    review_file_name = '%stop_n_app_reviews' % (MY_ROOT)
    review_file_name = '%sreviews/top_n_app_tag_201' % (MY_ROOT)
    with open(review_file_name) as f:
        for line in f.readlines():
            if index % 100 == 0:
                print 'The %s hundred line.' % (str(index / 100))
            index += 1
            app_id, title, content = line.split('\t')

            if current_app_id is None:
                current_app_id = app_id
            if app_id != current_app_id:
                app_tags = defaultdict(int)
                try:
                    create_tag_and_save(aggregate_comment, current_app_id)
                except Exception as e:
                    print e
                aggregate_comment = ''
                current_app_id = app_id
            aggregate_comment += (title + content)
        try:
            create_tag_and_save(aggregate_comment, current_app_id)
        except Exception as e:
            print e

def create_tag_and_save(aggregate_comment, app_id):
    app_tags = defaultdict(int)
    result = get_tag(aggregate_comment)
    for tag, count in result.iteritems():
        app_tags[tag] += count
    for tag, times in app_tags.iteritems():
        Tag.objects.create(tag=tag, app_id=app_id, times=times)


if __name__ == '__main__':
    single_process()
    # threading_cnt = 1 
    # index_list = range(200, 8401, 200)
    # split_index_list = list(chunks(index_list, len(index_list)/threading_cnt))
    # tag_workers = []
    # for index_list in split_index_list:
    #     tag_workers.append(TagWorker(index_list, split_index_list.index(index_list)))
    # [tag_worker.start() for tag_worker in tag_workers]
