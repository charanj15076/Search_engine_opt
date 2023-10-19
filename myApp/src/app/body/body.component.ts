import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ValidatorFn, Validators } from '@angular/forms';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.css']
})

export class BodyComponent {
  viewStats: boolean = false;
  myForm: FormGroup;
  checkboxes: string[] = ["Naive String Matching", "Rabin Karp", "KMP", "Suffix Array", "Suffix Tree"]
  constructor(private fb: FormBuilder) {
    this.myForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern('https?://.+')]],
      checkbox0: [false],
      checkbox1: [false],
      checkbox2: [false],
      checkbox3: [false],
      checkbox4: [false],
      selectAll: [false]
    });
    this.myForm.setValidators(this.atLeastOneCheckboxSelected());
  }

  onSubmit() {
    if (this.myForm.valid) {
      // Handle form submission here
      console.log("Form Submitted");
    }
  }
  private atLeastOneCheckboxSelected(): ValidatorFn {
    return (control: AbstractControl) => {
      const hasSelectedCheckbox = Object.keys(control.value)
        .filter(key => key.startsWith('checkbox'))
        .some(key => control.value[key]);

      return hasSelectedCheckbox ? null : { noCheckboxSelected: true };
    };
  }

  updateSelectAllCheckbox() {
    const allCheckboxesSelected = this.checkboxes.every((_, index) =>
      this.myForm.get('checkbox' + index)?.value
    );
    this.myForm.get('selectAll')?.setValue(allCheckboxesSelected);
  }

  toggleAllCheckboxes(event: any): void {
    const selectAllValue = event.target.checked;
    this.checkboxes.forEach((_, index) => {
      this.myForm.get('checkbox' + index)?.setValue(selectAllValue)
    });
  }
}
