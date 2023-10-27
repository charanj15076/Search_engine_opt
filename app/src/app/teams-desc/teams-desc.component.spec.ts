import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamsDescComponent } from './teams-desc.component';

describe('TeamsDescComponent', () => {
  let component: TeamsDescComponent;
  let fixture: ComponentFixture<TeamsDescComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TeamsDescComponent]
    });
    fixture = TestBed.createComponent(TeamsDescComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
