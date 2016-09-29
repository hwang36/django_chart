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
      xAxis: { // TODO
        categories: data_categories
        //categories: ['0', '1', '2', '3', '4', '5',
        //  '6', '7', '8', '9', '10', '11']
      },
      yAxis: {
        title: { // TODO
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
      series: data_series
      //series:
      //  [ // TODO
      //  {
      //  name: 'Device ' + deviceId,
      //  data:  testData
      //},
      //{
      //  name: 'Device 533',
      //  data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]
      //}, {
      //  name: 'sum',
      //  data: [132.5, 116.6, 137.8, 134.8, 153.0, 132.8, 164.0, 163.9, 143.6, 148.7, 165.9, 143.5]
      //}
      //]
    });
  };
  $(document).ready(function(){
    drawChart();
  });
});