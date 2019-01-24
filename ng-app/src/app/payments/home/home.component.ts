import { Component, OnInit, ChangeDetectionStrategy, ViewChild, ViewContainerRef } from '@angular/core';
import { ROUTE_ANIMATIONS_ELEMENTS, routeAnimations } from '@app/core';
import { FormGroup } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { PaymentcodeInfo } from '../payment.models';
import { MatTableDataSource, MatSort, MatPaginator } from '@angular/material';
import { SelectionModel } from '@angular/cdk/collections';
import { Overlay } from '@angular/cdk/overlay';
import { BaseComponent } from '@app/shared';
import { PaymentDetailsService } from '../payment-details.service';

@Component({
  selector: 'lynx-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0', visibility: 'hidden' })),
      state('expanded', style({ height: '*', visibility: 'visible' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class HomeComponent extends BaseComponent implements OnInit {

  paymentdetails: PaymentcodeInfo[]
  displayedColumns = ['select', 'paymentcode', 'paymentcodedue', 'paymentrecieved', 'balance'];
  dataSource = new MatTableDataSource(this.paymentdetails);
  selection = new SelectionModel<PaymentcodeInfo>(true, []);

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  flaggedOnly = false;
  flaggedOnlyValueChange($event) {
    this.flaggedOnly = $event.checked;
    this.updateBasedOnFlaggedStatus();
  }

  isExpansionDetailRow = (i: number, row: Object) => row.hasOwnProperty('detailRow');
  expandedElement: any;

  constructor(private service: PaymentDetailsService,
    overlay: Overlay,
    viewContainerRef: ViewContainerRef) {
    super(overlay, viewContainerRef);
  }
  ngOnInit() {
    this.processing = true;

    this.service.getPaymentDetails().subscribe(
      (response) => {
        console.log("ngOnInit -> PaymentDetailsComponent" + JSON.stringify(response));
        this.paymentdetails = response;
        const rows = [];
        this.paymentdetails.forEach(element => rows.push(element, { detailRow: true, element }));
        console.log(rows);
        this.dataSource = new MatTableDataSource(rows)
        this.dataSource.paginator = this.paginator;
        // this.closeInProgessOverlay();
        this.processing = false;
      },
      error => {
        console.log("failed in ngOnInit" + JSON.stringify(error));
        // this.closeInProgessOverlay();
        this.processing = false;
      }
    );
  }


  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
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
  updateBasedOnFlaggedStatus() {
    console.log(this.flaggedOnly);
    const rows = [];
    //this.selection.clear();
    if (this.flaggedOnly) {
      var filteredPaymentDetails = this.paymentdetails.filter(p => (p.flagged != 'NONE'));
      filteredPaymentDetails.forEach(element => rows.push(element, { detailRow: true, element }));
    }
    else {
      this.paymentdetails.forEach(element => rows.push(element, { detailRow: true, element }));
    }

    this.dataSource = new MatTableDataSource(rows)

    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }
}
