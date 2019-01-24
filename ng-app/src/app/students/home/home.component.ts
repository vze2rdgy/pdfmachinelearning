import { Component, OnInit, ChangeDetectionStrategy, OnDestroy, ViewChild, ViewContainerRef, ChangeDetectorRef } from '@angular/core';
import { Store, select } from '@ngrx/store';
import { State } from '../student.state';
import { ActionStudentsRetrieve, ActionStudentsRetrieveSuccess, ActionStudentsToggleActiveOnly } from './home.actions';
import { ROUTE_ANIMATIONS_ELEMENTS, NotificationService } from '@app/core';
import { Observable, Subscription } from 'rxjs';
import { StudentsHomeState, StudentBasicInfo } from './home.model';
import { take, takeUntil } from 'rxjs/operators';
import { MatTableDataSource, MatPaginator, MatSort, MatDialog } from '@angular/material';
import { componentDestroyed } from '@w11k/ngx-componentdestroyed';
import { SelectionModel } from '@angular/cdk/collections';
import { selectStudentsHomeActiveOnly, selectStudentsHomeItems, selectStudentsHomeStudentFiltered } from './home.selectors';
import { Overlay } from '@angular/cdk/overlay';
import { StudentsService } from '../students.service';
import { GenerateFamilyCodeReq } from '../generateFamilyCodeResponse';
import { PaymecodeGenDialogComponent } from './paymecode-gen-dialog/paymecode-gen-dialog.component';

@Component({
  selector: 'lynx-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit, OnDestroy {
  students: StudentBasicInfo[] = [];

  routeAnimationsElements = ROUTE_ANIMATIONS_ELEMENTS;
  activeOnly: Boolean;
  displayedColumns: string[] = ['select', 'studentid', 'name', 'dob', 'subjects', 'totalfee', 'paymentcode'];

  dataSource = new MatTableDataSource(this.students);
  selection = new SelectionModel<StudentBasicInfo>(true, []);
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;


  datasubscription: Subscription;

  constructor(
    private store: Store<State>,    
    public dialog: MatDialog,
    overlay: Overlay, 
    viewContainerRef: ViewContainerRef,
    private notificationService: NotificationService,
    private studentService: StudentsService,
    private cdf: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    this.store.pipe(
      select(selectStudentsHomeActiveOnly))
      .pipe(
        takeUntil(componentDestroyed(this)) // <--- magic is here!
      )
      .subscribe(
        ao => {
          this.activeOnly = ao;
        }
      );

    this.retrieveStudents();
    this.store.pipe(select(selectStudentsHomeStudentFiltered))
      .pipe(
        takeUntil(componentDestroyed(this)) // <--- magic is here!
      )
      .subscribe(students => {
        console.log("Data contains => " + students);
        this.students = JSON.parse(JSON.stringify(students));

        if (this.students != null) {
          this.dataSource.data = this.students;
          this.cdf.detectChanges();         
          // this.dataSource  = new MatTableDataSource(this.students);
        }
      });
  }
  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
      this.selection.clear() :
      this.dataSource.data.forEach(row => this.selection.select(row));
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  ngOnDestroy() {
  }

  retrieveStudents() {
    this.store.dispatch(new ActionStudentsRetrieve({ timestamp: '10-10-219' }));
  }
  activeOnlyValueChange($event) {
    // this.activeOnly = $event.checked;
    this.store.dispatch(new ActionStudentsToggleActiveOnly({ activeOnly: $event.checked }));
  }



  generateFamilyCode(selectedStudent) {
    console.log("generateFamilyCode" + JSON.stringify(selectedStudent));
    let req = new GenerateFamilyCodeReq([selectedStudent.studentid], false, null);

    this.studentService.generateFamilyCode(req).subscribe(
      (response) => {
        console.log("Response from generateFamilyCode ->" + JSON.stringify(response));

        // Ananlyse the response
        // Something went wrong
        if (response.status == 0) {
          this.notificationService.error("Unbale to gernerate the code");
        }
        //Code generated sucessfully
        if (response.status == 1) {
          selectedStudent.paymentcode = response.message;
          this.cdf.detectChanges();
          // this.retrieveStudents();
          this.notificationService.info("New code is " + response.message);
        }
        // siblings found
        if (response.status == 2) {
          const dialogRef = this.dialog.open(PaymecodeGenDialogComponent, {
            width: "800px",
            height: "500px",
            data : response
          });

          dialogRef.afterClosed().subscribe(result => {
            console.log('The dialog was closed' + JSON.stringify(result));     
            this.retrieveStudents();
          });
        }

      },
      error => {
        console.log("Unable to generate the family code ->" + JSON.stringify(error));
      }
    );
  }


}
