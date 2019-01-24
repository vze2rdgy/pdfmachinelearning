import { Injectable, Inject } from '@angular/core';
import { Router } from '@angular/router';
import { Action } from '@ngrx/store';
import { Actions, Effect, ofType } from '@ngrx/effects';
import { tap, switchMap, map, catchError } from 'rxjs/operators';

import { LocalStorageService } from '../local-storage/local-storage.service';

import {
  ActionAuthLogin,
  ActionAuthLogout,
  AuthActionTypes,
  ActionAuthorize,
  ActionUnAuthorize,
  ActionReqAuthorization,
  ActionAuthSessionEnded
} from './auth.actions';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { APP_CONFIG, IAppConfig } from '@app/app.config';
import { AuthProfile } from './auth-profile';
import { AuthService } from './auth-service.service';
import { AsyncScheduler } from 'rxjs/internal/scheduler/AsyncScheduler';
import { ActionStockMarketRetrieve, StockMarketActionTypes, ActionStockMarketRetrieveSuccess, ActionStockMarketRetrieveError } from '@app/examples/stock-market/stock-market.actions';
import { StockMarketService } from '@app/examples/stock-market/stock-market.service';

export const AUTH_KEY = 'AUTH';

@Injectable()
export class AuthEffects {
  constructor(
    private actions$: Actions<Action>,
    private localStorageService: LocalStorageService,
    private router: Router,
    private http: HttpClient,
    private authService: AuthService,
  ) { }

  @Effect({ dispatch: false })
  login = this.actions$.pipe(
    ofType<ActionAuthLogin>(AuthActionTypes.LOGIN),
    tap(() =>
      this.localStorageService.setItem(AUTH_KEY, { isAuthenticated: true })
    )
  );


  @Effect()
  retrieveProfile = this.actions$.pipe(
    ofType<ActionReqAuthorization>(AuthActionTypes.REQAUTHORIZATION),
    switchMap((action: ActionReqAuthorization) =>
      this.authService.getAuthProfile().pipe(
        map(profile => {

          // Profile should never be empty. empty profile should result 401 
          if (profile != null && profile.userinfo != null && profile.locids == null ||
            profile.locids != null && profile.locids.length == 0) {
            console.log("Profile recieved ++");
            return new ActionUnAuthorize(profile);
          }
          else {
            return new ActionAuthorize(profile, profile.locs[0]);
          }
        }),
        catchError(error => {
          console.log("Unable to get the profile " + JSON.stringify(error));
          return of(new ActionAuthLogout())
        })
      )
    )
  );

  //redirect users to registration view
  @Effect({ dispatch: false })
  unauthorized = this.actions$.pipe(
    ofType<ActionAuthLogout>(AuthActionTypes.UNAUTHORIZE),
    tap(() => {
      console.log("inside UNAUTHORIZE effect");
      this.router.navigate(['register']);
    })
  );

  // redirect user to students 
  @Effect({ dispatch: false })
  authorized = this.actions$.pipe(
    ofType<ActionAuthLogout>(AuthActionTypes.AUTHORIZE),
    tap(() => {
      console.log("inside AUTHORIZE effect");
      this.router.navigate(['students']);
    })
  );

  //redirect user to login page
  @Effect()
  logout = this.actions$.pipe(
    ofType<ActionAuthLogout>(AuthActionTypes.LOGOUT),
    switchMap((action: ActionAuthLogout) =>
    this.authService.clearAuthSession().pipe(
      map(data => {
          this.router.navigate(['']);
          this.localStorageService.setItem(AUTH_KEY, { isAuthenticated: false });        
          return new ActionAuthSessionEnded();
      }),
      catchError(error => {        
        return of( new ActionAuthSessionEnded());
      })
    )
  ),


    // tap(() => {
    //   this.authService.clearAuthSession().pipe(
    //     map( (data: boolean)=>{
    //       this.router.navigate(['']);
    //       this.localStorageService.setItem(AUTH_KEY, { isAuthenticated: false });
    //     })
    //   )


    // })
  );
}
