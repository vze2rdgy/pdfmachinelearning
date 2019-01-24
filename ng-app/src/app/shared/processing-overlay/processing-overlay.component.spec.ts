import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProcessingOverlayComponent } from './processing-overlay.component';

describe('ProcessingOverlayComponent', () => {
  let component: ProcessingOverlayComponent;
  let fixture: ComponentFixture<ProcessingOverlayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProcessingOverlayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProcessingOverlayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
