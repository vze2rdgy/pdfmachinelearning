import { Action } from '@ngrx/store';
import { AuthProfile, Loc } from './auth-profile';

export enum AuthActionTypes {
  LOGIN = '[Auth] Login',
  LOGOUT = '[Auth] Logout',
  REQAUTHORIZATION = '[Auth] Request Authorization',
  CHANGELOCATION = '[Auth] Change Location',
  AUTHORIZE = '[Auth] Authorize',
  UNAUTHORIZE = '[Auth] UnAuthorize',
  SESSIONENDED = '[Auth] Session ended'
}

export class ActionAuthLogin implements Action {
  readonly type = AuthActionTypes.LOGIN;
}

export class ActionReqAuthorization implements Action {
  readonly type = AuthActionTypes.REQAUTHORIZATION;
}

export class ActionAuthorize implements Action {
  readonly type = AuthActionTypes.AUTHORIZE;
  constructor(public payload: AuthProfile, public selectedLocation:Loc){}
}

export class ActionChangeLocation implements Action {
  readonly type = AuthActionTypes.CHANGELOCATION;
  constructor(public payload: Loc){}
}


export class ActionUnAuthorize implements Action {
  readonly type = AuthActionTypes.UNAUTHORIZE;
  constructor(public payload: AuthProfile){}
}

export class ActionAuthLogout implements Action {
  readonly type = AuthActionTypes.LOGOUT;
}
export class ActionAuthSessionEnded implements Action {
  readonly type = AuthActionTypes.SESSIONENDED;
}



export type AuthActions = ActionAuthLogin | ActionReqAuthorization|  ActionAuthorize | ActionChangeLocation | ActionUnAuthorize | ActionAuthLogout|ActionAuthSessionEnded;
