import os
from collections import defaultdict, OrderedDict
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from models import Tag


def get_top_n_similar_app(app_id, top_n=None):
    similarity = defaultdict(int)
    tags = get_top_n_tag_for_app(app_id, with_times=True)
    tags_dict = dict(tags)
    all_app_tags = Tag.objects.filter(tag__in=tags_dict.keys())
    for tag_obj in all_app_tags:
        tag = tag_obj.tag
        times = tag_obj.times
        app_id = tag_obj.app_id
        if tag in tags_dict:
            similarity[app_id] += tags_dict[tag] + times
    if top_n is None:
        similarity = OrderedDict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
    else:
        similarity = OrderedDict(sorted(similarity.items()[:top_n], key=lambda x: x[1], reverse=True))
    return similarity


def get_top_n_tag_for_app(app_id, top_n=None, with_times=False):
    if top_n is None:
        tags = Tag.objects.filter(app_id=app_id).order_by('-times')
    else:
        tags = Tag.objects.filter(app_id=app_id).order_by('-times')[:top_n]
    if with_times:
        return [(tag.tag, tag.times) for tag in tags]
    else:
        return [tag.tag for tag in tags]
