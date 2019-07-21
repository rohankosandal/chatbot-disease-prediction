# -*- coding: utf-8 -*-
import tools
import wikipedia
import aiml
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import json
myBot=aiml.Kernel()
myBot.setBotPredicate("botname","Wiki")
myBot.learn("aimlfiles/basic_chat.aiml")
# Create your views here.
def query(Data):
    return myBot.respond(Data)

def response(Data):
    if tools.isQuestion(Data):
        qtype=tools.getQuestionType(Data)
        myBot.learn("aimlfiles/questions.aiml")

        print qtype
        if qtype=='NUM:date':
            ners=tools.structure_ne(tools.chunk(Data))
            try:
                ny=wikipedia.page(ners[0][0])
                date=tools.extractDate(ny.summary)[0][0]
                myBot.setPredicate("date",date)
                myBot.setPredicate("title",ny.title)
                return query(Data)
            except wikipedia.exceptions.DisambiguationError as e:
                 otheroptions=e.options
                 myBot.setPredicate("options",otheroptions)
                 return ("Did you mean "+" ".join(otheroptions))
        elif qtype=='HUM:ind' or qtype=='DESC:manner':
            ners=tools.structure_ne(tools.chunk(Data))
            ny=wikipedia.page(ners[0][0])
            imageURL=ny.images[0]
            print imageURL
            summary=wikipedia.summary(ny.title,sentences=2)
            myBot.setPredicate("title",ny.title)
            myBot.setPredicate("desc",summary)
            return query(Data)
        else:
            return query(Data)
    else:
        return query(Data)

def exe():
    imageURL=""
    # myData=request.POST.get('msg')
    myData="Who is Narendra Modi"
    PosData=response(myData)
    print JsonResponse({'message':PosData,'imageURL':imageURL})

exe()
