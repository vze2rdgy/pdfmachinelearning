import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { ConnectService } from './connect.service';
import { Store } from '@ngrx/store';
import { State } from './connect.state';
import { selectTemplates } from './connect.selectors';
import { take, filter, switchMap, takeUntil, delay } from 'rxjs/operators';
import { ActionConnectTemplRetrieve } from './connect.actions';
import { Template } from './templates/template.models';
import { map } from 'bluebird';


@Injectable()
export class ConnectResolver implements Resolve<Observable<Template[]>> {
  constructor(private connectService: ConnectService,
              private store: Store<State>) { }

  resolve(route: ActivatedRouteSnapshot,   state: RouterStateSnapshot): Observable<Template[]> {
    this.store.select(selectTemplates).pipe(take(1))
        .subscribe(
          x => {             
            if ( !x || x.length === 0){
              this.store.dispatch(new ActionConnectTemplRetrieve({ timestamp: Date()}));
            }
        });

    return  this.store
    .select(selectTemplates).pipe(filter(x => x !== null), filter(x => x.length > 0),  take(1));
    } 
}