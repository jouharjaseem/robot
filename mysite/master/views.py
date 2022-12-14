
import json
from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from parrot import Parrot
import torch
import warnings
from .models import Person
from googletrans import Translator
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
def savedata(request):
    if request.method == "POST":
        
        id = request.POST['id']
      
        tag = request.POST['content']
        ob= Person.objects.get(id=id)
        ob.content = tag
        ob.identiy = 2
        ob.save()
       
        return redirect('home')
        
    return render(request,'index.html',{"cont":""}) 
def home(request):
    data = Person.objects.values().order_by('id')

    return render(request,'home.html',{"cont":data}) 

def trans(request):
    data = Person.objects.values().order_by('id')

    return render(request,'trans.html',{"cont":data}) 
def trascheck(request,id): 
    data = Person.objects.filter(id=id).values().order_by('id')
    content = data[0]['content']
    translator = Translator()
    translation = translator.translate(content, dest='ml')
    
    ob= Person.objects.get(id=id)
    ob.content = translation.text
    ob.identiy = 2
    ob.save()
       
    return redirect('trans')
 
    
def check(request,id):
    data = Person.objects.filter(id=id).values().order_by('id')
    content = data[0]['content']
    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
    para_phrases = parrot.augment(input_phrase=content)
    para_phrases = [('database optimization has become critical for web developers for improving the performance of web applications and thus improving user experience it might sound a little unappealing to some but the benefits are worth the work', 133), ('database optimization has become crucial to web developers for improving the performance of web applications and thus improving user experience it might seem a little unappealing to some but the benefits are worth the work', 132), ('database optimization has become crucial to web developers for improving the performance of web applications and thus improving user experience it might sound a little unappealing to some but the benefits are worth the work', 128), ('database optimization has become crucial for web developers for improving the performance of web applications and thus bettering user experience it might sound a bit unappealing to some but the benefits are worth the work', 120), ("database optimization is critical to web developers for improving the performance of web applications and thus improving the user experience it might seem a little unappealing to some but the benefits are worth the work if you optimize your database properly you'll improve performance reduce bottlenecks and save resources", 46)]
     
        #ob= Person.objects.get(id=d['id'])
        #ob.content = para_phrases[2][0]
        #ob.save()
   
        #parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
        #para_phrases = parrot.augment(input_phrase=d['content'])
        
        
    return render(request,'check.html',{"cont":data,"phrase":para_phrases,"id":id}) 
def updatedata(request,id):
    data = Person.objects.values().order_by('id')
    data = [user.get('content') for user in data]
    data = ' '.join(data)
    
    url = "https://www.letsthink.in/addnew"
    data = {'id': id, 'name':data}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=('rzp_test_yourTestApiKey', 'yourTestApiSecret'))
    return render(request,'index.html',{"cont":""}) 
