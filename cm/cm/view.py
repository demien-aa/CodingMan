from django import http
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
import json


class HomeView(View):

    def get(self, *args, **kwargs):
        test = {'name': 'cc', 'age': 1}
        return render_to_response('home.html', {'test': mark_safe(json.dumps(test))})
