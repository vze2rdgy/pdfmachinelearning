import { Component, OnInit, ChangeDetectionStrategy, ViewContainerRef, OnDestroy } from '@angular/core';
import { Overlay } from '@angular/cdk/overlay';
import { Store, select } from '@ngrx/store';
import { ActionAuthLogin, ActionAuthorize, ActionReqAuthorization, ActionUnAuthorize, selectAuthorization } from '@app/core';
import { AuththorizationStatus } from '@app/core/auth/auth.models';
import { Observable } from 'rxjs';
import { AuthProfile } from '@app/core/auth/auth-profile';
import { BaseComponent } from '../base-component';

@Component({
  selector: 'lynx-auth-handler',
  templateUrl: './auth-handler.component.html',
  styleUrls: ['./auth-handler.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AuthHandlerComponent extends BaseComponent implements OnInit, OnDestroy {
  // authrizationStatus$: Observable<AuththorizationStatus>;

  constructor(
    overlay: Overlay,
    viewContainerRef: ViewContainerRef,
    private store: Store<any>
  ) { 
    super(overlay, viewContainerRef);

  }

  ngOnInit() {
    this.openInProgessOverlay();
    // this.isAuthenticated$ = this.store.pipe(select(selectIsAuthenticated));
    this.store.dispatch(new ActionAuthLogin());
    this.store.dispatch(new ActionReqAuthorization());
    // this.authrizationStatus$ = this.store.pipe(select(selectAuthorization));
    
  }
  ngOnDestroy(){
    this.closeInProgessOverlay();
  }

  login(){
    this.store.dispatch(new ActionAuthLogin());
  }
  reqAuthrize(){
    this.store.dispatch(new ActionReqAuthorization());
  }
  authrize(){
    this.store.dispatch(new ActionAuthorize(null, null));
  }

  unauthrize(){
    this.store.dispatch(new ActionUnAuthorize(null));
  }
  
}
