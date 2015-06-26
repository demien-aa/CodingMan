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

class TagWorker(threading.Thread):

    def __init__(self, file_index_list, worker_cnt):
        threading.Thread.__init__(self)  
        self.file_index_list = file_index_list
        self.worker_cnt = worker_cnt

    def run(self):
        for file_index in self.file_index_list:
            self.tagging(str(file_index))

    def tagging(self, file_index):
        file_name = '%sreviews/top_n_app_tag_%s' % (MY_ROOT, file_index)
        current_app_id = None
        app_tags = defaultdict(lambda: defaultdict(int))
        aggregate_comment = ''
        app_detail = get_app_detail()
        index = 0
        sort_app_tags = {}
        with open(file_name) as f:
            for line in f.readlines():
                if index % 100 == 0:
                    print 'Worker %s: The %s hundred line of file_index %s' % (str(self.worker_cnt), str(index / 100), file_index)
                index += 1
                app_id, title, content = line.split('\t')

                if current_app_id is None:
                    current_app_id = app_id
                if app_id != current_app_id:
                    app_tags = defaultdict(int)
                    try:
                        detail = app_detail[current_app_id]
                        create_tag_and_save(aggregate_comment + detail, current_app_id)
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

    def get_tag(self, content, top_n=1000):
        result = defaultdict(int)
        text = nltk.word_tokenize(content.lower())
        stemmer = LancasterStemmer()
        for tag, category in nltk.pos_tag(text):
            if category in ['NN', 'NNP', 'NNS', 'NNPS']:  # http://www.monlp.com/2011/11/08/part-of-speech-tags/
                result[tag] += 1
        ordered_tags = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return ordered_tags

def get_tag(content, top_n=1000):
    result = defaultdict(int)
    text = nltk.word_tokenize(content.lower())
    stemmer = LancasterStemmer()
    re = nltk.pos_tag(text)
    # http://www.monlp.com/2011/11/08/part-of-speech-tags/
    for tag, category in re:   
        # if category in ['NN', 'NNP' 'NNS', 'NNPS']:
        if category in ['NN', 'NNS']:
            result[tag] += 1
    ordered_tags = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:top_n])
    return ordered_tags

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def create_tag_and_save(aggregate_comment, app_id):
    app_tags = defaultdict(int)
    try:
        result = get_tag(aggregate_comment)
    except:
        result = get_tag(aggregate_comment.decode('utf-8'))
    for tag, count in result.iteritems():
        app_tags[tag] += count
    for tag, times in app_tags.iteritems():
        Tag.objects.create(tag=tag, app_id=app_id, times=times)


def get_app_detail():
    result = defaultdict(str)
    review_file_name = '%stop_n_app_details' % (MY_ROOT)
    with open(review_file_name) as f:
        for line in f.readlines():
            app_id, app_name, app_description, app_icon, app_rank = line.split('\t')
            result[app_id] = app_name + app_description
    return result


if __name__ == '__main__':
    threading_cnt = 10
    index_list = range(200, 8401, 200)
    split_index_list = list(chunks(index_list, len(index_list)/threading_cnt))
    tag_workers = []
    for index_list in split_index_list:
        tag_workers.append(TagWorker(index_list, split_index_list.index(index_list)))
    [tag_worker.start() for tag_worker in tag_workers]
