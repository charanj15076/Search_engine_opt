import { ChangeDetectorRef, Component } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';

import * as Highcharts from 'highcharts';
declare var require: any;
// const More = require('highcharts/highcharts-more');
// More(Highcharts);

// import Histogram from 'highcharts/modules/histogram-bellcurve';
// Histogram(Highcharts);

// const Exporting = require('highcharts/modules/exporting');
// Exporting(Highcharts);

// const ExportData = require('highcharts/modules/export-data');
// ExportData(Highcharts);

// const Accessibility = require('highcharts/modules/accessibility');
// Accessibility(Highcharts);

const Wordcloud = require('highcharts/modules/wordcloud');
Wordcloud(Highcharts);

@Component({
  selector: 'app-word-cloud-container',
  templateUrl: './word-cloud-container.component.html',
  styleUrls: ['./word-cloud-container.component.css'],
})
export class WordCloudContainerComponent {
  isSubmitted: boolean = false;
  options:any;
  myForm: FormGroup;
  checkboxes: string[] = [
    'Naive String Matching',
    'Rabin Karp',
    'KMP',
    'Suffix Array',
    'Suffix Tree',
  ];
  constructor(private fb: FormBuilder, private router: Router, private cdr: ChangeDetectorRef) {
    this.myForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern('https?://.+')]],
      checkbox0: [false],
      checkbox1: [false],
      checkbox2: [false],
      checkbox3: [false],
      checkbox4: [false],
      selectAll: [false],
    });
    this.myForm.setValidators(this.atLeastOneCheckboxSelected());

    // highcharts
    var text = 'Education For betterment As all we know that, in front of GOD we are equal. GOD gave us similar power  in front of GOD we are equal. GOD gave us similar power to all. He is not did any partiality for creating all of us. Instead all those we create this Reservation Education For betterment system which force us to create discrimination among us. Because of this discrimination there are many social hazards taking place. Education For betterment As all we are in front of GOD we are equal. GOD gave us similar power Human, so we maintain it also. Not accepting any Reservation Education For betterment system. Education For betterment It hampering our mentality. It also create many social violence. Today I like to create many social violence. Today I like to Education For betterment convey all of you about this harmful and Education For betterment violent system that already playing it’s game among us.';
    var obj: any = {name:'', weight:0}
    var lines = text.split(/[,\. ]+/g),
    data = Highcharts.reduce(lines, function (arr: any, word: string) {
        
        obj = Highcharts.find(arr, function (obj: { name: string; weight: number}) {
            return obj.name === word;
        });
        if (obj) {
             obj.weight += 1;
        } else {
            obj = {
                name: word,
                weight: 1
            };
            arr.push(obj);
        }
        return arr;
    }, []);

    this.options = {
    
    series: [{
        type: 'wordcloud',
        data: data,
        name: 'Occurrences'
    }],
    title: {
        text: 'Word Cloud'
    }
};
  }
  onSubmit() {
    if (this.myForm.valid) {
      // Handle form submission here
      this.isSubmitted = true;
      this.cdr.detectChanges();
      console.log('Form Submitted');
      Highcharts.chart('container', this.options);
    }
  }
  private atLeastOneCheckboxSelected(): ValidatorFn {
    return (control: AbstractControl) => {
      const hasSelectedCheckbox = Object.keys(control.value)
        .filter((key) => key.startsWith('checkbox'))
        .some((key) => control.value[key]);

      return hasSelectedCheckbox ? null : { noCheckboxSelected: true };
    };
  }

  updateSelectAllCheckbox() {
    const allCheckboxesSelected = this.checkboxes.every(
      (_, index) => this.myForm.get('checkbox' + index)?.value
    );
    this.myForm.get('selectAll')?.setValue(allCheckboxesSelected);
  }

  toggleAllCheckboxes(event: any): void {
    const selectAllValue = event.target.checked;
    this.checkboxes.forEach((_, index) => {
      this.myForm.get('checkbox' + index)?.setValue(selectAllValue);
    });
  }

  routeToStats() {
    this.router.navigate(['stats']);
  }
}
