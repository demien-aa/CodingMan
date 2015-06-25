import nltk
import pprint
from collections import defaultdict, OrderedDict


def get_tag(content, top_n=10):
    result = defaultdict(int)
    text = nltk.word_tokenize(content)
    for tag, category in nltk.pos_tag(text):
        if category in ['NN', 'NNP', 'NNS', 'NNPS']:  # http://www.monlp.com/2011/11/08/part-of-speech-tags/
            result[tag] += 1
    ordered_tags = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:top_n])
    return ordered_tags

if __name__ == '__main__':
    sort_app_tags = {}
    app_tags = defaultdict(lambda: defaultdict(int))
    index = 0
    with open('top_n_app_reviews') as f:
        for line in f.readlines()[:5000]:
            if index % 100 == 0:
                print 'The %s hundred line' % str(index / 100)
            index += 1
            app_id, title, content = line.split('\t')
            try:
                result = get_tag(title + content)
            except:
                continue
            for tag, count in result.iteritems():
                app_tags[app_id][tag] += count
    for app, tags in app_tags.iteritems():
        sort_app_tags[app] = OrderedDict(sorted(tags.items(), key=lambda x: x[1], reverse=True))

    with open('top_n_app_tag', 'w') as output:
        for app, tags in sort_app_tags.iteritems():
            tag_str = ' '.join(['%s,%s' % (tag, count) for tag, count in tags.iteritems() if count > 1])
            oneline = '%s\t%s\n' % (app, tag_str)
            output.write(oneline)
        output.close()
