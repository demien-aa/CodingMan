from django import http
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
import json


class HomeView(View):

    def get(self, *args, **kwargs):
        test = []
        for k in range(6):
            tags = []
            for i in range(28):
                imgs = []
                for j in range(100):
                    imgObj = {
                        'src': 'https://static-s.aa-cdn.net/img/ios/284882215/414fb5243cf13d547113e8741d51c3f2',
                        'title': 'Facebook',
                        'link': 'https://www.appannie.com/apps/ios/app/app-annie/'
                    }
                    imgs.append(imgObj)
                tagObj = {
                    'tagName': 'Test Tag %d' % i,
                    'tagMessage': 'Tag message',
                    'imgs': imgs
                }
                tags.append(tagObj)
            test.append(tags)
        return render_to_response('home.html', {'tagDatas': mark_safe(json.dumps(test))})
