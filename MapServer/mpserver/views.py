# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, models
from django.views.decorators.csrf import csrf_exempt
import json
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


# Create your views here.
def index(request):
    return HttpResponse("<h2>Hello World!</h2>A Server for a Feng Ru Cup Project.<br><br><footer><center>College of Software, Beihang University</center></footer>")

@csrf_exempt
def getmsg(request):
    # get json
    if(request.method=='POST'):
        print "POST Method"
        # json.loads(request.body)
    xpos = 39.983836
    ypos = 116.352276
    addr = "中国北京市海淀区知春路29号1"
    # get city
    city = "海淀"
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

    # print weather info
    print "城市："+weatherInfo['city']
    print "天气："+weatherInfo['weather']

    #get time
    h_str=time.strftime("%H", time.localtime(time.time()))
    h_chn=int(h_str)
    print h_chn

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
    res['kind']="0"
    res['content']="hh"
    ans=json.dumps(res, ensure_ascii=False)
    return HttpResponse(ans)
