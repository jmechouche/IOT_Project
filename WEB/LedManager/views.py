from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from LedManager.forms import HomeForm

import paho.mqtt.publish as publish

# Create your views here.
class Accueil(TemplateView):
    template_name = 'LedManager/accueil.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            publish.single(topic, message, hostname='192.168.43.246')
            args = {'form':form, 'topic': topic, 'message': message}
            return render(request, self.template_name, args)
