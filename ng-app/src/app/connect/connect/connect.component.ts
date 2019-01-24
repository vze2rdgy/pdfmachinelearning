import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { Observable } from 'rxjs';
import { Store, select } from '@ngrx/store';
import { AppState, selectAuth, routeAnimations } from '@app/core';
import { map } from 'rxjs/operators';

@Component({
  selector: 'lynx-connect',
  templateUrl: './connect.component.html',
  styleUrls: ['./connect.component.scss'],
  animations: [routeAnimations],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ConnectComponent implements OnInit {
  isAuthenticated$: Observable<boolean>;
  connectMenu = [
    { link: 'templates', label: 'lynx.connect.menu.template' },
    { link: 'schedule', label: 'lynx.connect.menu.schedule' }
  ]
  constructor(private store: Store<AppState>) {}
  ngOnInit() {
    this.isAuthenticated$ = this.store.pipe(
      select(selectAuth),
      map(auth => auth.isAuthenticated)      
    );
  }
}
