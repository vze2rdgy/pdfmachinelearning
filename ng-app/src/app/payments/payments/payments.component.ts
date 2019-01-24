import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { Observable } from 'rxjs';
import { ROUTE_ANIMATIONS_ELEMENTS, routeAnimations } from '@app/core';

@Component({
  selector: 'lynx-payments',
  templateUrl: './payments.component.html',
  styleUrls: ['./payments.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  animations: [routeAnimations],
})
export class PaymentsComponent implements OnInit {
  routeAnimationsElements = ROUTE_ANIMATIONS_ELEMENTS;
  isAuthenticated$: Observable<boolean>;

  paymentsMenu = [
    { link: 'home', label: 'lynx.payments.menu.home' },    
    { link: 'upload', label: 'lynx.payments.menu.upload' },
  ]

  constructor() { }

  ngOnInit() {
  }

}
