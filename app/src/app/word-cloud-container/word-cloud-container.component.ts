import { ChangeDetectorRef, Component } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { environment } from 'src/environments/environment'

import * as Highcharts from 'highcharts';
import { Options } from 'highcharts';
declare var require: any;

const Wordcloud = require('highcharts/modules/wordcloud');
Wordcloud(Highcharts);

@Component({
  selector: 'app-word-cloud-container',
  templateUrl: './word-cloud-container.component.html',
  styleUrls: ['./word-cloud-container.component.css'],
})
export class WordCloudContainerComponent {
  isLoading: boolean = false;
  isSubmitted: boolean = false;
  options:any;
  myForm: FormGroup;
  
  analysisURL: string='';
  siteText: string = '';
  siteImage: string = '';
  siteKeywords: any[] = [];
  keywordsPages = 1;
  siteInternalLinks: any[] = [];
  linksPages = 1;
  
  constructor(
    private fb: FormBuilder, 
    private router: Router, 
    private cdr: ChangeDetectorRef,
    private apiService: ApiService
  ) {
    this.myForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern('https?://.+')]],
    });
  }

  onSubmit() {
    if (this.myForm.valid) {
      // Handle form submission here
      this.isLoading = true;
      this.isSubmitted = true;
      this.cdr.detectChanges();

      this.analysisURL = this.myForm.controls['url'].value;
      this.apiService.getCrawlerData(this.analysisURL).subscribe((response: any) => {
        this.siteText = response.text;
        this.siteImage = environment.apiUrl + '/' + response.img_url
        this.siteInternalLinks = response.links;
        console.log(response)

        let postData = {
          text: response.text,
        }
    
        this.apiService.analyzeFrequencies(postData).subscribe( (res) => {
          console.log(res)
          let frequencies = JSON.parse(res.data.kmp)

          let data = []
          for (const key in frequencies.Word) {
            let tmpObj = {
              name: frequencies.Word[key],
              weight: frequencies.count[key],
            }
            data.push(tmpObj);
          }
          this.siteKeywords = data.reverse();

          this.options = {
            series: [{
              type: 'wordcloud',
              data: data,
              name: 'Occurrences'
            }],
            title: { text: null },
            credits: { enabled: false },
          };
          console.log(this.siteKeywords)

          // generate word cloud
          Highcharts.chart('container', this.options);

          // building the algorithm performance data
          const algoLabels: any = {
            kmp: 'KMP',
            naive: 'Naive String Matching',
            suffix_array: 'Suffix Array',
            suffix_tree: 'Suffix Tree', 
            rabin_karp: 'Rabin-Karp'
          }

          let graphCats = [];
          let graphData = [];

          for (const key in res.data) {
            if (res.data[key] != '{}') {    // {} means that the algorithm was skipped because it timed out
              graphCats.push(algoLabels[key]);
              graphData.push(res.times[key] / 1000000);
            }
          }

          // generate the algorithm performance bar chart
          let graphOptions: Options = {
            chart: { type: 'column' },
            title: { text: 'Algorithms Runtime' },
            xAxis: {
              categories: graphCats,
              title: { text: null }
            },
            yAxis: {
              min: 0,
              title: {
                text: 'Runtime (ms)',
                align: 'high'
              },
              labels: { overflow: 'justify' }
            },
            plotOptions: {
              bar: {
                dataLabels: { enabled: true }
              }
            },
            credits: { enabled: false },
            series: [{
              type: 'column',
              name: 'Algorithm',
              data: graphData,
              // data: [res.times.kmp / 1000000, res.times.naive / 1000000, res.times.suffix_array / 1000000, res.times.suffix_tree / 1000000, res.times.rabin_karp / 1000000]
            }]
          };

          Highcharts.chart('graph-container', graphOptions);

          this.isLoading = false;
        });
      });
    }
  }

  analyzeFromLink(link: string) {
    this.myForm.controls['url'].setValue(link);
    this.onSubmit();
  }
  


  // routeToStats() {
  //   this.router.navigate(['stats']);
  // }
}
