import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LynxProcessingOverlayComponent } from './lynx-processing-overlay.component';

describe('LynxProcessingOverlayComponent', () => {
  let component: LynxProcessingOverlayComponent;
  let fixture: ComponentFixture<LynxProcessingOverlayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LynxProcessingOverlayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LynxProcessingOverlayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
