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

def clearStandardName(word):
    return word.replace ('_',' ').title()

def pieChart (dataDictionaryInList,chartTitle,unit):
    yAxis =[]
    for dic in dataDictionaryInList:
        yAxis.append([dic['name'],dic['data']])

    if unit is None:
        unit = ''

    return setChart(chartTitle, None, yAxis,None,None,unit)

def ChartDays (dataDictionaryInList,xAxisFrom,xAxisTo,chartTitle,yAxisTitle,yAxisTitle2,unit,stand,standParameters):
    xAxis =[]
    yAxis =[]
    for dic in dataDictionaryInList:
        yAxis.append(yAxisForm(dic['name'], dic['data']))
    
    if stand is not None:
        for s in stand:
            for parameters in standParameters:
                name = str(s)+' Standard - '+clearStandardName(parameters)
                data = []
                for oneStand in stand.get(s):
                    data.append(oneStand[parameters])
                if len(data) + xAxisFrom > xAxisTo:
                    xAxisTo = len(data) + xAxisFrom
                yAxis.append(yAxisForm(name, data))
    if unit is None:
        unit = ''

    for i in range(xAxisFrom,xAxisTo):
        xAxis.append(str(i))

    return setChart(chartTitle, xAxis, yAxis,yAxisTitle, yAxisTitle2, unit)

def ChartWeeks (dataDictionaryInList,xAxisFrom,xAxisTo,chartTitle,yAxisTitle,yAxisTitle2,unit,stand,standParameters):
    xAxis =[]
    yAxis =[]
    for dic in dataDictionaryInList:
        yAxis.append(yAxisForm(dic['name'], dic['data']))

    if stand is not None:
        for s in stand:
            for parameters in standParameters:
                name = str(s)+' Standard - '+clearStandardName(parameters)
                data = []
                for oneStand in stand.get(s):
                    data.append(oneStand[parameters])
                    if len(data) + xAxisFrom > xAxisTo:
                        xAxisTo = len(data) + xAxisFrom
                yAxis.append(yAxisForm(name, data))

    if unit is None:
        unit = ''

    for i in range(xAxisFrom,xAxisTo+1):
        xAxis.append('week '+str(i))

    return setChart(chartTitle, xAxis, yAxis,yAxisTitle, yAxisTitle2, unit)

def yAxisForm(name,data,visible=True):
    if all(x is None for x in data):
        visible = False
    data = json.dumps(data)
    if visible == True:
        return {'name':name,'data':data,'visible': 'true'}
    else:
        return {'name':name,'data':data,'visible': 'false'}

def setChart(chartTitle,xAxis,yAxis,yAxisTitle,yAxisTitle2,unit):
    axis = {}
    if xAxis is not None:
        axis['xAxis'] = xAxis
    if yAxis is not None:
        axis['yAxis'] = yAxis
    if yAxisTitle is not None:
        axis['yAxis_title'] = yAxisTitle
    if yAxisTitle2 is not None:
        axis['yAxis_title2'] = yAxisTitle2
    if unit is not None:
        axis['unit'] = unit
    if chartTitle is not None:
        axis['title'] = chartTitle
    return axis
