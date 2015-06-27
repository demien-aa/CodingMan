from django.views.generic import View
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
import json
from .services import get_similar_tags, get_apps_by_tag


class HomeView(View):
    TOP_N_TAGS = ['warrior']

    def get(self, request, *args, **kwargs):
        tag_objs = []
        for tag in self.TOP_N_TAGS:
            similar_tags = get_similar_tags(tag)
            similar_tag_objs = []
            for similar_tag in similar_tags:
                app_objs = get_apps_by_tag(similar_tag)
                tagObj = {
                    'tagName': similar_tag[0],
                    # 'tagMessage': '%s - %s - %s' % (app_objs[0]['title'], app_objs[1]['title'], app_objs[2]['title']),
                    'imgs': app_objs
                }
                similar_tag_objs.append(tagObj)
            tag_objs.append(similar_tag_objs)
        return render_to_response('home.html', {'tagDatas': mark_safe(json.dumps(tag_objs))})