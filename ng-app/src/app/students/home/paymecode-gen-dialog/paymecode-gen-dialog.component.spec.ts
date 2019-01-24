import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PaymecodeGenDialogComponent } from './paymecode-gen-dialog.component';

describe('PaymecodeGenDialogComponent', () => {
  let component: PaymecodeGenDialogComponent;
  let fixture: ComponentFixture<PaymecodeGenDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PaymecodeGenDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PaymecodeGenDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
