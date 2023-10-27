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
  // loading element
  isLoading: boolean = false;
  loadingMsgHeading: string = 'Loading...';
  loadingMsgBody: string = 'This may take a moment. please don\'t close this page.';
  
  // form validation
  isSubmitted: boolean = false;
  options:any;
  myForm: FormGroup;
  
  // these are all dom elements related to the crawled site
  analysisURL: string='';
  siteText: string = '';
  siteImage: string = '';
  siteKeywords: any[] = [];
  keywordsPages = 1;
  siteInternalLinks: any[] = [];
  linksPages = 1;
  idxOccurrence: any = null;
  occurrenceData: any[] = [];
  occurrencePages = 1;
  
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

  // buttom submit - crawl and display data
  onSubmit() {
    if (this.myForm.valid) {
      // Handle form submission here
      this.isSubmitted = true;
      this.cdr.detectChanges();

      this.analysisURL = this.myForm.controls['url'].value;

      this.isLoading = true;
      this.loadingMsgHeading = 'Crawling ' + this.analysisURL;

      // call api to crawl the site
      this.apiService.getCrawlerData(this.analysisURL).subscribe((response: any) => {
        this.siteText = response.text;
        this.siteImage = environment.apiUrl + '/' + response.img_url;
        this.siteInternalLinks = response.links;

        let postData = {
          text: response.text,
        }
        
        this.loadingMsgHeading = 'Analyzing keywords...';
        // get frequencies from the api
        this.apiService.analyzeFrequencies(postData).subscribe( (res) => {
          let frequencies = JSON.parse(res.data.kmp)

          let data = []
          for (const key in frequencies.Word) {
            let tmpObj = {
              showOccurrences: false,
              name: frequencies.Word[key],
              weight: frequencies.count[key],
            }
            data.push(tmpObj);
          }
          this.siteKeywords = data.reverse();

          const topWordsData = data
            .sort((a, b) => b.weight - a.weight)
            .slice(0, 200);

          this.options = {
            series: [{
              type: 'wordcloud',
              wordSpaces: 1,
              data: topWordsData,
              name: 'Occurrences',
              minFontSize: 10,
              maxFontSize: 90
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
            title: { text: '' },
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
              name: 'Algorithm Performance',
              data: graphData,
            }]
          };

          Highcharts.chart('graph-container', graphOptions);

          this.isLoading = false;
        });
      });
    }
  }

  // keyword click behavior
  showOccurrences(keywordIdx: any) {
    this.isLoading = true;
    this.loadingMsgHeading = 'Showing occurrences of "' + this.siteKeywords[keywordIdx].name +  '"...';

    let postData = {
      text: this.siteText,
      term: this.siteKeywords[keywordIdx].name
    }
    this.apiService.runSearch(postData).subscribe((response: any) => {
      this.occurrenceData = response.data.kmp;
      this.occurrencePages = 1;

      // hide old idx
      if (this.idxOccurrence != null) {
        this.siteKeywords[this.idxOccurrence].showOccurrences = false;
      }
      
      this.siteKeywords[keywordIdx].showOccurrences = true;
      this.idxOccurrence = keywordIdx;    // set new idx as current idx
      this.isLoading = false;
    })
  }

  // clicking a link will analyze the clicked link
  analyzeFromLink(link: string) {
    this.myForm.controls['url'].setValue(link);
    this.onSubmit();
  }

  // open a new tab/window to the keyword analysis site
  goToLink(url: string) {
    window.open(url, "_blank");
  }
  
}
