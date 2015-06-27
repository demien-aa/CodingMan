import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.conf import settings
from models import App, Tag_Similarity, Tag

MY_ROOT = settings.ROOT + '/../../'

def import_detial():
    review_file_name = '%stop_n_app_details' % (MY_ROOT)
    with open(review_file_name) as f:
        for line in f.readlines():
            app_id, app_name, app_description, app_icon, app_rank = line.split('\t')
            try:
                App.objects.create(pk=app_id, name=app_name, description=app_description, icon=app_icon, weight=int(app_rank))
            except:
                continue

def import_similarity():
    review_file_name = '%stag_similarity' % (MY_ROOT)
    with open(review_file_name) as f:
        for line in f.readlines():
            ori_tag, similar_tag, weight = line.split('\t')
            try:
                Tag_Similarity.objects.create(base_tag=ori_tag, tag=similar_tag, similarity=float(weight))
            except Exception as e:
                print e
                continue

def import_tag():
    review_file_name = '%strimed_tag_15w' % (MY_ROOT)
    with open(review_file_name) as f:
        for line in f.readlines():
            app_id, tag, times = line.split('\t')
            try:
                Tag.objects.create(tag=tag, app_id=app_id, times=int(times))
            except Exception as e:
                print e
                continue

if __name__ == '__main__':
    # import_detial()
    # import_similarity()
    import_tag()
