import { Component } from '@angular/core';
import * as Highcharts from 'highcharts';
import { Options } from 'highcharts';

@Component({
  selector: 'app-stats-container',
  templateUrl: './stats-container.component.html',
  styleUrls: ['./stats-container.component.css'],
})
export class StatsContainerComponent {
  Highcharts = Highcharts; 
  chartOptions: Options = {
    chart: {
      type: 'column'
    },
    title: {
      text: 'Algorithms Runtime'
    },
    xAxis: {
      categories: ['Rabin-Karp', 'Suffix Tree', 'Suffix Array', 'Naive String Matching', 'KMP algorithm'],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Runtime (ms)',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
        }
      }
    },
    credits: {
      enabled: false
    },
    series: [{
      type: 'column',
      name: 'Runtime',
      data: [5, 2, 3, 1, 4]
    }]
  };
}
