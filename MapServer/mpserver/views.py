# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, models
from django.views.decorators.csrf import csrf_exempt
import json
import urllib2
import sys
import time
from .models import *
from django.db.models import Q
reload(sys)
sys.setdefaultencoding('utf-8')


# Create your views here.
def index(request):
    return HttpResponse("<h2>Hello World!</h2>A Server for a Feng Ru Cup Project.<br><br><footer><center>College of Software, Beihang University</center></footer>")

@csrf_exempt
def getmsg(request):
    # get json
    addr = "中国北京市海淀区知春路29号1"
    xpos=200
    ypos=200
    if request.method=='POST':
        print "POST Method"
        reqans = request.POST
        print reqans
        xpos = request.REQUEST.get('longitude', 200)
        ypos = request.POST.get('latitude', 200)
    if xpos == 200 or ypos == 200:
        res2 = {}
        res2['status'] = "false"
        res2['time'] = ""
        res2['weather'] = ""
        res2['temp'] = ""
        res2['temp1'] = ""
        res2['temp2'] = ""
        res2['humid'] = ""
        res2['WD'] = ""
        res2['WSE'] = ""
        res2['kind'] = "0"
        res2['content'] = ""
        ans2 = json.dumps(res2, ensure_ascii=False)
        return HttpResponse(ans2)
    # get city to be continued
    city = "海淀"
    #cope with string of city and select citycode
    cursor = connection.cursor()
    cursor.execute("select CityCode from cityweather WHERE CityName = %s", [city])
    row = cursor.fetchone()
    city_url='http://www.weather.com.cn/data/cityinfo/'+row[0]+'.html'
    city_url2='http://www.weather.com.cn/data/sk/'+row[0]+'.html'
    # get weather html and parse to json
    weatherHtml = urllib2.urlopen(city_url).read()
    weatherJSON = json.JSONDecoder().decode(weatherHtml)
    weatherInfo = weatherJSON['weatherinfo']
    weatherHtml2 = urllib2.urlopen(city_url2).read()
    weatherJSON2 = json.JSONDecoder().decode(weatherHtml2)
    weatherInfo2 = weatherJSON2['weatherinfo']
    #get time
    h_str=time.strftime("%H", time.localtime(time.time()))
    h_chn=int(h_str)
    print h_chn

    MS = Noticepoint.objects.filter(
        Q(fromxp__lte=xpos, fromyp__gte = ypos, targetxp__gte = xpos, targetyp__lte = ypos) |
        Q(fromxp__gte=xpos, fromyp__gte = ypos, targetxp__lte = xpos, targetyp__lte = ypos) |
        Q(fromxp__gte=xpos, fromyp__lte = ypos, targetxp__lte = xpos, targetyp__gte = ypos) |
        Q(fromxp__lte=xpos, fromyp__lte = ypos, targetxp__gte = xpos, targetyp__gte = ypos))

    if MS.count() == 0:
        kind=0
        content=""
    else:
        kind=MS[0].type
        content=MS[0].content

    res={}
    res['status']="true"
    #time 2017-03-03 12:37:00
    res['time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res['weather']=weatherInfo['weather']
    res['temp']=weatherInfo2['temp']
    res['temp1']=weatherInfo['temp1']
    res['temp2'] = weatherInfo['temp2']
    res['humid'] = weatherInfo2['SD']
    res['WD']=weatherInfo2['WD']
    res['WSE']=weatherInfo2['WSE']
    res['kind']=kind
    res['content']=content
    ans=json.dumps(res, ensure_ascii=False)
    return HttpResponse(ans)