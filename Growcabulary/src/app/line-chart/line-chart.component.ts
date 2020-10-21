import { Component, Input, OnInit, ChangeDetectorRef } from '@angular/core';
import { ChartDataSets, ChartOptions, ChartType } from 'chart.js';
import { Label } from 'ng2-charts';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss']
})
export class LineChartComponent implements OnInit {
  lookBack: number;
  lineChartType: ChartType;
  lineChartOptions: ChartOptions;
  averageData: number[];
  lineChartLabels: Label[];
  lineChartData: ChartDataSets[];
  @Input() data: number[];
  
  constructor() {
    this.lookBack = 10;
    this.averageData = [0];
    this.lineChartType = 'line';
    this.lineChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
    };
  }
  
  ngOnInit() {
    this.lineChartData = [
      { data: this.data, label: 'WPM' },
      { data: this.averageData, label: 'Moving Average (' + this.lookBack.toString() + ' Games)'}
    ];
    this.updateData();
  }
  
  updateData() {
    // calculate moving average
    if (this.averageData.length < this.data.length) {
      let sum = 0;
      let numValues = Math.min(this.lookBack, this.data.length - 1);
      for (let i = this.data.length - 1; i >= this.data.length - numValues; i--)
        sum += this.data[i];
      this.averageData.push(sum / numValues);
    }
    
    let labels = Array(this.data.length);
    this.lineChartLabels = Array.from(labels, (_, i) => (i + 1).toString());
  }
  
  ngAfterContentChecked() {
    this.updateData();
  }
}