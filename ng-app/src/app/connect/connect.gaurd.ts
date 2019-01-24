import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';

import { Store } from '@ngrx/store';

import { Observable, of, pipe } from 'rxjs';
import { State } from './connect.state';
import { selectTemplates } from './connect.selectors';
import { ActionConnectTemplRetrieve } from './connect.actions';
import { tap, filter, take, map, switchMap } from 'rxjs/operators';

@Injectable()
export class ConnectGuard implements CanActivate {
  constructor(private store: Store<State>) { }

  getFromStoreOrAPI(): Observable<boolean> {
    return this.store
      .select(selectTemplates)
      .pipe(
        filter(x => x.length > 0),
        take(1),
        switchMap(() => of(true))
        );
  }

canActivate(): Observable < boolean > {

  this.store.select(selectTemplates).pipe(
    take(1))
    .subscribe(
      x => {
        if ( !x || x.length === 0){
          this.store.dispatch(new ActionConnectTemplRetrieve({ timestamp: Date()}));
        }
    });
  return this.getFromStoreOrAPI();    
}
}
