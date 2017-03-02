# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, models
import json
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


# Create your views here.
def index(request):
    return HttpResponse("<h2>Hello World!</h2>A Server for a Feng Ru Cup Project.<br><br><footer><center>College of Software, Beihang University</center></footer>")

def getmsg(request):
    # get city
    city = "海淀"
    cursor = connection.cursor()
    cursor.execute("select CityCode from cityweather WHERE CityName = %s", [city])
    row = cursor.fetchone()
    city_url='http://www.weather.com.cn/data/cityinfo/'+row[0]+'.html'
    # get weather html and parse to json
    weatherHtml = urllib2.urlopen(city_url).read()
    weatherJSON = json.JSONDecoder().decode(weatherHtml)
    weatherInfo = weatherJSON['weatherinfo']

    # print weather info
    print "城市："+weatherInfo['city']
    print "天气："+weatherInfo['weather']

    #get time
    h_str=time.strftime("%H", time.localtime(time.time()))
    h_chn=int(h_str)
    print h_chn

    res={}
    res['msg']="hehehe"
    res['code']="python"
    res['weather']=weatherInfo['weather']
    res['city']=weatherInfo['city']
    ans=json.dumps(res, ensure_ascii=False)
    return HttpResponse(ans)
