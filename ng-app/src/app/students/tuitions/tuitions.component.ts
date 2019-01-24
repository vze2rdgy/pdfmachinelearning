import { Component, OnInit, ChangeDetectionStrategy, ViewChild, OnDestroy } from '@angular/core';
import { ROUTE_ANIMATIONS_ELEMENTS, NotificationService } from '@app/core';
import { MatTableDataSource, MatPaginator, MatSort } from '@angular/material';
import { Tuition } from './tuitions.model';
import { SelectionModel } from '@angular/cdk/collections';
import { Store, select } from '@ngrx/store';
import { State } from '../student.state';
import { ActionTuitionsRetrieve, ActionTuitionsUpdate } from './tuitions.actions';
import { selectTuitions, selectUpdateRes } from './tuitions.selectors';
import { takeUntil } from 'rxjs/operators';
import { componentDestroyed } from '@w11k/ngx-componentdestroyed';

@Component({
  selector: 'lynx-tuitions',
  templateUrl: './tuitions.component.html',
  styleUrls: ['./tuitions.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TuitionsComponent implements OnInit, OnDestroy {
  activeOnly: Boolean;

  routeAnimationsElements = ROUTE_ANIMATIONS_ELEMENTS;
  displayedColumns = ['studentid', 'fname', 'lname', 'math', 'reading'];
  dataSource = new MatTableDataSource();
  selection = new SelectionModel<Tuition>(true, []);
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;



  // tuitions: Tuition[] = [];

  // displayedColumns = ['studentid', 'fname', 'lname', 'math', 'reading'];
  // dataSource = new TuitionDataSource(this.tuitions);
  // @ViewChild(MatPaginator) paginator: MatPaginator;
  // @ViewChild(MatSort) sort: MatSort;

  constructor(
    private store: Store<State>,
    private notificationService: NotificationService
  ) { }

  ngOnInit() {

    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    this.retrieveTuitions();
    this.store.pipe(select(selectTuitions))
      .pipe(
        takeUntil(componentDestroyed(this))
      )
      .subscribe(data => {
        console.log("Data contain => " + data);
        if (data != null) {
          this.dataSource.data = data;
        }
      });

    this.store.pipe(select(selectUpdateRes))
      .pipe(
        takeUntil(componentDestroyed(this))
      )
      .subscribe(
        response => {
          if (response != null) {
            if (response.updateerror != null) {
              this.notificationService.error(response.updateerror.error);
            } else {
              this.notificationService.info(response.updatesucess.message);
            }
          }
        }
      );
  }
  update(el: Tuition, math: any) {
    console.log(el.studentid + "s---d" + math);
  }
  retrieveTuitions() {
    this.store.dispatch(new ActionTuitionsRetrieve({ timestamp: '10-10-219' }));
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  ngOnDestroy() {
  }

  save() {
    // console.log(JSON.stringify(this.tuitions));
    this.store.dispatch(new ActionTuitionsUpdate({ data: this.dataSource.data }))

    // this.dataSource.data

    // this.service.UpdateTuitions(this.tuitions).subscribe(
    //   (response)=>{
    //     console.log(JSON.stringify(response));
    //   },
    //   error =>{
    //     console.log(JSON.stringify(error));
    //   }
    // );
  }
}
