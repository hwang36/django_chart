/**
 * Created by huawang on 9/28/16.
 */

$(function () {
  var drawChart = function() {
    $('#container').highcharts({
      title: {
        text: 'Daily kWh Summary',
        x: -20 //center
      },
      subtitle: {
        text: 'Source: Device ' + deviceId,
        x: -20
      },
      xAxis: {
        categories: ['0', '1', '2', '3', '4', '5',
          '6', '7', '8', '9', '10', '11']
      },
      yAxis: {
        title: {
          text: 'kWh'
        },
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      },
      tooltip: {
        valueSuffix: '°C'
      },
      legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        borderWidth: 0
      },
      series: [
        {
        name: 'Device ' + deviceId,
        data:  testData
      }]
    });
  };
  $(document).ready(function(){
    drawChart();
  });
});