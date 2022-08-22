
from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from parrot import Parrot
import torch
import warnings
from .models import Person
warnings.filterwarnings("ignore")
def addnew(request):

     if request.method == "POST":
        
        identify = request.POST['identiy']
        classname = request.POST['class']
        tag = request.POST['tag']
       
        url = request.POST['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('div',  {'class': classname})
        table=table.find_all(tag)
        for ta in table:
             Person.objects.create(content = ta.get_text(),identiy=identify)
            
        return redirect('home')
        
     return render(request,'index.html',{"cont":""}) 
def home(request):
   
    return render(request,'home.html',{"cont":""}) 
def hello(request): 
    url = "https://dzone.com/articles/10-database-optimization-best-practices-for-web-de"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('div',  {'class': 'content-html'})
    table=table.find_all('p')
    cont = []
  
    for ta in table:
          
          #translation=translator.translate(ta.get_text(),  dest='ml')
          #cont.append(translation.text)
          #translation=translator.translate(translation.text,  dest='en')  
          cont.append(ta.get_text())
          break
    

    return render(request,'index.html',{"cont":cont}) 
def check(request,id):
    data = Person.objects.filter(identiy=id).values().order_by('id')

    for d in data:
        parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
        para_phrases = parrot.augment(input_phrase=d['content'])
        ob= Person.objects.get(id=d['id'])
        ob.content = para_phrases[2][0]
        ob.save()
        
    return redirect('home') 