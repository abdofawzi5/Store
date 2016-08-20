function rereadVar_yAXisDrilldown(arr)
{
  var out = [];
  for (var i = 0;i<arr.length;i++)
  {
    out.push({
      name: arr[i].name,
      // color: colors[i],
      drilldown: arr[i].drilldown,
      y: arr[i].y
    });
  }
  return out;
}

function rereadVar_drilldown(arr)
{
  var out = [];
  for (var i = 0;i<arr.length;i++)
  {
    out.push({
      name: arr[i].name,
      // color: colors[i],
      id: arr[i].id,
      data: arr[i].data
    });
  }
  return out;
}

function rereadVar(arr,colors,switchEach=null)
{
  var out = [];
  var switchFlag = false;
  for (var i = 0;i<arr.length;i++)
  {
    if (switchEach != null)
    {
      if (i%switchEach == 0)
      {
        if (switchFlag == true)
        {
          switchFlag = false;
        }else{
          switchFlag = true;
        }
      }
    }
    if (switchFlag == true || switchEach == null)
    {
    	out.push({
		    name: arr[i].name,
        color: colors[i],
        visible: (arr[i].visible === 'true'),
		    data: JSON.parse(arr[i].data)
    	});
    }
    else{
      out.push({
		    name: arr[i].name,
        color: colors[i],
        visible: (arr[i].visible === 'true'),
        yAxis:1,
		    data: JSON.parse(arr[i].data)
    	});
    }
  }
  return out;
}


function draw_chart(className,axis,chartType,switchEach,floatSize,reverse)
{
  var colors=[
      '#800000','#FFA500','#20B2AA','#191970','#BA55D3','#BC8F8F', '#B22222','#FFD700','#ADFF2F','#008080','#0000CD','#DDA0DD','#000000', '#DC143C','#B8860B','#006400',
      '#0000FF','#FF0000','#DAA520','#228B22','#00CED1','#4169E1','#C71585','#FF6347','#EEE8AA','#90EE90','#7FFFD4','#8A2BE2','#FF69B4','#FF7F50','#BDB76B','#8FBC8F',
      '#4682B4','#4B0082','#8B4513','#CD5C5C','#808000','#00FA9A','#6495ED','#6A5ACD','#A0522D','#F08080','#9ACD32','#2E8B57','#1E90FF','#7B68EE','#D2691E','#E9967A',
      '#556B2F','#66CDAA','#ADD8E6','#9370DB','#CD853F','#FF8C00','#6B8E23','#3CB371','#87CEFA','#8B008B','#F4A460'];        
  if (floatSize == null)
  {
    floatSize=0;
  }
  if (reverse == null)
  {
    reverse = false;
  }
  var yAxisDic ={}
  if(switchEach == null)
  {
      yAxisDic = {
        opposite: reverse,
        title: {
          text: axis.yAxis_title
        },
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      }
  }else{
    yAxisDic = [{ // Primary yAxis
      labels: {
        format: '{value}',
        style: {
            color: Highcharts.getOptions().colors[1]
        }
      },
      title: {
        text: axis.yAxis_title,
        style: {
            color: Highcharts.getOptions().colors[1]
        }
      }
    }, { // Secondary yAxis
      title: {
        text: axis.yAxis_title2,
        style: {
            color: Highcharts.getOptions().colors[1]
        }
      },
      labels: {
        format: '{value}',
        style: {
        color: Highcharts.getOptions().colors[1]
        }
      },
      opposite: true
    }]    
  }

  $(function () {
    $(className).highcharts({
  		chart: {
  			defaultSeriesType: chartType,
  			renderTo: 'container'
  		},
      title: {
        text: axis.title,
          x: -20
        },
      subtitle: {
      	text: axis.subtitle,
      	x: -20
      },
      xAxis: {
      	categories: axis.xAxis,
      	reversed: reverse
      },
      yAxis:yAxisDic 
      ,plotOptions: {
      	series: {
      		connectNulls: true
      	}
      },tooltip: {
      	headerFormat: '<span style="font-size:10px">{% trans "Day" %}: {point.key}</span><table>',
      	pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
      	'<td style="padding:0"><b> {point.y} '+axis.unit+'</b></td></tr>',
      	footerFormat: '</table>',
      	shared: true,
      	useHTML: true,
      	valueDecimals:floatSize,
      },
      series: rereadVar(axis.yAxis,colors,switchEach)
    });
  });
}


function draw_chart_with_Drilldown(className,axis,floatSize,reverse)
{
  $(function () {
    // Create the chart
    $(className).highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: axis.title,
        },
        subtitle: {
            text: axis.subtitle
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: axis.yAxis_title
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.1f}%'
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
        },
        series:  [{
            name: '',
            colorByPoint: true,
            data: axis.yAxis,
        }]
        ,
        drilldown: {
            series: axis.yAxisDrilldown,
        }
    });
});
}


