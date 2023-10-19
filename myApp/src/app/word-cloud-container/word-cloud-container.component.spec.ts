import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WordCloudContainerComponent } from './word-cloud-container.component';

describe('WordCloudContainerComponent', () => {
  let component: WordCloudContainerComponent;
  let fixture: ComponentFixture<WordCloudContainerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WordCloudContainerComponent]
    });
    fixture = TestBed.createComponent(WordCloudContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
