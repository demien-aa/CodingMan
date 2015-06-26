import nltk
import pprint
import threading
from collections import defaultdict, OrderedDict


class Tag(threading.Thread):

    def __init__(self, file_index_list, worker_cnt):
        threading.Thread.__init__(self)  
        self.file_index_list = file_index_list
        self.worker_cnt = worker_cnt

    def run(self):
        for file_index in self.file_index_list:
            self.tagging(str(file_index))

    def tagging(self, file_index):
        sort_app_tags = {}
        app_tags = defaultdict(lambda: defaultdict(int))
        index = 0
        file_name = 'reviews/top_n_app_tag_%s' % file_index
        with open(file_name) as f:
            for line in f.readlines():
                if index % 100 == 0:
                    print 'Worker %s: The %s hundred line of file_index %s' % (str(self.worker_cnt), str(index / 100), file_index)
                index += 1
                app_id, title, content = line.split('\t')
                try:
                    result = self.get_tag(title + content)
                except:
                    continue
                for tag, count in result.iteritems():
                    app_tags[app_id][tag] += count
        for app, tags in app_tags.iteritems():
            sort_app_tags[app] = OrderedDict(sorted(tags.items(), key=lambda x: x[1], reverse=True))

        output_file_name = 'tags/top_n_app_tag_%s' % self.file_index
        with open(output_file_name, 'w') as output:
            for app, tags in sort_app_tags.iteritems():
                tag_str = ' '.join(['%s,%s' % (tag, count) for tag, count in tags.iteritems() if count > 1])
                oneline = '%s\t%s\n' % (app, tag_str)
                output.write(oneline)
            output.close()

    def get_tag(self, content, top_n=10):
        result = defaultdict(int)
        text = nltk.word_tokenize(content)
        for tag, category in nltk.pos_tag(text):
            if category in ['NN', 'NNP', 'NNS', 'NNPS']:  # http://www.monlp.com/2011/11/08/part-of-speech-tags/
                result[tag] += 1
        ordered_tags = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return ordered_tags


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


if __name__ == '__main__':
    threading_cnt = 20 
    index_list = range(200, 8401, 200)
    split_index_list = list(chunks(index_list, len(index_list)/threading_cnt))
    tag_workers = []
    for index_list in split_index_list:
        tag_workers.append(Tag(index_list, split_index_list.index(index_list)))
    [tag_worker.start() for tag_worker in tag_workers]
