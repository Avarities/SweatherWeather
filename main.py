
import datetime
from ctypes import c_int
from unidecode import unidecode
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import urllib2
import urllib
import json
from flask import Flask, render_template
from flask import request

app = Flask(__name__)
matplotlib.rcParams.update({'font.size': 5})

@app.route("/")
def main():
    return render_template('weather.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    czyt = ReadData()
    czyt.readData('514048',text)
    return render_template('weather.html')

class SaveData:
    def __init__(self):
        self.dataList = []

    def getWeatherInfo(self,cityCode):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_atmo = "select atmosphere from weather.forecast where woeid=" +cityCode
        yql_temp = "select item from weather.forecast where u='c' and woeid=" + cityCode
        yql_url_atmo = baseurl + urllib.urlencode({'q': yql_atmo}) + "&format=json"
        yql_url_temp = baseurl + urllib.urlencode({'q': yql_temp}) + "&format=json"
        result_atmo = urllib2.urlopen(yql_url_atmo).read()
        result_temp = urllib2.urlopen(yql_url_temp).read()
        data = json.loads(result_atmo)
        data1 = json.loads(result_temp)
        self.addToArray(data,data1)

    def addToArray(self,data,data1):
        self.dataList.append(datetime.datetime.now())
        self.dataList.append(data1['query']['results']['channel']['item']['condition']['temp'])
        self.dataList.append(data['query']['results']['channel']['atmosphere']['humidity'])
        self.dataList.append(data['query']['results']['channel']['atmosphere']['pressure'])


    def saveToFile(self,cityCode):
        file = open('Yahoo'+cityCode +' ' + str(self.dataList[0].date()),'a+')
        file.write(str(self.dataList[0].hour) + ':' + str(self.dataList[0].minute) + "|")
        file.write(str(self.dataList[1]) + "|")
        file.write(str(self.dataList[2]) + "|")
        file.write(str(self.dataList[3]) + "\n")
        file.close()




class ReadData:

    def __init__(self):
        self.yahooHourList = []
        self.yahooHumidList = []
        self.yahooTempList = []
        self.yahooPressureList = []

        self.baseHourList = []
        self.baseHumidList = []
        self.baseTempList = []
        self.basePressureList = []


    def readData(self, cityCode, day):
        with open('Yahoo' + cityCode +' ' + str(day)) as f:
            for line in f:
                encodeArray = self.encodeData(line)
                self.addDataToTables(encodeArray,line,'yahoo')

        with open('Base' + cityCode +' ' + str(day)) as f:
            for line in f:
                encodeArray = self.encodeData(line)
                self.addDataToTables(encodeArray, line, 'base')

        print('Yahoo' + cityCode +' ' + str(day))
        print self.yahooTempList
        self.createCharts(day)




    def encodeData(sexdzilf, line):
        i = 0;
        encodeArray = []
        for l in line:
            if ( l == '|'):
                encodeArray.append(i)
            i = i + 1
        return encodeArray


    def addDataToTables(self, encodeArray, line, option):
        if(option == 'yahoo'):
            self.addDataToYahoo(encodeArray,line)

        elif(option == 'base'):
            self.addDataToBase(encodeArray,line)

    def addDataToYahoo(self, encodeArray,line):
        self.yahooHourList.append(self.normalizeHours(line[:encodeArray[0]]))
        self.yahooTempList.append(line[encodeArray[0] + 1:encodeArray[1]])
        self.yahooHumidList.append(line[encodeArray[1] + 1:encodeArray[2]])
        self.yahooPressureList.append(line[encodeArray[2] + 1:-2])

    def addDataToBase(self, encodeArray,line):
        self.baseHourList.append(self.normalizeHours(line[:encodeArray[0]]))
        self.baseTempList.append(line[encodeArray[0] + 1:encodeArray[1]])
        self.baseHumidList.append(line[encodeArray[1] + 1:encodeArray[2]])
        self.basePressureList.append(line[encodeArray[2] + 1:-2])


    def normalizeHours(self, hour):
        fullHour = float(hour[:hour.find(':')]) + (float(hour[hour.find(':')+1:])/60.0)
        return fullHour


    def createCharts(self, day):
        self.createHumidChart(day)
        self.createPressureChart(day)
        self.createTemperatureChart(day)


    def createTemperatureChart(self,day):
        plt.figure(figsize = (4,4))
        plt.plot(self.yahooHourList,self.yahooTempList, 'ro', markersize = 3)
        plt.plot(self.baseHourList, self.baseTempList, 'ro', markersize=3 , color = 'cyan')
        plt.tick_params(
            top='off',
            right ='off',
        )

        plt.xticks(np.arange(0, 25, 1))
        plt.yticks(np.arange(0, 60, 5))
        plt.savefig('static/temperature' + '.png')
        plt.close()

    def createPressureChart(self, day):
        plt.figure(figsize = (4,4))
        plt.plot(self.yahooHourList,self.yahooPressureList, 'ro', markersize = 3)
        plt.plot(self.baseHourList, self.basePressureList, 'ro', markersize=3 , color = 'cyan')
        plt.tick_params(
            top='off',
            right ='off',
        )
        plt.xticks(np.arange(0, 24, 1))
        plt.yticks(np.arange(900, 1030, 5))
        plt.savefig('static/pressure' +'.png')
        plt.close()

    def createHumidChart(self, day):
        plt.figure(figsize = (4,4))
        plt.plot(self.yahooHourList,self.yahooHumidList, 'ro', markersize = 3)
        plt.plot(self.baseHourList, self.baseHumidList, 'ro', markersize=3 , color = 'cyan')
        plt.tick_params(
            top='off',
            right ='off',
        )
        plt.xticks(np.arange(0, 24, 1))
        plt.yticks(np.arange(0, 101, 5))
        plt.savefig('static/humid' +'.pgn')
        plt.close()

#poz = SaveData()
#poz.getWeatherInfo('514048')
#poz.saveToFile('514048')
#czyt = ReadData()
#czyt.readData('514048',datetime.datetime.now().date())

if __name__ == "__main__":

    app.run();
