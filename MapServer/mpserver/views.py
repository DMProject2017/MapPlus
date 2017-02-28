from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.
def index(request):
    return HttpResponse("<h2>Hello World!</h2>A Server for a Feng Ru Cup Project.<br><br><footer><center>College of Software, Beihang University</center></footer>")

def getmsg(request):
    res={}
    res['msg']="hehehe"
    res['code']="python"
    ans=json.dumps(res)
    return HttpResponse(ans)
