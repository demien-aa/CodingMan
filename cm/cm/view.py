from django import http
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response


class HomeView(View):

    def get(self, *args, **kwargs):
        return render_to_response('home.html')
