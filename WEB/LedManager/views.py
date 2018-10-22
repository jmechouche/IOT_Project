from django.http import HttpResponse
from django.shortcuts import render

import paho.mqtt.publish as publish

# Create your views here.
def home(request):
    return HttpResponse("""
        <h1>RETOUR HTML DEGUEU</h1>
    """)

def view_article(request, id_article):
    return HttpResponse(
        "Vous avez demandé l'article n {0} !".format(id_article)
    )

def turnon(request, topic, Msg):
    MqttBroker = "192.168.43.246"
    MqttChannel = topic
    print('Msg = ')
    print(Msg)
    publish.single(MqttChannel, Msg, hostname=MqttBroker)
    return HttpResponse('OK')