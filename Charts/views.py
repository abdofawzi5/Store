'''
******************** Chart Documentation  ********************
Chart functions is based on HighChart, and it draw charts in 
HTML using chart.js (static/Chart/chart.js)

In views: 
    1- add data in list
    2- send list and series name to yAxisForm 
    3- append returned data from yAxisForm in newList 
    4- send newList to ChartDays or ChartWeeks, then send returned data to HTML

In HTML:
    1- call draw_chart in JS
'''

import json
from datetime import timedelta

def pieChart (dataDictionaryInList,chartTitle,unit):
    yAxis =[]
    for dic in dataDictionaryInList:
        yAxis.append([dic['name'],dic['data']])

    if unit is None:
        unit = ''

    return setChart(chartTitle, None, yAxis,None,None,unit)

def xAxisListDates(fromDate,toDate):
    xAxis = []
    while fromDate <= toDate:
        xAxis.append(str(fromDate))
        fromDate += timedelta(1)
    return xAxis

def xAxisListNumbers(fromNum,toNum,unit):
    xAxis = []
    if unit is None:
        unit = ''
    while fromNum <= toNum:
        xAxis.append((str(fromNum)+unit))
        fromNum += 1
    return xAxis

def yAxisForm(name,data,visible=True):
    if all(x is None for x in data):
        visible = False
    data = json.dumps(data)
    if visible == True:
        return {'name':name,'data':data,'visible': 'true'}
    else:
        return {'name':name,'data':data,'visible': 'false'}

def yAxisWithDrilldownForm(name,data,ID):
#     data = json.dumps(data)
    return {'name':name,'y':data,'drilldown':str(ID)}

def DrilldownForm(name,data,ID):
#     data = json.dumps(data)
    return {'name':name,'data':data,'id':str(ID)}

def setChart(chartTitle,subtitle,xAxis,yAxis,yAxisDrilldown,yAxisTitle,yAxisTitle2,unit):
    axis = {}
    axis['yAxis'] = yAxis
    if yAxisDrilldown is not None:
        axis['yAxisDrilldown'] = yAxisDrilldown
    axis['title'] = chartTitle
    if xAxis is not None:
        axis['xAxis'] = xAxis
    if yAxisTitle is not None:
        axis['yAxis_title'] = yAxisTitle
    else:
        axis['yAxis_title'] = ''
    if unit is not None:
        axis['unit'] = unit
    else:
        axis['unit'] = ''
    if yAxisTitle2 is not None:
        axis['yAxis_title2'] = yAxisTitle2
    if subtitle is not None:
        axis['subtitle'] = subtitle
    else:
        axis['subtitle'] = ''
    return json.dumps(axis)

def drawChart (dataDictionaryInList,chartTitle,subtitle,yAxisTitle,yAxisTitle2,unit,xAxisList):
    """
        dataDictionaryInList contain
            1- name: series name
            2- data: list of data
    """
    yAxis =[]
    for dic in dataDictionaryInList:
        yAxis.append(yAxisForm(dic['name'], dic['data']))
    
    return setChart(chartTitle,subtitle, xAxisList, yAxis,None,yAxisTitle, yAxisTitle2, unit)

def drawChartWithDrilldown(dataDictionaryInList,chartTitle,subtitle,yAxisTitle,yAxisTitle2,unit,xAxisList):
    """
        dataDictionaryInList contain
            1- name: category name
            2- value: category value
            3- data: list of list
    """
    yAxis =[]
    yAxisDrilldown =[]
    i = 0
    for dic in dataDictionaryInList:
        yAxis.append(yAxisWithDrilldownForm(dic['name'], dic['value'],i))
        yAxisDrilldown.append(DrilldownForm(dic['name'], dic['data'],i))
        i += 1
    return setChart(chartTitle,subtitle, xAxisList, yAxis,yAxisDrilldown,yAxisTitle, yAxisTitle2, unit)


