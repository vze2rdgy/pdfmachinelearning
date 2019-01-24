import { Component, OnInit, Inject, ViewContainerRef } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatTableDataSource, MatSnackBar } from '@angular/material';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { SelectionModel } from '@angular/cdk/collections';
import { Overlay } from '@angular/cdk/overlay';

import { Additionaldetail, GenerateFamilyCodeRes, GenerateFamilyCodeReq } from '@app/students/generateFamilyCodeResponse';
import { StudentsService } from '@app/students/students.service';
import { NotificationService } from '@app/core';
import { BaseComponent } from '@app/shared/base-component';

@Component({
  selector: 'app-paymecode-gen-dialog',
  templateUrl: './paymecode-gen-dialog.component.html',
  styleUrls: ['./paymecode-gen-dialog.component.scss']
})
export class PaymecodeGenDialogComponent extends BaseComponent implements OnInit {
  isLinear = false;
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;

  displayedColumnsWPC: string[] = ['select', 'studentid', 'name', 'dob', 'paymentcode'];
  displayedColumnsWOPC: string[] = ['select', 'studentid', 'name', 'dob'];

  sibWPC = new MatTableDataSource();
  sibWOPC = new MatTableDataSource();
  selection = new SelectionModel<Additionaldetail>(true, []);
  basedOn = null

  studentrequestingFC = null

  constructor(public dialogRef: MatDialogRef<PaymecodeGenDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: GenerateFamilyCodeRes,
    private _formBuilder: FormBuilder,
    private studentService: StudentsService,
    public notificationService: NotificationService,
    overlay : Overlay,
    viewContinerRef : ViewContainerRef    
  ) {
    super(overlay, viewContinerRef);

    this.studentrequestingFC = this.data.sibWOPC.filter(student => student.selected == true)[0]
    this.sibWOPC = new MatTableDataSource(this.data.sibWOPC.filter(student => student.selected == false));
    this.sibWPC = new MatTableDataSource(this.data.sibWPC);
  }

  ngOnInit() {
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.secondFormGroup = this._formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
  }

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.sibWOPC.data.length;
    return numSelected === numRows;
  }

  basedOnStudent(student) {
    console.log("basedon" + student.studentid);
    this.basedOn = student;
  }
  onNoClick(): void {
    console.log("closing..");
    this.dialogRef.close();
  }
  GenerateCode() {
    this.openInProgessOverlay();

    var FCRequestForStudent = [];
    FCRequestForStudent.push(this.studentrequestingFC.studentid);
    this.selection.selected.forEach(item => {
      FCRequestForStudent.push(item.studentid);
    })

    // Generate the request
    // if there are more than 1 objects in FCRequestForStudent than ignoreSiblining should be false
    let req = new GenerateFamilyCodeReq(FCRequestForStudent, FCRequestForStudent.length == 1, (this.basedOn)?this.basedOn.studentid:null);

    console.log ("GenerateFamilyCodeReq --> " + JSON.stringify(req) + "<---");

    this.studentService.generateFamilyCode(req).subscribe(
      (response) => {
        if (response.status == 0) {
          this.notificationService.error("Unable to generate the code");
        }
        //Code generated sucessfully
        if (response.status == 1) {
          this.notificationService.info("New Code is " + response.message);
        }
        if (response.status == 2) {
          this.notificationService.error("Unable to generate the code - 002");
        }

        // this.dialogRef.close("return object here...");
        console.log(this.selection.selected.length);
        console.log(JSON.stringify(this.selection));
        this.closeInProgessOverlay();
        this.dialogRef.close(this.data);


      },
      error => {
        console.log("Unable to generate the family code ->" + JSON.stringify(error));
        this.closeInProgessOverlay();
        this.dialogRef.close(this.data);
      }
    );
  }
}
